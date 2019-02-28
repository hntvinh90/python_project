#!/usr/bin/python

from Tkinter import Canvas,Frame
from mylib import new_window
from threading import Thread
from time import sleep
from random import randrange,choice

def init():
	global position,list_thread,exit,next,pause,max_point,shape,shape_future,shape,shape_future
	pause=False
	next=0
	exit=0
	list_thread=[]
	position=[0,0]
	screen_draw()
	matrix_create()
	shape=choice_shape()
	shape_future=choice_shape()
	position[1]=5-len(shape[0])/2
	position[0]=4-len(shape)
	read_config()
	
def screen_draw():
	global window,canvas_frame,canvas_play,canvas_play1,canvas_play2,canvas_future,level,point,max_point,canvas_pause
	level=1
	point=0
	max_point=0
	canvas_frame=Canvas(window)#,bg='red')
	canvas_frame.place(x=0,y=0,relwidth=1.0,relheight=1.0)
	global frame1,frame2
	frame1=Frame(window)
	frame2=Frame(window)
	frame1.place(x=0,y=0,width=300,height=600)
	frame2.place(x=0,y=0,width=300,height=600)
	canvas_play1=Canvas(frame1,bg='#000000')
	canvas_play1.place(x=0,y=0,width=300,height=600)
	for x in range(1,10):
		for y in range(1,20):
			canvas_play1.create_line(30*x,0,30*x,600,fill='#111111')#,tag='play')
			canvas_play1.create_line(0,30*y,300,30*y,fill='#111111')#,tag='play')
	canvas_play2=Canvas(frame2,bg='#000000')
	canvas_play2.place(x=0,y=0,width=300,height=600)
	for x in range(1,10):
		for y in range(1,20):
			canvas_play2.create_line(30*x,0,30*x,600,fill='#111111')
			canvas_play2.create_line(0,30*y,300,30*y,fill='#111111')
	canvas_play=frame2
	canvas_frame.create_text(370,200,font=('Purisa',24),text='Level',anchor='n')
	canvas_frame.create_text(370,336,font=('Purisa',24),text='Point',anchor='n')
	canvas_frame.create_text(370,436,font=('Purisa',24),text='Max',anchor='n')
	canvas_frame.create_text(370,270,text=str(level),font=('',24),fill='#0000ff',tag='level')
	canvas_frame.create_text(370,400,text=str(point),font=('',24),fill='#0000ff',tag='point')
	canvas_frame.create_text(370,500,text=str(max_point),font=('',24),fill='#ff0000',tag='max')
	canvas_future=Canvas(window)#,bg='#0000ff')
	canvas_future.place(x=310,y=10,width=120,height=120)
	canvas_pause=Canvas(canvas_frame)#,bg='yellow')
	canvas_pause.place(x=345,y=540,width=50,height=50)
	draw_play()
	canvas_pause.bind('<ButtonPress-1>',event_pause)
	
def event_pause(e):
	global pause
	if pause==True: 
		pause=False
		draw_play()
	else:
		pause=True
		draw_pause()

def draw_pause():
	global canvas_pause
	canvas_pause.delete('pause')
	canvas_pause.create_rectangle(13,10,23,40,fill='#ff0000',tag='pause')
	canvas_pause.create_rectangle(27,10,37,40,fill='#ff0000',tag='pause')
	
def draw_play():
	global canvas_pause
	canvas_pause.delete('pause')
	canvas_pause.create_polygon(10,10,40,25,10,40,fill='#00ff00',tag='pause')

def dot_draw(master,x0,y0,color,string):
	x=1+30*x0; y=1+30*y0
	master.create_rectangle(x,y,x+28,y+28,fill='#ffffff',outline='#ffffff',tag=string)
	master.create_rectangle(x+2,y+2,x+26,y+26,fill=color,outline=color,tag=string)

def rotate(matrix):
	target=[]
	for x in range(len(matrix[0])):
		k=len(matrix)-1
		target.append([])
		for y in range(len(matrix)):
			target[len(target)-1].append([])
			target[x][y]=matrix[k][x]
			k-=1
	return target

def matrix_create():
	global matrix_main,matrix_shape,matrix_future,matrix_temp
	matrix_main=[]
	matrix_temp=[]
	matrix_shape=[]
	matrix_future=[[[0,''],[0,''],[0,''],[0,'']],[[0,''],[0,''],[0,''],[0,'']],[[0,''],[0,''],[0,''],[0,'']],[[0,''],[0,''],[0,''],[0,'']]]
	for i in range(24):
		matrix_main.append([])
		matrix_temp.append([])
		for j in range(10):
			matrix_main[len(matrix_main)-1].append([])
			matrix_temp[len(matrix_temp)-1].append([])
			matrix_main[i][j]=[0,'']
	matrix_shape.append([[[1,'#00ffff'],[1,'#00ffff'],[1,'#00ffff'],[1,'#00ffff']]])
	matrix_shape.append([[[1,'#0000ff'],[0,''],[0,'']],[[1,'#0000ff'],[1,'#0000ff'],[1,'#0000ff']]])
	matrix_shape.append([[[0,''],[0,''],[1,'#ff7700']],[[1,'#ff7700'],[1,'#ff7700'],[1,'#ff7700']]])
	matrix_shape.append([[[1,'#ffff00'],[1,'#ffff00']],[[1,'#ffff00'],[1,'#ffff00']]])
	matrix_shape.append([[[0,''],[1,'#ff00ff'],[0,'']],[[1,'#ff00ff'],[1,'#ff00ff'],[1,'#ff00ff']]])
	matrix_shape.append([[[0,''],[1,'#00ff00'],[1,'#00ff00']],[[1,'#00ff00'],[1,'#00ff00'],[0,'']]])
	matrix_shape.append([[[1,'#ff0000'],[1,'#ff0000'],[0,'']],[[0,''],[1,'#ff0000'],[1,'#ff0000']]])

def delete_row(index):
	global matrix_main
	for i in range(index,3,-1):
		for j in range(10):
			if i==4:
				matrix_main[i][j]=[0,'']
			else:
				matrix_main[i][j]=matrix_main[i-1][j]

def check_point():
	global matrix_main
	point=[]
	k=0
	for i in range(4,24):
		for j in range(10):
			if matrix_main[i][j][0]==1: k+=1
			else: break
		if k==10: point.append(i)
		k=0
	for i in point:
		delete_row(i)
	k=len(point)
	flip()
	return k*(k+1)/2

def add_point():
	global canvas_frame,point,max_point,level
	point+=check_point()
	level=point/50+1
	canvas_frame.itemconfigure('point',text=str(point))
	canvas_frame.itemconfigure('level',text=str(level))
	if max_point<point:
		max_point=point
		canvas_frame.itemconfigure('max',text=str(max_point))
		
def check_gameover():
	global matrix_main
	for j in range(10):
		if matrix_main[4][j][0]==1: return True
	return False

def choice_shape():
	global matrix_shape,canvas_future
	if check_gameover()==True:
		print 'Game Over'
		replay()
	add_point()
	shape=matrix_shape[randrange(7)]
	n=choice([0,90,180,270])/90
	for i in range(n):
		shape=rotate(shape)
	canvas_future.delete('future')
	draw_future(shape)
	return shape
	
def draw_future(shape):
	global canvas_future
	pos=[0,0]
	pos[0]=4-len(shape)
	pos[1]=2-len(shape[0])/2
	for i in range(len(shape)):
		for j in range(len(shape[0])):
			if shape[i][j][0]==1: dot_draw(canvas_future,j+pos[1],i+pos[0],shape[i][j][1],'future')
	
def flip():
	global matrix_temp,matrix_main,shape,position,canvas_play,canvas_play1,canvas_play2,frame1,frame2
	
	if canvas_play==frame1:
		canvas=canvas_play2
		canvas_play=frame2
	else:
		canvas=canvas_play1
		canvas_play=frame1
	canvas.delete('play')
	canvas.delete('stop')
	for i in range(4,24):
		for j in range(10):
			if matrix_main[i][j][0]==1: dot_draw(canvas,j,i-4,matrix_main[i][j][1],'stop')
	canvas_play.lift()

def move():
	pause=True
	global shape,canvas_play1,canvas_play2,frame1,frame2,position
	if canvas_play==frame1:
		canvas=canvas_play1
	else:
		canvas=canvas_play2
	canvas.delete('play')
	for i in range(len(shape)):
		if i+position[0]>=4:
			for j in range(len(shape[0])):
				if shape[i][j][0]==1:
					dot_draw(canvas,j+position[1],i+position[0]-4,shape[i][j][1],'play')
	pause=False

class play(Thread):

	def __init__(self):
		Thread.__init__(self)
		
	def run(self):
		global exit,level
		try:
			while exit==0:
				down(1)
				sleep(0.5/level)
		except Exception:
			print 'Error in play thread'
			restart_thread().start()
		else: print 'Thread out'

class restart_thread(Thread):
	
	def __init__(self):
		Thread.__init__(self)
	
	def run(self):
		if exit==0:
			global list_thread
			list_thread[0]=play()
			list_thread[0].start()

def replay():
	global matrix_main,point,canvas_frame
	for i in range(24):
		for j in range(10):
			matrix_main[i][j]=[0,'']
	point=0
	canvas_frame.itemconfigure('point',text=str(point))
	flip()

def up():
	global pause
	if pause==True: return
	global shape,position
	temp=rotate(shape)
	error=0
	for i in range(len(temp)):
		for j in range(len(temp[0])):
			if i+position[0]<24:
				if j+position[1]<10:
					if matrix_main[i+position[0]][j+position[1]][0]==1 and temp[i][j][0]==1: error=1;break
				else: error=1;break
			else: error=1;break
		if error==1: break
	if error==0: shape=temp
	move()
	
def down(speed):
	global pause
	if pause==True: return
	global position,shape,shape_future,matrix_main,matrix_temp,next
	position[0]+=speed
	if position[0]+len(shape)>=24:
		position[0]=24-len(shape)
	error=1
	end=0
	while error==1:
		error=0
		for i in range(len(shape)):
			for j in range(len(shape[0])):
				if matrix_main[i+position[0]][j+position[1]][0]==1 and shape[i][j][0]==1: error=1;break
			if error==1: break
		if error==1: 
			position[0]-=1
			if next==1: end=1
			else: next=1
	if position[0]==24-len(shape): 
		if next==0: next=1
		else: position[0]+=1
	if end==1 or position[0]>24-len(shape):
		next=0
		if position[0]>24-len(shape): position[0]=24-len(shape)
		for i in range(len(shape)):
			for j in range(len(shape[0])):
				if shape[i][j][0]==1:
					matrix_main[i+position[0]][j+position[1]]=shape[i][j]
		flip()
		shape=shape_future
		shape_future=choice_shape()
		position[1]=5-len(shape[0])/2
		position[0]=4-len(shape)
	move()

def left():
	global pause
	if pause==True: return
	global position,shape
	if position[1]>0: position[1]-=1
	error=0
	for i in range(len(shape)):
		for j in range(len(shape[0])):
			if matrix_main[i+position[0]][j+position[1]][0]==1 and shape[i][j][0]==1:
				error=1; break
		if error==1: break
	if error==1: position[1]+=1
	move()
	
def right():
	global pause
	if pause==True: return
	global position,shape
	if position[1]<10-len(shape[0]): position[1]+=1
	error=0
	for i in range(len(shape)):
		for j in range(len(shape[0])):
			if matrix_main[i+position[0]][j+position[1]][0]==1 and shape[i][j][0]==1:
				error=1; break
		if error==1: break
	if error==1: position[1]-=1
	move()

def write_config():
	global max_point,matrix_main,shape,shape_future,position,point,pause
	f=open('.config','w')
	f.write(str(max_point)+' ')
	f.write('1 ')
	for i in range(24):
		for j in range(10):
			f.write(str(matrix_main[i][j][0])+' ')
			f.write(str(matrix_main[i][j][1])+' ')
	f.write(str(len(shape))+' ')
	f.write(str(len(shape[0]))+' ')
	for i in range(len(shape)):
		for j in range(len(shape[0])):
			f.write(str(shape[i][j][0])+' ')
			f.write(str(shape[i][j][1])+' ')
	f.write(str(len(shape_future))+' ')
	f.write(str(len(shape_future[0]))+' ')
	for i in range(len(shape_future)):
		for j in range(len(shape_future[0])):
			f.write(str(shape_future[i][j][0])+' ')
			f.write(str(shape_future[i][j][1])+' ')
	f.write(str(position[0])+' ')
	f.write(str(position[1])+' ')
	f.write(str(point)+' ')
	if pause==False: f.write('0 ')
	else: f.write('1 ')
	f.close()

def read_config():
	global max_point,matrix_main,shape,shape_future,position,point,canvas_frame,level,pause
	try: f=open('.config','r')
	except Exception: print 'Error open .config file';return False
	else:
		data=f.readline().split()
		f.close()
		k=0
		max_point=int(data[k])
		k+=1
		canvas_frame.itemconfigure('max',text=str(max_point))
		
		if int(data[k])==0: return False
		else:
			k+=1
			for i in range(24):
				for j in range(10):
					matrix_main[i][j][0]=int(data[k]);k+=1
					if matrix_main[i][j][0]==1:
						matrix_main[i][j][1]=data[k];k+=1
			shape=[]
			shape_future=[]
			x=int(data[k]);k+=1
			y=int(data[k]);k+=1
			for i in range(x):
				shape.append([])
				for j in range(y):
					shape[len(shape)-1].append([0,''])
					shape[i][j][0]=int(data[k]);k+=1
					if shape[i][j][0]==1:
						shape[i][j][1]=data[k];k+=1
			x=int(data[k]);k+=1
			y=int(data[k]);k+=1
			for i in range(x):
				shape_future.append([])
				for j in range(y):
					shape_future[len(shape_future)-1].append([0,''])
					shape_future[i][j][0]=int(data[k]);k+=1
					if shape_future[i][j][0]==1:
						shape_future[i][j][1]=data[k];k+=1
			position[0]=int(data[k]);k+=1
			position[1]=int(data[k]);k+=1
			point=int(data[k]);k+=1
			canvas_frame.itemconfigure('point',text=str(point))
			level=point/50+1
			canvas_frame.itemconfigure('level',text=str(level))
			if int(data[k])==0: pause=False
			else: pause=True; draw_pause()
			flip()
			move()
			return True

def exit_main():
	global window,list_thread,exit,canvas_future,canvas_frame,max_point
	exit=1
	del canvas_frame
	if len(list_thread)!=0:
		for thread in list_thread:
			while thread.isAlive()==True: print 'Have a thread running'; sleep(0.5)
	write_config()
	window.destroy()

def press(e):
	if e.keysym=='Up':
		pass
		up()
	if e.keysym=='Down':
		pass
		down(2)
	if e.keysym=='Right':
		pass
		right()
	if e.keysym=='Left':
		pass
		left()

window=new_window('Tetris',440,600,'',False)
window.protocol('WM_DELETE_WINDOW',exit_main)
window.bind('<KeyPress>',press)

init()

list_thread.append(play())
list_thread[0].start()

window.mainloop()
