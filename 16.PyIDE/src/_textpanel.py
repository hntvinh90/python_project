#!/usr/bin/python

""""""

import os
import wx
import wx.stc
from img import Image
import re


class TextPanel(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)
        self.parent = parent #mainwindow
        self.indexfornew = []
        self.currenttext = -1
        self.listtext = []
        self.setImageList()
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnChangeTab)
        self.Bind(wx.EVT_CONTEXT_MENU, self.onPopup)
        
        self.new()
        
    def setImageList(self):
        il = wx.ImageList(16, 16)
        il.Add(Image['menu_file_save'].GetBitmap())
        il.Add(Image['save_unactive'].GetBitmap())
        il.Add(Image['not_save_active'].GetBitmap())
        il.Add(Image['not_save_unactive'].GetBitmap())
        self.AssignImageList(il)
        
    def new(self, style='yp.'):
        index = self.getIndex()
        currenttext = len(self.listtext)
        if style == self.parent.setting.PYTHON_STYLE:
            self.listtext.append(PythonText(self, index))
            '''
        elif style == self.parent.setting.HTML_STYLE:
            return False
        #'''
        else:
            self.listtext.append(Text(self, index))
        self.indexfornew.append(index)
        self.AddPage(self.listtext[currenttext], 'Untitled ' + str(index))
        self.SetSelection(currenttext)
        if currenttext == 0:
            self.OnChangeTab(0)
        return True
    
    def open(self, path):
        if path[::-1].find(self.parent.setting.PYTHON_STYLE) == 0:
            style = self.parent.setting.PYTHON_STYLE
        elif path[::-1].find(self.parent.setting.HTML_STYLE) == 0:
            style = self.parent.setting.HTML_STYLE
        else:
            style = ''
        text = self.listtext[self.currenttext]
        if (text.path != '') or (text.style != style) or (text.modified) or (text.GetValue() != ''):
            if not self.new(style):
                return False
        text = self.listtext[self.currenttext]
        with open(path, 'r') as f:
            try:
                text.SetValue(f.read())
            except:
                wx.MessageBox('Can not read the file!', 'Read File Error')
                path = ''
        self.save(path)
        
    def save(self, path):
        text = self.listtext[self.currenttext]
        text.SetModified(False)
        text.path = path
        text.modified = False
        self.OnChangeTab(0)
        
    def close(self, index, checkTabEmpty=True):
        text = self.listtext[index]
        if text.index != -1:
            self.indexfornew.remove(text.index)
        self.listtext.pop(index)
        self.DeletePage(index)
        if checkTabEmpty and len(self.listtext)==0:
            self.new()
        
    def getIndex(self):
        index = 1
        while index in self.indexfornew:
            index += 1
        return index
    
    def updateTitle(self, *index):
        for i in index:
            if i == self.currenttext:
                title = self.parent.setting.TITLE + ' - '
                if self.listtext[i].path == '':
                    title += self.GetPageText(i)
                else:
                    title += self.listtext[i].path
                    self.SetPageText(i, os.path.basename(self.listtext[i].path))
                    if self.listtext[i].index != -1:
                        self.indexfornew.remove(self.listtext[i].index)
                        self.listtext[i].index = -1
                if self.listtext[i].modified:
                    self.SetPageImage(i, 2)
                    title += ' [Modified]'
                else:
                    self.SetPageImage(i, 0)
                self.parent.SetTitle(title)
            else:
                if self.listtext[i].modified:
                    self.SetPageImage(i, 3)
                else:
                    self.SetPageImage(i, 1)
                    
    def OnChangeTab(self, event):
        oldtext = self.currenttext
        self.currenttext = self.GetSelection()
        if oldtext == self.currenttext or oldtext == -1 or oldtext >= len(self.listtext):
            self.updateTitle(self.currenttext)
        else:
            self.updateTitle(oldtext, self.currenttext)
        self.listtext[self.currenttext].SetFocus()
        
    def onPopup(self, event):
        popup = wx.Menu()
        popup.Append(self.parent.setting.ID_CLOSE, 'Close')
        popup.Append(self.parent.setting.ID_CLOSE_ALL, 'Close All Tabs')
        popup.Append(self.parent.setting.ID_CLOSE_OTHERS, 'Close All Other Tabs')
        popup.AppendSeparator()
        popup.Append(self.parent.setting.ID_NEXT, 'Next Tab')
        popup.Append(self.parent.setting.ID_PREVIOUS, 'Previous Tab')
        popup.Append(self.parent.setting.ID_FIRST, 'First Tab')
        popup.Append(self.parent.setting.ID_LAST, 'Last Tab')
        popup.AppendSeparator()
        popup.Append(self.parent.setting.ID_SAVE, 'Save')
        
        position = self.ScreenToClient(event.GetPosition())
        tab = self.HitTest(position)[0]
        if tab!=-1:
            self.SetSelection(tab)
        self.PopupMenu(popup, position)


class Text(wx.stc.StyledTextCtrl):
    def __init__(self, parent, index):
        wx.stc.StyledTextCtrl.__init__(self, parent)
        self.parent = parent #notebook
        self.style = ''
        self.path = ''
        self.index = index
        self.modified = False
        
        self.__setSetting()
        
        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnModified)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        
    def __setSetting(self):
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, self.parent.parent.setting.TEXT_STYLE)
        self.StyleClearAll()
        self.SetTabWidth(self.parent.parent.setting.TABWIDTH)
        self.SetUseTabs(0)
        
        self.SetIndentationGuides(1)
        self.StyleSetForeground(wx.stc.STC_STYLE_INDENTGUIDE, self.parent.parent.setting.TEXT_INDENTGUIDE_COLOR)
        
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, self.TextWidth(wx.stc.STC_STYLE_LINENUMBER, '10000'))
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER, self.parent.parent.setting.TEXT_LINENUMBER_COLOR)
        
        self.SetCaretLineVisible(1)
        
        self.SetEdgeColumn(self.parent.parent.setting.TEXT_EDGE_COLUMN)
        self.SetEdgeMode(wx.stc.STC_EDGE_LINE)
        self.SetEdgeColour(self.parent.parent.setting.TEXT_EDGE_COLOR)
        
        self.SetSelForeground(1, self.parent.parent.setting.TEXT_SELECTION_COLOR['fore'])
        self.SetSelBackground(1, self.parent.parent.setting.TEXT_SELECTION_COLOR['back'])
        
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT, self.parent.parent.setting.TEXT_BRACELIGHT)
        
        #sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(self, 1, wx.EXPAND)
        #self.parent.SetSizer(sizer)
        #self.parent.Layout()
        
    def OnModified(self, event):
        if self.modified is not self.GetModify():
            self.modified = self.GetModify()#True
            self.parent.OnChangeTab(0)
        
    def onKeyUp(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            current = self.GetCurrentPos()
            befLine = self.LineFromPosition(current) - 1
            number = self.GetLineIndentation(befLine)
            self.AddText(' ' * number)
            self.GotoPos(current + number)
        event.Skip()


class PythonText(Text):
    def __init__(self, parent, index):
        Text.__init__(self, parent, index)
        self.style = self.parent.parent.setting.PYTHON_STYLE
        self.__setSetting()
        self.hint = Hint(self)
        
        self.Unbind(wx.EVT_KEY_UP)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp2)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_UPDATE_UI, self.onUpdateUI)
        
    def __setSetting(self):
        self.SetLexer(self.parent.parent.setting.TEXT_LEXER)
        
        self.SetKeyWords(0, ' '.join(self.parent.parent.setting.KEYWORD))
        self.StyleSetSpec(wx.stc.STC_P_WORD, self.parent.parent.setting.TEXT_KW_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, self.parent.parent.setting.TEXT_DEF_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, self.parent.parent.setting.TEXT_DEF_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, self.parent.parent.setting.TEXT_COMMENT_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_STRING, self.parent.parent.setting.TEXT_STRING_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, self.parent.parent.setting.TEXT_STRING_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, self.parent.parent.setting.TEXT_STRING_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, self.parent.parent.setting.TEXT_STRING_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_STRINGEOL, self.parent.parent.setting.TEXT_STRING_COLOR)
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, self.parent.parent.setting.TEXT_NUMBER_COLOR)
        
    def onKeyUp2(self, event):
        key = event.GetKeyCode()
        current = self.GetCurrentPos()
        if key == wx.WXK_RETURN:
            befLine = self.LineFromPosition(current) - 1
            number = self.GetLineIndentation(befLine)
            number = (number // self.parent.parent.setting.TABWIDTH) * self.parent.parent.setting.TABWIDTH
            befText = self.GetLineText(befLine).strip()
            if befText!='' and befText[-1]==':':
                number += self.parent.parent.setting.TABWIDTH
            for word in ('return', 'break', 'continue', 'pass', 'raise'):
                if word in befText:
                    number -= self.parent.parent.setting.TABWIDTH
                    if number < 0:
                        number = 0
                    break
            text = self.GetTextRange(current, current+1)
            if text!='' and text in ')]}':
                number = self.GetColumn(self.BraceMatch(current)) + 1
            self.AddText(' ' * number)
            self.GotoPos(current + number)
        
        # Tao goi y cho ten bien, ham da duoc khai bao
        #'''
        if not self.hint.hinting or (self.hint.hinting and key not in [wx.WXK_TAB, wx.WXK_UP, wx.WXK_DOWN]):
            word = self.GetTextRange(self.WordStartPosition(current, True), current)
            if word != '':
                text = self.GetText()
                ls = []
                modules = re.findall('import([, _a-zA-Z0-9]+)', text, re.I)
                new_md = []
                for module in modules:
                    module = module.replace(' ', '').split(',')
                    new_md += module
                for i in list(set(re.findall('def +([_a-zA-Z0-9]+)', text, re.I) + 
                                  re.findall('class +([_a-zA-Z0-9]+)', text, re.I) + 
                                  re.findall('([_a-zA-Z0-9]+) *=[^=]', text, re.I) +
                                  new_md +
                                  self.parent.parent.setting.KEYWORD)
                              ):
                    if i.find(word) == 0 and i != word:
                        ls.append(i)
                if ls == []:
                    try:
                        self.hint.hide()
                    except: pass
                else:
                    try:
                        self.hint.show(ls, current)
                    except: pass
            else:
                try:
                    self.hint.hide()
                except: pass
        #'''
        
        event.Skip()
        
    def onKeyDown(self, event):
        if self.hint.hinting:
            key = event.GetKeyCode()
            if key == wx.WXK_TAB:
                self.hint.selectHint()
                return
            elif key == wx.WXK_UP:
                self.hint.SetSelection((self.hint.GetSelection() + self.hint.GetCount() - 1)%self.hint.GetCount())
                return
            elif key == wx.WXK_DOWN:
                self.hint.SetSelection((self.hint.GetSelection() + 1)%self.hint.GetCount())
                return
        event.Skip()
            
    def onUpdateUI(self, event):
        current = self.GetCurrentPos()
        brace = -1
        opposite = -1
        if self.GetTextRange(current-1, current) in '()[]{}':
            brace = current - 1
        elif self.GetTextRange(current, current+1) in '()[]{}':
            brace = current
        if brace >= 0:
            opposite = self.BraceMatch(brace)
        self.BraceHighlight(brace, opposite)
        
        try:
            self.parent.parent.statusbar.SetStatusText('    Line: %d, Col: %d' %(self.LineFromPosition(current)+1, self.GetColumn(current)))
            if current != self.hint.current:
                self.hint.hide()
        except: pass
        

class Hint(wx.ListBox):
    def __init__(self, parent):
        wx.ListBox.__init__(self, parent, style=wx.LB_SORT)
        self.parent = parent # Text
        self.current = -1
        self.Bind(wx.EVT_SET_FOCUS, self.onFocus)
        self.hide()
        
    def show(self, ls, current):
        self.current = current
        self.Set(ls)
        self.SetPosition(self.parent.PointFromPosition(current))
        self.Show(True)
        
        #self.select = 0
        self.SetSelection(0)
        self.hinting = True
        
    def hide(self):
        self.Show(False)
        self.hinting = False
        
    def onFocus(self, event):
        self.parent.SetFocus()
        #self.SetSelection(self.select)
        
    def selectHint(self):
        self.parent.SetSelection(self.parent.WordStartPosition(self.current, True), self.current)
        self.parent.ReplaceSelection(self.GetStringSelection())
        self.hide()


def main():
    return True

if __name__ == '__main__':
    main()
