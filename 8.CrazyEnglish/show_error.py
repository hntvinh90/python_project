from Tkinter import Tk,Label,Button,PhotoImage

def show_error(err):
	root=Tk()
	root.title('Error')
	try:
		root.call('wm','iconphoto',root._w,PhotoImage(file='ico.png'))
	except Exception:
		print 'Error loading icon'
	root.geometry('200x100+100+100')
	root.overrideredirect(True)
	
	Label(root,text=err).place(x=0,y=0,height=50,relwidth=1.0)
	
	Button(root,text='Ok',command=lambda: exit(root)).place(x=60,y=60,height=30,width=80)
	
	root.mainloop()
	
def exit(root):
	root.destroy()
