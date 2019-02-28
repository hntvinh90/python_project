#!/usr/bin/env python

''''''

import wx
import sys
from ParentWindow import ParentWindow

def main():
    app = wx.App()
    ext = sys.argv
    print ext
    ParentWindow(ext[1] if len(ext)>1 else '')
    app.MainLoop()

if __name__ == '__main__':
    main()
