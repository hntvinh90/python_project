#!/usr/bin/python

""""""

import wx, sys, os, re
from _img import Image
from _finddialog import FindDialog
from myLibs import isThread


class MenuBar(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent #mainwindow
        self.shortcut = []
        self.addFileMenu()
        self.addEditMenu()
        self.addViewMenu()
        self.addProgramMenu()
        self.addHelpMenu()
        self.parent.SetMenuBar(self)
        self.SetAcceleratorTable(wx.AcceleratorTable(self.shortcut))
        
    def addFileMenu(self):
        filemenu = wx.Menu()
        menu_file_new = filemenu.Append(-1, 'New\tCtrl+N')
        menu_file_open = filemenu.Append(-1, 'Open\tCtrl+O')
        self.openrecent = OpenRecent(filemenu, self)
        menu_file_save = filemenu.Append(-1, 'Save\tCtrl+S')
        menu_file_saveas = filemenu.Append(-1, 'Save As\tCtrl+Shift+S')
        filemenu.AppendSeparator()
        menu_file_out = filemenu.Append(-1, 'Open Output')
        filemenu.AppendSeparator()
        menu_file_close = filemenu.Append(-1, 'Close\tCtrl+W')
        menu_file_clear = filemenu.Append(-1, 'Clear Recent File List')
        filemenu.AppendSeparator()
        menu_file_exit = filemenu.Append(-1, 'Exit\tAlt+X')
        self.Append(filemenu, '&File')
        
        self.shortcut.append((wx.ACCEL_CTRL, ord('n'), menu_file_new.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord('o'), menu_file_open.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord('s'), menu_file_save.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('s'), menu_file_saveas.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord('w'), menu_file_close.GetId()))
        self.shortcut.append((wx.ACCEL_ALT, ord('x'), menu_file_exit.GetId()))
        
        self.Bind(wx.EVT_MENU, self.onNew, menu_file_new)
        self.Bind(wx.EVT_MENU, self.onOpen, menu_file_open)
        self.Bind(wx.EVT_MENU, self.onSave, menu_file_save)
        self.Bind(wx.EVT_MENU, self.onSaveas, menu_file_saveas)
        self.Bind(wx.EVT_MENU, self.onOutput, menu_file_out)
        self.Bind(wx.EVT_MENU, self.onClose, menu_file_close)
        self.Bind(wx.EVT_MENU, self.onClearRecent, menu_file_clear)
        self.Bind(wx.EVT_MENU, self.onExit, menu_file_exit)
        
    def onNew(self, event):
        self.parent.workingnotebook.addPage('input')
        
    def onOpen(self, event, path=''):
        if path is '':
            path = wx.FileSelector('Choose a file')
        if path is not '':
            page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
            if page.path is '' and not page.modified:
                self.parent.workingnotebook.number.remove(page.number)
                page.number = 0
                page.path = path
                page.setData()
                self.parent.workingnotebook.SetPageText(self.parent.selectedpage, page.name)
                self.parent.SetTitle('MCNP Editor - [%s]' %(page.path))
            else:
                self.parent.workingnotebook.addPage('input', path)
            self.openrecent.add(path)
    
    def onSave(self, event):
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        if page.path is not '':
            #if page.modified:
            self.saveFile(page)
            page.modified = False
            self.parent.workingnotebook.SetPageText(self.parent.selectedpage, page.name)
            self.parent.SetTitle('MCNP Editor - [%s]' %(page.path))
            self.openrecent.add(page.path)
            page.setData()
        else:
            return self.onSaveas(0)
        return True
    
    def onSaveas(self, event):
        path = wx.FileSelector('Save As', flags=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if path is not '':
            page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
            page.path = path
            if page.number is not 0:
                self.parent.workingnotebook.number.remove(page.number)
                page.number = 0
            page.name = os.path.basename(path)
            return self.onSave(0)
        return False
    
    def saveFile(self, page):
        data = self.getData(page)
        with open(page.path, 'w') as f:
            f.write('\n\n'.join(data) + '\n')
    
    def getData(self, page):
        data = []
        data.append(page.cellcard.GetValue())
        data.append(page.surfcard.GetValue())
        data.append(page.datacard.GetValue())
        for i in [0, 1, 2]:
            data[i] = re.sub('[C,c]\n', 'c \n', re.sub('\n+', '\n', re.sub('\n*$', '', re.sub('^\n*', '', data[i].strip()))))
        if data[0][:2] not in ['c ', 'C ']:
            data[0] = 'c \n' + data[0]
        return data
    
    def onOutput(self, event, path=''):
        if path is '':
            path = wx.FileSelector('Choose a output file')
        if path is not '':
            self.parent.workingnotebook.addPage('output', path)
    
    def onClose(self, event):
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        if page.modified:
            if wx.MessageBox('Do you want to save file before closing it?', style=wx.YES_NO) == wx.YES:
                if not self.onSave(0):
                    return False
        self.closePage()
        return True
     
    def closePage(self):
        index = self.parent.selectedpage
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        self.parent.workingnotebook.DeletePage(index)
        self.parent.workingnotebook.tablist.pop(index)
        if page.number is not 0:
            self.parent.workingnotebook.number.remove(page.number)
        length = len(self.parent.workingnotebook.tablist)
        if length is 0:
            self.parent.workingnotebook.checkCloseAll()
        else:
            if index is length:
                self.parent.selectedpage = index - 1
            self.parent.workingnotebook.SetSelection(self.parent.selectedpage)
    
    def onClearRecent(self, event):
        self.openrecent.clear()
        
    def onExit(self, event):
        if wx.MessageBox('Do you want to exit?', style=wx.YES_NO) == wx.YES and self.closeAllTab():
            self.parent.Destroy()
            
    def closeAllTab(self, event=0):
        while len(self.parent.workingnotebook.tablist) > 1 or (
              len(self.parent.workingnotebook.tablist)==1 and self.parent.workingnotebook.tablist[0].modified):
            if not self.onClose(0):
                break
        else:
            return True
        return False
    
    def addEditMenu(self):
        editmenu = wx.Menu()
        menu_edit_find = editmenu.Append(-1, 'Find\tCtrl+F')
        #menu_edit_next = editmenu.Append(-1, 'Find Next\tF3')
        editmenu.AppendSeparator()
        menu_edit_add = editmenu.Append(-1, 'Add Comment\tCtrl+[')
        menu_edit_del = editmenu.Append(-1, 'Delete Comment\tCtrl+]')
        self.Append(editmenu, '&Edit')
        
        self.shortcut.append((wx.ACCEL_CTRL, ord('f'), menu_edit_find.GetId()))
        #self.shortcut.append((wx.ACCEL_CTRL, ord('F3'), menu_edit_next.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord('['), menu_edit_add.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord(']'), menu_edit_del.GetId()))
        
        self.Bind(wx.EVT_MENU, self.onFind, menu_edit_find)
        self.Bind(wx.EVT_MENU, self.onAddComment, menu_edit_add)
        self.Bind(wx.EVT_MENU, self.onDelComment, menu_edit_del)
    
    def onFind(self, event):
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        window = page.FindFocus()
        if page.id == 'input':
            if window not in [page.cellcard, page.surfcard, page.datacard]:
                window = page.cellcard
        else:
            window = page.text
        FindDialog(window)
    
    def onAddComment(self, event):
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        window = page.FindFocus()
        if window in [page.cellcard, page.surfcard, page.datacard]:
            pos = window.GetSelection()
            for row in range(window.PositionToXY(pos[0])[2], window.PositionToXY(pos[1])[2]+1):
                pos = window.XYToPosition(0, row)
                str = window.GetRange(pos, pos+2)
                if str not in ['c ', 'C ', 'c\n', 'C\n']:
                    window.SetInsertionPoint(pos)
                    window.WriteText('c ')
    
    def onDelComment(self, event):
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        window = page.FindFocus()
        if window in [page.cellcard, page.surfcard, page.datacard]:
            pos = window.GetSelection()
            for row in range(window.PositionToXY(pos[0])[2], window.PositionToXY(pos[1])[2]+1):
                pos = window.XYToPosition(0, row)
                str = window.GetRange(pos, pos+2)
                if str in ['c ', 'C ']:
                    window.Replace(pos, pos+2, '')
    
    def addViewMenu(self):
        viewmenu = wx.Menu()
        self.cell = viewmenu.AppendCheckItem(-1, 'Cell Card\tCtr+1')
        self.surf = viewmenu.AppendCheckItem(-1, 'Surface Card\tCtr+2')
        self.data = viewmenu.AppendCheckItem(-1, 'Data Card\tCtr+3')
        viewmenu.AppendSeparator()
        menu_view_all = viewmenu.Append(-1, 'Select All')
        self.cell.Check(True)
        self.surf.Check(True)
        self.data.Check(True)
        self.Append(viewmenu, '&View')
        
        self.shortcut.append((wx.ACCEL_CTRL, ord('1'), self.cell.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord('2'), self.surf.GetId()))
        self.shortcut.append((wx.ACCEL_CTRL, ord('3'), self.data.GetId()))
        
        self.Bind(wx.EVT_MENU, self.onViewCell, self.cell)
        self.Bind(wx.EVT_MENU, self.onViewSurf, self.surf)
        self.Bind(wx.EVT_MENU, self.onViewData, self.data)
        self.Bind(wx.EVT_MENU, self.onViewAll, menu_view_all)
        
    def onViewCell(self, event):
        self.parent.workingnotebook.tablist[self.parent.selectedpage].toggleCards('cell')
    
    def onViewSurf(self, event):
        self.parent.workingnotebook.tablist[self.parent.selectedpage].toggleCards('surf')
    
    def onViewData(self, event):
        self.parent.workingnotebook.tablist[self.parent.selectedpage].toggleCards('data')
    
    def onViewAll(self, event):
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        page.cellstatus = False
        page.surfstatus = False
        page.datastatus = False
        page.toggleCards('cell', 'surf', 'data')
    
    def addProgramMenu(self):
        progmenu = wx.Menu()
        menu_prog_run = progmenu.Append(-1, 'Run')
        progmenu.AppendSeparator()
        menu_prog_vised = progmenu.Append(-1, 'Open Visual Editor')
        self.Append(progmenu, '&Program')
        
        self.Bind(wx.EVT_MENU, self.onRun, menu_prog_run)
        self.Bind(wx.EVT_MENU, self.onVised, menu_prog_vised)
        
    def onRun(self, event):
        '''
        os.system('echo %DATAPATH% && pause')
        '''
        page = self.parent.workingnotebook.tablist[self.parent.selectedpage]
        if self.onSave(0):
            import subprocess
            os.system('(cd /d "%s" && mcnp5 %s) || pause' %(os.path.dirname(page.path), os.path.basename(page.path)))
            #command = '(cd_/d_"%s"_&&_mcnp5_%s)_||_pause' %(os.path.dirname(page.path), os.path.basename(page.path))
            #subprocess.Popen(command.split('_'))
            self.onOutput(0, page.path + '.o')
        #'''
        
    #@isThread
    def onVised(self, event):
        from subprocess import Popen
        #os.system('vised.exe')
        Popen(['(cd', '/d', os.path.dirname(sys.argv[0]), '&&', 'vised.exe)', '||', 'pause'], shell=True)
        
    def addHelpMenu(self):
        helpmenu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.onAbout, helpmenu.Append(-1, 'About'))
        self.Append(helpmenu, '&Help')
    
    def onAbout(self, event):
        dlg = wx.Dialog(self.parent, -1, 'About', size=(300, 300))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((10, 10), 1)
        sizer.Add(wx.StaticBitmap(dlg, -1, Image['icon'].GetBitmap()), 0, wx.CENTER)
        sizer.Add((10, 10))
        title = wx.StaticText(dlg, -1, 'MCNP EDITOR', style=wx.ALIGN_CENTER)
        title.SetFont(wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour('#5b9bd5')
        sizer.Add(title, 0, wx.EXPAND)
        sizer.Add((10,10), 1)
        sizer.Add(wx.StaticText(dlg, -1, 'Copyright by HoNguyenThanhVinh\nDaLat Nuclear Research Institute', style=wx.ALIGN_CENTER), flag=wx.EXPAND)
        sizer.Add((10,10))
        sizer.Add(wx.StaticLine(dlg), flag=wx.EXPAND)
        sizer.Add((10,10))
        sizer.Add(wx.Button(dlg, -1, 'OK'), flag=wx.ALIGN_CENTER)
        sizer.Add((10,10))
        sizer_parent = wx.BoxSizer(wx.HORIZONTAL)
        #sizer_parent.Add((10, 10))
        sizer_parent.Add(sizer, 1, wx.EXPAND)
        #sizer_parent.Add((10, 10))
        dlg.SetSizer(sizer_parent)
        dlg.Layout()
        dlg.Bind(wx.EVT_BUTTON, lambda event: dlg.Close())
        dlg.ShowModal()
        dlg.Destroy()


class OpenRecent(wx.Menu):
    def __init__(self, parent, grandparent):
        wx.Menu.__init__(self)
        self.parent = parent #filemenu
        self.grandparent = grandparent #menubar
        self.length = 10
        self.parent.Append(-1, 'Open Recent', self)
        self.update()
        
    def update(self):
        for item in self.GetMenuItems():
            self.Remove(item)
        path = os.path.join(os.path.dirname(sys.argv[0]), 'openrecent.dat')
        if os.path.exists(path):
            with open(path, 'r') as f:
                items = f.read()[:-1].split('\n')
            while len(items) > self.length:
                items.pop(0)
            with open(path, 'w') as f:
                f.write('\n'.join(items) + '\n')
            for item in items:
                self.Bind(wx.EVT_MENU, self.onRecent, self.AppendCheckItem(-1, item))
        else:
            self.Append(-1, '<None>').Enable(False)
            
    def onRecent(self, event):
        for item in self.GetMenuItems():
            if item.IsChecked():
                item.Check(False)
                self.grandparent.onOpen(0, self.GetLabel(item.GetId()))
    
    def add(self, path):
        items = []
        if os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), 'openrecent.dat')):
            with open(os.path.join(os.path.dirname(sys.argv[0]), 'openrecent.dat'), 'r') as f:
                items = f.read()[:-1].split('\n')
        if path not in items:
            #print(path, items)
            with open(os.path.join(os.path.dirname(sys.argv[0]), 'openrecent.dat'), 'a') as f:
                f.write(path + '\n')
            self.update()
    
    def clear(self):
        try:
            os.remove(os.path.join(os.path.dirname(sys.argv[0]), 'openrecent.dat'))
        except: pass
        self.update()


def main():
    return True

if __name__ == '__main__':
    main()
