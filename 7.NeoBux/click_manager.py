from time import sleep,time
from pyautogui import locateCenterOnScreen,FAILSAFE,moveTo,click,hotkey,scroll,position,typewrite

class click_manager:

	def __init__(self,status):
	
		self.status=status
		self.exitproc=False
		self.__check_ad()
		
	
	def __check_ad(self):
		FAILSAFE=False
		while not self.exitproc:
			self.status.put('Checking Ad')
			try:
				pos=locateCenterOnScreen('data/signal.png')
			except Exception:
				self.status.put('Err in __check_ad 18')
				print 'Err in __check_ad 18'
			else:
				if pos==None:
					self.__check_login()
				else: self.status.put('Have no Ad')
			sleep(10)
							
		
		
	def __check_login(self):
		self.status.put('Checking login')
		try:
			pos=locateCenterOnScreen('data/notlogin.png')
		except Exception:
			self.status.put('Err in __check_login 33')
			print 'Err in __check_login 33'
		else:
			if pos==None:
				self.__click_ad()
			else:
				click(pos[0],pos[1])
				sleep(1)
				self.__login()
		
		
	def __login(self):
		try:
			pos=locateCenterOnScreen('data/login.png')
		except Exception:
			self.status.put('Err in __login 48')
			print 'Err in __login 48'
		else:
			if pos==None:
				print 'Err in __login 52'
			else:
				click(pos[0],pos[1])
				sleep(1)
				pos=locateCenterOnScreen('data/send.png')
				while pos==None:
					self.status.put('Waiting login page')
					pos=locateCenterOnScreen('data/send.png')
					sleep(0.1)
				sleep(1)
				typewrite('hntvinh1990')
				hotkey('tab')
				typewrite('tinhhuynh')
				hotkey('enter')
				sleep(1)
				pos=locateCenterOnScreen('data/name.png')
				while pos==None:
					self.status.put('Logining ...')
					pos=locateCenterOnScreen('data/name.png')
					sleep(0.1)
				pos=locateCenterOnScreen('data/view.png')
				while pos==None:
					self.status.put('Find View Ad')
					pos=locateCenterOnScreen('data/view.png')
					sleep(0.1)
				click(pos[0],pos[1])
				sleep(20)
		
		
	def __click_ad(self):
		self.status.put('Click Ad')
		pos0=locateCenterOnScreen('data/refresh.png')
		if pos0==None:
			self.status.put('Not found refresh')
		else:
			try:
				moveTo(pos0[0],pos0[1]+100)
			except Exception:
				self.status.put('Old err')
				self.exitproc=True
				return
			pos0=position()
			scroll(100,pos0[0],pos0[1])
			sleep(1)
			pos=locateCenterOnScreen('data/view.png')
			if pos==None:
				self.status.put('Website not run')
				return
			pos=locateCenterOnScreen('data/view.png')
			while pos==None:
				self.status.put('Find View Ad')
				pos=locateCenterOnScreen('data/view.png')
				sleep(0.1)
			click(pos[0],pos[1])
			sleep(1)
			pos=locateCenterOnScreen('data/config_refresh.png')
			while pos==None:
				self.status.put('Wait refresh')
				pos=locateCenterOnScreen('data/config_refresh.png')
				sleep(0.1)
			sleep(1)
			
			num=0
			while True:
				moveTo(pos0[0],pos0[1])
				pos=locateCenterOnScreen('data/star.png')
				if pos==None:
					self.status.put('Not found star')
					if num<5:
						num+=1
						scroll(-5,pos0[0],pos0[1])
						sleep(1)
					else: break
				else:
					click(pos[0],pos[1])
					sleep(1)
					pos=locateCenterOnScreen('data/dot.png')
					if pos==None:
						self.status.put('Not found dot')
						sleep(1)
					else:
						click(pos[0],pos[1])
						moveTo(pos0[0],pos0[1])
						sleep(5)
						hotkey('esc')
						ct=time()
						while True:
							pos=locateCenterOnScreen('data/ok.png')
							if pos==None:
								self.status.put('Waiting close')
								pos=locateCenterOnScreen('data/expired.png')
								if pos!=None:
									self.status.put('Expired')
									hotkey('ctrl','w')
									hotkey('enter')
									moveTo(pos0[0],pos0[1])
									sleep(1)
									break
								else: sleep(0.1)
							else:
								hotkey('ctrl','w')
								hotkey('enter')
								moveTo(pos0[0],pos0[1])
								sleep(1)
								break
							if time()-ct>180:
								hotkey('ctrl','w')
								hotkey('enter')
								self.status.put('Error when watch Ad')
								sleep(1)
								break
							pos=locateCenterOnScreen('data/err.png')
							if pos!=None:
								self.status.put('Error loading')
								hotkey('f5')
								hotkey('enter')
								sleep(5)
								ct=time()
			
			while True:
				moveTo(pos0[0],pos0[1])
				pos=locateCenterOnScreen('data/adprize.png')
				if pos==None:
					self.status.put('Not found adprize')
					if num>0:
						num-=1
						scroll(5,pos0[0],pos0[1])
						sleep(1)
					else: break
				else:
					click(pos[0],pos[1]+40)
					moveTo(pos0[0],pos0[1])
					sleep(5)
					hotkey('esc')
					ct=time()
					while True:
						pos=locateCenterOnScreen('data/ok.png')
						if pos==None:
							self.status.put('Waiting close')
							pos=locateCenterOnScreen('data/expired.png')
							if pos!=None:
								self.status.put('Expired')
								hotkey('ctrl','w')
								hotkey('enter')
								moveTo(pos0[0],pos0[1])
								sleep(1)
								break
							else: sleep(0.1)
						else:
							pos=locateCenterOnScreen('data/next.png')
							if pos==None:
								hotkey('ctrl','w')
								hotkey('enter')
								moveTo(pos0[0],pos0[1])
								sleep(1)
								break
							else:
								ct=time()
								click(pos[0],pos[1])
								hotkey('enter')
								moveTo(pos0[0],pos0[1])
								sleep(5)
								hotkey('esc')
						if time()-ct>180:
							hotkey('ctrl','w')
							hotkey('enter')
							self.status.put('Error when watch Ad')
							sleep(1)
							break
						pos=locateCenterOnScreen('data/err.png')
						if pos!=None:
							self.status.put('Error loading')
							hotkey('f5')
							hotkey('enter')
							sleep(5)
							ct=time()
		
		
