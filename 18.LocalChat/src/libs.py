#!/usr/bin/python

""""""

import threading, base64

BUF_SIZE = 1024

class MyThread(threading.Thread):

    def __init__(self, func, *var):
        threading.Thread.__init__(self)
        self.func = func
        self.var = var

    def run(self):
        self.func(*self.var)


def isThread(func):
    
    def wrap(*var):
        thread = MyThread(func, *var)
        thread.start()
        return thread
        
    return wrap

def sendOnSocket(connection, data):
    if data=='':
        return False
    try:
        l = len(data)
        i = 0
        ls_data = []
        while True:
            j = i + BUF_SIZE
            if j>=l:
                ls_data.append(data[i:l])
                break
            ls_data.append(data[i:j])
            i += BUF_SIZE
        l = len(ls_data)
        connection.send(str(l).encode())
        connection.recv(BUF_SIZE)
        for data in ls_data:
            connection.send(data.encode())
            connection.recv(BUF_SIZE)
    except:
        return False
    return True

def recvOnSocket(connection):
    datasize = ''
    try:
        datasize = connection.recv(BUF_SIZE).decode()
        if datasize=='':
            return ''
        connection.send(b'y')
        data = []
        for _ in range(int(datasize)):
            data.append(connection.recv(BUF_SIZE).decode())
            connection.send(b'y')
    except:
        return ''
    return ''.join(data)

def sendFileOnSocket(connection, filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        connection.send(str(len(data)).encode())
        connection.recv(2)
        connection.send(data)
    except:
        return False
    return True

def recvFileOnSocket(connection, savepath):
    datasize = ''
    try:
        datasize = connection.recv(1024).decode()
    except: pass
    if datasize=='':
        return False
    try:
        connection.send('y'.encode())
    except:
        return False
    datasize = int(datasize)
    data = b''
    while len(data)!=datasize:
        chuck = b''
        try:
            chuck = connection.recv(1024)
        except: pass
        #print('%d: '%datasize + chuck)
        if chuck==b'':
            return False
        data += chuck
    with open(savepath, 'wb') as f:
        f.write(data)
    return True

def getStringFromImageFile(filepath):
    with open(filepath, 'rb') as f:
        data = base64.b64encode(f.read()).decode()
    return data

def main():
    data = getStringFromImageFile('image/mask.png')
    with open('asd.txt', 'w') as f:
        f.write(data)
    return
    data64 = []
    begin = 0
    end = begin + 80
    length = len(data)
    while end < length:
        data64.append(data[begin:end])
        begin, end = end, end + 80
    data64.append(data[begin:length])
    with open('asd.txt', 'w') as f:
        f.write('\n'.join(data64))
    return True

if __name__ == '__main__':
    main()