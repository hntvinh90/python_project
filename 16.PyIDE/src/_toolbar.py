#!/usr/bin/python

""""""

import wx
from img import Image

def addToolBar(parent):
    tb = parent.CreateToolBar()
    tb.AddTool(parent.setting.ID_NEW, '', Image['menu_file_new'].GetBitmap(), 'New')
    tb.AddTool(parent.setting.ID_OPEN, '', Image['menu_file_open'].GetBitmap(), 'Open')
    tb.AddTool(parent.setting.ID_SAVE, '', Image['menu_file_save'].GetBitmap(), 'Save')
    tb.AddTool(parent.setting.ID_CLOSE, '', Image['menu_file_close'].GetBitmap(), 'Close')
    tb.AddTool(-1, '', Image['null'].GetBitmap())
    tb.AddTool(parent.setting.ID_UNDO, '', Image['menu_edit_undo'].GetBitmap(), 'Undo')
    tb.AddTool(parent.setting.ID_REDO, '', Image['menu_edit_redo'].GetBitmap(), 'Redo')
    tb.AddTool(-1, '', Image['null'].GetBitmap())
    tb.AddTool(parent.setting.ID_FIND, '', Image['menu_edit_find'].GetBitmap(), 'Find')
    tb.AddTool(parent.setting.ID_COMMENT, '', Image['menu_edit_comment'].GetBitmap(), 'Comment')
    tb.AddTool(parent.setting.ID_UNCOMMENT, '', Image['menu_edit_uncomment'].GetBitmap(), 'Uncomment')
    tb.AddTool(parent.setting.ID_INDENT, '', Image['menu_edit_indent'].GetBitmap(), 'Indent')
    tb.AddTool(parent.setting.ID_DEDENT, '', Image['menu_edit_dedent'].GetBitmap(), 'Dedent')
    tb.AddTool(parent.setting.ID_SHOWMARKS, '', Image['menu_edit_showmarks'].GetBitmap(), 'Show Marks')
    tb.AddTool(-1, '', Image['null'].GetBitmap())
    tb.AddTool(parent.setting.ID_PYTHON, '', Image['menu_program_python'].GetBitmap(), 'Restart Python Interpreter')
    tb.AddTool(parent.setting.ID_RUN, '', Image['menu_program_run'].GetBitmap(), 'Run')
    tb.Realize()

def main():
    return True

if __name__ == '__main__':
    main()