#!/usr/bin/python

""""""

import wx


class Printer(wx.Printout):
    def __init__(self):
        wx.Printout.__init__(self)


def main():
    def printer(event):
        print('Print')
        
    app = wx.App()
    frame = wx.Frame(None, title='Example', size=(600, 400))
    frame.Center()
    
    text = wx.TextCtrl(frame, style=wx.TE_MULTILINE)
    btn = wx.Button(frame, -1, 'Print')
    
    with open('text', 'r', encoding='utf-8') as f:
        text.SetValue(f.read())
    btn.Bind(wx.EVT_BUTTON, printer)
    
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(text, 1, wx.EXPAND)
    sizer.Add(btn, 0, wx.CENTER)
    frame.SetSizer(sizer)
    
    frame.Show()
    app.MainLoop()
    return True

if __name__ == '__main__':
    main()
