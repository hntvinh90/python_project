#!/usr/bin/python

size_game=[40,20]
boom_number=[100]
exit=[0]
def e():
	global root,exit
	exit[0]=1
	root.destroy()

if __name__=='__main__':
	from Tkinter import Tk,Canvas,PhotoImage
	
	root=Tk()
	root.title('MineSweeper')
	root.geometry(str(size_game[0]*25)+'x'+str(size_game[1]*25+45))	
	root.resizable(False,False)
	root.protocol('WM_DELETE_WINDOW',e)
	#i=PhotoImage(file='data/ico.png')
	#root.call('wm','iconphoto',root._w,i)
	
	import main
	from header import header
	from  img import load_img
	flag_number=[boom_number[0]]
	game_status=['normal']
	img=load_img()
	
	root.call('wm','iconphoto',root._w,img['icon'])
	
	h=header()
	h.frame=[Canvas(root)]
	h.frame[0].place(x=0,y=10,height=25,relwidth=1.0)
	h.flag_number=flag_number
	h.img=img
	h.exit=exit
	h.status=game_status
	h.list_cell=main.list_cell
	h.size_game=size_game
	
	main.frame=[Canvas(root)]
	main.frame[0].place(x=0,y=45,height=size_game[1]*25,relwidth=1.0)
	main.flag_number=flag_number
	main.img=img
	main.game_status=game_status
	main.size_game=size_game
	main.boom_number=boom_number
	
	main.start()
	h.start()
	
	root.mainloop()
	
	game_status[0]='normal'
	h.join()
