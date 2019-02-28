#!/usr/bin/python
import pygame
import pygame.locals

pygame.init()

BLACK = (0, 255, 0)
size = (700, 500)
screen = pygame.display.set_mode(size)
screen.fill(BLACK)
pygame.display.set_caption('My Game')

clock = pygame.time.Clock()

#pygame.draw.circle(screen,(255,0,0),(200,200),100,2)
#pygame.draw.line(screen,(255,0,0),(200,200),(100,100),2)
#r = pygame.Rect(100,100,100,100)
##print screen.get_locked()
#pa = pygame.PixelArray(screen)
#print screen.get_locked()
#pa[101][100]=(255,0,0)
#pa[100][101]=(255,0,0)
#pa[100][102]=(255,0,0)
#pa[101][100]=(255,0,0)
#pa[101][101]=(255,0,0)
#pa[101][102]=(255,0,0)
#del pa
#print screen.get_locked()

re = pygame.Surface((100,100),3,(0,0,255))
#re.fill(BLACK)
pygame.draw.circle(re,(255,0,0),(50,50),50,2)
screen.blit(re, (100,100))
#for i in dir(pygame.locals): print i

print pygame.cdrom.get_init()
pygame.cdrom.init()
pygame.cdrom.CD(0)
print pygame.cdrom.get_init()

while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT: print 'before';pygame.quit();print 'after'; exit()
	#screen.fill(BLACK)

	#Write code here

	pygame.display.flip()
	clock.tick(60) #So khung hinh tren giay

