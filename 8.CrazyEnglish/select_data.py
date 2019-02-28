from time import localtime,time
from random import randrange

class select_data:
	value=0
	def __init__(self):
		self.value=self.__check_config()
	
	def __check_config(self):
		t=localtime(time())
		t=str(t.tm_mday)+str(t.tm_mon)+str(t.tm_year)
		s=self.value
		try:
			f=open('./data/config','r')
		except Exception:
			print 'Have no config file'
			s+=1
		else:
			date=f.readline().split(';')
			select=f.readline().split(';')
			f.close()
			if date[0]==t:
				s=select[0]
			else:
				s=int(select[0])+1
				if s>21: s=1
		self.__write_config(t,s)
		return s
			
	def __write_config(self,t,s):
		f=open('./data/config','w')
		f.write(t+';\n'+str(s)+';')
		f.close()
