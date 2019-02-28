#!/usr/bin/python

""""""

import wx, os
from img import Image


class FindDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Find', size=(400, 300))
        self.parent = parent
        self.text = parent.textpanel.listtext[parent.textpanel.currenttext]
        
        self.find = wx.TextCtrl(self, -1, self.text.GetSelectedText())
        self.replace = wx.TextCtrl(self)
        self.direction = wx.RadioBox(self, choices=['Down', 'Up'], majorDimension=wx.RA_SPECIFY_ROWS)
        self.btn_find = wx.Button(self, -1, 'Find')
        self.btn_replace = wx.Button(self, -1, 'Replace')
        self.btn_replaceall = wx.Button(self, -1, 'Replace All')
        
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add((20,20))
        sizer1.Add(wx.StaticText(self, -1, 'Search For:'))
        sizer1.Add(self.find, 0, wx.EXPAND)
        sizer1.Add((20,20))
        sizer1.Add(wx.StaticText(self, -1, 'Replace By:'))
        sizer1.Add(self.replace, 0, wx.EXPAND)
        sizer1.Add(self.direction, 0, wx.CENTER)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.btn_find)
        sizer2.Add(self.btn_replace)
        sizer2.Add(self.btn_replaceall)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add((20,20))
        sizer3.Add(sizer1, 1, wx.EXPAND)
        sizer3.Add((20,20))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sizer3, 1, wx.EXPAND)
        sizer.Add(sizer2, 0, wx.CENTER)
        sizer.Add((20,20))
        self.SetSizer(sizer)
        
        self.find.Bind(wx.EVT_TEXT, self.OnText)
        self.replace.Bind(wx.EVT_TEXT, self.OnText)
        self.btn_find.Bind(wx.EVT_BUTTON, self.OnFind)
        self.btn_replace.Bind(wx.EVT_BUTTON, self.OnReplace)
        self.btn_replaceall.Bind(wx.EVT_BUTTON, self.OnReplaceAll)
        
        if self.find.GetValue() == '':
            self.btn_find.Enable(False)
        self.btn_replace.Enable(False)
        self.btn_replaceall.Enable(False)
        self.findnext = False
        
        self.ShowModal()
        
    def OnText(self, event):
        self.text.SetSelection(self.text.GetCurrentPos(), self.text.GetCurrentPos())
        if self.find.GetValue() == '':
            self.btn_find.Enable(False)
            self.btn_replace.Enable(False)
            self.btn_replaceall.Enable(False)
        else:
            self.btn_find.Enable(True)
            if self.replace.GetValue() == '':
                self.btn_replace.Enable(False)
                self.btn_replaceall.Enable(False)
            else:
                self.btn_replace.Enable(True)
                self.btn_replaceall.Enable(True)
                
    def OnChangeDirection(self, event):
        print(self.direction.GetSelection())
        
    def OnFind(self, event, searchall=False, replaceall=False):
        findtext = self.find.GetValue()
        begin = 0
        end = self.text.GetLastPosition()
        if searchall:
            if self.direction.GetSelection() == 0:
                target = self.text.FindText(begin, end, findtext, 0)
            else:
                target = self.text.FindText(end, begin, findtext, 0)
            if target == -1:
                if replaceall:
                    wx.MessageBox('Replaced All.', self.parent.setting.TITLE)
                else:
                    wx.MessageBox('"%s" is not found.' %(findtext), self.parent.setting.TITLE)
            else:
                self.text.GotoPos(target)
                self.text.SetSelection(target, target+len(findtext))
            return
        if self.direction.GetSelection() == 0:
            begin = self.text.GetSelectionEnd()
            target = self.text.FindText(begin, end, findtext, 0)
        else:
            end = self.text.GetSelectionStart()
            target = self.text.FindText(end, begin, findtext, 0)
        if target == -1:
            self.OnFind(0, True, replaceall)
        else:
            self.text.GotoPos(target)
            self.text.SetSelection(target, target+len(findtext))
    
    def OnReplace(self, event):
        replacetext = self.replace.GetValue()
        if self.text.GetSelectedText().lower() == self.find.GetValue().lower():
            self.text.ReplaceSelection(replacetext)
            current = self.text.GetCurrentPos()
            self.text.SetSelection(current-len(replacetext), current)
            
    
    def OnReplaceAll(self, event):
        self.OnFind(0)
        while self.text.GetSelectedText() not in ('', self.replace.GetValue()):
            self.OnReplace(0)
            self.OnFind(0, False, True)


class ModManDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='Modules Manager', size=(300, 400))
        self.parent = parent
        self.python = os.path.join(self.parent.setting.HOMEPATH, self.parent.setting.PYTHONEXE)
        self.lb = wx.ListBox(self, style=wx.LB_HSCROLL)
        self.lb.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))
        self.new = wx.TextCtrl(self)
        self.install = wx.Button(self, -1, 'Install')
        self.install.Disable()
        
        self.getModules()
        self.install.Bind(wx.EVT_BUTTON, self.onInstall)
        self.new.Bind(wx.EVT_TEXT, self.onNew)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.lb, 1, wx.EXPAND)
        sizer.Add((1, 10))
        sizer.Add(wx.StaticText(self, -1, 'Type name of module that you want to install'))
        sizer.Add(self.new, 0, wx.EXPAND)
        sizer.Add(self.install, 0, wx.CENTER)
        self.SetSizer(sizer)
        self.Center()
        self.ShowModal()
        
    def getModules(self):
        os.system('"%s" -m pip list > .modules || pause' %(self.python))
        with open('.modules', 'r') as f:
            data = f.read().strip().split('\n')
        os.remove('.modules')
        self.lb.Clear()
        for item in data:
            self.lb.Append(item)
            
    def onInstall(self, event):
        os.system('"%s" -m pip install %s || pause' %(self.python, self.new.GetValue()))
        self.new.SetValue('')
        self.getModules()
    
    def onNew(self, event):
        if self.new.GetValue() is '':
            self.install.Disable()
        else:
            self.install.Enable()


class AboutDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title='About PyIDE', size=(400, 300))
        self.parent = parent
        title = wx.StaticText(self, -1, 'PyIDE')
        title.SetFont(wx.Font(24, wx.MODERN, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour('#82AEE3')
        desc = wx.StaticText(self, -1, 'A Python Integrated Development Environment\nCopyright by Ho Nguyen Thanh Vinh', style=wx.TE_MULTILINE|wx.ALIGN_CENTER)
        desc.SetFont(wx.Font(8, wx.MODERN, wx.NORMAL, wx.NORMAL))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticBitmap(self, -1, Image['pyide'].GetBitmap()), 0, wx.CENTER)
        sizer.Add(title, 0, wx.CENTER)
        sizer.Add((1,1), 1)
        sizer.Add(desc, 0, wx.CENTER)
        sizer.Add((1,1), 1)
        self.SetSizer(sizer)
        self.Center()
        self.ShowModal()


def main():
    return True

if __name__ == '__main__':
    main()
