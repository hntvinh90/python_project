import pygame
import random
import time
from __images import Images
from __setting import Setting
from myLibs import isThread

class Cell():#pygame.sprite.Sprite):
    def __init__(self, index):
        #pygame.sprite.Sprite.__init__(self)
        print('start', index)
        self.x = index % Setting.X_CELLS_NUMBER
        self.y = index // Setting.X_CELLS_NUMBER
        self.ball = 0
        self.image = pygame.Surface((Setting.PIXEL_OF_X, Setting.PIXEL_OF_Y))
        self.image.blit(Images.img_balls[self.ball], (0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x * Setting.PIXEL_OF_X
        self.rect.y = self.y * Setting.PIXEL_OF_Y + Setting.HEIGHT_FOR_INFO
        print('tinh bf')
        #self.getNeighbours()
        self.neighbours = Setting.NEIGHBOURS[index]
        #self.getLines()
        self.lines = Setting.LINES[index][0]
        print('tih at')
        self.jumping = False
        print(index, 'end\n')

    def getNeighbours(self):
        self.neighbours = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                print(i,j)
                if (abs(i)!=abs(j) and self.x+i>=0 and self.x+i<Setting.X_CELLS_NUMBER and
                    self.y+j>=0 and self.y+j<Setting.Y_CELLS_NUMBER
                ):
                    self.neighbours.append((self.y+j)*Setting.X_CELLS_NUMBER + self.x+i)
                    print((self.y+j)*Setting.X_CELLS_NUMBER + self.x+i)

    def getLines(self):
        # list 0 is horizontal line
        # list 1 is vertical line
        # list 2 is left-top right-bottom line
        # list 3 is left-bottom right-top line
        self.lines = [
            self.getHorizontalLine(), 
            self.getVerticalLine(),
            self.getLTRBLine(),
            self.getLBRTLine()
        ]
    
    def getHorizontalLine(self):
        # chứa các ô cùng hàng ngang
        # list 0 là các ô cùng hàng bên trái
        # list 1 là các ô cùng hảng bên phải
        horizontal_line = [[], []]
        i = 1
        while True:
            x1 = self.x - i
            x2 = self.x + i
            if x1 < 0:
                if x2 < Setting.X_CELLS_NUMBER:
                    horizontal_line[1].append(self.y*Setting.X_CELLS_NUMBER + x2)
                else:
                    break
            else:
                horizontal_line[0].append(self.y*Setting.X_CELLS_NUMBER + x1)
                if x2 < Setting.X_CELLS_NUMBER:
                    horizontal_line[1].append(self.y*Setting.X_CELLS_NUMBER + x2)
            i += 1
        return horizontal_line

    def getVerticalLine(self):
        # chứa các ô cùng hảng dọc
        # list 0 la các ô cùng hàng phía trên
        # list 1 là các ô cùng hàng phía dưới
        vertical_line = [[], []]
        i = 1
        while True:
            y1 = self.y - i
            y2 = self.y + i
            if y1 < 0:
                if y2 < Setting.Y_CELLS_NUMBER:
                    vertical_line[1].append(y2*Setting.X_CELLS_NUMBER + self.x)
                else:
                    break
            else:
                vertical_line[0].append(y1*Setting.X_CELLS_NUMBER + self.x)
                if y2 < Setting.Y_CELLS_NUMBER:
                    vertical_line[1].append(y2*Setting.X_CELLS_NUMBER + self.x)
            i += 1
        return vertical_line

    def getLTRBLine(self):
        # left-top right-bottom line
        # list 0 là các ô bên trái
        # list 1 là các ô bên phải
        lt_rb_line = [[], []]
        i = 1
        while True:
            x1 = self.x - i
            y1 = self.y - i
            x2 = self.x + i
            y2 = self.y + i
            if x1 >= 0 and y1 >= 0:
                lt_rb_line[0].append(y1*Setting.X_CELLS_NUMBER + x1)
                if x2 < Setting.X_CELLS_NUMBER and y2 < Setting.Y_CELLS_NUMBER:
                    lt_rb_line[1].append(y2*Setting.X_CELLS_NUMBER + x2)
            else:
                if x2 < Setting.X_CELLS_NUMBER and y2 < Setting.Y_CELLS_NUMBER:
                    lt_rb_line[1].append(y2*Setting.X_CELLS_NUMBER + x2)
                else:
                    break
            i += 1
        return lt_rb_line

    def getLBRTLine(self):
        # left-bottom right-top line
        # list 0 là các ô bên trái
        # list 1 là các ô bên phải
        lb_rt_line = [[], []]
        i = 1
        while True:
            x1 = self.x - i
            y1 = self.y + i
            x2 = self.x + i
            y2 = self.y - i
            if x1 >= 0 and y1 < Setting.Y_CELLS_NUMBER:
                lb_rt_line[0].append(y1*Setting.X_CELLS_NUMBER + x1)
                if x2 < Setting.X_CELLS_NUMBER and y2 >= 0:
                    lb_rt_line[1].append(y2*Setting.X_CELLS_NUMBER + x2)
            else:
                if x2 < Setting.X_CELLS_NUMBER and y2 >= 0:
                    lb_rt_line[1].append(y2*Setting.X_CELLS_NUMBER + x2)
                else:
                    break
            i += 1
        return lb_rt_line

    @isThread
    def addBall(self, color):
        self.ball = color
        while True:
            try:
                self.image.blit(Images.img_balls[0], (0, 0))
                self.image.blit(Images.img_balls[self.ball], (0, 0))
                break
            except: pass

    @isThread
    def removeBall(self):
        self.ball = 0
        while True:
            try:
                self.image.blit(Images.img_balls[self.ball], (0, 0))
                break
            except: pass

    @isThread
    def addNext(self, color):
        while True:
            try:
                self.image.blit(Images.img_balls[0], (0, 0))
                self.image.blit(pygame.transform.scale(Images.img_balls[color], (20, 20)), 
                    ((Setting.PIXEL_OF_X-20)//2, (Setting.PIXEL_OF_Y-20)//2)
                )
                break
            except: pass

    @isThread
    def startJumping(self):
        self.jumping = True
        height = [0, -3, -5, -6, -5, -3]
        i = 0
        while self.jumping:
            try:
                self.image.blit(Images.img_balls[0], (0, 0))
                self.image.blit(Images.img_balls[self.ball], (0, height[i%6]))
            except: pass
            i += 1
            time.sleep(0.1)
        while True:
            try:
                self.image.blit(Images.img_balls[0], (0, 0))
                self.image.blit(Images.img_balls[self.ball], (0, 0))
                break
            except: pass

    def stopJumping(self):
        self.jumping = False

class Text():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((Setting.SCREEN_WIDTH, 30))
        self.rect = self.image.get_rect()
        #self.drawText()

    def drawText(self):
        self.image.fill(Setting.BACKGROUND_COLOR)
        print('bf')
        font = pygame.font.SysFont(pygame.font.get_default_font(), Setting.SIZE_OF_TEXT)
        print('at')
        width = Setting.WIDTH_ASIDE
        text = font.render('Best Point', True, Setting.TEXT_COLOR)
        rect = text.get_rect()
        rect.x = (width-rect.width)//2
        rect.y = (self.rect.height-rect.height)//2
        self.image.blit(text, rect)
        text = font.render('Point', True, Setting.TEXT_COLOR)
        rect = text.get_rect()
        rect.x = self.rect.width - (width+rect.width)//2
        rect.y = (self.rect.height-rect.height)//2
        self.image.blit(text, rect)

class BestPoint():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.point = self.readFile()
        self.image = pygame.Surface((Setting.WIDTH_ASIDE, Setting.PIXEL_OF_Y))
        self.rect = self.image.get_rect()
        self.rect.y = 30
        self.update(self.point)

    def readFile(self):
        try:
            with open('data', 'rb') as f:
                return int(f.read().strip())
        except: 
            return 0

    def writeFile(self):
        with open('data', 'wb') as f:
            f.write(str(self.point).encode())

    @isThread
    def update(self, point):
        self.point = point
        self.writeFile()
        while True:
            try:
                self.image.fill(Setting.BACKGROUND_COLOR)
                text = pygame.font.SysFont(Setting.FONT_OF_TEXT, Setting.SIZE_OF_POINT).render(
                    str(point), True, Setting.TEXT_COLOR
                )
                rect = text.get_rect()
                rect.x = (self.rect.width-rect.width)//2
                rect.y = (self.rect.height-rect.height)//2
                self.image.blit(text, rect)
                break
            except: pass

class Point():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.point = 0
        self.image = pygame.Surface((Setting.WIDTH_ASIDE, Setting.PIXEL_OF_Y))
        self.rect = self.image.get_rect()
        self.rect.x = Setting.SCREEN_WIDTH - self.rect.width
        self.rect.y = 30
        self.addPoint(0)

    @isThread
    def addPoint(self, point):
        self.point += point
        while True:
            try:
                self.image.fill(Setting.BACKGROUND_COLOR)
                text = pygame.font.SysFont(Setting.FONT_OF_TEXT, Setting.SIZE_OF_POINT).render(
                    str(self.point), True, Setting.TEXT_COLOR
                )
                rect = text.get_rect()
                rect.x = (self.rect.width-rect.width)//2
                rect.y = (self.rect.height-rect.height)//2
                self.image.blit(text, rect)
                break
            except: pass

class NextBalls():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.next_images = []
        self.next_cells = []
        self.image = pygame.Surface((Setting.PIXEL_OF_X * 3, Setting.PIXEL_OF_Y))
        self.rect = self.image.get_rect()
        self.rect.x = Setting.WIDTH_ASIDE
        self.rect.y = 30
        self.image.fill(Setting.BACKGROUND_COLOR)

    #@isThread
    def update(self, scene):
        for i, cell in enumerate(self.next_cells):
            if scene.cells[cell].ball != 0:
                temp = list(scene.empty_cells)
                for c in self.next_cells:
                    try:
                        temp.remove(c)
                    except: pass
                cell = random.choice(temp)
            self.next_cells[i] = cell
        size = 20
        while size<Setting.PIXEL_OF_X:
            for i, cell in enumerate( self.next_cells):
                try:
                    scene.cells[cell].image.blit(Images.img_balls[0], (0, 0))
                    scene.cells[cell].image.blit(
                        pygame.transform.scale(Images.img_balls[self.next_images[i]], (size, size)),
                        ((Setting.PIXEL_OF_X-size)/2, (Setting.PIXEL_OF_Y-size)/2)
                    )
                except: pass
            size += 10
            time.sleep(0.1)
        for i, cell in enumerate(self.next_cells):
            self.next_cells = []
            scene.cells[cell].addBall(self.next_images[i])
            scene.empty_cells.remove(cell)
            scene.checkPoint(cell)
        self.next_images = []
        if not scene.empty_cells:
            scene.game_over = True
            return
        while True:
            try:
                self.image.fill(Setting.BACKGROUND_COLOR)
                break
            except: pass
        temp = list(scene.empty_cells)
        color = [i for i in range(1, 8)]
        while True:
            l = len(self.next_cells)
            if l==3 or temp==[]:
                break
            cell = random.choice(temp)
            temp.remove(cell)
            self.next_cells.append(cell)
            self.next_images.append(random.choice(color))
            while True:
                try:
                    self.image.blit(Images.img_balls[self.next_images[l]], (Setting.PIXEL_OF_X*l, 0))
                    break
                except: pass
            scene.cells[cell].addNext(self.next_images[l])

class Time():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((Setting.PIXEL_OF_X * 3, 30))
        self.rect = pygame.Rect((Setting.WIDTH_ASIDE, 0, Setting.PIXEL_OF_X * 3, 30))
        self.time = 0
        #self.font = pygame.font.SysFont(Setting.FONT_OF_TEXT, Setting.SIZE_OF_TEXT)
        self.isRunning = False
        self.image.fill(Setting.BACKGROUND_COLOR)

    @isThread
    def run(self):
        self.isRunning = True
        font = pygame.font.SysFont(Setting.FONT_OF_TEXT, Setting.SIZE_OF_TEXT)
        while self.isRunning:
            t = int(time.time()) - self.time
            text = ':'.join((str(t//3600).rjust(2, '0'), str(t%3600//60).rjust(2, '0'), str(t%3600%60).rjust(2, '0')))
            img = font.render(text, True, Setting.TEXT_COLOR)
            rect = img.get_rect()
            rect.x = (self.rect.width - rect.width)//2
            rect.y = (self.rect.height - rect.height)//2
            while True:
                try:
                    self.image.fill(Setting.BACKGROUND_COLOR)
                    self.image.blit(img, rect)
                    break
                except: pass
            time.sleep(0.5)
    
    def stop(self):
        self.isRunning = False

class Play_Btn():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.image = Images.img_playbtn
        rect = self.image.get_rect()
        x = (Setting.SCREEN_WIDTH-rect.width)//2
        y = (Setting.SCREEN_HEIGHT-rect.height)//2
        self.rect = pygame.Rect((x, y, rect.width, rect.height))

class HighScoreTable():#pygame.sprite.Sprite):
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((400, 600))
        self.title = pygame.font.SysFont(Setting.FONT_OF_TEXT, Setting.SIZE_OF_TEXT).render(
            'HIGHEST POINTS', True, (255, 255, 255)
        )
        rect = self.image.get_rect()
        x = (Setting.SCREEN_WIDTH-rect.width)//2
        y = (Setting.SCREEN_HEIGHT-rect.height)//2
        self.rect = pygame.Rect((x, y, rect.width, rect.height))
        self.update()

    def update(self):
        self.image.fill(Setting.TEXT_COLOR)
        rect = self.title.get_rect()
        self.image.blit(self.title, ((self.rect.width-rect.width)//2, 10))