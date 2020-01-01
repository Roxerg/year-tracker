import psycopg2
import asyncio




def connect():
    conn = psycopg2.connect(host="localhost",
                            database="newyear", 
                            user="resolutions", 
                            password="mongol111")
    cur = conn.cursor()

    return conn, cur

def disconnect(conn, cur):
    cur.close()
    conn.close()


def execute_query(q, p):

    conn, cur = connect()
    
    cur.execute(q, p)
    
    try:
        res = cur.fetchall()
    except:
        res = []

    conn.commit()
    disconnect(conn, cur)

    return res

def execute_query_no_args(q):

    conn, cur = connect()
    
    cur.execute(q)
    
    try:
        res = cur.fetchall()
    except:
        res = []

    conn.commit()
    disconnect(conn, cur)

    return res

def execute_queries(qs, ps):

    conn, cur = connect()

    for n in range(0, len(qs)):
        cur.execute(qs[n],tuple([ps[n]]))

    conn.commit()
    disconnect(conn, cur)

def repeat_queries(q, ps):

    conn, cur = connect()

    for n in range(0, len(ps)):
        print("query:")
        print(q)
        print("params:")
        print(ps[n])
        print("after params")
        cur.execute(q,tuple([ps[n]]))

    conn.commit()
    disconnect(conn, cur)




def create_tables():

    daily_goals = """
    CREATE TABLE daily_goals(
    id SERIAL PRIMARY KEY,
    reading int DEFAULT 0,
    exercise int DEFAULT 0,
    proper_sleep int DEFAULT 0,
    day DATE);
    """

    monthly_goals = """
    CREATE TABLE monthly_goals(
    id SERIAL PRIMARY KEY,
    alcohol int DEFAULT 0,
    meal_preps int DEFAULT 0,
    resist int DEFAULT 0,
    month DATE);
    """

    execute_query_no_args(daily_goals)
    execute_query_no_args(monthly_goals)




def date_gen(year, month, day, j):
    if(int(day)<10):
        day = "0" + str(day)
    else:
        day = str(day)

    res = j.join([str(year), str(month), str(day)])

    return res



def populate_tables(): 
    
    populate_daily = "INSERT INTO daily_goals (day) VALUES (%s);"
    populate_monthly = "INSERT INTO monthly_goals (month) VALUES (%s);"

    dates = []
    months = []
    year = "2020"
    month = "01"
    j = "-"


    for m in range(1, 12):
        months.append(date_gen(year, m, "1", j)) 

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))
        

    month = "02"

    for day in range(1, 30):
        dates.append(date_gen(year, month, day, j))

    month = "03"

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))

    month = "04"

    for day in range(1, 31):
        dates.append(date_gen(year, month, day, j))

    month = "05"

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))

    month = "06"

    for day in range(1, 31):
        dates.append(date_gen(year, month, day, j))

    month = "07"

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))

    month = "08"

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))

    month = "09"

    for day in range(1, 31):
        dates.append(date_gen(year, month, day, j))

    month = "10"

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))

    month = "11"

    for day in range(1, 31):
        dates.append(date_gen(year, month, day, j))

    month = "12"

    for day in range(1, 32):
        dates.append(date_gen(year, month, day, j))

    repeat_queries(populate_daily, dates)
    repeat_queries(populate_monthly, months)


def update_day(reading, exercise, sleep):
    
    update_daily = """
    UPDATE daily_goals 
    SET reading=reading+%s, exercise=exercise+%s, proper_sleep=proper_sleep+%s
    WHERE EXTRACT(DOY FROM NOW()) = EXTRACT(DOY FROM TIMESTAMP day)
    AND EXTRACT(YEAR FROM NOW()) = EXTRACT(YEAR FROM day);  
    """

    execute_query(update_daily, (reading, exercise, sleep))



def update_month(alcohol, meal, resist):

    update_monthly = """
    UPDATE monthly_goals
    SET alcohol=alcohol+%s, meal_preps=meal_preps+%s, resist=resist+%s,
    WHERE EXTRACT(MONTH FROM NOW()) = EXTRACT(MONTH FROM month)
    AND EXTRACT(YEAR FROM NOW()) = EXTRACT(YEAR FROM month); 
    """

    execute_query(update_monthly, (alcohol, meal, resist))

def fetch_all_daily():
    omg = "SELECT * FROM daily_goals"
    return execute_query_no_args(omg)

def fetch_all_monthly():
    omg = "SELECT * FROM monthly_goals"
    return execute_query_no_args(omg)

def fetch_current_week():
    get = """SELECT * FROM daily_goals 
    WHERE EXTRACT(WEEK FROM day) = EXTRACT(WEEK FROM NOW())
    AND EXTRACT(YEAR FROM NOW()) = EXTRACT(YEAR FROM day); """
    return execute_query_no_args(get)


def fetch_current_month():
    get = """SELECT * FROM daily_goals 
    WHERE EXTRACT(MONTH FROM day) = EXTRACT(MONTH FROM now)
    AND EXTRACT(YEAR FROM NOW()) = EXTRACT(YEAR FROM day); """
    return execute_query_no_args(get)


def fetch_today():
    get = """SELECT * FROM daily_goals 
    WHERE EXTRACT(DOY FROM day) = EXTRACT(DOY FROM NOW())
    AND EXTRACT(YEAR FROM NOW()) = EXTRACT(YEAR FROM day)
    LIMIT 1; """
    return execute_query_no_args(get)