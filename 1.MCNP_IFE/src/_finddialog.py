#!/usr/bin/python

""""""

import wx


class FindDialog(wx.Dialog):
    def __init__(self, window):
        wx.Dialog.__init__(self, None, -1, 'Find', size=(500, 300))
        self.window = window # textctrl
        self.index = 0
        self.direction = [[self.leftfind, self.firstposition], [self.rightfind, self.lastposition]]
        self.correct = True
        
        font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL)
        correctcb = wx.CheckBox(self, -1, 'Correct position error')
        correctcb.SetValue(True)
        self.findtext = wx.TextCtrl(self, -1, self.window.GetStringSelection().strip())
        self.replacetext = wx.TextCtrl(self)
        self.directionrd = wx.RadioBox(self, choices=['Down', 'Up'])
        self.findbtn = wx.Button(self, -1, 'Find')
        self.replacebtn = wx.Button(self, -1, 'Replace')
        self.replaceallbtn = wx.Button(self, -1, 'Replace All')
        
        sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
        sizer_btn.Add(self.findbtn)
        sizer_btn.Add((20,20))
        sizer_btn.Add(self.replacebtn)
        sizer_btn.Add((20,20))
        sizer_btn.Add(self.replaceallbtn)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1,20))
        sizer.Add(correctcb)
        sizer.Add((1,20))
        sizer.Add(wx.StaticText(self, -1, 'Search For:'))
        sizer.Add(self.findtext, 0, wx.EXPAND)
        sizer.Add((1,10))
        sizer.Add(wx.StaticText(self, -1, 'Replace With:'))
        sizer.Add(self.replacetext, 0, wx.EXPAND)
        sizer.Add(self.directionrd, 0, wx.CENTER)
        sizer.Add((1,1), 1)
        sizer.Add(sizer_btn, 0, wx.CENTER)
        sizer.Add((1,20))
        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        sizerh.Add((20, 1))
        sizerh.Add(sizer, 1, wx.EXPAND)
        sizerh.Add((20, 1))
        self.SetSizer(sizerh)
        
        correctcb.Bind(wx.EVT_CHECKBOX, self.onCorrect)
        self.directionrd.Bind(wx.EVT_RADIOBOX, self.onDirection)
        self.findbtn.Bind(wx.EVT_BUTTON, self.onFind)
        self.replacebtn.Bind(wx.EVT_BUTTON, self.onReplace)
        self.replaceallbtn.Bind(wx.EVT_BUTTON, self.onReplaceAll)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Show()
        
        font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.findtext.SetFont(font)
        self.replacetext.SetFont(font)
        self.findtext.SetInsertionPointEnd()
        self.findtext.SetFocus()
        
    def leftfind(self, string, index, searchstring):
        return string.find(searchstring, index)
    
    def firstposition(self, string):
        return 0
    
    def lastposition(self, string):
        return len(string)
    
    def rightfind(self, string, index, searchstring):
        return string.rfind(searchstring, 0, index + 1)
    
    def onCorrect(self, event):
        self.correct = not self.correct
        print(self.correct)
    
    def onDirection(self, event):
        self.index = self.directionrd.GetSelection()
        print(self.index)
    
    def onFind(self, event):
        begin, end = self.findString()
        if begin == end:
            wx.MessageBox('The string not found.')
        else:
            self.window.SetFocus()
            self.window.SetSelection(begin, end)
    
    def onReplace(self, event):
        begin, end = self.window.GetSelection()
        if begin == end:
            wx.MessageBox('The string not found.')
        else:
            self.window.Replace(begin, end, self.replacetext.GetValue())
    
    def onReplaceAll(self, event):
        begin, end = self.findString()
        while begin is not end:
            self.window.Replace(begin, end, self.replacetext.GetValue())
            begin, end = self.findString()
        wx.MessageBox('All the string is replaced.')
            
    def findString(self):
        string = self.window.GetValue()
        begin, end = self.window.GetSelection()
        searchstring = self.findtext.GetValue()
        if string is not '':
            if self.correct:
                string = string.replace('\n', '\n\n')
            if begin == end:
                index = [begin, end][self.index]
            else:
                index = [begin, end][(self.index + 1) % 2]
            pos = self.direction[self.index][0](string, index, searchstring)
            if pos is -1:
                index = self.direction[self.index][1](string)
                pos = self.direction[self.index][0](string, index, searchstring)
                if pos is -1:
                    end = begin
                    return begin, end
            begin = pos
            end = begin + len(searchstring)
        else:
            end = begin
        return begin, end
    
    def onClose(self, event):
        self.Destroy()


def main():
    return True

if __name__ == '__main__':
    main()
