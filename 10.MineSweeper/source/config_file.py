#!/usr/bin/python

size_game=''

def read():
	global size_game
	try:
		f=open('config'+str(size_game[0]*size_game[1]),'r')
	except Exception:
		yield(9999)
	else:
		yield(int(f.readline()))
		f.close()
		del f
	
def write(max):
	global size_game
	f=open('config'+str(size_game[0]*size_game[1]),'w')
	f.write(str(max))
	f.close()

if __name__=='__main__':
	pass
