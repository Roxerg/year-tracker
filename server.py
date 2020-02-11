import os
import json
from datetime import datetime

from werkzeug.urls import url_parse

# Flask
from flask import Flask, escape, request, render_template, url_for, redirect, abort, session, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_login import LoginManager


# This Application 
import goaldb
from models import User, getUser


# Externally Visible Server
# app.run(host='0.0.0.0')


app = Flask(__name__)

login_manager = LoginManager(app)   
login_manager.login_view = 'login'
login_manager.init_app(app)
app.config.from_json("config.json")

# </dev/urandom tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' | head -c 13  ; echo
app.secret_key = "b8*'ER#~P'>qn#~<rD<T1.]!b2){"



def convert_dates(e):

    e = list(e)
    e[4] = e[4].strftime("%Y-%m-%d")

    print(e)

    return e


@app.route('/')
def root():
    if not current_user.is_authenticated:
        return redirect(url_for('guest'))
    else:
        return redirect(url_for('home'))



@app.route('/home')
@login_required
def home():

    today_data = goaldb.fetch_today()
    today = checked_unchecked(today_data[0])
    daily = goaldb.fetch_all_daily()
    week = goaldb.fetch_current_week()

    month = goaldb.fetch_current_month()[0]

    data = list(daily)
    data = list(map(convert_dates, data))

    today_data = list(map(convert_dates, today_data))[0]

    print(week)

    return render_template("home.html", daily=color_picker(daily),
                                        week=color_picker(week),
                                        data=data,
                                        today_data=today_data,
                                        lonk=len(daily),
                                        today=today,
                                        month=month)





@app.route('/update/day/specific', methods=['GET'])
def mark_specific():

    if (int(request.args.get('day', '-1')) == -1):
        return redirect("/")

    reading = request.args.get('reading', '0')
    exercise = request.args.get('exercise', '0')
    sleep = request.args.get('sleep', '0')
    day = request.args.get('day', '-1')
    

    goaldb.update_day_specific(reading, exercise, sleep, day)

    return redirect("/")




@app.route('/update/day', methods=['GET'])
def mark_today():

    reading = request.args.get('reading', '0')
    exercise = request.args.get('exercise', '0')
    sleep = request.args.get('sleep', '0')

    goaldb.update_day(reading, exercise, sleep)

    return redirect("/")

@app.route('/update/month', methods=['GET'])
def mark_month():

    alcohol = request.args.get('alcohol', '0')
    meal = request.args.get('meal', '0')
    resist = request.args.get('resist', '0')

    goaldb.update_month(alcohol, meal, resist)

    return redirect("/")

def checked_unchecked(e):

    a,b,c = "unchecked","unchecked","unchecked"

    try:
        if int(e[1]) > 0: a = "checked"
    except:
        pass

    try:
        if int(e[2]) > 0: b = "checked"
    except:
        pass

    try:
        if int(e[3]) > 0: c = "checked"
    except: 
        pass


    return [a,b,c]




def color_picker(daily):
    color = []
    day_of_year = datetime.now().timetuple().tm_yday
    for d in daily:
        if day_of_year < d[0]:
            color.append("grey")
        else:
            count = 0
            if int(d[1]) > 0: count += 1
            if int(d[2]) > 0: count += 1
            if int(d[3]) > 0: count += 1

            if(count == 3):
                color.append("green")
            elif(count == 2):
                color.append("yellow")
            elif(count == 1):
                color.append("orange")
            else:
                color.append("red")
    return color 

@app.route('/init')
def init():

    goaldb.create_tables()
    goaldb.populate_tables()

    return json.dumps("done!")



@app.route("/guest", methods=['GET'])
def guest():

    
    today = goaldb.fetch_today()
    today = checked_unchecked(today[0])
    daily = goaldb.fetch_all_daily()
    week = goaldb.fetch_current_week()

    month = goaldb.fetch_current_month()[0]


    return render_template("guest.html",  daily=color_picker(daily),
                                          week=color_picker(week),
                                          data=daily,
                                          lonk=len(daily),
                                          today=today,
                                          month=month)



from models import User

### LOGIN ###

@login_manager.user_loader
def load_user(user_id):
    return getUser(user_id)       

@app.route('/login', methods=['GET', 'POST'])
def login():
    incorrect_attempt = ""
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    if request.method == 'POST':

        print("LOGIN DETAILS:")
        print(escape(request.form['username']))
        print(escape(request.form['password']))
        session['username'] = escape(request.form['username'])
        session['password'] = escape(request.form['password'])

        user = User(username=session['username'])

        if user.check_password(session['password']):    
        # Login and validate the user.
        # user should be an instance of your `User` class

            login_user(user)

            flash('Logged in successfully.')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not escape(next):
                return abort(400)

            return redirect(next or url_for('home'))
        else:
            incorrect_attempt = "Wrong username/password!"
    return render_template('login.html', incorrect_attempt=incorrect_attempt)                                   