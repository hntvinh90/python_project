#!/usr/bin/python

from threading import Thread
from time import time,sleep

class header(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.frame=''
		self.flag_number=''
		self.img=''
		self.status=''
		self.exit=''
		self.t=0
		self.max=0
		self.list_cell=''
		self.size_game=''

	def run(self):
		import config_file
		config_file.size_game=self.size_game
		self.max=list(config_file.read())[0]
		self.item1=self.frame[0].create_text(30,10,fill='red',font=('Purisa',16),text=str(self.flag_number[0]))
		self.item2=self.frame[0].create_image(70,0,anchor='nw',image=self.img[self.status[0]])
		self.frame[0].tag_bind(self.item2,'<ButtonPress-1>',self.__press)
		self.frame[0].tag_bind(self.item2,'<ButtonRelease-1>',self.__release)
		self.item4=self.frame[0].create_text(135,10,fill='red',font=('Purisa',16),text=str(self.max))
		self.frame[0].create_text(170,10,fill='red',font=('Purisa',16),text='/')
		self.item3=self.frame[0].create_text(205,10,fill='red',font=('Purisa',16),text=str(999))
		self.t=time()
		while self.exit[0]==0:
			try:
				self.frame[0].itemconfigure(self.item1,text=str(self.flag_number[0]))
				self.frame[0].itemconfigure(self.item2,image=self.img[self.status[0]])
				if self.status[0]=='normal':
					self.frame[0].itemconfigure(self.item3,text=str(int(time()-self.t)))
				elif self.status[0]=='win':
					if self.max>(time()-self.t):
						self.max=int(time()-self.t)
						config_file.write(self.max)
						self.frame[0].itemconfigure(self.item4,text=str(self.max))
				sleep(0.1)
			except Exception: break
	
	def __press(self,e):
		self.frame[0].itemconfigure(self.item2,image=self.img[self.status[0]+'_press'])
	
	def __release(self,e):
		self.frame[0].itemconfigure(self.item2,image=self.img[self.status[0]])
		if self.status[0]=='normal':
			self.list_cell[0][0].gameover()
		self.status[0]='normal'
		self.t=time()

if __name__=='__main__':
	pass
