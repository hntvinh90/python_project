#!/usr/bin/python

frame=''
list_cell=[]
flag_number=''
right=[0]
img=''
game_status=''
size_game=''
boom_number=''

def load():
	from cell import cell
	global list_cell,size_game
	for i in range(size_game[0]*size_game[1]):
		list_cell.append([cell()])
	del i

def load_boom():
	from random import choice
	global list_cell,size_game,boom_number
	temp=[i for i in range(size_game[0]*size_game[1])]
	for i in range(boom_number[0]):
		k=choice(temp)
		temp.remove(k)
		list_cell[k][0].carry=-1
	del temp,i,k

def find_near(i):
	global list_cell,size_game
	near=[]
	r=i//size_game[0]
	c=i%size_game[0]
	for k in [-1,0,1]:
		for l in [-1,0,1]:
			if (k!=0 or l!=0)and(r!=0 or k!=-1)and(r!=(size_game[1]-1) or k!=1)and(c!=0 or l!=-1)and(c!=(size_game[0]-1) or l!=1):
				near.append(list_cell[(r+k)*size_game[0]+(c+l)])
	del r,c,k,l
	return(near)

def find_carry(i):
	global list_cell
	if list_cell[i][0].carry!=-1:
		count=0
		for k in list_cell[i][0].near:
			if k[0].carry==-1: count+=1
		del k
		return(count)
	return(-1)

def start():
	global frame,list_cell,flag_number,right,img,game_status,size_game
	load()
	load_boom()
	for i in range(size_game[0]*size_game[1]):
		list_cell[i][0].root=frame
		list_cell[i][0].status='hide'
		list_cell[i][0].near=find_near(i)
		list_cell[i][0].row=i//size_game[0]
		list_cell[i][0].col=i%size_game[0]
		list_cell[i][0].carry=find_carry(i)
		list_cell[i][0].flag_number=flag_number
		list_cell[i][0].right=right
		list_cell[i][0].list_cell=list_cell
		list_cell[i][0].img=img
		list_cell[i][0].game_status=game_status
		list_cell[i][0].size_game=size_game
		list_cell[i][0].boom_number=boom_number
		list_cell[i][0].show()
	del i

if __name__=='__main__':
	from Tkinter import Tk,Canvas
	root=Tk()
	c=[Canvas(root,width=225,height=225)]
	c[0].pack()
	frame=c
	start()
	for i in range(81):
		if i%9==0: print('')
		print(str(list_cell[i][0].carry).rjust(4,' '),)
	print('')
	root.mainloop()
