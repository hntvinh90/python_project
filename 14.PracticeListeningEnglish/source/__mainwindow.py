#!/usr/bin/python

import wx
from __image import Image
from __tab_nowplaying import TabNowPlaying
from __tab_list import TabList
from __tab_info import TabInfo


class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'English Listening Practice', style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER))
        self.CreateStatusBar()
        self.SetIcon(Image['icon'])
        
        self.addTabs()

        self.setEvents()
        self.show()

    def addTabs(self):
        self.tabs = wx.Notebook(self, style=wx.NB_FIXEDWIDTH)
        TabNowPlaying(self)
        TabList(self)
        TabInfo(self)

    def setEvents(self):
        
        def close(event):
            print 'Finished'
            self.tabs.tab_playing.timer.Stop()
            self.Destroy()
            
        self.Bind(wx.EVT_CLOSE, close)

    def show(self):
        self.SetMinSize((650, 400))
        self.Center()
        self.Show()

    


def main():
    app = wx.App()
    MainWindow()
    app.MainLoop()
    return True

if __name__ == '__main__':
    main()
