#!/usr/bin/python

class cell:

	def __init__(self):
		self.root=''
		self.status='hide'
		self.near=''
		self.row=0
		self.col=0
		self.carry=0
		self.flag_number=''
		self.right=''
		self.list_cell=''
		self.img=''
		self.game_status=''
		self.size_game=''
		self.boom_number=''
		
	def show(self):
		try:
			self.__item
		except Exception:
			self.__item=self.root[0].create_image(25*self.col,25*self.row,anchor='nw')
			self.root[0].tag_bind(self.__item,'<Button-3>',self.__right_click)
			self.root[0].tag_bind(self.__item,'<Button-1>',self.__left_click)
			self.root[0].tag_bind(self.__item,'<ButtonPress-2>',self.__mid_click_down)
			self.root[0].tag_bind(self.__item,'<ButtonRelease-2>',self.__mid_click_up)
		if self.status=='open':
			self.root[0].itemconfigure(self.__item,image=self.img[self.carry])
		else: 
			self.root[0].itemconfigure(self.__item,image=self.img[self.status])
	
	def gameover(self):
		for i in self.list_cell:
			if i[0].status=='hide':
				i[0].status='open'
			elif i[0].status=='flag':
				if i[0].carry!=-1: i[0].status='wflag'
			i[0].show()
		if self.flag_number[0]>0:
			print('You lose')
			self.game_status[0]='lose'
		else:
			if self.right[0]>=10:
				print('You win')
				self.game_status[0]='win'
			else: 
				print('You lose')
				self.game_status[0]='lose'
		from restart import restart
		r=restart()
		r.list_cell=self.list_cell
		r.flag_number=self.flag_number
		r.right=self.right
		r.game_status=self.game_status
		r.size_game=self.size_game
		r.boom_number=self.boom_number
		r.start()
		del r
	
	def __right_click(self,e):
		if self.status=='hide':
			self.status='flag'
			self.flag_number[0]-=1
			if self.carry==-1: self.right[0]+=1
			self.show()
			if self.flag_number[0]<=0: self.gameover()
		elif self.status=='flag':
			self.status='hide'
			self.flag_number[0]+=1
			if self.carry==-1: self.right[0]-=1
			self.show()
	
	def __left_click(self,e):
		if self.status=='hide':
			if self.carry==-1:
				self.status='wrong'
				self.show()
				self.gameover()
			elif self.carry==0:
				self.open_around()
			else:
				self.status='open'
				self.show()

	def open_around(self):
		self.status='open'
		self.show()
		for i in self.near:
			if i[0].status=='hide':
				if i[0].carry==0: i[0].open_around()
				elif i[0].carry==-1:
					i[0].status='wrong'
					i[0].show()
					i[0].gameover()
				else:
					i[0].status='open'
					i[0].show()
		del i
	
	def __mid_click_down(self,e):
		if self.status=='open':
			for i in self.near:
				if i[0].status=='hide':
					i[0].status='press'
					i[0].show()
			del i
	
	def __mid_click_up(self,e):
		if self.status=='open':
			for i in self.near:
				if i[0].status=='press':
					i[0].status='hide'
					i[0].show()
			if self.__check_flag(): self.open_around()
			del i
	
	def __check_flag(self):
		n=0
		for i in self.near:
			if i[0].status=='flag': n+=1
		if n==self.carry: return(True)
		else: return(False)

if __name__=='__main__':
	from Tkinter import Tk,Canvas
	root=Tk()
	
	c=[Canvas(root,width=225,height=225)]
	c[0].pack()
	
	cell=cell()
	cell.root=c
	cell.row=0
	cell.col=0
	cell.carry=2
	cell.rest=10
	cell.show()
	
	root.mainloop()
