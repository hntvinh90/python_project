from threading import Thread

class save_data(Thread):
	def __init__(self,data,word,select):
		Thread.__init__(self)
		self.data=data
		self.word=word
		self.select=select
	def run(self):
		i=self.data.index(self.word)
		self.data[i][4]=str(self.select)
		f=open('data','w')
		for j in self.data:
			f.write(j[0]+';'+j[1]+';'+j[2]+';'+j[3]+';'+j[4]+';\n')
		f.close()
