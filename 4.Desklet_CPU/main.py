#!/usr/bin/python
from tkinter import Tk,Button,Canvas,Frame
from threading import Thread
from mylib import cpu
from time import sleep

core_number=cpu().core_number
main_width=200
main_height=130+core_number*50

MainGUI=Tk()
MainGUI.overrideredirect(True)
MainGUI.geometry(str(main_width)+'x'+str(main_height)+'+'+str(MainGUI.winfo_screenwidth()-main_width)+'+50')
MainGUI.resizable(False,False)
def event(e):
    print(e.type,e.widget,e.x,e.y,e.x_root,e.y_root)
def show_close_button(e):
    if e.widget==MainGUI:
        close_button.lift()
        close_button.place(x=main_width-15,y=0,height=15,width=15)
        MainGUI.update()
def hide_close_button(e):
    if e.widget==MainGUI:
        close_button.place(x=main_width-15,y=-15,height=15,width=15)
        MainGUI.update()
global begin_x,begin_y
def get_begin_position(e):
    if e.widget==cpu_canvas:
        global begin_x,begin_y
        begin_x=e.x_root
        begin_y=e.y_root
def move_MainGUI(e):
    if e.widget==cpu_canvas:
        global begin_x,begin_y
        step=50
        x=e.x_root
        y=e.y_root
        delta_x=(x-begin_x)
        bias_x=abs(delta_x)
        delta_y=(y-begin_y)
        bias_y=abs(delta_y)
        if bias_x>step:
            direct_x=delta_x/bias_x
            MainGUI.geometry(str(main_width)+'x'+str(main_height)+'+'+str(MainGUI.winfo_x()+step*direct_x)+'+'+str(MainGUI.winfo_y()))
            MainGUI.update()
            begin_x+=step*direct_x
        if bias_y>step:
            direct_y=delta_y/bias_y
            MainGUI.geometry(str(main_width)+'x'+str(main_height)+'+'+str(MainGUI.winfo_x())+'+'+str(MainGUI.winfo_y()+step*direct_y))
            MainGUI.update()
            begin_y+=step*direct_y
MainGUI.bind('<Button-1>',get_begin_position)
MainGUI.bind('<B1-Motion>',move_MainGUI)
MainGUI.bind('<Enter>',show_close_button)
MainGUI.bind('<Leave>',hide_close_button)

close_button=Button(MainGUI,text="X",command=exit)
close_button.place(x=main_width-15,y=0,height=15,width=15)
def exit():
    MainGUI.destroy()

cpu_coor=[]
for i in range(core_number+1): 
    if i==0: cpu_coor.append([0,100])
    else: cpu_coor.append([])
cpu_canvas=Canvas(MainGUI,bg='white')
cpu_canvas.place(x=0,y=0,width=main_width,height=main_height)
cpu_canvas.create_text(15,0,text='100',anchor='ne',fill='gray',font=('','6'))
cpu_canvas.create_text(15,50,text='50',anchor='e',fill='gray',font=('','6'))
cpu_canvas.create_text(15,100,text='0',anchor='se',fill='gray',font=('','6'))
cpu_canvas.create_text(100,115,text='CPU:        %',anchor='center')
for i in range(1,len(cpu_coor)):
    cpu_canvas.create_text(5,105+50*i,text='Core '+str(i),anchor='w',fill='gray')
    cpu_coor[i].append(cpu_canvas.create_rectangle(0,0,0,0))
    cpu_coor[i].append(cpu_canvas.create_text(120,105+50*i,text='',font=('','6'),fill='gray'))
    cpu_canvas.create_rectangle(50,95+50*i,190,115+50*i)
for i in range(25,200):
    if i%5==0: 
        cpu_canvas.create_line(i,50,i+1,50,fill='gray')
        cpu_canvas.create_line(i,1,i+1,1,fill='gray')
        cpu_canvas.create_line(i,100,i+1,100,fill='gray')
cpu_line=cpu_canvas.create_line(0,0,0,0,smooth=True,fill='blue',width=2)
cpu_percent_text=cpu_canvas.create_text(110,115,text='',anchor='center')
config='I am master'
class update_graph(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        try:
            data=cpu().percent
            if len(data)==2 and data[0]==0 and data[1]==0: print('error when get cpu percent');sleep(0.5)
            else:
                if len(cpu_coor[0])>=68: 
                    del(cpu_coor[0][0])
                    del(cpu_coor[0][1])
                cpu_coor[0].append(0)
                cpu_coor[0].append(100-data[0])
                for i in range(len(cpu_coor[0])):
                    if i%2==0: cpu_coor[0][i]=25+i/2*5
                cpu_canvas.coords(cpu_line,tuple(cpu_coor[0]))
                cpu_canvas.itemconfigure(cpu_percent_text,text=data[0])
                for i in range(1,len(data)):
                    if data[i]<11: color='#33ff00'
                    elif data[i]<21: color='#66ff00'
                    elif data[i]<31:color='#99ff00'
                    elif data[i]<41: color='#ccff00'
                    elif data[i]<51: color='#ffff00'
                    elif data[i]<61: color='#ffcc00'
                    elif data[i]<71: color='#ff9900'
                    elif data[i]<81: color='#ff6600'
                    elif data[i]<91: color='#ff3300'
                    else: color='#ff0000'
                    cpu_canvas.itemconfigure(cpu_coor[i][0],outline=color,fill=color)
                    cpu_canvas.itemconfigure(cpu_coor[i][1],text=data[i])
                    cpu_canvas.coords(cpu_coor[i][0],50,95+50*i,50+1.4*data[i],115+50*i)
        except Exception: 
            print('raise a error',config)
            return 0
        self.run()
update_graph().start()

MainGUI.mainloop()
