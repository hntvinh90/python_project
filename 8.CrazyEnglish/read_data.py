from select_data import select_data

def read_data():
	data=[]
	try:
		f=open('./data/'+str(select_data().value),'r')
	except Exception:
		print 'Error read data file'
	else:
		r=f.readline()
		while r<>'':
			data.append(r.split(';'))
			r=f.readline()
		f.close()
	finally: return data
