import sqlite3

with sqlite3.connect('database.db') as con:
    cur = con.cursor()
    cur.execute('SELECT username, online FROM accounts')
    print(cur.fetchall())
    cur.execute('UPDATE accounts SET online="False"')
    cur.execute('SELECT username, online FROM accounts')
    print(cur.fetchall())