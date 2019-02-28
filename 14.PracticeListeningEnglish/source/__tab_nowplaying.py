#!/usr/bin/python

import wx
from wx.media import MediaCtrl
import time as t
from __image import Image


class TabNowPlaying(wx.Panel):

    def __init__(self, parent):
        # parent la class MainWindow
        self.parent = parent
        parent.tabs.tab_playing = self
        wx.Panel.__init__(self, parent.tabs)
        parent.tabs.AddPage(self, 'NowPlaying')

        
        self.media = MediaCtrl(self)
        self.timer = wx.Timer(self)
        self.playing = False
        self.step = []
        self.step_now = 0
        self.k = 0
        self.time_rest = 0

        self.title = wx.StaticText(self, -1, '...')
        self.title.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        #self.title.SetForegroundColour('#00a2e8')
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.slider = wx.Slider(self, -1, 0, 0, 1)#, style=wx.SL_LABELS)
        #self.counter = wx.StaticText(self, -1, '00:00:00')
        parent.SetStatusText('00:00:00')
        self.btn_play = wx.BitmapButton(self, -1, Image['play'])

        self.setEvents()
        self.show()

    def setEvents(self):

        def btn_play(event):
            if self.playing==False:
                self.play()
            else:
                self.pause()

        def timer(event):
            if self.step_now==len(self.step):
                self.pause()
                self.k = 1
                self.time_rest = 0
                self.step_now = 0
                self.media.Seek(self.step[self.step_now][0])
            elif self.step[self.step_now][1]=='':
                self.step_now += 1
                if self.step_now==len(self.step):
                    self.pause()
                    self.step_now = 0
                    self.media.Seek(self.step[self.step_now][0])
                elif self.step[self.step_now][1]!='':
                    self.media.Seek(self.step[self.step_now][0])
                    self.media.Play()
            else:
                time = self.media.Tell()
                if self.k<=4:
                    if time>self.step[self.step_now+1][0]:
                        self.k += 1
                        self.media.Seek(self.step[self.step_now][0])
                        if self.k==4:
                            self.text.SetValue('\n'+self.step[self.step_now][1])
                        elif self.k>4:
                            self.media.Pause()
                else:
                    if self.time_rest==0:
                        self.time_rest = t.time()
                    if t.time()-self.time_rest>5:
                        self.step_now += 1
                        self.k = 1
                        self.text.SetValue('')
                        self.time_rest = 0
                        if self.step_now==len(self.step):
                            self.pause()
                            self.step_now = 0
                            self.media.Seek(self.step[self.step_now][0])
                        elif self.step[self.step_now][1]!='':
                            self.media.Seek(self.step[self.step_now][0])
                            self.media.Play()
            setCounter()

        def slider(event):
            if self.media.Length()>0:
                value = self.slider.GetValue()
                min = 0
                max = len(self.step)
                target = 0
                while max-min>1:
                    target = (max+min)/2
                    if value>self.step[target][0]:
                        min = target
                    else:
                        max = target
                    #print target, min, max
                self.media.Seek(self.step[min][0])
                self.k = 1
                self.text.SetValue('')
                self.step_now = min
                setCounter()
                #event.Skip()

        def pressKey(event):
            #print 'press some keys'
            if self.media.Length()>0:
                if event.GetKeyCode() in [wx.WXK_UP, wx.WXK_RIGHT]:
                    self.step_now += 1
                elif event.GetKeyCode() in [wx.WXK_DOWN, wx.WXK_LEFT]:
                    self.step_now -= 1
                self.k = 1
                self.text.SetValue('')
                self.media.Seek(self.step[self.step_now][0])
                setCounter()

        def setCounter():
            self.slider.SetValue(self.media.Tell())
            second = self.slider.GetValue()/1000
            hour = second/3600
            minute = (second%3600)/60
            second -= hour*3600 + minute*60
            #self.counter.SetLabel(str(hour).rjust(2, '0')+':'+str(minute).rjust(2, '0')+':'+str(second).rjust(2, '0'))
            self.parent.SetStatusText(str(hour).rjust(2, '0')+':'+str(minute).rjust(2, '0')+':'+str(second).rjust(2, '0'))
            self.Layout()
        
        self.btn_play.Bind(wx.EVT_BUTTON, btn_play)
        self.Bind(wx.EVT_TIMER, timer)
        self.slider.Bind(wx.EVT_SCROLL_ENDSCROLL, slider)
        self.slider.Bind(wx.EVT_KEY_DOWN, pressKey)
        #self.Bind(wx.EVT_KEY_DOWN, pressKey)

    def play(self):
        if self.media.Length()>0:
            self.playing = True
            self.btn_play.SetBitmapLabel(Image['pause'])
            #self.setSlider()
            if self.k==0:
                self.media.Seek(self.step[self.step_now][0])
                self.k = 1
            self.media.Play()
            self.timer.Start(250)
        else:
            self.parent.tabs.SetSelection(1)
        self.Layout()

    def pause(self):
        self.playing = False
        self.btn_play.SetBitmapLabel(Image['play'])
        self.media.Pause()
        self.timer.Stop()
        self.Layout()

    def stop(self):
        self.pause()
        self.media.Stop()
        self.k = 0
        self.text.SetValue('')
        self.time_rest = 0
        self.step_now = 0
        self.setSlider()

    def show(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add((1, 20))
        sizer.Add(self.title, 0, wx.CENTER)
        sizer.Add((1, 20))
        sizer.Add(self.text, 1, wx.EXPAND)
        sizer.Add(self.slider, 0, wx.EXPAND)
        #sizer.Add(self.counter, 0, wx.CENTER)
        sizer.Add(self.btn_play, 0, wx.CENTER)
        sizer.Add((1, 20))
        self.SetSizer(sizer)
        self.Layout()

    def setSlider(self):
        self.slider.SetRange(self.step[0][0], self.step[-1][0])
        self.slider.SetValue(self.step[0][0])
        self.Layout()


def main():
    return True

if __name__ == '__main__':
    main()
