#!/usr/bin/python

from time import time,sleep
from read_data import read_data
from select_word import select_word
from show_word import show_word
from show_error import show_error
from check_time import check_time

data=read_data()

if data==[]: show_error('Error read data of\nCrazy English')
else:
	before=[time()-600]
	while True:
		if check_time(before): 
			if show_word(select_word(data))==-1: break
		sleep(5)
	

