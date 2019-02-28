#!/usr/bin/python

""""""

import wx
from img import Image
from _setting import Setting
from _menubar import MenuBar
from _toolbar import addToolBar
from _textpanel import TextPanel
from _projectpanel import ProjectPanel
from _interpreter import Interpreter


class App(wx.App):
    def OnInit(self):
        MainFrame()
        self.MainLoop()
        return True
    
    def OnExit(self):
        return True


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.setting = Setting(self)
        self.SetTitle(self.setting.TITLE)
        self.SetSize((self.setting.WINDOW_WIDTH, self.setting.WINDOW_HEIGHT))
        self.Center()
        self.Maximize(self.setting.MAXIMIZE)
        self.SetIcon(Image['pyide'].GetIcon())
        self.statusbar = self.CreateStatusBar()
        self.menubar = MenuBar(self)
        addToolBar(self)
        self.textpanel = TextPanel(self)
        self.interpreter = Interpreter(self)
        self.projectpanel = ProjectPanel(self, self)
        
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        self.show()
    
    def show(self):
        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.textpanel, 100-self.setting.INTERPRETERSIZE, wx.EXPAND)
        sizer1.Add(self.interpreter, self.setting.INTERPRETERSIZE, wx.EXPAND)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(self.projectpanel, self.setting.PROJECTPANELSIZE, wx.EXPAND)
        sizer2.Add(sizer1, 100-self.setting.PROJECTPANELSIZE, wx.EXPAND)
        self.SetSizer(sizer2)
        self.Show()
        
    def onSize(self, event):
        self.Layout()
        self.setting.MAXIMIZE = int(self.IsMaximized())
    
    def onClose(self, event):
        self.menubar.OnExit(0)


def main():
    App()
    return True

if __name__ == '__main__':
    main()
