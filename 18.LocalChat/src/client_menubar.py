#!/usr/bin/python

""""""

import wx
from img import Image

class MenuBar(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent
        self.addFileMenu()
        self.addHelpMenu()
        self.parent.SetMenuBar(self)
        
    def addFileMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&File')
        item = wx.MenuItem(menu, -1, 'Exit')
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.onExit, item)
        
    def addHelpMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&Help')
        item = wx.MenuItem(menu, -1, 'About')
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.onAbout, item)
        
    def onExit(self, event):
        self.parent.exit()
        
    def onAbout(self, event):
        dlg = wx.Dialog(self.parent, title='About LocalChat', size=(300, 300))
        title = wx.StaticText(dlg, -1, 'LocalChat')
        title.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour('#82AEE3')
        desc = wx.StaticText(dlg, -1, 'A Local Chatting Program\nCopyright by Ho Nguyen Thanh Vinh\n\nv.%s'%(self.parent.setting.VERSION), style=wx.TE_MULTILINE|wx.ALIGN_CENTER)
        desc.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticBitmap(dlg, -1, Image['icon'].GetBitmap()), 0, wx.CENTER)
        sizer.Add(title, 0, wx.CENTER)
        sizer.Add((1,1), 1)
        sizer.Add(desc, 0, wx.CENTER)
        sizer.Add((1,1), 1)
        dlg.SetSizer(sizer)
        dlg.Center()
        dlg.ShowModal()
        
class LoggedMenuBar(MenuBar):
    def __init__(self, parent):
        MenuBar.__init__(self, parent)
        self.addToFileMenu()
        
    def addToFileMenu(self):
        menu = self.GetMenu(0)
        menu.InsertSeparator(0)
        item = wx.MenuItem(menu, -1, 'Log Out')
        menu.Insert(0, item)
        self.parent.Bind(wx.EVT_MENU, self.onLogOut, item)
        menu.InsertSeparator(0)
        item = wx.MenuItem(menu, -1, 'Announcement')
        menu.Insert(0, item)
        self.parent.Bind(wx.EVT_MENU, self.onAnnouncement, item)
        #item = wx.MenuItem(menu, -1, 'Create Group Chat')
        #menu.Insert(0, item)
        #self.parent.Bind(wx.EVT_MENU, self.onCreateGroup, item)
        
    def onAnnouncement(self, event=0):
        dlg = wx.Dialog(self.parent, title='Select To Announce', size=(400, 300))
        list_friend = wx.CheckListBox(dlg, size=(100, 1), choices=self.parent.logedpanel.friends)
        btn_all = wx.Button(dlg, -1, 'Select All')
        text = wx.TextCtrl(dlg, style=wx.TE_MULTILINE)
        btn = wx.Button(dlg, -1, 'Send')
        btn.Enable(False)
        s1 = wx.BoxSizer(wx.VERTICAL)
        s1.Add(text, 1, wx.EXPAND)
        s1.Add(btn, 0, wx.CENTER)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(list_friend, 1)
        s2.Add(btn_all, 0, wx.EXPAND)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(s2, 0, wx.EXPAND)
        sizer.Add(s1, 1, wx.EXPAND)
        dlg.SetSizer(sizer)
        dlg.Center()
        
        def onText(event):
            if text.GetValue()=='':
                btn.Enable(False)
            else:
                btn.Enable(True)
        def onBtn(event):
            for To in list_friend.GetCheckedStrings():
                self.parent.cache.append(('announcement', To, text.GetValue()))
            dlg.Destroy()
        def onSelect(event):
            if btn_all.GetLabel()=='Select All':
                btn_all.SetLabel('Unselect All')
                for i in range(list_friend.GetCount()):
                    list_friend.Check(i) 
            else:
                btn_all.SetLabel('Select All')
                for i in range(list_friend.GetCount()):
                    list_friend.Check(i, False) 
        btn_all.Bind(wx.EVT_BUTTON, onSelect)
        text.Bind(wx.EVT_TEXT, onText)
        btn.Bind(wx.EVT_BUTTON, onBtn)
        
        dlg.ShowModal()
        
    def onCreateGroup(self, event):
        dlg = wx.Dialog(self.parent, title='Create Group', size=(300, 300))
        dlg.Center()
        dlg.ShowModal()
    
    def onLogOut(self, event):
        if wx.MessageBox('Do you want to log out?', 'Warning', style=wx.YES_NO)==wx.YES:
            self.parent.logedpanel.disconnect()

def main():
    return True

if __name__ == '__main__':
    main()
