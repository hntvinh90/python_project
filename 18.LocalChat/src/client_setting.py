#!/usr/bin/python

""""""

from libs import isThread, sendOnSocket
import socket as sk
import wx

class Setting:
    def __init__(self, parent):
        self.parent = parent
        self.VERSION = '1.05072018'
        self.PATH = '.client'
        self.username = ''
        self.HOST = ''
        self.POST = 9999
        self.loadPref()
        if self.HOST=='' or not self.testHost():
            if not self.searchServer():
                ip = wx.GetTextFromUser('Can not find out server. Can you configure server address?', 'Warning')
                if ip!='':
                    self.HOST = ip
                    if not self.testHost():
                        self.HOST = ''
        self.savePref()
        
    def loadPref(self):
        try:
            with open(self.PATH, 'r') as f:
                data = f.read().split('\n')
            self.HOST = data[0]
            self.username = data[1]
        except: pass
    
    def savePref(self):
        with open(self.PATH, 'w') as f:
            f.write('\n'.join((self.HOST, self.username)))

    def searchServer(self):
        root = '.'.join(sk.gethostbyname(sk.gethostname()).split('.')[:3])
        ls = []
        for i in range(256):
            ip = '.'.join((root, str(i)))
            ls.append(self.testIP(ip))
        for thread in ls:
            if self.HOST!='':
                break
            thread.join()
        if self.HOST=='':
            return False
        return True

    @isThread
    def testIP(self, ip):
        s = sk.socket()
        try:
            s.connect((ip, self.POST))
        except:
            s.close()
            return
        if self.HOST=='':
            self.HOST = ip
        sendOnSocket(s, 'test')
        s.close()
    
    def testHost(self):
        s = sk.socket()
        try:
            s.connect((self.HOST, self.POST))
        except:
            s.close()
            self.HOST = ''
            return False
        sendOnSocket(s, 'test')
        s.close()
        return True

def main():
    return True

if __name__ == '__main__':
    main()
