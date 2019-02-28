#!/usr/bin/python

""""""

import wx, time, hashlib, sys
from wx.lib.embeddedimage import PyEmbeddedImage
import socket as sk
from libs import isThread, sendOnSocket, recvOnSocket
from client_setting import Setting
from client_menubar import MenuBar, LoggedMenuBar
from client_popupmenu import PopupAvatar
from img import Image

TIME_SLEEP = 100 #miliseconds

class MainWin(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="LocalChat", size=(400, 600),
            style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        )
        self.SetIcon(Image['icon'].GetIcon())
        self.setting = Setting(self)
        if self.setting.HOST=='':
            wx.MessageBox('Can not find out server', 'Error')
            sys.exit()
        self.menubar = MenuBar(self)
        self.loginpanel = LogInPanel(self)
        self.logedpanel = LoggedPanel(self)
        self.cache = []
        self.chatingwindow = {}
        self.announcementwindow = {}
        self.Bind(wx.EVT_CLOSE, self.exit)
        self.show()
        
    def show(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.loginpanel, 1, wx.EXPAND)
        sizer.Add(self.logedpanel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.logedpanel.hide()
        self.Show()
        
    def exit(self, event=0):
        if wx.MessageBox('Do you want to exit?', 'Warning', style=wx.YES_NO)==wx.YES:
            try:
                self.client.close()
            except: pass
            wins = list(self.chatingwindow.values())
            for win in wins:
                win.Close()
            wins = list(self.announcementwindow.values())
            for win in wins:
                win.Close()
            self.Destroy()
        
    def onCloseBtn(self, event):
        self.Iconize(True)
        
    def connectToServer(self, var):
        self.client = sk.socket()
        try:
            self.client.connect((self.setting.HOST, self.setting.POST))
        except:
            self.client.close()
            return 'can not connect to server'
        sendOnSocket(self.client, 'connect')
        for string in var:
            if not sendOnSocket(self.client, string):
                return 'can not connect to server'
        data = recvOnSocket(self.client)
        if data == '':
            return 'can not connect to server'
        else:
            return data
        
class LogInPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.SetBackgroundColour('#5b9bd5')
        self.addWidgets()
        
    def addWidgets(self):
        self.user_input = wx.TextCtrl(self, -1, self.parent.setting.username)
        self.pasw_input = wx.TextCtrl(self, -1, style=wx.TE_PASSWORD)
        self.repasw_input = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.user_lbl = wx.StaticText(self, -1, 'Username')
        self.pasw_lbl = wx.StaticText(self, -1, 'Password')
        self.repasw_lbl = wx.StaticText(self, -1, 'Confirm Password')
        self.sex = wx.RadioBox(self, choices=['Male', 'Female'])
        self.reg_lbl = wx.StaticText(self, -1, 'Register')
        self.log_lbl = wx.StaticText(self, -1, 'Log in')
        self.log_btn = wx.Button(self, -1, 'Log in')
        self.reg_btn = wx.Button(self, -1, 'Register')
        self.status_lbl = wx.StaticText(self)
        
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add((1,1), 1)
        sizer1.Add(self.user_lbl)
        sizer1.Add(self.user_input, 0, wx.EXPAND)
        sizer1.Add((20, 20))
        sizer1.Add(self.pasw_lbl)
        sizer1.Add(self.pasw_input, 0, wx.EXPAND)
        sizer1.Add((20, 20))
        sizer1.Add(self.repasw_lbl)
        sizer1.Add(self.repasw_input, 0, wx.EXPAND)
        sizer1.Add((20, 20))
        sizer1.Add(self.sex, 0, wx.CENTER)
        sizer1.Add((20, 20))
        sizer1.Add(self.reg_lbl, 0, wx.CENTER)
        sizer1.Add(self.log_lbl, 0, wx.CENTER)
        sizer1.Add((20, 20))
        sizer1.Add(self.log_btn, 0, wx.CENTER)
        sizer1.Add(self.reg_btn, 0, wx.CENTER)
        sizer1.Add((20, 20))
        sizer1.Add(self.status_lbl, 0, wx.EXPAND)
        sizer1.Add((1,1), 1)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((1, 1), 1)
        sizer.Add(sizer1, 3, wx.EXPAND)
        sizer.Add((1, 1), 1)
        self.SetSizer(sizer)
        
        self.repasw_lbl.Show(False)
        self.repasw_input.Show(False)
        self.sex.Show(False)
        self.log_lbl.Show(False)
        self.reg_btn.Show(False)
        
        font = wx.Font(wx.DEFAULT, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=True)
        self.reg_lbl.SetFont(font)
        self.log_lbl.SetFont(font)
        self.reg_lbl.SetForegroundColour('#0000ff')
        self.log_lbl.SetForegroundColour('#0000ff')
        self.reg_lbl.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.log_lbl.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.status_lbl.SetForegroundColour('#ff0000')
        
        self.reg_lbl.Bind(wx.EVT_LEFT_DOWN, self.onRegLbl)
        self.log_lbl.Bind(wx.EVT_LEFT_DOWN, self.onLogLbl)
        self.log_btn.Bind(wx.EVT_BUTTON, self.onLogIn)
        self.reg_btn.Bind(wx.EVT_BUTTON, self.onRegister)
        
    def show(self):
        self.Show()
        self.onLogLbl(0)
        self.menubar = MenuBar(self.parent)
        self.parent.Layout()
        self.Enable(True)
        self.user_input.SetFocus()
        self.user_input.SetSelection(0, self.user_input.GetLastPosition())
        self.parent.Bind(wx.EVT_CLOSE, self.parent.exit)
        
    def hide(self):
        self.Show(False)
        self.parent.Layout()
        self.Enable(False)
        
    def onRegLbl(self, event):
        self.status_lbl.SetLabel('')
        self.repasw_lbl.Show()
        self.repasw_input.Show()
        self.sex.Show()
        self.log_lbl.Show()
        self.reg_btn.Show()
        self.reg_lbl.Show(False)
        self.log_btn.Show(False)
        self.Layout()
        self.user_input.Clear()
        self.pasw_input.Clear()
        self.repasw_input.Clear()
        self.user_input.SetFocus()
        
    def onLogLbl(self, event):
        self.status_lbl.SetLabel('')
        self.repasw_lbl.Show(False)
        self.repasw_input.Show(False)
        self.sex.Show(False)
        self.log_lbl.Show(False)
        self.reg_btn.Show(False)
        self.reg_lbl.Show()
        self.log_btn.Show()
        self.Layout()
        self.user_input.SetValue(self.parent.setting.username)
        self.pasw_input.Clear()
        self.user_input.SetFocus()
        self.user_input.SetSelection(0, self.user_input.GetLastPosition())
    
    def onLogIn(self, event):
        self.status_lbl.SetLabel('')
        username = self.user_input.GetValue()
        password = self.pasw_input.GetValue()
        if username=='':
            self.status_lbl.SetLabel('** Username is empty')
        if password=='':
            self.status_lbl.SetLabel(self.status_lbl.GetLabel() + '\n** Password is empty')
        self.Layout()
        if self.status_lbl.GetLabel()=='':
            status = self.parent.connectToServer(('log in', username, hashlib.md5(password.encode()).hexdigest()))
            if status != 'OK':
                self.parent.client.close()
                if status == 'can not connect to server':
                    wx.MessageBox('Can not connect to server', 'Error')
                elif status == 'user does not exist':
                    wx.MessageBox('Username is not available', 'Error')
                elif status == 'password is wrong':
                    wx.MessageBox('Password was wrong', 'Error')
                elif status == 'can not log in':
                    wx.MessageBox('Can not log in\nCheck your username and password', 'Error')
                elif status == 'isOnline':
                    wx.MessageBox('An account can not log in multiple times\nPerhaps someone is using your account', 'Error')
            else:
                self.parent.setting.username = username
                self.parent.setting.savePref()
                self.hide()
                self.parent.logedpanel.show(username)
        
    def onRegister(self, event):
        self.status_lbl.SetLabel('')
        username = self.user_input.GetValue()
        password = self.pasw_input.GetValue()
        repassword = self.repasw_input.GetValue()
        sex = self.sex.GetStringSelection()
        if username=='':
            self.status_lbl.SetLabel('** Username is empty\n')
        elif username.find(' ')!=-1:
            self.status_lbl.SetLabel(self.status_lbl.GetLabel() + '** Username contains space character\n')
        if password=='':
            self.status_lbl.SetLabel(self.status_lbl.GetLabel() + '** Password is empty\n')
        if repassword!=password:
            self.status_lbl.SetLabel(self.status_lbl.GetLabel() + '** The password confirmation does not match\n')
        self.Layout()
        if self.status_lbl.GetLabel()=='':
            status = self.parent.connectToServer(('register', username, hashlib.md5(password.encode()).hexdigest(), sex))
            if status == 'can not connect to server':
                wx.MessageBox('Can not connect to server', 'Error')
            elif status == 'user is available':
                wx.MessageBox('Username is available', 'Error')
            else:
                wx.MessageBox('Successful registration!', 'Attention')
                self.onLogLbl(0)
            self.parent.client.close()
        else:
            self.pasw_input.Clear()
            self.repasw_input.Clear()
    
class LoggedPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.addWidgets()
        self.addTimer()
        
    def addWidgets(self):
        self.avatar = wx.StaticBitmap(self, -1, wx.Bitmap())
        self.avatar.SetToolTip(wx.ToolTip('Right click to change your avatar'))
        self.userlbl = wx.StaticText(self)
        self.userlbl.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        self.userlbl.SetForegroundColour('#5b9bd5')
        add_btn = wx.BitmapButton(self, -1, Image['add'].GetBitmap(), style=wx.NO_BORDER)
        add_btn.SetBitmapCurrent(Image['add_hover'].GetBitmap())
        add_btn.SetBitmapPressed(Image['add_pressed'].GetBitmap())
        add_btn.SetToolTip(wx.ToolTip('Add New Friend'))
        self.contacts = ContactPanel(self)
        
        siz = wx.BoxSizer(wx.HORIZONTAL)
        siz.Add((10,1))
        siz.Add(self.avatar)
        siz.Add((10,1))
        siz.Add(self.userlbl, 1, wx.ALIGN_CENTER_VERTICAL)
        siz.Add(add_btn, 0, wx.ALIGN_CENTER_VERTICAL)
        siz.Add((10,1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1,10))
        sizer.Add(siz, 0, wx.EXPAND)
        sizer.Add((1,10))
        sizer.Add(self.contacts, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        add_btn.Bind(wx.EVT_BUTTON, self.onAddFriend)
        self.avatar.Bind(wx.EVT_RIGHT_UP, self.onAvatar)
        
    def addTimer(self):
        self.timer = wx.Timer(self)
        self.lock = False
        self.lock_GUI = False
        self.Bind(wx.EVT_TIMER, self.onTimer)
        
    def show(self, user):
        self.user = user
        self.friends = []
        self.cache = []
        self.Show()
        self.menubar = LoggedMenuBar(self.parent)
        self.parent.Layout()
        self.parent.Bind(wx.EVT_CLOSE, self.parent.onCloseBtn)
        self.Enable(True)
        self.parent.cache.append(('avatar',))
        self.parent.cache.append(('loadfriendlist',))
        self.timer.Start(TIME_SLEEP)
        
    def hide(self):
        self.Show(False)
        self.parent.Layout()
        self.Enable(False)
        self.parent.cache = []
        wins = list(self.parent.chatingwindow.values())
        for win in wins:
            win.Close()
        wins = list(self.parent.announcementwindow.values())
        for win in wins:
            win.Close()
        self.timer.Stop()
        
    def disconnect(self, event=0):
        try:
            self.parent.client.close()
            self.hide()
            self.parent.loginpanel.show()
            print('client out')
        except: 
            pass
            print('can not log out')
    
    @isThread
    def openConnection(self, event=0):
        if self.lock:
            return
        self.lock = True
        print(self.user,'in', time.time())
        if len(self.parent.cache)==0:
            if not self.check():
                return self.disconnect()
        else:
            for data in self.parent.cache[0]:
                if not sendOnSocket(self.parent.client, data):
                    return self.disconnect()
            if self.parent.cache[0][0]=='avatar':
                if not self.getAvatar():
                    return self.disconnect()
            elif self.parent.cache[0][0]=='loadfriendlist':
                if not self.loadFriendList():
                    return self.disconnect()
            elif self.parent.cache[0][0]=='addfriend':
                data = recvOnSocket(self.parent.client)
                if data=='OK':
                    self.parent.cache.append(('loadfriendlist',))
                else:
                    wx.MessageBox(data, 'Error')
            elif self.parent.cache[0][0]=='changeavatar':
                if not self.getAvatar():
                    return self.disconnect()
            elif self.parent.cache[0][0]=='newmsg':
                if not self.sendMsg(self.parent.cache[0][1], self.parent.cache[0][2]):
                    return self.disconnect()
            elif self.parent.cache[0][0]=='loadhistory':
                if not self.loadHistory(self.parent.cache[0][1]):
                    return self.disconnect()
            elif self.parent.cache[0][0]=='startchat':
                if not self.startChat(self.parent.cache[0][1]):
                    return self.disconnect()
            self.parent.cache.pop(0)
        self.lock = False
        print(self.user,'out', time.time())
            
    def check(self):
        client = self.parent.client
        if not sendOnSocket(client, 'check'):
            return False
        data = recvOnSocket(client)
        if data=='':
            return False
        elif data=='addfriend':
            user = recvOnSocket(client)
            if user=='':
                return False
            if wx.MessageBox("%s would like to become your friend.\nDo you agree?"%(user,), 'Add Friend', style=wx.YES_NO)==wx.YES:
                self.parent.cache.append(('addfriend', user))
        elif data=='online':
            user = recvOnSocket(client)
            online = recvOnSocket(client)
            avatar = recvOnSocket(client)
            if user=='' or online=='' or avatar=='':
                return False
            self.contacts.updateFriend(user, avatar, online)
        elif data=='newmsg':
            From = recvOnSocket(client)
            date = recvOnSocket(client)
            content = recvOnSocket(client)
            if From=='' or date=='' or content=='':
                return False
            c = ''.join(('recv', date, '::', content))
            #if From not in self.parent.chatingwindow.keys():
            #    win = None
            #else:
            #    win = self.parent.chatingwindow[From]
            #if not win:
            #    win = ChattingWin(self.parent, From)
            #    self.parent.chatingwindow.update({From:win})
            self.cache.append(('appendhistory', From, c))
            #win.text.appendHistory(c)
        elif data=='announcement':
            From = recvOnSocket(client)
            date = recvOnSocket(client)
            content = recvOnSocket(client)
            if From=='' or date=='' or content=='':
                return False
            self.cache.append(('announcement', From, date, content))
        return True
            
    def getAvatar(self):
        client = self.parent.client
        data = recvOnSocket(client)
        if data=='':
            return False
        self.avatar.SetBitmap(PyEmbeddedImage(data).GetBitmap())
        self.userlbl.SetLabel(self.user)
        self.Layout()
        return True
        
    def loadFriendList(self):
        client = self.parent.client
        number = recvOnSocket(client)
        self.friends = []
        self.contacts.clearFriends()
        if number=='':
            return False
        elif number!='0':
            number = int(number)
            for i in range(number):
                user = recvOnSocket(client)
                avatar = recvOnSocket(client)
                online = recvOnSocket(client)
                if user!='' and avatar!='':
                    self.contacts.addFriend(user, avatar, online)
                    self.friends.append(user)
                else:
                    return False
        return True
    
    def startChat(self, friend):
        client = self.parent.client
        avatar_me = recvOnSocket(client)
        avatar_you = recvOnSocket(client)
        t = recvOnSocket(client)
        if avatar_me=='' or avatar_you=='' or t=='':
            print('error')
            return False
        win = self.parent.chatingwindow[friend]
        win.text.avatar_me = wx.Bitmap(PyEmbeddedImage(avatar_me).GetImage().Rescale(32, 32))
        win.text.avatar_you = wx.Bitmap(PyEmbeddedImage(avatar_you).GetImage().Rescale(32, 32))
        self.cache.append(('appendtime', win, t))
        #win.text.appendTime(t)
        return True
    
    def sendMsg(self, To, content):
        t = recvOnSocket(self.parent.client)
        if t=='':
            return False
        c = ''.join(('send', t, '::', content))
        #if To not in self.parent.chatingwindow.keys():
        #    win = None
        #else:
        #    win = self.parent.chatingwindow[To]
        #if not win:
        #    win = ChattingWin(self.parent, To)
        #    self.parent.chatingwindow.update({To:win})
        self.cache.append(('appendhistory', To, c))
        #win.text.appendHistory(c)
        return True
    
    def loadHistory(self, friend):
        size = recvOnSocket(self.parent.client)
        if size!='':
            lines = []
            for _ in range(int(size)):
                lines.append(recvOnSocket(self.parent.client))
            t = recvOnSocket(self.parent.client)
            win = self.parent.chatingwindow[friend]
            self.cache.append(('inserthistory', win, lines))
            self.cache.append(('appendtime', win, t))
            #win.text.insertHistory(lines, 1, 'history')
            #win.text.appendTime(t)
            return True
        else:
            return False
        
    def onAddFriend(self, event):
        username = wx.GetTextFromUser('Nickname of your friend:', 'Add Friend')
        if username!='':
            if username in self.friends:
                wx.MessageBox('The username was your friend', 'Attention')
            else:
                self.parent.cache.append(('addfriend', username))
    
    def onAvatar(self, event):
        self.PopupMenu(PopupAvatar(self.parent), event.GetPosition())
        
    def onTimer(self, event=0):
        print('OnTimer')
        self.openConnection()
        if self.lock_GUI:
            return
        self.lock_GUI = True
        if len(self.cache)!=0:
            data = self.cache[0]
            self.cache.pop(0)
            if data[0]=='appendhistory':
                if data[1] not in self.parent.chatingwindow.keys():
                    win = None
                else:
                    win = self.parent.chatingwindow[data[1]]
                if not win:
                    win = ChattingWin(self.parent, data[1])
                    self.parent.chatingwindow.update({data[1]:win})
                win.text.appendHistory(data[2])
            elif data[0]=='appendtime':
                data[1].text.appendTime(data[2])
            elif data[0]=='inserthistory':
                data[1].text.insertHistory(data[2], 1, 'history')
            elif data[0]=='announcement':
                if data[1] not in self.parent.announcementwindow.keys():
                    win = None
                else:
                    win = self.parent.announcementwindow[data[1]]
                if not win:
                    win = AnnouncementWindow(self.parent, data[1])
                    self.parent.announcementwindow.update({data[1]:win})
                win.appendAnnoucement(data[2], data[3])
        self.lock_GUI = False
        
class ContactPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.parent = parent #logged panel
        self.nofriend = wx.StaticText(self, -1, 'You have no friend.')
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.nofriend, 0, wx.EXPAND)
        
        self.contacts = wx.ListCtrl(self, style=wx.LC_REPORT|wx.LC_NO_HEADER|wx.LC_HRULES)
        self.contacts.AppendColumn('Avatar')
        self.contacts.AppendColumn('Username')
        self.contacts.SetColumnWidth(0, 64)
        self.sizer.Add(self.contacts, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.imgList = wx.ImageList(32, 32)
        self.contacts.AssignImageList(self.imgList, wx.IMAGE_LIST_SMALL)
        self.contacts.Show(False)
        self.contacts.Bind(wx.EVT_SIZE, self.onSizeContactPanel)
        self.contacts.Bind(wx.EVT_LEFT_DCLICK, self.startChat)
        self.contacts.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.showPopupOnItem)
        
    def clearFriends(self):
        self.imgList.RemoveAll()
        self.contacts.DeleteAllItems()
        self.contacts.Show(False)
        self.nofriend.Show()
        self.Layout()
    
    def addFriend(self, user, avatar, online=True):
        self.nofriend.Show(False)
        self.contacts.Show()
        item = self.contacts.Append(('', user))
        self.contacts.SetItemFont(item, self.font)
        if online=='True':
            self.imgList.Add(wx.Bitmap(PyEmbeddedImage(avatar).GetImage().Rescale(32, 32)))
        else:
            self.imgList.Add(wx.Bitmap(PyEmbeddedImage(avatar).GetImage().Rescale(32, 32).ConvertToDisabled()))
        self.contacts.SetItemImage(item, self.imgList.GetImageCount()-1)
        self.Layout()
        
    def updateFriend(self, user, avatar, online):
        for item in range(self.contacts.GetItemCount()):
            if self.contacts.GetItemText(item, 1)==user:
                if online=='True':
                    self.imgList.Replace(item, wx.Bitmap(PyEmbeddedImage(avatar).GetImage().Rescale(32, 32)))
                else:
                    self.imgList.Replace(item, wx.Bitmap(PyEmbeddedImage(avatar).GetImage().Rescale(32, 32).ConvertToDisabled()))
                self.contacts.SetItemImage(item, item)
                break
        
    def onSizeContactPanel(self, event):
        w = self.contacts.GetSize()[0]
        self.contacts.SetColumnWidth(1, w-64)
        
    def startChat(self, event):
        item = self.contacts.GetFirstSelected()
        if item!=-1:
            user = self.contacts.GetItemText(item, 1)
            if user in self.parent.parent.chatingwindow.keys():
                self.parent.parent.chatingwindow[user].SetFocus()
            else:
                self.parent.parent.chatingwindow.update({user:ChattingWin(self.parent.parent, user)})
        
    def showPopupOnItem(self, event):
        print(self.contacts.GetItemText(self.contacts.GetFirstSelected(), 1))
    
class ChattingWin(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, title="%s" %id, size=(400, 600),
            style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        )
        self.SetIcon(Image['icon_chat'].GetIcon())
        self.parent = parent #Client Window
        self.id = id
        self.ctrl = False
        self.addWidgets()
        self.addEvents()
        
        self.show()
        self.parent.cache.append(('startchat', self.id))
        
    def addWidgets(self):
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.text = HistoryPanel(self)
        self.input = wx.TextCtrl(self, size=(1, 100), style=wx.TE_MULTILINE|wx.TE_RICH)
        self.input.SetFont(self.font)
        self.send_btn = wx.Button(self, -1, 'Send')
        self.send_btn.Enable(False)
        self.input.SetFocus()
        
    def addEvents(self):
        self.Bind(wx.EVT_CLOSE, self.onExit)
        self.input.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.input.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.input.Bind(wx.EVT_TEXT, self.onInputMod)
        self.send_btn.Bind(wx.EVT_BUTTON, self.onSendBtn)
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
    
    def show(self):
        size1 = wx.BoxSizer(wx.HORIZONTAL)
        size1.Add(self.input, 1, wx.EXPAND)
        size1.Add(self.send_btn, 0, wx.EXPAND)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND)
        sizer.Add(size1, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()
        
    def loadHistory(self, event):
        pass
        
    def onExit(self, event):
        del self.parent.chatingwindow[self.id]
        self.Destroy()
        
    def onKeyDown(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_CONTROL:
            self.ctrl = True
        elif key == wx.WXK_RETURN:
            if not self.ctrl:
                if self.input.GetValue() != '':
                    self.onSendBtn(0)
                return
        event.Skip()
        
    def onKeyUp(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_CONTROL:
            self.ctrl = False
        event.Skip()
        
    def onSendBtn(self, event):
        self.parent.cache.append(('newmsg', self.id, self.input.GetValue()))
        self.input.SetValue('')
        self.input.SetFocus()
        
    def onInputMod(self, event):
        if self.input.GetValue() == '':
            self.send_btn.Enable(False)
        else:
            self.send_btn.Enable(True)
            
    def onFocus(self, event=0):
        self.input.SetFocus()
            
class HistoryPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, style=wx.SUNKEN_BORDER)
        self.parent = parent #Chatting window
        self.SetBackgroundColour('#ffffff')
        self.SetScrollbars(0, 10, 0, 0)
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        btn_get_history = wx.StaticText(self, -1, 'Get more history')
        btn_get_history.SetFont(wx.Font(wx.DEFAULT, wx.ROMAN, wx.NORMAL, wx.NORMAL, underline=True))
        btn_get_history.SetForegroundColour('#0000ff')
        btn_get_history.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        btn_get_history.Bind(wx.EVT_LEFT_DOWN, self.getHistory)
        self.sizer.Add(btn_get_history, 0, wx.CENTER)
        self.SetSizer(self.sizer)
        
        self.setting()
        
    def setting(self):
        self.avatar_me, self.avatar_you = None, None
        self.showed_avatar, self.avatar_id, self.state, self.before_id = [], 0, None, None
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.font2 = wx.Font(8, wx.ROMAN, wx.ITALIC, wx.NORMAL)
        
    def getHistory(self, event):
        self.parent.parent.cache.append(('loadhistory', self.parent.id))
        
    def insertHistory(self, text, index, act='end'):
        if act=='history':
            org_state, self.state, org_before, self.before_id = self.state, None, self.before_id, None
        before = self.GetScrollLines(wx.VERTICAL)
        for line in text:
            self.sizer.Insert(index, MessagePanel(self, line), 0, wx.EXPAND)
            index += 1
        self.FitInside()
        self.Refresh()
        after = self.GetScrollLines(wx.VERTICAL)
        if act=='end':
            self.Scroll(0, after)
        elif act=='history':
            self.Scroll(0, after-before)
            self.state, self.before_id = org_state, org_before
        
    def appendHistory(self, text):
        self.insertHistory((text,), self.sizer.GetItemCount())
        
    def appendTime(self, text):
        self.sizer.Insert(1, wx.StaticLine(self), 0, wx.EXPAND)
        st = wx.StaticText(self, -1, text)
        st.SetFont(self.font2)
        st.SetForegroundColour('#aaaaaa')
        self.sizer.Insert(1, st, 0, wx.CENTER)
        self.FitInside()
        
class MessagePanel(wx.Panel):
    def __init__(self, parent, text):
        w_parent = parent.GetSize().width-10
        dc = wx.ClientDC(parent)
        dc.SetFont(parent.font)
        w_char, h_char = dc.GetCharWidth(), dc.GetCharHeight()
        dc.SetFont(parent.font2)
        start = text.find('::')
        w_max, h_date = dc.GetTextExtent(text[4:start])
        w_limit = w_parent - 84
        lines=[]
        for line in text[start+2:].split('\n'):
            w = 0
            lines.append([])
            for word in line.split(' '):
                w += w_char*(len(word)+1)
                if w>=w_limit:
                    w = 0
                    lines.append([])
                    w_max = w_limit
                if w>w_max:
                    w_max = w
                lines[-1].append(word)
        w_text = w_max + 20
        h_text = len(lines)*h_char + h_date + 20
        wx.Panel.__init__(self, parent, size=(w_parent, h_text))
        self.parent = parent #HistoryPanel
        #self.SetBackgroundColour('#00ff00')
        self.state = text[:4]
        self.date = text[4:start]
        self.lines = lines
        self.w_text = w_text
        self.h_text = h_text
        self.h_char = h_char
        self.h_date = h_date
        if self.state=='send':
            self.x = w_parent - self.w_text - 32
            self.bg = '#5b9bd5'
            self.x_avatar = w_parent - 32
            self.y_avatar = self.h_text//2-16
            self.avatar = self.parent.avatar_me
        else:
            self.x = 32
            self.bg = '#464646'
            self.x_avatar = 0
            self.y_avatar = self.h_text//2-16
            self.avatar = self.parent.avatar_you
        if self.parent.state==self.state:
            if self.parent.before_id:
                self.parent.showed_avatar.remove(self.parent.before_id)
        self.org_state = self.parent.before_id = self.parent.avatar_id
        self.parent.showed_avatar.append(self.org_state)
        self.parent.avatar_id += 1
        self.parent.state = self.state
        self.Bind(wx.EVT_PAINT, self.onPaint)
        
    def onPaint(self, event):
        x = self.x
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#ffffff'))
        dc.SetBrush(wx.Brush(self.bg))
        dc.DrawRoundedRectangle(x, 0, self.w_text, self.h_text, 10)
        x += 10
        dc.SetBackgroundMode(wx.TRANSPARENT)
        dc.SetFont(self.parent.font2)
        dc.SetTextForeground('#000000')
        dc.DrawText(self.date, x, 10)
        dc.SetFont(self.parent.font)
        dc.SetTextForeground('#ffffff')
        y = 10 + self.h_date
        for line in self.lines:
            dc.DrawText(' '.join(line), x, y)
            y += self.h_char
        try:
            if self.org_state in self.parent.showed_avatar:
                dc.DrawBitmap(self.avatar, self.x_avatar, self.y_avatar, True)
        except: pass
    
class AnnouncementWindow(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, -1, "%s's annoucement"%id, size=(400, 300),
            style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX)
        )
        self.SetIcon(Image['announcement'].GetIcon())
        self.parent = parent #Clientwindow
        self.id = id
        self.text = wx.TextCtrl(self, style=wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_RICH)
        self.style_date = wx.TextAttr('#000000', self.text.GetBackgroundColour(), wx.Font(8, wx.ROMAN, wx.ITALIC, wx.NORMAL))
        self.style_content = wx.TextAttr('#5b9bd5', self.text.GetBackgroundColour(), wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD))
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Show()
        
    def appendAnnoucement(self, date, content):
        start = self.text.GetLastPosition()
        self.text.AppendText(date + '\n')
        end = self.text.GetLastPosition()
        self.text.SetStyle(start, end, self.style_date)
        start = end
        self.text.AppendText(content + '\n\n')
        end = self.text.GetLastPosition()
        self.text.SetStyle(start, end, self.style_content)
        
    def onClose(self, event=0):
        del self.parent.announcementwindow[self.id]
        self.Destroy()

def main():
    app = wx.App()
    MainWin()
    app.MainLoop()
    return True

if __name__ == '__main__':
    main()
