#!/usr/bin/python

""""""

import wx, time, os, base64
import socket as sk
from libs import isThread, sendOnSocket, recvOnSocket
from img import Image
from database import DataBase

HOST = sk.gethostname()
POST = 9999

class MainWin(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Server', size=(400, 400))
        self.SetIcon(Image['icon'].GetIcon())
        self.statusbar = self.CreateStatusBar()
        self.notexitted = True
        self.clients = []
        self.statusbar.SetStatusText('%s connection(s) currently' %len(self.clients))
        self.addWidgets()
        self.database = DataBase()
        self.Bind(wx.EVT_CLOSE, self.exit)
        self.show()
        self.thread = self.openServer()
        
    def addWidgets(self):
        self.text = wx.ListCtrl(self, style=wx.LC_REPORT|wx.LC_VRULES|wx.LC_HRULES)
        self.text.AppendColumn('Ip Address')
        self.text.AppendColumn('Port')
        self.text.AppendColumn('Username')
        
    def show(self):
        self.Show()
        
    def exit(self, event):
        self.notexitted = False
        self.server.close()
        self.Destroy()

    @isThread
    def openServer(self):
        self.server = sk.socket()
        self.server.bind((HOST, POST))
        while True:
            try:
                self.server.listen()
                client, addr = self.server.accept()
            except:
                break
            self.openConnection(client, addr)
            self.clients.append(client)
            
    @isThread
    def openConnection(self, client, addr):
        self.statusbar.SetStatusText('%s connection(s) currently' %len(self.clients))
        if recvOnSocket(client)!='test':
            online = False
            status = recvOnSocket(client)
            user = recvOnSocket(client)
            pasw = recvOnSocket(client)
            if user!='' and pasw!='':
                if status=='register':
                    sex = recvOnSocket(client)
                    check = self.database.checkAccount(user)
                    if check=='OK':
                        self.database.addAccount(user, pasw, sex)
                elif status=='log in':
                    check = self.database.checkAccount(user, pasw)
                    if check=='OK':
                        self.text.Append((addr[0], addr[1], user))
                        online = True
                if not sendOnSocket(client, check):
                    online = False
            if online:
                self.database.setOnline(user, True)
                history = [{}, {}] #0.after 1.before
            while online and self.notexitted:
                #print(user, check)
                data = recvOnSocket(client)
                #if data!='check':
                print(user+': '+data, time.time())
                if data=='':
                    break
                elif data=='check':
                    if not self.check(client, user, history):
                        break
                elif data=='avatar':
                    if not self.getAvatar(client, user):
                        break
                elif data=='loadfriendlist':
                    if not self.loadFriendList(client, user):
                        break
                elif data=='addfriend':
                    if not self.addFriend(client, user):
                        break
                elif data=='changeavatar':
                    if not self.changeAvatar(client, user):
                        break
                elif data=='newmsg':
                    if not self.sendMsg(client, user):
                        break
                elif data=='loadhistory':
                    if not self.loadHistory(client, user, history):
                        break
                elif data=='startchat':
                    if not self.startChat(client, user, history):
                        break
                elif data=='announcement':
                    if not self.announcement(client, user):
                        break
            if online:
                self.database.setOnline(user, False)
            for item in range(self.text.GetItemCount()):
                if (self.text.GetItemText(item, 0)==addr[0] and 
                    self.text.GetItemText(item, 1)==str(addr[1]) and 
                    self.text.GetItemText(item, 2)==user
                ):
                    self.text.DeleteItem(item)
                    break
        client.close()
        self.clients.remove(client)
        self.statusbar.SetStatusText('%s connection(s) currently' %len(self.clients))
        
    def check(self, client, user, history):
        data = self.database.checkNewMsg(user)
        #print(user+': ', data)
        if data:
            if not sendOnSocket(client, data[0]):
                return False
            if data[0]=='addfriend':
                if not sendOnSocket(client, data[1]):
                    return False
            elif data[0]=='online':
                if not sendOnSocket(client, data[1]):
                    return False
                if not sendOnSocket(client, data[3]):
                    return False
                if not sendOnSocket(client, self.database.getAvatar([(data[1],)])[0][0]):
                    return False
            elif data[0]=='newmsg':
                if data[1] not in history[0].keys():
                    history[0].update({data[1]:data[2]})
                    history[1].update({data[1]:data[2]-86400})
                if not sendOnSocket(client, data[1]):
                    return False
                if not sendOnSocket(client, time.ctime(data[2])):
                    return False
                if not sendOnSocket(client, data[3]):
                    return False
            elif data[0]=='announcement':
                if not sendOnSocket(client, data[1]):
                    return False
                if not sendOnSocket(client, time.ctime(data[2])):
                    return False
                if not sendOnSocket(client, data[3]):
                    return False
        else:
            if not sendOnSocket(client, 'NO'):
                return False
        return True
        
    def getAvatar(self, client, user):
        if not sendOnSocket(client, self.database.getAvatar([(user,)])[0][0]):
            return False
        return True
        
    def loadFriendList(self, client, user):
        data = self.database.getFriendList(user)
        l = len(data)
        if not sendOnSocket(client, str(l)):
            return False
        if l!=0:
            avatar = self.database.getAvatar(data)
            online = self.database.getOnline(data)
            for i in range(l):
                if not sendOnSocket(client, data[i][0]):
                    return False
                if not sendOnSocket(client, avatar[i][0]):
                    return False
                if not sendOnSocket(client, online[i][0]):
                    return False
        return True
    
    def addFriend(self, client, user):
        friend = recvOnSocket(client)
        if friend=='':
            return False
        if self.database.checkAccount(friend)=='user is available':
            self.database.addFriend(user, friend)
            if not sendOnSocket(client, 'OK'):
                return False
        else:
            if not sendOnSocket(client, 'Username is not available'):
                return False
        return True
    
    def changeAvatar(self, client, user):
        avatar = recvOnSocket(client)
        if avatar=='':
            return False
        self.database.changeAvatar(user, avatar)
        if not self.getAvatar(client, user):
            return False
        self.database.setOnline(user, True)
        return True
    
    def sendMsg(self, client, From):
        To = recvOnSocket(client)
        content = recvOnSocket(client)
        if To=='' or content=='':
            return False
        t = time.time()
        self.database.sendMsg(From, To, content, t)
        if not sendOnSocket(client, time.ctime(t)):
            return False
        return True
    
    def loadHistory(self, client, user, history):
        friend = recvOnSocket(client)
        if friend=='':
            return False
        data = self.database.loadHistory(user, friend, history[0][friend], history[1][friend])
        history[0][friend] -= 86400
        history[1][friend] -= 86400
        l = len(data)
        if not sendOnSocket(client, str(l)):
            return False
        for line in data:
            if not sendOnSocket(client, line):
                return False
        if not sendOnSocket(client, time.ctime(history[0][friend])):
            return False
        return True
    
    def startChat(self, client, user, history):
        friend = recvOnSocket(client)
        if friend not in history[0].keys():
            history[0].update({friend:time.time()})
            history[1].update({friend:time.time()-86400})
        if friend=='':
            return False
        avatars = self.database.getAvatar(((user,),(friend,)))
        for data in avatars:
            if not sendOnSocket(client, data[0]):
                return False
        if not sendOnSocket(client, time.ctime(history[0][friend])):
            return False
        return True
    
    def announcement(self, client, From):
        To = recvOnSocket(client)
        content = recvOnSocket(client)
        if To=='' or content=='':
            return False
        t = time.time()
        self.database.announcement(From, To, content, t)
        return True

def main():
    app = wx.App()
    MainWin()
    app.MainLoop()
    return True

if __name__ == '__main__':
    main()
