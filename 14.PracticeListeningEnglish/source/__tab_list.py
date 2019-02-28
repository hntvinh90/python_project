#!/usr/bin/python

import wx
import re
import os


class TabList(wx.Panel):

    def __init__(self, parent):
        # parent la class MainWindow
        #self.parent = parent
        parent.tabs.tab_list = self
        wx.Panel.__init__(self, parent.tabs)
        parent.tabs.AddPage(self, 'List')
        
        self.papa = wx.ScrolledWindow(self)
        self.papa.SetScrollbars(0, 10, 0, 0)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.papa, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.papa.sizer = wx.BoxSizer(wx.VERTICAL)
        self.papa.sizer.Add((1, 20))
        self.papa.SetSizer(self.papa.sizer)

        self.list(parent)

    def list(self, parent):
        path = 'data'
        files = os.listdir(path)
        for file in files:
            if len(file)>4 and file[-4:]=='.mp3':
                try:
                    int(file[:-4])
                except:
                    pass
                else:
                    Exercise(self.papa, path+'\\'+file[:-4], parent)


class Exercise(wx.Panel):

    def __init__(self, papa, path, parent):
        # Luc nay class TabList chua ket thuc nen chua co bien tab_list trong class MainWindow
        # Do do phai su dung bien papa - chinh la class TabList
        # path la file nhac
        # parent la class MainWindow
        #self.path = path
        wx.Panel.__init__(self, papa)
        with open(path+'.dat', 'r') as f:
            data = f.read().decode('base64')
        self.title = wx.StaticText(self, -1, re.search('<name>(.*)</name>', data).group(1))
        self.title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        describe = wx.StaticText(self, -1, re.search('<describe>(.*)</describe>', data).group(1), size=(600, 100), style=wx.TE_MULTILINE)
        describe.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.step = [[int(i[0]), i[1]] for i in [str.split('::') for str in re.search('<steps>(.*)</steps>', data, re.S).group(1).splitlines(0)]]
        #print self.step
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title)
        sizer.Add(describe)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

        self.setEvents(path, parent)
        self.show(papa)

    def setEvents(self, path, parent):

        def click(event):
            parent.tabs.SetSelection(0)
            parent.tabs.tab_playing.title.SetLabel(self.title.GetLabel())
            parent.tabs.tab_playing.text.SetValue('')
            parent.tabs.tab_playing.pause()
            parent.tabs.tab_playing.media.Load(path+'.mp3')
            parent.tabs.tab_playing.step = self.step
            parent.tabs.tab_playing.step_now = 0
            parent.tabs.tab_playing.k = 0
            parent.tabs.tab_playing.setSlider()
            parent.tabs.tab_playing.Layout()

        def enter(event):
            self.title.SetCursor(wx.Cursor(wx.CURSOR_HAND))
            self.title.SetForegroundColour('#00a2e8')
            self.title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD, True))

        def leave(event):
            self.title.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
            self.title.SetForegroundColour('#000000')
            self.title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))

        self.title.Bind(wx.EVT_LEFT_DOWN, click)
        self.title.Bind(wx.EVT_ENTER_WINDOW, enter)
        self.title.Bind(wx.EVT_LEAVE_WINDOW, leave)

    def show(self, papa):
        papa.sizer.Add(self)
        papa.Layout()


def main():
    return True

if __name__ == '__main__':
    main()
