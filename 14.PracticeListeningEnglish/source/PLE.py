#!/usr/bin/python

import wx
from __mainwindow import MainWindow

def main():
    app = wx.App()
    MainWindow()
    app.MainLoop()
    return True

if __name__ == '__main__':
    main()
