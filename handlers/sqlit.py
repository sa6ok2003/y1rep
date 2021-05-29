import sqlite3
def reg_user(id,refka):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time (
        id BIGINT,
        status_pod,
        money,
        ref
        ) """)
    db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id ={id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?,?,?)", (id,0,0,f'{refka}'))
        db.commit()

    #Создание таблицы с метками
    sql.execute(""" CREATE TABLE IF NOT EXISTS url_metka (
           metka,
           opisanie
           ) """)
    db.commit()
    sql.execute(f"SELECT metka FROM url_metka WHERE metka ='{0}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO url_metka VALUES (?,?)", ('0','0'))
        db.commit()

def add_urlmetka(url,text):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT metka FROM url_metka WHERE metka = '{url}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO url_metka VALUES (?,?)", (url,text))
        db.commit()

def dannie_metki(metka):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM user_time WHERE ref = '{metka}'").fetchall()[0][0]
    money = sql.execute(f"SELECT money FROM user_time WHERE ref = '{metka}'").fetchall()

    s = 0
    for i in money:
        s+= i[0]

    return a,s

def info_metki():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute("SELECT * FROM url_metka").fetchall()
    return a


def channeg_status(id): #Изменения статуса пользователя
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE user_time SET status_pod = 1 WHERE id = {id}")
    db.commit()

def channeg_money(id,summ): #Изменения баланса
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    money = sql.execute(f"SELECT money FROM user_time WHERE id ={id}").fetchone()
    money = money[0]
    sql.execute(f"UPDATE user_time SET money = {summ+money} WHERE id = {id}")
    db.commit()

def cheak_status(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT status_pod FROM user_time WHERE id ={id}").fetchone()
    return a[0]

def cheak_money(id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT money FROM user_time WHERE id ={id}").fetchone()
    return a[0]

def members_list():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a