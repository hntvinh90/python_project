#!/usr/bin/python
from Tkinter import Tk, PhotoImage,Canvas,Label,IntVar
from time import sleep
from math import acos,degrees
from re import sub
from threading import Thread
from random import randrange

mainframe=Tk()
mainframe.title('LINE')
mainframe.geometry('490x544')
mainframe.call('wm','iconphoto',mainframe._w,PhotoImage(file='data/ico.png'))
mainframe.resizable(False,False)
def mainexit():
	global cv,cv_frame,viewer,select_ball
	del cv
	del cv_frame
	del viewer
	select_ball[0]=-1
	mainframe.destroy()
mainframe.protocol('WM_DELETE_WINDOW',mainexit)
cv_bg_color='#d5d5d5'
cv_frame=Canvas(mainframe)#,bg=cv_bg_color
cv_frame.place(x=0,y=0,relwidth=1.0,relheight=1.0)
point=0
point_max=0
point_canvas=cv_frame.create_text(81,27,font=('Purisa',24),text=point)
point_max_canvas=cv_frame.create_text(405,27,font=('Purisa',24),text=point_max)
viewer=Canvas(cv_frame)#,bg=cv_bg_color)
viewer.place(x=162,y=0,width=162,height=54)
cv=Canvas(cv_frame)#,bg=cv_bg_color)
cv.place(x=0,y=55,width=490,height=490)

width_board=9
height_board=9
map_board=[]
map_color=['red','green','blue','yellow','pink','aqua','white']
id_ball=0
select_ball=[-1,-1,-1]
empty=[]
for i in range(width_board*height_board): empty.append(i)
ball_future=[]

def draw_ball(master,name,x,y,idcolor,mapboard,size='big'):
	name='ball'+str(name)
	x0=54*x+28; y0=54*y+28
	R=20
	x1=x0+float(R)/2; y1=y0-float(R)/2*1.7321
	master.create_oval(x0-R,y0-R,x0+R,y0+R,outline='#555555',fill='#555555',tag=name)
	j=-1
	rate=25
	code=255
	for i in range(2*int(R)):
		r=2*R-i
		alpha=degrees(acos(float(r)/(2*R)))
		if (code+j*rate)<0: j=1;rate=9
		elif (code+j*rate)>255: j=-1
		code+=j*rate
		code_hex=sub('0x','',hex(code)).zfill(2)
		if idcolor=='red': color='#'+code_hex+'0000'
		elif idcolor=='green': color='#'+'00'+code_hex+'00'
		elif idcolor=='blue': color='#'+'0000'+code_hex
		elif idcolor=='yellow': color='#'+code_hex+code_hex+'00'
		elif idcolor=='pink': color='#'+code_hex+'00'+code_hex
		elif idcolor=='aqua': color='#'+'00'+code_hex+code_hex
		elif idcolor=='heavyred': color='#'+code_hex+'5555'
		else: color='#'+code_hex+code_hex+code_hex
		if size=='big': 
			master.tag_bind(master.create_arc(x1-r,y1-r,x1+r,y1+r,start=alpha-120,extent=-2*alpha,outline=color,tag=name),'<ButtonPress-1>',lambda e: event_ball(master,e,mapboard))
		elif size=='small': 
			master.tag_bind(master.create_arc(x1-r,y1-r,x1+r,y1+r,start=alpha-120,extent=-2*alpha,outline=color,tag=name),'<ButtonPress-1>',lambda e: event_board(master,e,map_board))
		else: master.create_arc(x1-r,y1-r,x1+r,y1+r,start=alpha-120,extent=-2*alpha,outline=color,tag=name)
	if size=='small': 
		master.scale(name,x0,y0,0.15,0.15)
		mapboard.append(name)
	elif size=='viewer':
		mapboard.append(name)
	else: 
		mapboard[x][y][0]=name
		mapboard[x][y][1]=idcolor

def event_ball(master,e,mapboard):
	if len(empty)>0:
		global select_ball
		x=e.x/54; y=e.y/54
		select_ball[1]=x
		select_ball[2]=y
		if select_ball[0]==mapboard[x][y][0]: select_ball[0]=-1
		else:
			select_ball[0]=mapboard[x][y][0]
			thread_jump_ball(master).start()
	else: print('Game Over!')

class thread_jump_ball(Thread):
	def __init__(self,master):
		global select_ball
		Thread.__init__(self)
		self.master=master
		self.select=select_ball[0]
	def run(self):
		v0=5;k=5;g=10;t=0.05;v=v0
		while self.select==select_ball[0]:
			y=k*(v*t-g*t*t/float(2))
			self.master.move(self.select,0,-y)
			v=v-g*t
			if v<=(-v0): v=v0
			sleep(t)
			if not select_ball: break
		y=0
		while v>(-v0):
			y=y+k*(v*t-g*t*t/2)
			v=v-g*t
			if not select_ball: break
		try: self.master.move(self.select,0,-y)
		except Exception: print('Thread out')

class thread_change_size_ball(Thread):
	def __init__(self,master,item,x,y,direct='show'):
		#global map_board
		Thread.__init__(self)
		self.master=master
		self.item=item
		self.x=28+54*x; self.y=28+54*y
		self.direct=direct
	def run(self):
		if self.direct=='show':
			self.master.scale(self.item,self.x,self.y,0.15,0.15)
			a=float(6); b=float(10)
			while b<=40:
				self.master.scale(self.item,self.x,self.y,b/a,b/a)
				a+=4;b+=4
				sleep(0.05)
			#get_point(self.x,self.y,map_board)
		elif self.direct=='delete':
			a=float(40); b=float(44); i=1
			while b>=6:
				if b>50: i=-1;a,b=b,a
				self.master.scale(self.item,self.x,self.y,b/a,b/a)
				a+=4*i;b+=4*i
				sleep(0.05)
			self.master.delete(self.item)
		else: print('Error in thread_change_size_ball')

def move_ball(master,idball,x0,y0,x1,y1,mapboard,em):
	select_ball[0]=-1
	master.move(idball,54*(x1-x0),54*(y1-y0))
	em.append(9*x0+y0)
	em.remove(9*x1+y1)
	mapboard[x1][y1][0]=mapboard[x0][y0][0]
	mapboard[x1][y1][1]=mapboard[x0][y0][1]
	mapboard[x0][y0][0]=-1
	mapboard[x0][y0][1]=''
	#get_point(x1,y1,mapboard)

def draw_board(master,x,y,color,mapboard):
	for i in range(x):
		mapboard.append([])
		for j in range(y):
			mapboard[i].append([])
			mapboard[i][j].append(-1) #id_ball
			mapboard[i][j].append('') #color
			mapboard[i][j].append([]) #map
			if i-1>=0: mapboard[i][j][2].append([i-1,j])
			if i+1<x: mapboard[i][j][2].append([i+1,j])
			if j-1>=0: mapboard[i][j][2].append([i,j-1])
			if j+1<y: mapboard[i][j][2].append([i,j+1])
			master.tag_bind(master.create_rectangle(1+i*54,1+j*54,54+i*54,54+j*54,fill=color,outline=color),'<ButtonPress-1>',lambda e: event_board(master,e,mapboard))
	for i in range(x+1):
		a=1+54*i
		master.create_line(a,1,a,54*y,fill='#888888',width=2)
		if i!=x:
			b=3+54*i
			for j in range(y):
				c=2+54*j
				master.create_line(b,c,b,c+52,fill='#ffffff',width=2)
	for i in range(y+1):
		a=1+54*i
		master.create_line(1,a,54*x,a,fill='#888888',width=2)
		if i!=0:
			b=-1+54*i
			for j in range(x):
				c=3+54*j
				master.create_line(c,b,c+51,b,fill='#ffffff',width=2)

def event_board(master,e,mapboard):
	x=e.x/54; y=e.y/54
	if mapboard[x][y][0]!=-1: print('Have a ball')
	else:
		if select_ball[0]!=-1:
			if find_way(select_ball[1],select_ball[2],x,y,mapboard):
				move_ball(master,select_ball[0],select_ball[1],select_ball[2],x,y,mapboard,empty)
				if not get_point(x,y,mapboard): show_future(empty)
			else: print('No way\a')
			if len(empty)==0:
				print('Game Over!')
				write_config()
				init_game()

def write_config():
	global point_max
	try: f=open('.config','w')
	except Exception: 
		print('Error open file')
	else:
		f.write(str(point_max))
		f.close()

def find_way(x0,y0,x1,y1,mapboard):
	parent=[[x0,y0]]
	temp=[]
	for i in mapboard[x0][y0][2]:
		temp.append(i)
	while len(temp)!=0 and [x1,y1] not in parent:
		x=temp[0][0]; y=temp[0][1]
		if mapboard[x][y][0]==-1 and [x,y] not in parent:
			parent.append([x,y])
			for i in mapboard[x][y][2]:
				if i not in temp: temp.append(i)
		del temp[0]
	if [x1,y1] in parent: return True
	else: return False

#draw_board(cv,width_board,height_board,cv_bg_color,map_board)
#print find_way(0,0,8,8,map_board)

def where_future(em,ballfuture):
	global id_ball
	if len(ballfuture)!=0:
		while len(ballfuture)>0:
			viewer.delete(ballfuture[0][3])
			del ballfuture[0]
	a=[]
	b=[]
	c=[]
	d=[]
	for i in range(3):
		if i<len(em):
			n=randrange(len(em))
			while em[n] in a: n=randrange(len(em)); print('lai')
			a.append(em[n])
			b.append(map_color[randrange(len(map_color))])
		else: break
	for i in range(len(a)):
		x=a[i]/9
		y=a[i]%9
		draw_ball(cv,id_ball,x,y,b[i],c,'small')											
		id_ball+=1
		draw_ball(viewer,id_ball,i,0,b[i],d,'viewer')
		id_ball+=1
		ballfuture.append([a[i],b[i],c[i],d[i]])

def show_future(em):
	global id_ball,map_board,ball_future
	a=[]
	b=[]
	for i in range(len(ball_future)):
		a.append(ball_future[i][0])
		b.append(ball_future[i][1])
		cv.delete(ball_future[i][2])
	for i in range(len(a)):
		if a[i] not in em:
			a[i]=-1
			n=randrange(len(em))
			while em[n] in a: n=randrange(len(em))
			a[i]=em[n]
		em.remove(a[i])
		x=a[i]/9
		y=a[i]%9
		draw_ball(cv,id_ball,x,y,b[i],map_board)
		id_ball+=1
		thread_change_size_ball(cv,map_board[x][y][0],x,y,'show').start()
		get_point(x,y,map_board)
	where_future(em,ball_future)

def get_point(x,y,mapboard):
	#print mapboard
	if mapboard[x][y][0]!=-1:
		global point,point_max,point_canvas,point_max_canvas,empty
		ls=[]
		total=[]
		ls.append([[x,y]])
		x1=x-1
		while x1>=0 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x1][y][1]: ls[len(ls)-1].append([x1,y]);x1=x1-1
		x1=x+1
		while x1<9 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x1][y][1]: ls[len(ls)-1].append([x1,y]);x1=x1+1
		ls.append([[x,y]])
		y1=y-1
		while y1>=0 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x][y1][1]: ls[len(ls)-1].append([x,y1]);y1=y1-1
		y1=y+1
		while y1<9 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x][y1][1]: ls[len(ls)-1].append([x,y1]);y1=y1+1
		ls.append([[x,y]])
		x1=x-1
		y1=y-1
		while x1>=0 and y1>=0 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x1][y1][1]: ls[len(ls)-1].append([x1,y1]);x1=x1-1;y1=y1-1
		x1=x+1
		y1=y+1
		while x1<9 and y1<9 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x1][y1][1]: ls[len(ls)-1].append([x1,y1]);x1=x1+1;y1=y1+1
		ls.append([[x,y]])
		x1=x-1
		y1=y+1
		while x1>=0 and y1<9 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x1][y1][1]: ls[len(ls)-1].append([x1,y1]);x1=x1-1;y1=y1+1
		x1=x+1
		y1=y-1
		while x1<9 and y1>=0 and mapboard[x][y][1]!=-1 and mapboard[x][y][1]==mapboard[x1][y1][1]: ls[len(ls)-1].append([x1,y1]);x1=x1+1;y1=y1-1
		for i in ls:
			if len(i)>=5:
				for j in i:
					if j not in total: total.append(j)
		#print ls,'\n',total
		if len(total)!=0:
			for i in total:
				thread_change_size_ball(cv,mapboard[i[0]][i[1]][0],i[0],i[1],'delete').start()
				empty.append(9*i[0]+i[1])
				mapboard[i[0]][i[1]][0]=-1
				mapboard[i[0]][i[1]][1]=''
			point+=(5+(len(total)-5)*(len(total)-4)/2)
			cv_frame.itemconfigure(point_canvas,text=point)
			if point_max<point:
				point_max=point
				cv_frame.itemconfigure(point_max_canvas,text=point_max)
				write_config()
			return True
		else: return False
	else: return False

def init_game():
	global point_max,point,id_ball,ball_future,empty,map_board,cv
	empty=[]
	for i in range(81): empty.append(i)
	draw_board(cv,width_board,height_board,cv_bg_color,map_board)
	try: f=open('.config','r')
	except Exception: 
		print('Error open file')
	else: 
		point_max=int(sub('\n','',f.readline()))
		cv_frame.itemconfigure(point_max_canvas,text=point_max)
		f.close()
	for i in range(9):
		for j in range(9):
			cv.delete(map_board[i][j][0])
			map_board[i][j][0]=-1
			map_board[i][j][1]=''
	where_future(empty,ball_future)
	show_future(empty)

init_game()

mainframe.mainloop()
