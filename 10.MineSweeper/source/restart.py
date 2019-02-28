#!/usr/bin/python

from threading import Thread

class restart(Thread):

	def __init__(self):
		Thread.__init__(self)
		from random import choice
		from time import sleep
		self.__choice=choice
		self.__sleep=sleep
		self.list_cell=''
		self.flag_number=''
		self.right=''
		self.game_status=''
		self.size_game=''
		self.boom_number=''
		
	def run(self):
		while self.game_status[0]!='normal':
			self.__sleep(0.1)
		try:
			self.flag_number[0]=self.boom_number[0]
			self.right[0]=0
			temp=[i for i in range(self.size_game[0]*self.size_game[1])]
			for i in self.list_cell: 
				i[0].carry=0
				i[0].status='hide'
			for i in range(self.boom_number[0]):
				k=self.__choice(temp)
				temp.remove(k)
				self.list_cell[k][0].carry=-1
			for i in self.list_cell:
				if i[0].carry!=-1:
					count=0
					for k in i[0].near:
						if k[0].carry==-1: count+=1
					i[0].carry=count
				i[0].show()
			del temp,i,k,count
		except Exception:
			print('Exit game')

if __name__=='__main__':
	pass
