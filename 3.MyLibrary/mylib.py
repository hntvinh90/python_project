#!/usr/bin/python

################################################################################
'''
	Get CPU info per 500ms: 
		Core number --> core_number
		CPU percent --> percent=[total,core_1,...,core_n]
'''

from os import popen
from time import sleep

class cpu:
	
	def __init__(self):
		try:
			self.core_number=self.__get_cpu_core_number()
			self.percent=self.__calculate_cpu_percent()
		except Exception: 
			self.core_number=1
			self.percent=[0,0]
			
	def __get_cpu_core_number(self):
		cmd=popen('grep "processor" /proc/cpuinfo')
		core_number=len(cmd.read().splitlines())
		cmd.close()
		return core_number
		
	def __get_cpu_job_info(self):
		cpu=[]
		cmd=popen('grep "cpu" /proc/stat')
		for i in range(self.core_number+1):
			cpu.append(cmd.readline().split())
		cmd.close()
		return cpu
		
	def __calculate_cpu_percent(self):
		cpu=[]
		jobs_begin=self.__get_cpu_job_info()
		sleep(0.5)
		jobs_end=self.__get_cpu_job_info()
		for i in range(len(jobs_begin)):
			active=(int(jobs_end[i][1])+int(jobs_end[i][3])+\
				int(jobs_end[i][5]))-(int(jobs_begin[i][1])+\
				int(jobs_begin[i][3])+int(jobs_begin[i][5]))
			total=active+int(jobs_end[i][4])-int(jobs_begin[i][4])
			if total==0:
				active=0
				total=1
			cpu.append(100*active/total)
		return cpu
################################################################################
# TEST
#print cpu().core_number
#print cpu().percent
#while True:
#	print cpu().percent
################################################################################

################################################################################
'''
	Create a WINDOW when passing variables:
		title     (string)
		width     (int)
		height    (int)
		icon      (string)
		resizable (True/False)
'''

from Tkinter import Tk,PhotoImage

def new_window(title='',width=-1,height=-1,icon='',resizable=True):
	root=Tk()
	if title=='': pass
	else: root.title(title)
	if width==-1 or height==-1: pass
	else: root.geometry(str(width)+'x'+str(height))
	if icon=='': pass
	else: root.call('wm','iconphoto',root._w,PhotoImage(file=str(icon)))
	if resizable==True: pass
	else: root.resizable(resizable,resizable)
	return root
################################################################################
# TEST
################################################################################

################################################################################
'''
	Get website source 
		when passing variable 'website_address'
'''

from httplib import HTTPSConnection

def get_website_source(add=''):
	if add=='':
		raise NameError('Have no website address yet')
	conn=HTTPSConnection(add)
	conn.request('GET','/the-thao-c101.html')
	r=conn.getresponse()
	if str(r.status)=='200':
		return r.read()
	else: return ''
	conn.close()
################################################################################
# TEST
print get_website_source('www.24h.com.vn')
################################################################################

################################################################################
#                                                                              #
# CPU info --------------------------------------------------------> page    3 #
#                                                                              #
# Window creating -------------------------------------------------> page   60 #
#                                                                              #
# Get website source ----------------------------------------------> page   87 #
#                                                                              #
################################################################################
