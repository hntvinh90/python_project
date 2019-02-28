#!/usr/bin/python

""""""

import wx, wx.stc
import time
from myLibs import isThread


class Interpreter(wx.stc.StyledTextCtrl):
    def __init__(self, parent):
        wx.stc.StyledTextCtrl.__init__(self, parent)
        self.parent = parent
        self.__setSetting()
        
        self.haveThread = False
        self.reset()
        
        self.Bind(wx.EVT_UPDATE_UI, self.updateUI)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDown)
        
    def __setSetting(self):
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, self.parent.setting.INTERPRETER_STYLE)
        self.StyleClearAll()
        self.UsePopUp(0)
        self.SetWrapMode(wx.stc.STC_WRAP_CHAR)
        self.SetMarginWidth(1, 0)
        self.SetTabWidth(self.parent.setting.TABWIDTH)
        #self.SetUseTabs(0)
        #self.SetViewWhiteSpace(1)
        #self.SetViewEOL(1)
        self.SetCaretStyle(2)
        self.SetCaretForeground(self.parent.setting.INTERPRETER_CARET)
        
    def reset(self):
        self.SetReadOnly(0)
        self.ClearAll()
        self.commandlist = []
        self.current_command_pos = -1
        self.process = wx.Process(self)
        self.process.Redirect()
        self.pip = wx.Execute(self.parent.setting.CALL_PYTHON, wx.EXEC_ASYNC, self.process)
        self.input = self.process.GetInputStream()
        self.output = self.process.GetOutputStream()
        self.error = self.process.GetErrorStream()
        self.getOutput()
        
    def getOutput(self):
        while True:
            text = ''
            try:
                if self.process.IsInputAvailable() and self.input.CanRead():
                    text += self.input.read().decode()
                if self.process.IsErrorAvailable() and self.error.CanRead():
                    text += self.error.read().decode()
            except: pass
            self.SetReadOnly(0)
            self.AppendText(text)
            if self.parent.setting.MARK_PYTHON in text or self.parent.setting.MARK_INDENT in text or not self.process.Exists(self.pip):
                return
            time.sleep(0.2)
    
    @isThread
    def executeCommand(self, command):
        self.haveThread = True
        self.output.write(command.encode())
        self.getOutput()
        self.haveThread = False
        
    def updateUI(self, event):
        limit = self.PositionFromLine(self.GetLineCount() - 1) + 4
        if self.GetSelectionStart() < limit or self.haveThread:
            self.SetReadOnly(1)
            self.GotoPos(self.GetLastPosition())
        else:
            self.SetReadOnly(0)
        if not self.haveThread and not self.process.Exists(self.pip):
            self.reset()
            
    def OnKeyDown(self, event):
        if self.haveThread:
            return
        key = event.GetKeyCode()
        if key == wx.WXK_BACK:
            limit = self.PositionFromLine(self.GetLineCount() - 1) + 4
            if self.GetCurrentPos() <= limit:
                return
        elif key == wx.WXK_UP:
            if len(self.commandlist) > 0:
                if self.current_command_pos > 0:
                    self.current_command_pos -= 1
                elif self.current_command_pos == -1:
                    self.current_command_pos = len(self.commandlist)-1
                self.SetTargetStart(self.PositionFromLine(self.GetLineCount() - 1)+4)
                self.SetTargetEnd(self.GetLastPosition())
                self.ReplaceTarget(self.commandlist[self.current_command_pos].rstrip())
                self.GotoPos(self.GetLastPosition())
            return
        elif key == wx.WXK_DOWN:
            if len(self.commandlist) > 0:
                if self.current_command_pos < len(self.commandlist)-1:
                    self.current_command_pos += 1
                self.SetTargetStart(self.PositionFromLine(self.GetLineCount() - 1)+4)
                self.SetTargetEnd(self.GetLastPosition())
                self.ReplaceTarget(self.commandlist[self.current_command_pos].rstrip())
                self.GotoPos(self.GetLastPosition())
            return
        elif key == wx.WXK_RETURN:
            if self.GetCurrentPos() < self.GetLastPosition():
                self.GotoPos(self.GetLastPosition())
        event.Skip()
        
    def OnKeyUp(self, event):
        if self.haveThread:
            return
        key = event.GetKeyCode()
        if key == wx.WXK_RETURN:
            begin = self.PositionFromLine(self.GetLineCount() - 2) + 4
            end = self.GetLastPosition()
            command = self.GetTextRange(begin, end)
            if len(self.commandlist) == 0 or self.commandlist[self.current_command_pos] != command:
                self.commandlist.append(command)
                self.current_command_pos = -1
            self.executeCommand(command)
        event.Skip()
        
    def OnMouseDown(self, event):
        self.SetFocus()
        return


def main():
    return True

if __name__ == '__main__':
    main()
