from time import time

def check_time(before):
	if time()-before[0] > 600:
		before[0]=time()
		return True
	else:
		return False
