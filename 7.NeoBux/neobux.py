#!/usr/bin/python

from Tkinter import Tk,Button,Label,PhotoImage,StringVar
from time import sleep
from multiprocessing import Process,Queue
from click_manager import click_manager

class gui:
	
	status=Queue()
	
	def __init__(self):
	
		self.onoff=0
		self.__gui_create()
		
	
	def __gui_create(self):
		self.root=Tk()
		self.root.title('ClickNEOBUX')
		w=self.root.winfo_screenwidth()-180
		h=self.root.winfo_screenheight()-50
		self.root.geometry('180x80+'+str(w)+'+'+str(h))
		self.root.resizable(False,False)
		self.root.protocol('WM_DELETE_WINDOW',self.__gui_exit)
		try:
			self.root.call('wm','iconphoto',self.root._w,PhotoImage(file='data/neobux.png'))
		except Exception:
			print 'Error loading icon'
	
		self.text_btn=StringVar()
		self.text_btn.set('Start')
		Button(self.root,textvariable=self.text_btn,command=self.__gui_click_btn).place(x=50,y=10,height=30,width=80)
	
		self.text_lb=StringVar()
		self.text_lb.set('Pausing ...')
		Label(self.root,textvariable=self.text_lb).place(x=0,y=50,width=180,height=30)
		
		#self.root.after(0,self.__check_status)
		
		self.root.mainloop()
		print 'Exit GUI'
		
		
	def __gui_exit(self):
		if self.onoff in [0,1]:
			self.root.destroy()
			self.proc.terminate()
		else: print 'Clicking ...'
		
	
	def __gui_click_btn(self):
		if self.onoff==0:
			self.text_btn.set('Pause')
			self.text_lb.set('Starting ...')
			self.onoff=1
			self.proc=Process(target=click_manager,args=(self.status,))
			self.proc.start()
			self.__check_status()
		elif self.onoff==1:
			self.text_btn.set('Start')
			self.text_lb.set('Pausing ...')
			self.onoff=0
			self.proc.terminate()
			self.proc.exitcode
			
			
	def __check_status(self):
		status=''
		try:
			status=self.status.get(False)
		except Exception:
			pass
		else:
			self.text_lb.set(status)
		finally:
			if self.onoff!=0:
				if not self.proc.is_alive():
					self.proc=Process(target=click_manager,args=(self.status,))
					self.proc.start()
				self.root.after(100,self.__check_status)
		
		
gui()
