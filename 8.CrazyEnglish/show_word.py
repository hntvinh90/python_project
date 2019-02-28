from Tkinter import Tk,PhotoImage,Canvas,Button,Entry
from time import time

def close_window(root,t):
	if time()-t<300: 
		root.after(5000,lambda: close_window(root,t))
	else:
		print 'miss'
		root.destroy()

def show_word(word):
	t=time()
	select=[0]
	root=Tk()
	root.title('CrazyEnglish')
	try:
		root.call('wm','iconphoto',root._w,PhotoImage(file='english.png'))
	except Exception:
		print 'Error loading icon'
	root.geometry(str(root.winfo_screenwidth())+'x'+str(root.winfo_screenheight())+'+0+0')#root.winfo_screenheight()
	root.resizable(False,False)
	root.protocol('WM_DELETE_WINDOW',lambda: exit(root,select))
	
	canvas=Canvas(root)#,bg='green')
	canvas.place(x=100,y=100,width=800,height=50)
	
	canvas.create_text(0,0,text=word[0],anchor='nw',font=('',14),fill='red')
	canvas.create_text(0,30,text='('+word[1]+')',anchor='nw')
	
	entry=Entry(root,font=('',10))
	entry.place(x=100,y=200,width=800,height=30)
	
	Button(root,text='OK',command=lambda: press_btn(root,entry,word[0])).place(x=100,y=250,height=30,width=80)
	
	root.after(0,lambda: close_window(root,t))
	
	entry.focus_force()
	
	root.mainloop()
	
	return select[0]

def press_btn(root,entry,word):
	if entry.get()==word:
		root.destroy()
	else: entry.delete(0,'end')

def exit(root,select):
	root.destroy()
	select[0]=-1
