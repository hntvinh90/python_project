#!/usr/bin/python

""""""

import wx
from _img import Image
from _menubar import MenuBar
from _workingnotebook import WorkingNotebook


class MyApp(wx.App):
    def OnInit(self):
        self.SetTopWindow(MainWindow())
        return True
    
    def OnExit(self):
        return True


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'MCNP Editor', size=(800, 600))
        self.SetIcon(Image['icon'].GetIcon())
        self.selectedpage = None
        self.menubar = MenuBar(self)
        self.workingnotebook = WorkingNotebook(self)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Maximize(True)
        self.Show()
        
    def onClose(self, event):
        self.menubar.onExit(0)


def main():
    MyApp().MainLoop()
    return True

if __name__ == '__main__':
    main()
