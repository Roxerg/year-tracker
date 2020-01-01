import os

from flask import Flask, escape, request, render_template, url_for, redirect
import json
from datetime import datetime


import goaldb

app = Flask(__name__)

app.config.from_json("config.json")

# Externally Visible Server
# app.run(host='0.0.0.0')



@app.route('/')
def home():

    today = goaldb.fetch_today()
    today = checked_unchecked(today[0])
    daily = goaldb.fetch_all_daily()
    week = goaldb.fetch_current_week()

    month = goaldb.fetch_current_month()[0]

    print(week)

    return render_template("home.html", daily=color_picker(daily),
                                        week=color_picker(week),
                                        data=daily,
                                        lonk=len(daily),
                                        today=today,
                                        month=month)




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

    print(e)
    print(e)
    print(e)
    print(e)
    print(e)
    print(e)
    print(e)
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