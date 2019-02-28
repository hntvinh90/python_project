#!/usr/bin/python

""""""

from myLibs import isThread
import time

DATA = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
LENGTH = 64

@isThread
def run(id):
    for i in range(1000000000):
        pass
    print('Finish', id)

def main():
    t = time
    ls = []
    for i in range(1000):
        ls.append(run(i))
    for l in ls:
        l.join()
    print(time()-t)
    return True

if __name__ == '__main__':
    main()
