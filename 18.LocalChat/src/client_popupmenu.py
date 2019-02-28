#!/usr/bin/python

""""""

import wx, base64, os
from img import Image

class PopupAvatar(wx.Menu):
    def __init__(self, parent):
        wx.Menu.__init__(self)
        self.parent = parent #client window
        self.parent.Bind(wx.EVT_MENU, self.changeAvatar, self.Append(-1, 'Change'))
        
    def changeAvatar(self, event):
        file = wx.FileSelector('Select an image')
        if file!='' and os.path.exists(file):
            try:
                try:
                    os.remove('temp_img.png')
                except: pass
                img = wx.Bitmap(wx.Image(file).Rescale(64, 64))
                img.SetMask(wx.Mask(Image['mask'].GetBitmap(), wx.BLACK))
                img.SaveFile('temp_img.png', wx.BITMAP_TYPE_PNG)
            except:
                wx.MessageBox('Error', 'Error')
                return
            with open('temp_img.png', 'rb') as f:
                self.parent.cache.append(('changeavatar', base64.b64encode(f.read()).decode()))
            os.remove('temp_img.png')

def main():
    return True

if __name__ == '__main__':
    main()
