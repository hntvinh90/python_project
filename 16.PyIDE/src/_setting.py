#!/usr/bin/python

""""""

import wx
import os, sys, keyword


class Setting():
    def __init__(self, parent):
        self.PLATFORM = sys.platform
        self.IS_WINDOW = 'win32'
        
        self.parent = parent
        self.TITLE = 'PyIDE'
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 600  
        self.MAXIMIZE = 0
        self.PROJECTPANELSIZE = 25 # percent
        self.INTERPRETERSIZE = 25 # percent
        
        # menu id
        self.ID_NEW = 101
        self.ID_OPEN = 102
        self.ID_SAVE = 103
        self.ID_SAVEAS = 104
        self.ID_CLOSE = 105
        self.ID_EXIT = 106
        self.ID_FIND = 107
        self.ID_COMMENT = 108
        self.ID_UNCOMMENT = 109
        self.ID_INDENT = 110
        self.ID_DEDENT = 111
        self.ID_UNDO = 112
        self.ID_REDO = 113
        self.ID_SHOWMARKS = 114
        self.ID_RUN = 115
        self.ID_PYTHON = 116
        self.ID_CLOSE_ALL = 117
        self.ID_CLOSE_OTHERS = 118
        self.ID_NEXT = 119
        self.ID_PREVIOUS = 120
        self.ID_FIRST = 121
        self.ID_LAST = 122
        self.ID_RECENT = (201, 202, 203, 204, 205, 206, 207, 208, 209, 210)
        self.NUMBEROFRECENT = len(self.ID_RECENT)
        
        # hotkeys
        self.HOTKEYS = {
            self.ID_NEW : 'Ctrl+N',
            self.ID_OPEN : 'Ctrl+O',
            self.ID_SAVE : 'Ctrl+S',
            self.ID_SAVEAS : 'Ctrl+Shift+S',
            self.ID_CLOSE : 'Ctrl+W',
            self.ID_EXIT : 'Ctrl+Q',
            self.ID_FIND : 'Ctrl+F',
            self.ID_COMMENT : 'Ctrl+[',
            self.ID_UNCOMMENT : 'Ctrl+]',
            self.ID_INDENT : 'Ctrl+I',
            self.ID_DEDENT : 'Ctrl+Shift+I',
            self.ID_UNDO : 'Ctrl+Z',
            self.ID_REDO : 'Ctrl+Shift+Z',
            self.ID_RUN : 'F5',
        }
        
        # HOMEPATH
        #self.HOMEPATH = "C:/Users/Ho Nguyen Thanh Vinh/OneDrive/Python/3.6.3"
        self.HOMEPATH = os.path.dirname(os.path.abspath(sys.argv[0]))
        #wx.MessageBox(self.HOMEPATH)
        self.PYTHONEXE = 'python'
        if self.PLATFORM == self.IS_WINDOW:
            self.PYTHONEXE += '.exe'
        if not os.path.exists(os.path.join(self.HOMEPATH, self.PYTHONEXE)):
            self.HOMEPATH = ''
        
        # style of document
        self.PYTHON_STYLE = 'yp.'
        self.HTML_STYLE = 'lmth.'
        self.WILDCARD = {
            self.PYTHON_STYLE : 'Python|*.py',
            self.HTML_STYLE : 'HTML|*.html',
            '' : 'All|*.*',
        }
        
        self.TABWIDTH = 4
        
        # interpreter
        self.CALL_PYTHON = '"%s" -u -i' %(os.path.join(self.HOMEPATH, self.PYTHONEXE))
        self.MARK_PYTHON = '>>> '
        self.MARK_INDENT = '... '
        self.INTERPRETER_STYLE = 'fore:#ffffff,back:#000000,size:10,face:Courier New'
        self.INTERPRETER_CARET = '#ffffff'
        
        # project panel
        #self.PP_BACKGROUND = '#eeeeee'
        
        # text panel
        self.TEXT_LEXER = wx.stc.STC_LEX_PYTHON
        self.TEXT_STYLE = 'fore:#000000,back:#ffffff,size:10,face:Courier New'
        self.TEXT_INDENTGUIDE_COLOR = '#aaaaaa'
        self.TEXT_LINENUMBER_COLOR = 'fore:#ffffff,back:#5b9bd5,bold'
        self.TEXT_EDGE_COLUMN = 80
        self.TEXT_EDGE_COLOR = '#5b9bd5'
        self.TEXT_BRACELIGHT = 'fore:#000000,back:#ff7900,bold'#'fore:#ffffff,back:#5b9bd5,bold'
        self.TEXT_KW_COLOR = 'fore:#ee0000,back:#ffffff'
        self.TEXT_DEF_COLOR = 'fore:#0000ff,back:#ffffff'
        self.TEXT_COMMENT_COLOR = 'fore:#aaaaaa,back:#ffffff'
        self.TEXT_STRING_COLOR = 'fore:#00aa00,back:#ffffff'
        self.TEXT_NUMBER_COLOR = 'fore:#ffaa00,back:#ffffff,bold'
        self.TEXT_SELECTION_COLOR = {'fore':'#ffffff', 'back':'#5b9bd5'}
        self.KEYWORD = keyword.kwlist
        
        try:
            with open(os.path.join(self.HOMEPATH,'.setting.dat'), 'r') as f:
                data = f.read().split('\n')
            self.MAXIMIZE = int(data[0])
        except: pass
        
    def saveSetting(self):
        self.parent.projectpanel.memoryExpandedItems()
        with open(os.path.join(self.HOMEPATH,'.setting.dat'), 'w') as f:
            f.write('\n'.join([str(self.MAXIMIZE)]))


def main():
    return True

if __name__ == '__main__':
    main()
