#!/usr/bin/python

import wx


class TabInfo(wx.Panel):

    def __init__(self, parent):
        #parent.tabs.tab_info = self
        wx.Panel.__init__(self, parent.tabs)
        parent.tabs.AddPage(self, 'About')

        lb1 = wx.StaticText(self, -1, 'Developed by')
        lb2 = wx.StaticText(self, -1, 'Ho Nguyen Thanh Vinh\n', style=wx.TE_MULTILINE|wx.ALIGN_CENTER)
        lb3 = wx.StaticText(self, -1, 'Researcher and Reactor Operator\n'+
                            'Reactor Center, Dalat Nuclear Research Institute, VINATOM\n'+
                            '01 Nguyen Tu Luc Str., Dalat, Lamdong, Vietnam',
                            style=wx.TE_MULTILINE|wx.ALIGN_CENTER)
        lb4 = wx.StaticText(self, -1, '\nEmail:  vinhhnt.re@dnri.vn\n'+
                            'Phone:  +84-1237573900\n'+
                            'Office: +84-263-3829613\n'+
                            'Fax:    +84-263-3821107',
                            style=wx.TE_MULTILINE)

        lb1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        lb2.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        lb3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        lb4.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(lb1, 0, wx.CENTER)
        sizer.Add(lb2, 0, wx.CENTER)
        sizer.Add(lb3, 0, wx.CENTER)
        sizer.Add(lb4, 0, wx.CENTER)
        s = wx.BoxSizer(wx.HORIZONTAL)
        s.Add(sizer, 1, wx.CENTER)
        self.SetSizer(s)


def main():
    return True

if __name__ == '__main__':
    main()
    '''
    Researcher and Reactor Operator 
    Reactor Center, Dalat Nuclear Research Institute, VINATOM
    Email:  vinhhnt.re@dnri.vn
    Phone:  +84-1237573900
    Office: +84-263-3829613
    Fax:    +84-263-3821107 
    01 Nguyen Tu Luc Str., Dalat, Lamdong, Vietnam
    '''
