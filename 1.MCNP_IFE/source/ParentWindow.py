#!/usr/bin/env python

''''''

import wx
import Image
import MenuBar
import re
import os


class ParentWindow(wx.Frame):

    def __init__(self, argv):
        wx.Frame.__init__(self, None, wx.NewId(), 'MCNP Input File Editor',
                          style=wx.DEFAULT_FRAME_STYLE|wx.MAXIMIZE, size=(800, 600))
        self.SetIcon(Image.img_icon.GetIcon())
        self.SetBackgroundColour('#ffffff')
        self.path = ''
        self.saved = True
        self.createEditor()
        self.createStatusBar()
        self.menubar = MenuBar.Menu(self)
        if argv!='':
            self.setData(argv)
        self.Bind(wx.EVT_CLOSE, self.onExit)
        self.showWindow()

    def createEditor(self):
        self.cell = wx.StaticBox(self, -1, 'Cell Card')
        self.face = wx.StaticBox(self, -1, 'Surface Card')
        self.data = wx.StaticBox(self, -1, 'Data Card')
        self.cell_btn = wx.BitmapButton(self.cell, -1, Image.img_close_leave.GetBitmap(), size=(16, 16))
        self.face_btn = wx.BitmapButton(self.face, -1, Image.img_close_leave.GetBitmap(), size=(16, 16))
        self.data_btn = wx.BitmapButton(self.data, -1, Image.img_close_leave.GetBitmap(), size=(16, 16))
        self.cell_edit = wx.TextCtrl(self.cell, style=wx.TE_MULTILINE|wx.HSCROLL)#|wx.TE_RICH)
        self.face_edit = wx.TextCtrl(self.face, style=wx.TE_MULTILINE|wx.HSCROLL)#|wx.TE_RICH)
        self.data_edit = wx.TextCtrl(self.data, style=wx.TE_MULTILINE|wx.HSCROLL)#|wx.TE_RICH)
        self.cell_btn.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.cell_btn.SetBitmap(Image.img_close_enter.GetBitmap()))
        self.cell_btn.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.cell_btn.SetBitmap(Image.img_close_leave.GetBitmap()))
        self.face_btn.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.face_btn.SetBitmap(Image.img_close_enter.GetBitmap()))
        self.face_btn.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.face_btn.SetBitmap(Image.img_close_leave.GetBitmap()))
        self.data_btn.Bind(wx.EVT_ENTER_WINDOW, lambda event: self.data_btn.SetBitmap(Image.img_close_enter.GetBitmap()))
        self.data_btn.Bind(wx.EVT_LEAVE_WINDOW, lambda event: self.data_btn.SetBitmap(Image.img_close_leave.GetBitmap()))
        self.cell_edit.Bind(wx.EVT_TEXT, self.modifyText)
        self.face_edit.Bind(wx.EVT_TEXT, self.modifyText)
        self.data_edit.Bind(wx.EVT_TEXT, self.modifyText)
        self.cell_btn.Bind(wx.EVT_BUTTON, self.hideCell)
        self.face_btn.Bind(wx.EVT_BUTTON, self.hideFace)
        self.data_btn.Bind(wx.EVT_BUTTON, self.hideData)

    def modifyText(self, event):
        print 'Check event on text'
        if self.saved:
            self.saved = False
            self.SetTitle('* '+ self.GetTitle() +' *')
            self.statusbar.SetStatusText('Not save.', 1)
        self.cell_edit.Unbind(wx.EVT_TEXT)
        self.face_edit.Unbind(wx.EVT_TEXT)
        self.data_edit.Unbind(wx.EVT_TEXT)

    def hideCell(self, event):
        self.menubar.cellmenuitem.Check(False)
        self.menubar.onCellFaceData(0)

    def hideFace(self, event):
        self.menubar.facemenuitem.Check(False)
        self.menubar.onCellFaceData(0)

    def hideData(self, event):
        self.menubar.datamenuitem.Check(False)
        self.menubar.onCellFaceData(0)
        
    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([0, 100, -1])
        self.statusbar.SetStatusText('Saved', 1)
        self.statusbar.SetStatusText(self.path, 2)

    def setData(self, path):
        with open(path, 'r') as f:
            data = re.search('^(.*?)\n\n(.*?)\n\n(.*?)\n*?$', f.read(), re.S)
        try:
            self.cell_edit.SetValue(data.group(1))
            self.face_edit.SetValue(data.group(2))
            self.data_edit.SetValue(data.group(3))
        except: pass
        self.path = path
        self.saved = True
        self.cell_edit.Bind(wx.EVT_TEXT, self.modifyText)
        self.face_edit.Bind(wx.EVT_TEXT, self.modifyText)
        self.data_edit.Bind(wx.EVT_TEXT, self.modifyText)
        self.statusbar.SetStatusText('Saved.', 1)
        self.statusbar.SetStatusText(self.path, 2)
        self.SetTitle(os.path.basename(self.path)+' - [MCNP IFE] - '+ self.path)
        self.menubar.manageRecent('add', self.path)

    def onExit(self, event):
        self.menubar.onExit(0)

    def showWindow(self):
        font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.cell_edit.SetFont(font)
        self.face_edit.SetFont(font)
        self.data_edit.SetFont(font)
        sizer_cell = wx.StaticBoxSizer(self.cell, wx.VERTICAL)
        sizer_cell.Add(self.cell_btn, proportion=0, flag=wx.ALIGN_RIGHT)
        sizer_cell.Add(self.cell_edit, proportion=1, flag=wx.EXPAND)
        sizer_face = wx.StaticBoxSizer(self.face, wx.VERTICAL)
        sizer_face.Add(self.face_btn, proportion=0, flag=wx.ALIGN_RIGHT)
        sizer_face.Add(self.face_edit, proportion=1, flag=wx.EXPAND)
        sizer_data = wx.StaticBoxSizer(self.data, wx.VERTICAL)
        sizer_data.Add(self.data_btn, proportion=0, flag=wx.ALIGN_RIGHT)
        sizer_data.Add(self.data_edit, proportion=1, flag=wx.EXPAND)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(sizer_cell, proportion=1, flag=wx.EXPAND)
        sizer.Add(sizer_face, proportion=1, flag=wx.EXPAND)
        sizer.Add(sizer_data, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()


def main():
    app = wx.App()
    ParentWindow('')
    app.MainLoop()

if __name__ == '__main__':
    main()
