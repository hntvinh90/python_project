import pygame
import random
import time
from myLibs import isThread
from __image import ImageString

class Game:
    def __init__(self, screen, X, Y, SIZE_IN_PIXEL):
        self.screen = screen
        self.X = X
        self.Y = Y
        self.SIZE_IN_PIXEL = SIZE_IN_PIXEL
        self.SIZE_OF_IMAGE = (self.SIZE_IN_PIXEL, self.SIZE_IN_PIXEL)
        self.SIZE_OF_SCORE = 72
        self.SIZE_OF_TEXT = 36
        self.FONT_NAME = 'New Courier'
        self.SCORE_FONT = pygame.font.SysFont(self.FONT_NAME, self.SIZE_OF_SCORE)
        self.TEXT_FONT = pygame.font.SysFont(self.FONT_NAME, self.SIZE_OF_TEXT)
        self.COLOR_OF_TEXT = (0, 0, 0)
        self.isRunning = False
        self.__loadGameImage()
        self.reset()

    def __loadGameImage(self):
        ''' game_images is a list, in which:
        0 : aqua ball
        1 : blue ball
        2 : brown ball
        3 : green ball
        4 : pink ball
        5 : red ball
        6 : yellow ball
        7 : background
        '''
        self.game_images = []
        self.game_images.append(pygame.image.fromstring(ImageString.img_aqua, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_blue, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_brown, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_green, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_pink, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_red, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_yellow, self.SIZE_OF_IMAGE, 'RGBA'))
        self.game_images.append(pygame.image.fromstring(ImageString.img_empty, self.SIZE_OF_IMAGE, 'RGBA'))

    def __generateMap(self):
        ''' game_map is a list, length of which is X*Y
        Each element is also a list with 4 element: 
            x coordinate, 
            y coordinate, 
            value of game_image (-1 means empty) and 
            a surface to blit to screen

        tree_map reveals relationship of a cell with around cells.
        Moi phan tu la mot list co 2 phan tu:
            0 index la list cac o ben canh luc bat dau
            1 index la list cac o ban canh hien tai
        '''
        self.game_map = []
        self.tree_map = []
        self.empty_map = []
        self.score = 0
        self.selectedCell = -1
        self.destroyedBalls = []
        for y in range(self.Y):
            for x in range(self.X):
                self.game_map.append([
                    x*self.SIZE_IN_PIXEL, (y+2)*self.SIZE_IN_PIXEL, -1,
                    pygame.Surface(self.SIZE_OF_IMAGE)
                ])
                self.game_map[-1][3].blit(self.game_images[7], (0, 0))
                temp = []
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if abs(i)!=abs(j) and x+i>=0 and x+i<self.X and y+j>=0 and y+j<self.Y:
                            temp.append((y+j)*self.X + x+i)
                self.tree_map.append([list(temp), list(temp)])
                self.empty_map.append(y*self.X + x)

    def __next(self):
        '''
        next_map co 3 phan tu tuong ung voi 3 ball tiep theo
        moi phan tu la mot list co 3 phan tu gom cell, color va size de hien thi truoc
        '''
        self.next_map = []
        temp = list(self.empty_map)
        if temp==[]:
            self.reset()
            return
        for _ in range(3):
            if temp != []:
                j = random.choice(temp)
                temp.remove(j)
                self.next_map.append([j, random.randrange(0, 7), 20])

    #@isThread
    def __showNext(self):
        #self.isRunning = True
        size = 20
        while size<self.SIZE_IN_PIXEL:
            for cell in self.next_map:
                cell[2] = size
                size += 10
            time.sleep(0.1)
        for cell in self.next_map:
            self.__addBall(cell[0], cell[1])
        for cell in self.next_map:
            self.__checkScore(cell[0])
        self.__next()
        #self.isRunning = False

    def __addBall(self, cell, color):
        while True:
            try:
                self.game_map[cell][2] = color
                self.game_map[cell][3].blit(self.game_images[7], (0, 0))
                self.game_map[cell][3].blit(self.game_images[self.game_map[cell][2]], (0, 0))
                break
            except: pass
        self.empty_map.remove(cell)
        for i in self.tree_map[cell][0]:
            self.tree_map[i][1].remove(cell)

    def __delBall(self, cell):
        while True:
            try:
                self.game_map[cell][2] = -1
                self.game_map[cell][3].blit(self.game_images[7], (0, 0))
                break
            except: pass
        self.empty_map.append(cell)
        for i in self.tree_map[cell][0]:
            self.tree_map[i][1].append(cell)

    def reset(self):
        self.__generateMap()
        self.__next()
        self.__showNext()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.selectedCell = -1
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.onClickDown()
        while True:
            try:
                for cell in self.game_map:
                    self.screen.blit(cell[3], (cell[0], cell[1]))
                for i in range(len(self.next_map)):
                    self.screen.blit(self.game_images[self.next_map[i][1]], (self.SIZE_IN_PIXEL*(i+3), self.SIZE_IN_PIXEL))
                    self.screen.blit(pygame.transform.scale(self.game_images[self.next_map[i][1]], (self.next_map[i][2], self.next_map[i][2])),
                        (self.game_map[self.next_map[i][0]][0]+(self.SIZE_IN_PIXEL-self.next_map[i][2])//2, self.game_map[self.next_map[i][0]][1]+(self.SIZE_IN_PIXEL-self.next_map[i][2])//2))
                self.screen.blit(self.SCORE_FONT.render(str(self.score).rjust(5, '0'), True, self.COLOR_OF_TEXT), (self.SIZE_IN_PIXEL*7, self.SIZE_IN_PIXEL))
                self.screen.blit(self.TEXT_FONT.render('Score', True, self.COLOR_OF_TEXT), (self.SIZE_IN_PIXEL*7, self.SIZE_IN_PIXEL//2))
                self.screen.blit(self.TEXT_FONT.render('Next', True, self.COLOR_OF_TEXT), (self.SIZE_IN_PIXEL, self.SIZE_IN_PIXEL//2))
                for cell in self.destroyedBalls:
                    self.screen.blit(cell[1], (self.game_map[cell[0]][0], self.game_map[cell[0]][1]))
                break
            except: pass
        return True

    def onClickDown(self):
        if self.isRunning:
            return
        x, y = pygame.mouse.get_pos()
        y -= self.SIZE_IN_PIXEL*2
        x //= self.SIZE_IN_PIXEL
        y //= self.SIZE_IN_PIXEL
        cell = y*self.X + x
        if cell>=0:
            if self.selectedCell == -1:
                if self.game_map[cell][2] != -1:
                    self.selectedCell = cell
                    self.jumpBall()
            else:
                if self.selectedCell==cell:
                    self.selectedCell = -1
                else:
                    if self.game_map[cell][2] == -1:
                        way = self.findWay(self.selectedCell, cell)
                        if way!=[]:
                            self.selectedCell = -1
                            self.moveBall(way)
                    else:
                        self.selectedCell = cell
                        self.jumpBall()
    
    @isThread
    def jumpBall(self):
        y = [0, -3, -5, -6, -5, -3]
        i = 0
        cell = self.selectedCell
        while self.selectedCell!=-1:
            try:
                if cell == self.selectedCell:
                    self.game_map[cell][3].blit(self.game_images[7], (0, 0))
                    self.game_map[cell][3].blit(self.game_images[self.game_map[cell][2]], (0, y[i%6]))
                    i += 1
                    time.sleep(0.1)
                else:
                    break
            except: pass
        while True:
            try:
                self.game_map[cell][3].blit(self.game_images[7], (0, 0))
                self.game_map[cell][3].blit(self.game_images[self.game_map[cell][2]], (0, 0))
                break
            except: pass

    @isThread
    def moveBall(self, way):
        self.isRunning = True
        for i in range(len(way)-1):
            self.__addBall(way[i+1], self.game_map[way[i]][2])
            self.__delBall(way[i])
            time.sleep(0.02)
        if not self.__checkScore(way[-1]):
            self.__modifyNext(way[-1])
            self.__showNext()
        self.isRunning = False

    def findWay(self, fromPos, toPos):
        way1 = [[fromPos]]
        way2 = [[toPos]]
        while True:
            temp1 = list(way1)
            way1 = []
            temp2 = list(way2)
            way2 = []
            for path in temp1:
                for node in self.tree_map[path[-1]][1]:
                    if node == toPos:
                        return path+[node]
                    else:
                        if node not in path:
                            way1.append(path+[node])
            for path in temp2:
                for node in self.tree_map[path[-1]][1]:
                    if node not in path:
                        way2.append(path+[node])
            if way1==[] or way2==[]:
                return []

    def __modifyNext(self, cell):
        j = -1
        temp = list(self.empty_map)
        for i in range(len(self.next_map)):
            if cell == self.next_map[i][0]:
                j = i
            else:
                temp.remove(self.next_map[i][0])
        if j!=-1:
            self.next_map[j][0] = random.choice(temp)

    def __checkScore(self, cell):
        if self.game_map[cell][2] != -1:
            x = cell % self.X
            y = cell // self.X
            lines = []
            temp = []
            i = 1
            while True:
                if y-i>=0:
                    k = (y-i)*self.X + x
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            i = 1
            while True:
                if y+i<self.Y:
                    k = (y+i)*self.X + x
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            if len(temp)>3:
                lines.extend(temp)
            temp = []
            i = 1
            while True:
                if x-i>=0:
                    k = y*self.X + x-i
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            i = 1
            while True:
                if x+i <self.X:
                    k = y*self.X + x+i
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            if len(temp)>3:
                lines.extend(temp)
            temp = []
            i = 1
            while True:
                if x-i>=0 and y-i>=0:
                    k = (y-i)*self.X + x-i
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            i = 1
            while True:
                if x+i <self.X and y+i<self.Y:
                    k = (y+i)*self.X + x+i
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            if len(temp)>3:
                lines.extend(temp)
            temp = []
            i = 1
            while True:
                if x-i>=0 and y+i<self.Y:
                    k = (y+i)*self.X + x-i
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            i = 1
            while True:
                if x+i <self.X and y-i>=0:
                    k = (y-i)*self.X + x+i
                    if self.game_map[cell][2]==self.game_map[k][2]:
                        temp.append(k)
                    else:
                        break
                else:
                    break
                i += 1
            if len(temp)>3:
                lines.extend(temp)
            if lines!=[]:
                lines.append(cell)
                self.__destroyBalls(lines)
                self.score += 5 + (len(lines)+1)*len(lines)//2
                for i in lines:
                    self.__delBall(i)
                return True
            else:
                return False

    def __destroyBalls(self, cells):
        size = self.SIZE_IN_PIXEL
        while size>0:
            try:
                for cell in cells:
                    surf = pygame.Surface(self.SIZE_OF_IMAGE)
                    surf.blit(self.game_images[7], (0, 0))
                    surf.blit(pygame.transform.scale(self.game_images[self.game_map[cell][2]], (size, size)), ((self.SIZE_IN_PIXEL-size)//2, (self.SIZE_IN_PIXEL-size)//2))
                    self.destroyedBalls.append([cell, surf])
            except: pass
            size -= 10
            time.sleep(0.1)
            self.destroyedBalls = []