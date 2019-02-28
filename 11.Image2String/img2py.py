#!/usr/bin/env python

''''''

import wx
import os
import re
from PIL import Image


class My_App(wx.App):

    def OnInit(self):
        Main_Window()
        self.MainLoop()
        return True


class Main_Window(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Convert img to pyfile', style=wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE)
        self.tabs = wx.Notebook(self)
        TabPNGtoICO(self)
        TabImagetoPyFile(self)
        self.Show()
        

class TabPNGtoICO(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent.tabs)
        parent.tabs.AddPage(self, 'PNG to ICO')

        btn = wx.Button(self, -1, 'ICO Convert')
        btn.Bind(wx.EVT_BUTTON, self.onClick)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.CENTER)
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add(sizer, 1, wx.CENTER)
        self.SetSizer(s)

    def onClick(self, event):
        dlg = wx.FileDialog(None, wildcard='PNG file (*.png)|*.PNG', style=wx.FD_OPEN|wx.FD_MULTIPLE)
        if dlg.ShowModal()==wx.ID_OK:
            for path in dlg.GetPaths():
                img = Image.open(path)
                img.save(path.replace('.png', '.ico'))
        dlg.Destroy()


class TabImagetoPyFile(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent.tabs)
        parent.tabs.AddPage(self, 'Image to PyFile')

        btn = wx.Button(self, -1, 'Choose File')
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.HSCROLL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, flag=wx.CENTER)
        sizer.Add(self.text, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        btn.Bind(wx.EVT_BUTTON, self.onClick)

    def onClick(self, event):
        dlg = wx.FileDialog(None, style=wx.FD_OPEN|wx.FD_MULTIPLE)
        if dlg.ShowModal()==wx.ID_OK:
            self.text.SetValue('''"""
Use methods: GetImage & GetBitmap & GetIcon
"""

from wx.lib.embeddedimage import PyEmbeddedImage

Image = {''')
            for path in dlg.GetPaths():
                with open(path, 'rb') as cf:
                    self.text.AppendText('''
"%s" : PyEmbeddedImage("""
%s"""),'''%(re.sub('\..*$', '', os.path.basename(path)), cf.read().encode('base64')))
            self.text.AppendText('}')
        dlg.Destroy()


def main():
    My_App()

if __name__ == '__main__':
    main()
