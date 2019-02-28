#!/usr/bin/python

""""""

import wx, os, re
from _img import Image


class WorkingNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.parent = parent #mainwindow
        self.number = []
        self.tablist = []
        self.popupmenu = PopupMenu(self)
        
        self.Bind(wx.EVT_RIGHT_UP, self.onPopup)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onPageChanged)
        
        self.checkCloseAll()
    
    def checkCloseAll(self):
        if len(self.tablist) is 0:
            self.addPage('input')
            #self.addPage()
            
    def addPage(self, id, path=''):
        if id == 'input':
            self.parent.selectedpage = len(self.tablist)
            if path is '':
                index = 1
                while index in self.number:
                    index += 1
                self.number.append(index)
                self.tablist.append(WorkingPanel(self, path, self.number[-1]))
            else:
                self.tablist.append(WorkingPanel(self, path))
            self.SetSelection(self.parent.selectedpage)
            self.onPageChanged(0)
        elif id == 'output':
            self.parent.selectedpage = len(self.tablist)
            self.tablist.append(OutputPanel(self, path))
            self.SetSelection(self.parent.selectedpage)
            self.onPageChanged(0)
    
    def onPopup(self, event):
        ht = self.HitTest(event.GetPosition())[0]
        if ht > -1:
            self.SetSelection(ht)
        self.PopupMenu(self.popupmenu, event.GetPosition())
        
    def onPageChanged(self, event):
        self.parent.selectedpage = self.GetSelection()
        page = self.tablist[self.parent.selectedpage]
        if page.path is '':
            if page.modified:
                self.parent.SetTitle('MCNP Editor - [%s] <<modified>>' %(page.name))
            else:
                self.parent.SetTitle('MCNP Editor - [%s]' %(page.name))
        else:
            if page.modified:
                self.parent.SetTitle('MCNP Editor - [%s] <<modified>>' %(page.path))
            else:
                self.parent.SetTitle('MCNP Editor - [%s]' %(page.path))
        if page.id == 'input':
            self.parent.menubar.cell.Enable(True)
            self.parent.menubar.surf.Enable(True)
            self.parent.menubar.data.Enable(True)
            self.parent.menubar.cell.Check(page.cellstatus)
            self.parent.menubar.surf.Check(page.surfstatus)
            self.parent.menubar.data.Check(page.datastatus)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('File', 'Save')).Enable()
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('File', 'Save As')).Enable()
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('Edit', 'Add Comment')).Enable()
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('Edit', 'Delete Comment')).Enable()
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('View', 'Select All')).Enable()
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('Program', 'Run')).Enable()
        else:
            self.parent.menubar.cell.Enable(False)
            self.parent.menubar.surf.Enable(False)
            self.parent.menubar.data.Enable(False)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('File', 'Save')).Enable(False)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('File', 'Save As')).Enable(False)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('Edit', 'Add Comment')).Enable(False)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('Edit', 'Delete Comment')).Enable(False)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('View', 'Select All')).Enable(False)
            self.parent.menubar.FindItemById(self.parent.menubar.FindMenuItem('Program', 'Run')).Enable(False)


class WorkingPanel(wx.Panel):
    def __init__(self, parent, path, number=0):
        wx.Panel.__init__(self, parent)
        self.parent = parent #workingnotebook
        self.path = path
        self.number = number
        self.modified = False
        self.cellstatus = True
        self.surfstatus = True
        self.datastatus = True
        self.id = 'input'
        self.createWidgets()
        self.setData()
        self.parent.AddPage(self, self.name)
        
    def createWidgets(self):
        self.cell = wx.StaticBox(self, -1, 'Cell Card')
        self.surf = wx.StaticBox(self, -1, 'Surface Card')
        self.data = wx.StaticBox(self, -1, 'Data Card')
        btn_cell = wx.BitmapButton(self.cell, -1, Image['close_leave'].GetBitmap(), size=(16, 16))
        btn_surf = wx.BitmapButton(self.surf, -1, Image['close_leave'].GetBitmap(), size=(16, 16))
        btn_data = wx.BitmapButton(self.data, -1, Image['close_leave'].GetBitmap(), size=(16, 16))
        self.cellcard = wx.TextCtrl(self.cell, style=wx.TE_MULTILINE|wx.HSCROLL)
        self.surfcard = wx.TextCtrl(self.surf, style=wx.TE_MULTILINE|wx.HSCROLL)
        self.datacard = wx.TextCtrl(self.data, style=wx.TE_MULTILINE|wx.HSCROLL)
        
        btn_cell.Bind(wx.EVT_ENTER_WINDOW, lambda event: btn_cell.SetBitmap(Image['close_enter'].GetBitmap()))
        btn_surf.Bind(wx.EVT_ENTER_WINDOW, lambda event: btn_surf.SetBitmap(Image['close_enter'].GetBitmap()))
        btn_data.Bind(wx.EVT_ENTER_WINDOW, lambda event: btn_data.SetBitmap(Image['close_enter'].GetBitmap()))
        btn_cell.Bind(wx.EVT_LEAVE_WINDOW, lambda event: btn_cell.SetBitmap(Image['close_leave'].GetBitmap()))
        btn_surf.Bind(wx.EVT_LEAVE_WINDOW, lambda event: btn_surf.SetBitmap(Image['close_leave'].GetBitmap()))
        btn_data.Bind(wx.EVT_LEAVE_WINDOW, lambda event: btn_data.SetBitmap(Image['close_leave'].GetBitmap()))
        btn_cell.Bind(wx.EVT_BUTTON, lambda event: self.toggleCards('cell'))
        btn_surf.Bind(wx.EVT_BUTTON, lambda event: self.toggleCards('surf'))
        btn_data.Bind(wx.EVT_BUTTON, lambda event: self.toggleCards('data'))
        
        cell_sizer = wx.StaticBoxSizer(self.cell, wx.VERTICAL)
        cell_sizer.Add(btn_cell, 0, wx.ALIGN_RIGHT)
        cell_sizer.Add(self.cellcard, 1, wx.EXPAND)
        surf_sizer = wx.StaticBoxSizer(self.surf, wx.VERTICAL)
        surf_sizer.Add(btn_surf, 0, wx.ALIGN_RIGHT)
        surf_sizer.Add(self.surfcard, 1, wx.EXPAND)
        data_sizer = wx.StaticBoxSizer(self.data, wx.VERTICAL)
        data_sizer.Add(btn_data, 0, wx.ALIGN_RIGHT)
        data_sizer.Add(self.datacard, 1, wx.EXPAND)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(cell_sizer, 1, wx.EXPAND)
        sizer.Add(surf_sizer, 1, wx.EXPAND)
        sizer.Add(data_sizer, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL)
        self.cellcard.SetFont(font)
        self.surfcard.SetFont(font)
        self.datacard.SetFont(font)
        
    def toggleCards(self, *arg):
        if 'cell' in arg:
            self.cellstatus = not self.cellstatus
        if 'surf' in arg:
            self.surfstatus = not self.surfstatus
        if 'data' in arg:
            self.datastatus = not self.datastatus
        self.cell.Show(self.cellstatus)
        self.surf.Show(self.surfstatus)
        self.data.Show(self.datastatus)
        self.parent.parent.menubar.cell.Check(self.cellstatus)
        self.parent.parent.menubar.surf.Check(self.surfstatus)
        self.parent.parent.menubar.data.Check(self.datastatus)
        self.Layout()
        
    def modifyText(self, event):
        self.modified = True
        self.parent.SetPageText(self.parent.parent.selectedpage, self.name + ' *')
        self.parent.onPageChanged(0)
        
    def setData(self):
        self.unbindText()
        if self.path is '':
            self.name = 'Untitled %d' %(self.number)
        else:
            self.name = os.path.basename(self.path)
            with open(self.path, 'r') as f:
                data = f.read().split('\n\n')[:3]
            #print(data)
            try:
                self.cellcard.SetValue(data[0])
            except: pass
            try:
                self.surfcard.SetValue(data[1])
            except: pass
            try:
                self.datacard.SetValue(data[2])
            except: pass
        self.cellcard.Bind(wx.EVT_TEXT, self.modifyText)
        self.surfcard.Bind(wx.EVT_TEXT, self.modifyText)
        self.datacard.Bind(wx.EVT_TEXT, self.modifyText)
        
    def unbindText(self):
        self.cellcard.Unbind(wx.EVT_TEXT)
        self.surfcard.Unbind(wx.EVT_TEXT)
        self.datacard.Unbind(wx.EVT_TEXT)


class OutputPanel(wx.Panel):
    def __init__(self, parent, path):
        wx.Panel.__init__(self, parent)
        self.parent = parent # workingnotebook
        self.path = path
        self.id = 'output'
        self.number = 0
        self.modified = False
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY)
        self.text.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.setData()
        self.parent.AddPage(self, self.name)
        
    def setData(self):
        self.name = os.path.basename(self.path)
        with open(self.path, 'r') as f:
            self.text.SetValue(f.read())
        
        
class PopupMenu(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent #workingnotebook
        close = self.Append(-1, 'Close')
        closeall = self.Append(-1, 'Close All Tabs')
        closeother = self.Append(-1, 'Close Other Tabs')
        #self.AppendSeparator()
        #save = self.Append(-1, 'Save')
        self.Bind(wx.EVT_MENU, self.parent.parent.menubar.onClose, close)
        self.Bind(wx.EVT_MENU, self.parent.parent.menubar.closeAllTab, closeall)
        self.Bind(wx.EVT_MENU, self.onCloseOtherTabs, closeother)
        
    def onCloseOtherTabs(self, event):
        page = self.parent.tablist[self.parent.parent.selectedpage]
        self.parent.SetSelection(len(self.parent.tablist) - 1)
        while len(self.parent.tablist) > 1:
            if page == self.parent.tablist[self.parent.parent.selectedpage]:
                self.parent.SetSelection(len(self.parent.tablist) - 2)
            if not self.parent.parent.menubar.onClose(0):
                break


def main():
    return True

if __name__ == '__main__':
    main()
