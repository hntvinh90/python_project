import wx
import random
import math
import thread
import time

class Win(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, '2048', style=wx.DEFAULT_FRAME_STYLE^(wx.MAXIMIZE_BOX|wx.RESIZE_BORDER))
        self.SetClientSize(440,440)
##        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.keyPress)
        self.Show()

        self.loadData()
        self.initGame()

    def onPaint(self, event):
        wx.BufferedPaintDC(self, wx.Bitmap())

    def multithread(func):
        def wrap(self, x, y, i, src):
            t = i
            if t == 5:
                s = 0.02
            else:
                s = 0.04
            for i in range(t):
                func(self, x, y, i, src)
                time.sleep(s)
        return wrap

    @multithread
    def draw_mix(self, x, y, i, src):
        x *= 110
        y *= 110
        xsrc = 110*i
        ysrc = 0
        dc = wx.BufferedDC(wx.ClientDC(self), wx.Bitmap())
        dc.SetClippingRegion(x, y, 110, 110)
        #dc.Clear()
        dc.Blit(x, y, 110, 110, self.img[src], xsrc, ysrc)
        dc.DestroyClippingRegion()

    def keyPress(self, event):
        key = event.GetKeyCode()
        if key==wx.WXK_LEFT:
            print 'left'
            self.keyLeft()
        if key==wx.WXK_UP:
            print 'up'
            self.keyUp()
        if key==wx.WXK_RIGHT:
            print 'right'
            self.keyRight()
        if key==wx.WXK_DOWN:
            print 'down'
            self.keyDown()

    def keyRight(self):
        temp = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        for row in range(4):
            for col in range(-1, -5, -1):
                if self.map[row][col]!=0:
                    for col_r in range(-1, -5, -1):
                        if temp[row][col_r]==0:
                            break
                    temp[row][col_r] = self.map[row][col]
        for row in range(4):
            for col in range(-1, -4, -1):
                if temp[row][col]==temp[row][col-1]:
                    temp[row][col] *= 2
                    temp[row][col-1] = 0
        result = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        for row in range(4):
            for col in range(-1, -5, -1):
                if temp[row][col]!=0:
                    for col_r in range(-1, -5, -1):
                        if result[row][col_r]==0:
                            break
                    result[row][col_r] = temp[row][col]
        #self.show(result)
        done = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        done_draw = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        if self.map!=result:
            while self.map!=result:
                for row in range(4):
                    for col in  range(-1, -4, -1):
                        if done[row][col]==0:
                            if self.map[row][col]==0:
                                if self.map[row][col-1]!=0:
                                    self.map[row][col], self.map[row][col-1] = self.map[row][col-1], self.map[row][col]
                            else:
                                if self.map[row][col-1]==self.map[row][col] and done[row][col-1]==0:
                                    self.map[row][col] *= 2
                                    self.map[row][col-1] = 0
                                    done[row][col] = 1
                print 'next'
                self.draw()
                for row in range(4):
                    for col in range(4):
                        if done[row][col]!= done_draw[row][col]:
                            thread.start_new_thread(self.draw_mix, (col, row, 2, str(self.map[row][col]), ))
##                            for i in range(2):
##                                self.draw_mix(col, row, i)
##                                done_draw[row][col] = done[row][col]
##                                time.sleep(0.05)
            self.newPoint()

    def keyLeft(self):
        temp = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        for row in range(4):
            for col in range(4):
                if self.map[row][col]!=0:
                    for col_r in range(4):
                        if temp[row][col_r]==0:
                            break
                    temp[row][col_r] = self.map[row][col]
        for row in range(4):
            for col in range(3):
                if temp[row][col]==temp[row][col+1]:
                    temp[row][col] *= 2
                    temp[row][col+1] = 0
        result = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        for row in range(4):
            for col in range(4):
                if temp[row][col]!=0:
                    for col_r in range(4):
                        if result[row][col_r]==0:
                            break
                    result[row][col_r] = temp[row][col]
        #self.show(result)
        done = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        done_draw = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        if self.map!=result:
            while self.map!=result:
                for row in range(4):
                    for col in  range(3):
                        if done[row][col]==0:
                            if self.map[row][col]==0:
                                if self.map[row][col+1]!=0:
                                    self.map[row][col], self.map[row][col+1] = self.map[row][col+1], self.map[row][col]
                            else:
                                if self.map[row][col+1]==self.map[row][col] and done[row][col+1]==0:
                                    self.map[row][col] *= 2
                                    self.map[row][col+1] = 0
                                    done[row][col] = 1
                print 'next'
                self.draw()
                for row in range(4):
                    for col in range(4):
                        if done[row][col]!= done_draw[row][col]:
                            thread.start_new_thread(self.draw_mix, (col, row, 2, str(self.map[row][col]), ))
##                            for i in range(2):
##                                self.draw_mix(col, row, i)
##                                done_draw[row][col] = done[row][col]
##                                time.sleep(0.05)
            self.newPoint()

    def keyDown(self):
        temp = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        for col in range(4):
            for row in range(-1, -5, -1):
                if self.map[row][col]!=0:
                    for row_r in range(-1, -5, -1):
                        if temp[row_r][col]==0:
                            break
                    temp[row_r][col] = self.map[row][col]
        for col in range(4):
            for row in range(-1, -4, -1):
                if temp[row][col]==temp[row-1][col]:
                    temp[row][col] *= 2
                    temp[row-1][col] = 0
        result = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        for col in range(4):
            for row in range(-1, -5, -1):
                if temp[row][col]!=0:
                    for row_r in range(-1, -5, -1):
                        if result[row_r][col]==0:
                            break
                    result[row_r][col] = temp[row][col]
        #self.show(result)
        done = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        done_draw = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        if self.map!=result:
            while self.map!=result:
                for col in range(4):
                    for row in  range(-1, -4, -1):
                        if done[row][col]==0:
                            if self.map[row][col]==0:
                                if self.map[row-1][col]!=0:
                                    self.map[row][col], self.map[row-1][col] = self.map[row-1][col], self.map[row][col]
                            else:
                                if self.map[row-1][col]==self.map[row][col] and done[row-1][col]==0:
                                    self.map[row][col] *= 2
                                    self.map[row-1][col] = 0
                                    done[row][col] = 1
                print 'next'
                self.draw()
                for row in range(4):
                    for col in range(4):
                        if done[row][col]!= done_draw[row][col]:
                            thread.start_new_thread(self.draw_mix, (col, row, 2, str(self.map[row][col]), ))
##                            for i in range(2):
##                                self.draw_mix(col, row, i)
##                                done_draw[row][col] = done[row][col]
##                                time.sleep(0.05)
            self.newPoint()

    def keyUp(self):
        temp = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        for col in range(4):
            for row in range(4):
                if self.map[row][col]!=0:
                    for row_r in range(4):
                        if temp[row_r][col]==0:
                            break
                    temp[row_r][col] = self.map[row][col]
        for col in range(4):
            for row in range(3):
                if temp[row][col]==temp[row+1][col]:
                    temp[row][col] *= 2
                    temp[row+1][col] = 0
        result = [[0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0],
                  [0, 0, 0, 0]]
        for col in range(4):
            for row in range(4):
                if temp[row][col]!=0:
                    for row_r in range(4):
                        if result[row_r][col]==0:
                            break
                    result[row_r][col] = temp[row][col]
        #self.show(result)
        done = [[0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]]
        done_draw = [[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]]
        if self.map!=result:
            while self.map!=result:
                for col in range(4):
                    for row in  range(3):
                        if done[row][col]==0:
                            if self.map[row][col]==0:
                                if self.map[row+1][col]!=0:
                                    self.map[row][col], self.map[row+1][col] = self.map[row+1][col], self.map[row][col]
                            else:
                                if self.map[row+1][col]==self.map[row][col] and done[row+1][col]==0:
                                    self.map[row][col] *= 2
                                    self.map[row+1][col] = 0
                                    done[row][col] = 1
                print 'next'
                self.draw()
                for row in range(4):
                    for col in range(4):
                        if done[row][col]!= done_draw[row][col]:
                            thread.start_new_thread(self.draw_mix, (col, row, 2, str(self.map[row][col]), ))
##                            for i in range(2):
##                                self.draw_mix(col, row, i)
##                                done_draw[row][col] = done[row][col]
##                                time.sleep(0.05)
            self.newPoint()

    def show(self, arg):
        for row in arg:
            for col in row:
                print col,
            print ' '

    def draw(self):
        dc = wx.BufferedDC(wx.ClientDC(self), wx.Bitmap())
        dc.Clear()
        for row in range(4):
            for col in range(4):
                dc.Blit(110*col, 110*row, 110, 110, self.img[str(self.map[row][col])], 110, 0)

    def loadData(self):
        self.img = {
               '0' : wx.MemoryDC(),
               '2' : wx.MemoryDC(),
               '4' : wx.MemoryDC(),
               '8' : wx.MemoryDC(),
              '16' : wx.MemoryDC(),
              '32' : wx.MemoryDC(),
              '64' : wx.MemoryDC(),
             '128' : wx.MemoryDC(),
             '256' : wx.MemoryDC(),
             '512' : wx.MemoryDC(),
            '1024' : wx.MemoryDC(),
            '2048' : wx.MemoryDC()
            }
        for i in range(12):
            if i==0:
                self.img['0'].SelectObject(wx.Bitmap('0.jpg'))
            else:
                self.img[str(2**i)].SelectObject(wx.Bitmap(str(2**i)+'.jpg'))

    def initGame(self):
        self.map = [[0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]]
        self.newPoint()
        self.newPoint()

    def checkEnd(self, empty):
        if empty==[]:
            for row in range(4):
                for col in range(3):
                    if self.map[row][col]==self.map[row][col+1]:
                        return
            for col in range(4):
                for row in range(3):
                    if self.map[row][col]==self.map[row+1][col]:
                        return
            wx.MessageBox('Sorry! You are loser :(')
            self.initGame()

    @multithread
    def draw_newPoint(self, x, y, i, src):
        x *= 110
        y *= 110
        xsrc = 110*(5-i)
        ysrc = 0
        dc = wx.BufferedDC(wx.ClientDC(self), wx.Bitmap())
        dc.SetClippingRegion(x, y, 110, 110)
        dc.Clear()
        dc.Blit(x, y, 110, 110, self.img[src], xsrc, ysrc)
        dc.DestroyClippingRegion()
    
    def newPoint(self):
        empty = []
        highscore = 0
        for row in range(4):
            for col in range(4):
                if self.map[row][col] == 0:
                    empty.append((row, col))
                else:
                    if self.map[row][col]>highscore:
                        highscore = self.map[row][col]
        if highscore == 2048:
            wx.MessageBox('Congratulation! You are winner ^^')
            self.initGame()
        else:
            pos = random.choice(empty)
            self.map[pos[0]][pos[1]] = 2
            empty.remove((pos[0], pos[1]))
            self.draw()
            thread.start_new_thread(self.draw_newPoint, (pos[1], pos[0], 5, '2', ))
##            for i in range(5):
##                self.draw_newPoint(pos[1], pos[0], i, '2')
##                time.sleep(0.02)
            self.show(self.map) #####
        self.checkEnd(empty)
    
def main():
    app = wx.App()
    Win()
    app.MainLoop()

if __name__=='__main__':
    main()

