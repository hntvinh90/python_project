#!/usr/bin/python
from read_data import read_data
from select_word import select_word
from show_word import show_word
from check_time import check_time
from show_error import show_error

from time import sleep,time

data=read_data('data')
#0 - word
#1 - phan loai tu
#2 - phien am
#3 - y nghia
#4 - know (1) or unkonw (0)

if data==[]: show_error('Error read data of\nEnglish3000')
else:
	word,i=select_word(data)
	#i=0 - hien thi word
	#i=3 - hien thi nghia cua tu

	before=[time()-600]
	number=0
	while True:
		if check_time(before): 
			if show_word(data,word,i)==-1: break
			number+=1
			if number==10: word,i=select_word(data,'check');number=0
			else: word,i=select_word(data)
		sleep(5)
		#print 'continue'
