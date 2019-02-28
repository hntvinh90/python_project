#!/usr/bin/python
import pygame
from random import random
from math import sin,cos,pi
from time import sleep

pygame.init()

BLACK = (0, 0, 0)
size = (700, 300)
screen = pygame.display.set_mode(size)
screen.fill((255,255,255))
pygame.display.set_caption('My Game')

clock = pygame.time.Clock()

img = pygame.image.load('ball.png').convert_alpha()
pos = img.get_rect().move(50,50)
bgimg = pygame.image.load('bgball1.png').convert_alpha()
x = random()
y = random()
#a = random()+random()
#l = 5
#x = 50
#y = 50
#screen.fill(BLACK)

while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT: pygame.quit(); exit()
	#screen.fill(BLACK)
	
	#pygame.draw.ellipse(screen, (255,255,255), [x,y,25,25])
	#if x>=700-25 or x<=0: 
	#	a=1-a
	#if y>=500-25 or y<=0: 
	#	a=-a
	#x+=l*cos(a*pi)
	#y-=l*sin(a*pi)
	#if x<=0: x=0
	#elif x>=700-25: x=700-25
	#if y<=0: y=0
	#elif y>=500-25: y=500-25
	screen.blit(bgimg,pos)
	pos = pos.move(5*x,5*y)
	if pos.left<0 or pos.right>700: 
		x=-x
		pos = pos.move(5*x,5*y)
	if pos.top<0 or pos.bottom>300:
		y=-y
		pos = pos.move(5*x,5*y)
	screen.blit(img,pos)

	pygame.display.flip()
	#pygame.display.update()
	clock.tick(30) #So khung hinh tren giay
	#sleep(0.1)

pygame.quit()
