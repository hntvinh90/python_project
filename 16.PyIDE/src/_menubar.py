#!/usr/bin/python

""""""

import os
import wx
from img import Image
from _dialogs import FindDialog, ModManDialog, AboutDialog
from myLibs import isThread


class MenuBar(wx.MenuBar):
    def __init__(self, parent):
        wx.MenuBar.__init__(self)
        self.parent = parent #mainwindow
        self.__shortkey = []
        self.__addMenus()
        self.__setHotkeys()
        self.parent.SetMenuBar(self)
    
    def __addMenus(self):
        self.__addFileMenu()
        self.__addEditMenu()
        self.__addProgramMenu()
        self.__addDocumentsMenu()
        self.__addHelpMenu()
        
    def __addFileMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&File')
        #''' menu_file_new
        item = wx.MenuItem(menu, self.parent.setting.ID_NEW, 'New')
        item.SetBitmap(Image['menu_file_new'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnNew, item)
        #'''
        #''' menu_file_open
        item = wx.MenuItem(menu, self.parent.setting.ID_OPEN, 'Open')
        item.SetBitmap(Image['menu_file_open'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnOpen, item)
        #'''
        #''' menu_file_recent
        self.openrecent = OpenRecent(self)
        menu.Append(-1, 'Open Recent', self.openrecent)
        #'''
        menu.AppendSeparator()
        #''' menu_file_clearrecentfilelist
        item = menu.Append(-1, 'Clear Recent File List')
        self.parent.Bind(wx.EVT_MENU, self.OnClearRecent, item)
        #'''
        menu.AppendSeparator()
        #''' menu_file_save
        item = wx.MenuItem(menu, self.parent.setting.ID_SAVE, 'Save')
        item.SetBitmap(Image['menu_file_save'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnSave, item)
        #'''
        #''' menu_file_saveas
        item = menu.Append(self.parent.setting.ID_SAVEAS, 'Save As')
        self.parent.Bind(wx.EVT_MENU, self.OnSaveas, item)
        #'''
        menu.AppendSeparator()
        #''' menu_file_close
        item = wx.MenuItem(menu, self.parent.setting.ID_CLOSE, 'Close')
        item.SetBitmap(Image['menu_file_close'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnClose, item)
        #'''
        menu.AppendSeparator()
        #''' menu_file_exit
        item = wx.MenuItem(menu, self.parent.setting.ID_EXIT, 'Exit')
        item.SetBitmap(Image['menu_file_exit'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnExit, item)
        #'''
        
    def __addEditMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&Edit')
        #''' menu_edit_undo
        item = wx.MenuItem(menu, self.parent.setting.ID_UNDO, 'Undo')
        item.SetBitmap(Image['menu_edit_undo'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnUndo, item)
        #'''
        #''' menu_edit_redo
        item = wx.MenuItem(menu, self.parent.setting.ID_REDO, 'Redo')
        item.SetBitmap(Image['menu_edit_redo'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnRedo, item)
        #'''
        menu.AppendSeparator()
        #''' menu_edit_find
        item = wx.MenuItem(menu, self.parent.setting.ID_FIND, 'Find')
        item.SetBitmap(Image['menu_edit_find'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnFind, item)
        #'''
        menu.AppendSeparator()
        #''' menu_edit_comment
        item = wx.MenuItem(menu, self.parent.setting.ID_COMMENT, 'Comment')
        item.SetBitmap(Image['menu_edit_comment'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnComment, item)
        #'''
        #''' menu_edit_uncomment
        item = wx.MenuItem(menu, self.parent.setting.ID_UNCOMMENT, 'Uncomment')
        item.SetBitmap(Image['menu_edit_uncomment'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnUncomment, item)
        #'''
        #''' menu_edit_indent
        item = wx.MenuItem(menu, self.parent.setting.ID_INDENT, 'Indent')
        item.SetBitmap(Image['menu_edit_indent'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnIndent, item)
        #'''
        #''' menu_edit_dedent
        item = wx.MenuItem(menu, self.parent.setting.ID_DEDENT, 'Dedent')
        item.SetBitmap(Image['menu_edit_dedent'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnDedent, item)
        #'''
        menu.AppendSeparator()
        #''' menu_edit_showmarks
        item = wx.MenuItem(menu, self.parent.setting.ID_SHOWMARKS, 'Show Marks')#, kind=wx.ITEM_CHECK)
        item.SetBitmap(Image['menu_edit_showmarks'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnShowMarks, item)
        #'''
        
    def __addProgramMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&Program')
        #''' menu_program_run
        item = wx.MenuItem(menu, self.parent.setting.ID_RUN, 'Run')
        item.SetBitmap(Image['menu_program_run'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnRun, item)
        #'''
        ''' menu_program_runwitharguments
        self.parent.Bind(wx.EVT_MENU, self.onRunWithArgs, menu.Append(-1, 'Run With Arguments'))
        #'''
        menu.AppendSeparator()
        #''' menu_program_restart_interpreter
        item = wx.MenuItem(menu, self.parent.setting.ID_PYTHON, 'Restart Python Interpreter')
        item.SetBitmap(Image['menu_program_python'].GetBitmap())
        menu.Append(item)
        self.parent.Bind(wx.EVT_MENU, self.OnRestart, item)
        #'''
        menu.AppendSeparator()
        #''' menu_program_restart_moduls
        item = menu.Append(-1, 'Modules Manager')
        self.parent.Bind(wx.EVT_MENU, self.OnModules, item)
        #'''
        
    def __addDocumentsMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&Documents')
        #''' menu_documents_next
        item = menu.Append(self.parent.setting.ID_NEXT, 'Next Document')
        self.parent.Bind(wx.EVT_MENU, self.OnNext, item)
        #'''
        #''' menu_documents_previous
        item = menu.Append(self.parent.setting.ID_PREVIOUS, 'Prev Document')
        self.parent.Bind(wx.EVT_MENU, self.OnPrevious, item)
        #'''
        #''' menu_documents_first
        item = menu.Append(self.parent.setting.ID_FIRST, 'First Document')
        self.parent.Bind(wx.EVT_MENU, self.OnFirst, item)
        #'''
        #''' menu_documents_last
        item = menu.Append(self.parent.setting.ID_LAST, 'Last Document')
        self.parent.Bind(wx.EVT_MENU, self.OnLast, item)
        #'''
        menu.AppendSeparator()
        #''' menu_documents_saveall
        item = menu.Append(-1, 'Save All Documents')
        self.parent.Bind(wx.EVT_MENU, self.OnSaveAll, item)
        #'''
        menu.AppendSeparator()
        #''' menu_documents_closeall
        item = menu.Append(self.parent.setting.ID_CLOSE_ALL, 'Close All Documents')
        self.parent.Bind(wx.EVT_MENU, self.OnCloseAll, item)
        #'''
        #''' menu_documents_closeallother
        item = menu.Append(self.parent.setting.ID_CLOSE_OTHERS, 'Close All Other Documents')
        self.parent.Bind(wx.EVT_MENU, self.OnCloseAllOther, item)
        #'''
        
    def __addHelpMenu(self):
        menu = wx.Menu()
        self.Append(menu, '&Help')
        #''' menu_help_about
        item = menu.Append(-1, 'About PyIDE')
        self.parent.Bind(wx.EVT_MENU, self.OnAbout, item)
        #'''
    
    def __setHotkeys(self):
        hotkeys = self.parent.setting.HOTKEYS
        for key in hotkeys:
            self.SetLabel(key, self.GetLabel(key) + '\t' + hotkeys[key])
        
    def OnNew(self, event):
        self.parent.textpanel.new()
    
    def OnOpen(self, event):
        path = wx.FileSelector('Open', wildcard='Python|*.py|All|*.*')
        if path is not '':
            if os.path.exists(path):
                self.parent.textpanel.open(path)
                #try:
                self.openrecent.update(path)
                #except: pass
            else:
                wx.MessageBox('The file is not available.', self.parent.setting.TITLE)
        
    def OnSave(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        if text.path == '':
            return self.OnSaveas(0)
        else:
            with open(text.path, 'w') as f:
                f.write(text.GetValue())
            self.parent.textpanel.save(text.path)
            return True
        
    def OnSaveas(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        path = wx.FileSelector('Save as', flags=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT, wildcard='|'.join((self.parent.setting.WILDCARD[text.style], 'All|*.*')))
        if path != '':
            text.path = path
            return self.OnSave(0)
        else:
            return False
        
    def OnClose(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        if text.modified:
            name = self.parent.textpanel.GetPageText(self.parent.textpanel.currenttext)
            dlg = wx.MessageBox('Do you want to save file named "%s"?' %(name), self.parent.setting.TITLE, style=wx.YES_NO|wx.CANCEL)
            if dlg == wx.YES:
                if not self.OnSave(0):
                    return False
            elif dlg == wx.CANCEL:
                return False
        self.parent.textpanel.close(self.parent.textpanel.currenttext)
        return True
        
    def OnClearRecent(self, event):
        try:
            self.openrecent.clear()
            self.openrecent.update()
        except: pass
        
    def OnExit(self, event):
        if self.closeMultiTab(False):
            self.parent.setting.saveSetting()
            self.parent.interpreter.process.Kill(self.parent.interpreter.pip)
            self.parent.Destroy()
                
    def closeMultiTab(self, checkTabEmpty=True, exception=False):
        current = self.parent.textpanel.currenttext
        for index in range(len(self.parent.textpanel.listtext)):
            self.parent.textpanel.SetSelection(index)
            text = self.parent.textpanel.listtext[index]
            if text.modified:
                name = self.parent.textpanel.GetPageText(index)
                dlg = wx.MessageBox('Do you want to save file named "%s"?' %(name), self.parent.setting.TITLE, style=wx.YES_NO|wx.CANCEL)
                if dlg == wx.YES:
                    if not self.OnSave(0):
                        self.parent.textpanel.SetSelection(current)
                        return False
                elif dlg == wx.CANCEL:
                    self.parent.textpanel.SetSelection(current)
                    return False
        self.parent.textpanel.SetSelection(current)
        index = 0
        while len(self.parent.textpanel.listtext) != 1:
            if index == self.parent.textpanel.currenttext:
                index = 1
            self.parent.textpanel.close(index)
            self.parent.textpanel.currenttext = self.parent.textpanel.GetSelection()
        if not exception:
            self.parent.textpanel.close(0, checkTabEmpty)
        return True
        
    def OnUndo(self, event):
        self.parent.textpanel.listtext[self.parent.textpanel.currenttext].Undo()
        
    def OnRedo(self, event):
        self.parent.textpanel.listtext[self.parent.textpanel.currenttext].Redo()
    
    def OnFind(self, event):
        FindDialog(self.parent)
        
    def OnComment(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        selbegin, selend = text.GetSelection()
        begin = text.LineFromPosition(selbegin)
        end = text.LineFromPosition(selend)+1
        for line in range(begin, end):
            text.GotoLine(line)
            text.AddText('#')
            selend += 1
        text.SetSelection(selbegin+1, selend)
        
    def OnUncomment(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        selbegin, selend = text.GetSelection()
        begin = text.LineFromPosition(selbegin)
        end = text.LineFromPosition(selend)+1
        firstloop = True
        for line in range(begin, end):
            text.GotoLine(line)
            text.SetCurrentPos(text.GetCurrentPos()+1)
            if text.GetSelectedText() == '#':
                text.ReplaceSelection('')
                selend -= 1
                if firstloop:
                    selbegin -= 1
            firstloop = False
        text.SetSelection(selbegin, selend)
        
    def OnIndent(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        selbegin, selend = text.GetSelection()
        begin = text.LineFromPosition(selbegin)
        end = text.LineFromPosition(selend)+1
        inserttext = ' ' * self.parent.setting.TABWIDTH
        for line in range(begin, end):
            text.GotoLine(line)
            text.AddText(inserttext)
            selend += self.parent.setting.TABWIDTH
        text.SetSelection(selbegin+self.parent.setting.TABWIDTH, selend)
        
    def OnDedent(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        selbegin, selend = text.GetSelection()
        begin = text.LineFromPosition(selbegin)
        end = text.LineFromPosition(selend)+1
        firstloop = True
        for line in range(begin, end):
            lenindent = text.GetLineIndentation(line)
            lendelete = lenindent % self.parent.setting.TABWIDTH
            if lendelete == 0 and lenindent != 0:
                lendelete = 4
            text.GotoLine(line)
            text.SetCurrentPos(text.GetCurrentPos() + lendelete)
            text.ReplaceSelection('')
            if firstloop:
                firstloop = False
                selbegin -= lendelete
            selend -= lendelete
        text.SetSelection(selbegin, selend)
        
    def OnShowMarks(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        text.SetViewWhiteSpace(not text.GetViewWhiteSpace())
        text.SetViewEOL(not text.GetViewEOL())
        
    def OnRun(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        if (text.path == '' or text.modified):
            if wx.MessageBox('The file must be saved before it can be run.\nWould you like to save it?', self.parent.setting.TITLE, style=wx.YES_NO) == wx.YES:
                if not self.OnSave(0):
                    return
            else:
                return
        self.runCmd(text.path)
        
    @isThread
    def runCmd(self, path, args=''):
        preCmd = 'cd'
        extraCmd = "read -rsp $'Press Enter to continue\n'"
        if self.parent.setting.PLATFORM == self.parent.setting.IS_WINDOW:
            preCmd += ' /d "%s"' %(os.path.dirname(path))
            extraCmd = "pause"
        else:
            preCmd += ' "%s"' %(os.path.dirname(path))
        command = '(%s && "%s" "%s" "%s") || %s' %(preCmd, os.path.join(self.parent.setting.HOMEPATH, self.parent.setting.PYTHONEXE), path, args, extraCmd)
        os.system(command)
        
    def onRunWithArgs(self, event):
        text = self.parent.textpanel.listtext[self.parent.textpanel.currenttext]
        if (text.path == '' or text.modified):
            if wx.MessageBox('The file must be saved before it can be run.\nWould you like to save it?', self.parent.setting.TITLE, style=wx.YES_NO) == wx.YES:
                if not self.OnSave(0):
                    return
            else:
                return
        args = wx.GetTextFromUser('Set Arguments To Run File:', 'Run')
        if args != '':
            self.runCmd(text.path, args)
        
    def OnRestart(self, event):
        self.parent.interpreter.executeCommand('exit()\n')
        
    def OnModules(self, event):
        ModManDialog(self.parent)
        
    def OnNext(self, event):
        self.parent.textpanel.SetSelection((self.parent.textpanel.currenttext + 1)%len(self.parent.textpanel.listtext))
        
    def OnPrevious(self, event):
        self.parent.textpanel.SetSelection((self.parent.textpanel.currenttext - 1 + len(self.parent.textpanel.listtext))%len(self.parent.textpanel.listtext))
        
    def OnFirst(self, event):
        self.parent.textpanel.SetSelection(0)
        
    def OnLast(self, event):
        self.parent.textpanel.SetSelection(len(self.parent.textpanel.listtext)-1)
        
    def OnSaveAll(self, event):
        current = self.parent.textpanel.currenttext
        for index in range(len(self.parent.textpanel.listtext)):
            self.parent.textpanel.SetSelection(index)
            text = self.parent.textpanel.listtext[index]
            if text.modified:
                name = self.parent.textpanel.GetPageText(index)
                dlg = wx.MessageBox('Do you want to save file named "%s"?' %(name), self.parent.setting.TITLE, style=wx.YES_NO|wx.CANCEL)
                if dlg == wx.YES:
                    self.OnSave(0)
                elif dlg == wx.CANCEL:
                    break
        self.parent.textpanel.SetSelection(current)
        
    def OnCloseAll(self, event):
        self.closeMultiTab()
        
    def OnCloseAllOther(self, event):
        self.closeMultiTab(True, True)
        
    def OnAbout(self, event):
        AboutDialog(self.parent)


class OpenRecent(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent #menubar
        self.savesetting = os.path.join(self.parent.parent.setting.HOMEPATH, '.recentlist.dat')
        self.data = []
        self.update()
        
        self.Bind(wx.EVT_MENU, self.onItem)
    
    def update(self, path=''):
        if path == '':
            try:
                with open(self.savesetting, 'r') as f:
                    self.data = f.read().strip().split('\n')
                self.__update()
            except:
                self.data = []
                self.Append(self.parent.parent.setting.ID_RECENT[0], '<None>').Enable(False)
        else:
            if path not in self.data:
                self.data.append(path)
                if len(self.data) > self.parent.parent.setting.NUMBEROFRECENT:
                    self.data.pop(0)
                with open(self.savesetting, 'w') as f:
                    f.write('\n'.join(self.data))
                self.__update()
        return
    
    def __update(self):
        self.clear(False)
        for i in range(len(self.data)):
            self.Append(self.parent.parent.setting.ID_RECENT[i], self.data[i])
        
    def clear(self, clearData=True):
        for item in self.GetMenuItems():
            self.Delete(item)
        if clearData:
            try:
                os.remove(self.savesetting)
            except: pass
        return
    
    def onItem(self, event):
        id = event.GetId()
        if id in self.parent.parent.setting.ID_RECENT:
            self.parent.parent.textpanel.open(self.GetLabel(id))


def main():
    return True

if __name__ == '__main__':
    main()
