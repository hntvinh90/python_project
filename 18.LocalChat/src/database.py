#!/usr/bin/python

""""""

import sqlite3, time
from img import Male, Female

class DataBase:
    def __init__(self):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            try:
                cur.execute('''CREATE TABLE accounts (
                    username text,
                    password text,
                    online text,
                    avatar text,
                    sex text
                )''')
                con.commit()
            except: pass
            cur.execute('UPDATE accounts SET online="False"')
            con.commit()
        
    def checkAccount(self, user, pasw=''):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT password, online FROM accounts WHERE username=?', (user,))
            data = cur.fetchone()
            if pasw=='':
                if data:
                    status = 'user is available'
                else:
                    status = 'OK'
            else:
                if data:
                    if data[1]=='True':
                        status = 'isOnline'
                    else:
                        if data[0]==pasw:
                            status = 'OK'
                        else:
                            status = 'password is wrong'
                else:
                    status = 'user does not exist'
        return status
        
    def addAccount(self, user, pasw, sex):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            if sex=='Female':
                avatar = Female
            else:
                avatar = Male
            cur.execute('INSERT INTO accounts VALUES (?, ?, ?, ?, ?)', (user, pasw, 'False', avatar, sex,))
            cur.execute('''CREATE TABLE %s (
                type text,
                username text,
                date real,
                content text,
                direction text
            )''' % (user+'history',))
            cur.execute('''CREATE TABLE %s (
                type text,
                username text,
                date real,
                content text
            )''' % (user+'newmsg',))
            cur.execute('''CREATE TABLE %s (
                username text
            )''' % (user+'friends',))
            con.commit()
            
    def getAvatar(self, users):
        data = []
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            for user in users:
                cur.execute('SELECT avatar FROM accounts WHERE username=?', (user[0],))
                data.append(cur.fetchone())
        return data
    
    def getOnline(self, users):
        data = []
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            for user in users:
                cur.execute('SELECT online FROM accounts WHERE username=?', (user[0],))
                data.append(cur.fetchone())
        return data
    
    def getFriendList(self, user):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT username FROM %sfriends ORDER BY username'%(user,))
            data = cur.fetchall()
        return data
    
    def checkNewMsg(self, user):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM %snewmsg ORDER BY date'%(user,))
            data = cur.fetchone()
            if data:
                cur.execute('DELETE FROM %snewmsg WHERE date=?'%(user,), (data[2],))
            con.commit()
        return data
    
    def addFriend(self, user, friend):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO %sfriends VALUES (?)'%(user,), (friend,))
            cur.execute('SELECT username FROM %sfriends'%(friend,))
            data = cur.fetchall()
            if (user,) not in data:
                cur.execute('INSERT INTO %snewmsg VALUES (?, ?, ?, ?)'%(friend,), ('addfriend', user, time.time(), ''))
            con.commit()
        
    def setOnline(self, user, state):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('UPDATE accounts SET online=? WHERE username=?', (str(state), user))
            cur.execute('SELECT username FROM %sfriends ORDER BY username'%(user,))
            data = cur.fetchall()
            for friend in data:
                cur.execute('SELECT online FROM accounts WHERE username=?', (friend[0],))
                if cur.fetchone()[0]=='True':
                    cur.execute('INSERT INTO %snewmsg VALUES (?, ?, ?, ?)'%(friend[0],), ('online', user, time.time(), str(state)))
            con.commit()
            
    def changeAvatar(self, user, avatar):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('UPDATE accounts SET avatar=? WHERE username=?', (avatar, user))
            con.commit()
            
    def sendMsg(self, From, To, content, date):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO %snewmsg VALUES (?, ?, ?, ?)'%(To,), ('newmsg', From, date, content))
            cur.execute('INSERT INTO %shistory VALUES (?, ?, ?, ?, ?)'%(To,), ('newmsg', From, date, content, 'recv'))
            cur.execute('INSERT INTO %shistory VALUES (?, ?, ?, ?, ?)'%(From,), ('newmsg', To, date, content, 'send'))
            con.commit()
            
    def loadHistory(self, user, friend, after, before):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('SELECT * FROM %shistory WHERE username=? AND date<? AND date>=? ORDER BY date'%(user,), (friend, after, before))
            data = cur.fetchall()
        result = []
        for line in data:
            result.append(line[4]+time.ctime(line[2])+'::'+line[3])
        return result
    
    def announcement(self, From, To, content, date):
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('INSERT INTO %snewmsg VALUES (?, ?, ?, ?)'%(To,), ('announcement', From, date, content))
            con.commit()
