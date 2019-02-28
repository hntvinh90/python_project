#!/usr/bin/python

import wx
import wx.media
import thread
import time


class App(wx.App):

    def OnInit(self):
        MainWindow()
        self.MainLoop()
        return True


class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Get Data")

        btn_load = wx.Button(self, -1, 'Load file')
        self.btn_start = wx.Button(self, -1, 'Start')
        btn_get = wx.Button(self, -1, 'Get time')
        btn_clear = wx.Button(self, -1, 'Clear')
        btn_base64 = wx.Button(self, -1, 'Base64')
        btn_unbase64 = wx.Button(self, -1, 'unBase64')
        
        btn_load.Bind(wx.EVT_BUTTON, self.onLoad)
        self.btn_start.Bind(wx.EVT_BUTTON, self.onStart)
        btn_get.Bind(wx.EVT_BUTTON, self.onGet)
        btn_clear.Bind(wx.EVT_BUTTON, lambda event: self.text.Clear())
        btn_base64.Bind(wx.EVT_BUTTON, self.onBase64)
        btn_unbase64.Bind(wx.EVT_BUTTON, self.onunBase64)
        
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add((0,0), proportion=1)
        btn_sizer.Add(btn_load)
        btn_sizer.Add(self.btn_start)
        btn_sizer.Add(btn_get)
        btn_sizer.Add(btn_clear)
        btn_sizer.Add(btn_base64)
        btn_sizer.Add(btn_unbase64)
        btn_sizer.Add((0,0), proportion=1)

        self.media = wx.media.MediaCtrl(self)
        self.scroll = wx.Slider(self, style=wx.SL_LABELS)
##        self.media.Bind(wx.media.EVT_MEDIA_LOADED, self.onLoaded)
        self.scroll.Bind(wx.EVT_SCROLL_ENDSCROLL, self.onScroll)

        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.HSCROLL)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text, proportion=1, flag=wx.EXPAND)
        sizer.Add(self.scroll, flag=wx.EXPAND)
        self.scroll.Hide()
        sizer.Add(btn_sizer, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

        self.Show()

    def onLoad(self, event):
        path = wx.FileSelector('Open', flags=wx.FD_OPEN)
        if path!='':
            if self.media.Load(path):
                self.scroll.Hide()
                self.Layout()
                self.btn_start.SetLabel('Start')
                #self.onFile(path)
                self.initText()

    def onStart(self, event):
        if self.media.Length()>0:
            if self.btn_start.GetLabel()=='Start':
                self.btn_start.SetLabel('Pause')
                self.scroll.SetRange(0, self.media.Length())
                self.scroll.Show()
                self.Layout()
                self.media.Play()
                self.timer.Start(100)
            else:
                self.btn_start.SetLabel('Start')
                self.media.Pause()
                self.timer.Stop()
        else:
            print 'no loaded file'

    def onGet(self, event):
        if self.media.Length()>0:
            self.text.AppendText(str(self.scroll.GetValue())+'::\n')
        else:
            print 'no loaded file'

    def onFile(self, path):
        with open(path, 'rb') as f:
            self.text.SetValue(f.read().encode('base64'))

    def onLoaded(self, event):
        print self.media.Length()
        print 'vinh'

    def onScroll(self, event):
        self.media.Seek(self.scroll.GetValue())

    def onTimer(self, event):
        self.scroll.SetValue(self.media.Tell())

    def onGetFile(self, event):
        with open('try.mp3', 'wb') as f:
            f.write(self.text.GetValue().decode('base64'))

    def initText(self):
         self.text.SetValue('''<name></name>
<describe></describe>
<steps></steps>''')

    def onBase64(self, event):
        self.text.SetValue(self.text.GetValue().encode('base64'))

    def onunBase64(self, event):
        self.text.SetValue(self.text.GetValue().decode('base64'))


def main():
    App()
    return True

if __name__ == '__main__':
    main()
