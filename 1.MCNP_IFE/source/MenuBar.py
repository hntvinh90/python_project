#!/usr/bin/python

''''''

import wx
import Image
import ParentWindow
import re
import os


class Menu(wx.MenuBar):

    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent
        self.parent.SetMenuBar(self)
        self.createMenuFile()
        self.createMenuEdit()
        self.createMenuView()
        self.createMenuHelp()
        self.manageRecent()
        self.createShortKey()
        self.FIND_DLG = False

    def createMenuFile(self):
        menufile = wx.Menu()
        self.parent.Bind(wx.EVT_MENU, self.onNew, menufile.Append(-1, 'New\tCtrl+N'))
        self.parent.Bind(wx.EVT_MENU, self.onOpen, menufile.Append(-1, 'Open\tCtrl+O'))
        self.recentmenuitem = wx.Menu()
        menufile.Append(-1, 'Recently Open', self.recentmenuitem)
        self.parent.Bind(wx.EVT_MENU, self.onSave, menufile.Append(-1, 'Save\tCtrl+S'))
        self.parent.Bind(wx.EVT_MENU, self.onSaveAs, menufile.Append(-1, 'Save As ...\tCtrl+Shift+S'))
        menufile.AppendSeparator()
        self.parent.Bind(wx.EVT_MENU, self.onExit, menufile.Append(-1, 'Exit\tAlt+X'))
        self.Append(menufile, '&File')

    def createMenuEdit(self):
        menuedit = wx.Menu()
        self.parent.Bind(wx.EVT_MENU, self.onFind, menuedit.Append(-1, 'Find\tCtrl+F'))
        menuedit.AppendSeparator()
        self.parent.Bind(wx.EVT_MENU, self.onAddComment, menuedit.Append(-1, 'Add Comment\tCtrl+-'))
        self.parent.Bind(wx.EVT_MENU, self.onDelComment, menuedit.Append(-1, 'Del Comment\tCtrl++'))
        self.Append(menuedit, '&Edit')

    def createMenuView(self):
        menuview = wx.Menu()
        self.cellmenuitem = menuview.AppendCheckItem(-1, 'Cell Card\tCtrl+1')
        self.facemenuitem = menuview.AppendCheckItem(-1, 'Surface Card\tCtrl+2')
        self.datamenuitem = menuview.AppendCheckItem(-1, 'Data Card\tCtrl+3')
        self.cellmenuitem.Check()
        self.facemenuitem.Check()
        self.datamenuitem.Check()
        menuview.AppendSeparator()
        self.parent.Bind(wx.EVT_MENU, self.onCellFaceData, self.cellmenuitem)
        self.parent.Bind(wx.EVT_MENU, self.onCellFaceData, self.facemenuitem)
        self.parent.Bind(wx.EVT_MENU, self.onCellFaceData, self.datamenuitem)
        self.parent.Bind(wx.EVT_MENU, self.onAllSelect, menuview.Append(-1, 'All Select\tCtrl+4'))
        self.Append(menuview, '&View')

    def createMenuHelp(self):
        menuhelp = wx.Menu()
        self.parent.Bind(wx.EVT_MENU, self.onAbout, menuhelp.Append(-1, 'About'))
        self.Append(menuhelp, '&Help')

    def onNew(self, event):
        print 'New'
        ParentWindow.ParentWindow('')
        
    def onOpen(self, event, path=''):
        print 'Open'
        if path=='':
            path = wx.FileSelector('Open')
        if path!='':
            if os.path.exists(path):
                self.manageRecent('add', path)
                if self.parent.path=='' and self.parent.saved:
                    self.parent.setData(path)
                else:
                    ParentWindow.ParentWindow(path)
            else:
                wx.MessageBox('File does not exist.', caption=' ')

    def onSave(self, event):
        print 'Save'
        if self.parent.path=='':
            return self.onSaveAs(0)
        else:
            with open(self.parent.path, 'w') as f:
                f.write('\n\n'.join((
                    re.sub('\n*$', '', self.parent.cell_edit.GetValue()),
                    re.sub('\n*$', '', self.parent.face_edit.GetValue()),
                    re.sub('\n*$', '', self.parent.data_edit.GetValue()), '')))
            self.parent.saved = True
            self.parent.cell_edit.Bind(wx.EVT_TEXT, self.parent.modifyText)
            self.parent.face_edit.Bind(wx.EVT_TEXT, self.parent.modifyText)
            self.parent.data_edit.Bind(wx.EVT_TEXT, self.parent.modifyText)
            self.parent.statusbar.SetStatusText('Saved.', 1)
            self.parent.statusbar.SetStatusText(self.parent.path, 2)
            self.parent.SetTitle(os.path.basename(self.parent.path)+' - [MCNP IFE] - '+ self.parent.path)
            return True

    def onSaveAs(self, event):
        print 'Save As'
        path = wx.FileSelector('Save', flags=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
        if path=='':
            return False
        else:
            self.parent.path = path
            self.onSave(0)
        return True

    def onExit(self, event):
        print 'Exit'
        if not self.parent.saved:
            ask = wx.MessageBox('Do you want to save file?', caption=' ', style=wx.YES_NO|wx.CANCEL)
            if ask==wx.YES:
                if self.onSave(0)==True:
                    self.parent.Close()
                else:
                    print 'Not Save'
            elif ask==wx.NO:
                self.parent.Destroy()
        else:
            self.parent.Destroy()

    def onCellFaceData(self, event):
        print 'Update Layout'
        self.parent.cell.Show(self.cellmenuitem.IsChecked())
        self.parent.face.Show(self.facemenuitem.IsChecked())
        self.parent.data.Show(self.datamenuitem.IsChecked())
        self.parent.Layout()

    def onAllSelect(self, event):
        print 'All Select'
        self.cellmenuitem.Check()
        self.facemenuitem.Check()
        self.datamenuitem.Check()
        self.onCellFaceData(0)

    def onFind(self, event):
        if not self.FIND_DLG:
            self.FIND_DLG = True
            self.__start = 1
            self.__card = self.parent.cell_edit
            self.__find = ''
            self.__replace = ''
            self.__direction = 'Down'
            print 'Find and Replace'
            dlg = wx.Dialog(self.parent, -1, 'Find and Replace')
            font = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL)
            card = wx.Choice(dlg, -1, choices=['Cell Card', 'Surface Card', 'Data Card'])
            card.SetSelection(0)
            self.__correct = wx.CheckBox(dlg, -1, 'Correct position error')
            self.__correct.SetValue(True)
            find = wx.TextCtrl(dlg, -1)
            find.SetFont(font)
            replace = wx.TextCtrl(dlg, -1)
            replace.SetFont(font)
            direction = wx.RadioBox(dlg, -1, '', choices=['Down', 'Up'], majorDimension=wx.RA_SPECIFY_ROWS)#, size=(300, 50))
            btn_find = wx.Button(dlg, -1, 'Find')
            btn_replace =wx.Button(dlg, -1, 'Replace')
            btn_replaceall = wx.Button(dlg, -1, 'Replace All')
            sizer_card = wx.BoxSizer(wx.HORIZONTAL)
            sizer_card.Add((20, 1))
            sizer_card.Add(wx.StaticText(dlg, -1, 'Which Card?', size=(80, 20)))
            sizer_card.Add(card)
            sizer_card.Add((1, 1), proportion=1)
            sizer_card.Add(self.__correct)
            sizer_card.Add((20, 1))
            sizer_find = wx.BoxSizer(wx.HORIZONTAL)
            sizer_find.Add((20, 1))
            sizer_find.Add(wx.StaticText(dlg, -1, 'Find', size=(80, 20)))
            sizer_find.Add(find, proportion=1)
            sizer_find.Add((20, 1))
            sizer_replace = wx.BoxSizer(wx.HORIZONTAL)
            sizer_replace.Add((20, 1))
            sizer_replace.Add(wx.StaticText(dlg, -1, 'Replace', size=(80, 20)))
            sizer_replace.Add(replace, proportion=1)
            sizer_replace.Add((20, 1))
            sizer_direction = wx.BoxSizer(wx.HORIZONTAL)
            sizer_direction.Add((20, 1))
            sizer_direction.Add(wx.StaticText(dlg, -1, 'Direction', size=(80, 20)), flag=wx.ALIGN_CENTER_VERTICAL)
            sizer_direction.Add(direction)
            sizer_direction.Add((20, 1))
            sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
            sizer_btn.Add((1, 1), proportion=1)
            sizer_btn.Add(btn_find)
            sizer_btn.Add((20, 1))
            sizer_btn.Add(btn_replace)
            sizer_btn.Add((20, 1))
            sizer_btn.Add(btn_replaceall)
            sizer_btn.Add((1, 1), proportion=1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add((1, 20))
            sizer.Add(sizer_card, flag=wx.EXPAND)
            sizer.Add((1, 5))
            sizer.Add(sizer_find, flag=wx.EXPAND)
            sizer.Add((1, 5))
            sizer.Add(sizer_replace, flag=wx.EXPAND)
            sizer.Add((1, 5))
            sizer.Add(sizer_direction, flag=wx.EXPAND)
            sizer.Add((1, 20))
            sizer.Add(sizer_btn, flag=wx.EXPAND)
            sizer.Add((1, 20))
            dlg.SetSizer(sizer)
            dlg.Fit()
            dlg.Show()
            dlg.Bind(wx.EVT_CLOSE, lambda event: self.__onFind('close', dlg))
            btn_find.Bind(wx.EVT_BUTTON, lambda event: self.__onFind('find', find.GetValue()))
            btn_replace.Bind(wx.EVT_BUTTON, lambda event: self.__onFind('replace', replace.GetValue()))
            btn_replaceall.Bind(wx.EVT_BUTTON, lambda event: self.__onFind('replaceall', find.GetValue(), replace.GetValue()))
            dlg.Bind(wx.EVT_CHOICE, lambda event: self.__onFind('card', card))
            dlg.Bind(wx.EVT_RADIOBOX, lambda event: self.__onFind('direction', direction))
        else:
            print 'Find dlg existed'

    def __onFind(self, *var):
        if var[0]=='close':
            print 'Closing find dlg'
            self.FIND_DLG = False
            del self.__card, self.__find, self.__replace, self.__direction, self.__start, self.__correct
            var[1].Destroy()
        if var[0]=='card':
            card = var[1].GetStringSelection()
            if card == 'Cell Card':
                self.__card = self.parent.cell_edit
            if card == 'Surface Card':
                self.__card = self.parent.face_edit
            if card == 'Data Card':
                self.__card = self.parent.data_edit
            self.__start = 1
            print card
        if var[0]=='direction':
            self.__direction = var[1].GetStringSelection()
            self.__start = 1
            print self.__direction
        if var[0]=='find':
            if var[1]!='':
                if self.__find!=var[1]:
                    self.__start = 1
                    self.__find = var[1]
                self.__card.SetFocus()
                begin = 0
                end = self.__card.GetLastPosition()
                index = self.__card.GetInsertionPoint()
                if self.__direction=='Down':
                    if self.__start==0:
                        index += 1
                    else:
                        self.__start = 0
                    begin = index
                    while True:
                        if self.__correct.GetValue():
                            find = self.__card.GetValue().replace('\n', '\n\n').find(self.__find, begin, end)
                        else:
                            find = self.__card.GetValue().find(self.__find, begin, end)
                        if find==-1:
                            if begin==0:
                                break
                            else:
                                begin = 0
                        else:
                            break
                elif self.__direction=='Up':
                    print index
                    if self.__start==0:
                        index -= 1
                    else:
                        self.__start=0
                    end = index
                    print index
                    while True:
                        if self.__correct.GetValue():
                            find = self.__card.GetValue().replace('\n', '\n\n').rfind(self.__find, begin, end)
                        else:
                            find = self.__card.GetValue().rfind(self.__find, begin, end)
                        if find==-1:
                            if end == self.__card.GetLastPosition():
                                break
                            else:
                                end = self.__card.GetLastPosition()
                        else:
                            break
                if find==-1:
                    print 'Not found'
                else:
                    print find
                    self.__card.SetSelection(find, find+len(self.__find))
        if var[0]=='replace':
            self.__card.SetFocus()
            (begin, end) = self.__card.GetSelection()
            if begin != end:
                if var[1]!='':
                    self.__card.Replace(begin, end, var[1])
                    self.__card.SetSelection(begin, begin+len(var[1]))
                else:
                    self.__card.SetSelection(begin, end)
        if var[0]=='replaceall':
            self.__find = var[1]
            self.__replace = var[2]
            if self.__find!='' and wx.MessageBox('Do you want to replace "'+self.__find+'" by "'+self.__replace+'"?', caption=' ', style=wx.YES_NO)==wx.YES:
                self.__card.SetFocus()
                data = self.__card.GetValue()
                self.__card.Clear()
                self.__card.WriteText(data.replace(self.__find, self.__replace))

    def onAddComment(self, event):
        print 'Add Comment'
        window = self.parent.FindFocus()
        if window==self.parent.cell_edit or window==self.parent.face_edit or window==self.parent.data_edit:
            pos = window.GetSelection()
            for row in range(window.PositionToXY(pos[0])[2], window.PositionToXY(pos[1])[2]+1):
                pos = window.XYToPosition(0, row)
                str = window.GetRange(pos, pos+2)
                if str!='c ' and str!='C':
                    window.SetInsertionPoint(pos)
                    window.WriteText('c ')

    def onDelComment(self, event):
        print 'Del Comment'
        window = self.parent.FindFocus()
        if window==self.parent.cell_edit or window==self.parent.face_edit or window==self.parent.data_edit:
            pos = window.GetSelection()
            for row in range(window.PositionToXY(pos[0])[2], window.PositionToXY(pos[1])[2]+1):
                pos = window.XYToPosition(0, row)
                str = window.GetRange(pos, pos+2)
                if str=='c ' or str=='C':
                    window.Replace(pos, pos+2, '')
    
    def onAbout(self, event):
        dlg = wx.Dialog(self.parent, -1, 'About')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((10, 10))
        sizer.Add(wx.StaticBitmap(dlg, -1, Image.img_icon.GetBitmap()), flag=wx.EXPAND)
        sizer.Add((10, 10))
        title = wx.StaticText(dlg, -1, 'MCNP INPUT FILE EDITOR', style=wx.ALIGN_CENTER)
        title.SetFont(wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD))
        title.SetForegroundColour('#5b9bd5')
        sizer.Add(title, flag=wx.EXPAND)
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(dlg, -1, 'Copyright by HoNguyenThanhVinh\nDaLat Nuclear Research Institute', style=wx.ALIGN_CENTER), flag=wx.EXPAND)
        sizer.Add((10,10))
        sizer.Add(wx.StaticLine(dlg), flag=wx.EXPAND)
        sizer.Add((10,10))
        sizer.Add(wx.Button(dlg, -1, 'OK'), flag=wx.ALIGN_CENTER)
        sizer.Add((10,10))
        sizer_parent = wx.BoxSizer(wx.HORIZONTAL)
        sizer_parent.Add((10, 10))
        sizer_parent.Add(sizer)
        sizer_parent.Add((10, 10))
        dlg.SetSizer(sizer_parent)
        dlg.Fit()
        dlg.Bind(wx.EVT_BUTTON, lambda event: dlg.Close())
        dlg.ShowModal()
        dlg.Destroy()

    def manageRecent(self, var='', path=''):
        if var=='':
            names = []
            try:
                with open('config', 'r') as f:
                    for data in f:
                        names.append(data.strip('\n'))
            except:
                print 'Error from reading config file'
            if names==[]:
                self.recentmenuitem.Append(-1, '<None>').Enable(False)
            else:
                for name in names:
                    self.parent.Bind(wx.EVT_MENU, self.onRecent,
                        self.recentmenuitem.AppendCheckItem(-1, os.path.basename(name)))
            return True
        if var=='add':
            names = []
            try:
                with open('config', 'r') as f:
                    for data in f:
                        names.append(data.strip('\n'))
            except:
                print 'Error from reading config file'
            if path not in names:
                names.insert(0, path)
                if len(names)>5:
                    names.pop()
                with open('config', 'w') as f:
                    f.write('\n'.join(names))
                for item in self.recentmenuitem.GetMenuItems():
                    self.recentmenuitem.Remove(item)
                self.manageRecent()

    def onRecent(self, event):
        for i in range(self.recentmenuitem.GetMenuItemCount()):
            item = self.recentmenuitem.FindItemByPosition(i)
            if item.IsChecked():
                item.Check(False)
                names = []
                try:
                    with open('config', 'r') as f:
                        for data in f:
                            names.append(data.strip('\n'))
                except:
                    print 'Error from reading config file'
                self.onOpen(0, names[i])
                return True

    def createShortKey(self):
        self.SetAcceleratorTable(wx.AcceleratorTable([
            (wx.ACCEL_CTRL, ord('n'), self.FindMenuItem('File', 'New')),
            (wx.ACCEL_CTRL, ord('o'), self.FindMenuItem('File', 'Open')),
            (wx.ACCEL_CTRL, ord('s'), self.FindMenuItem('File', 'Save')),
            (wx.ACCEL_CTRL|wx.ACCEL_SHIFT, ord('s'), self.FindMenuItem('File', 'Save As ...')),
            (wx.ACCEL_ALT, ord('x'), self.FindMenuItem('File', 'Exit')),
            (wx.ACCEL_CTRL, ord('F'), self.FindMenuItem('Edit', 'Find')),
            (wx.ACCEL_CTRL, ord('-'), self.FindMenuItem('Edit', 'Add Comment')),
            (wx.ACCEL_CTRL, ord('+'), self.FindMenuItem('Edit', 'Del Comment')),
            (wx.ACCEL_CTRL, ord('1'), self.FindMenuItem('View', 'Cell Card')),
            (wx.ACCEL_CTRL, ord('2'), self.FindMenuItem('View', 'Surface Card')),
            (wx.ACCEL_CTRL, ord('3'), self.FindMenuItem('View', 'Data Card')),
            (wx.ACCEL_CTRL, ord('4'), self.FindMenuItem('View', 'All Select'))]))


def main():
    return True

if __name__ == '__main__':
    main()
