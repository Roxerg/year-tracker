import os

from flask import Flask, escape, request, render_template, url_for
import json
from datetime import datetime


import goaldb

app = Flask(__name__)



@app.route('/')
def home():

    daily = goaldb.fetch_all_daily()
    week = goaldb.fetch_current_week()

    print(week)
    
    return render_template("home.html", daily=color_picker(daily),
                                        week=color_picker(week))


def color_picker(daily):
    color = []
    day_of_year = datetime.now().timetuple().tm_yday
    for d in daily:
        if day_of_year > d[0]:
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