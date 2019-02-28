import pygame
import os
import time
from __images import Images
from __setting import Setting
from __events import Events
from __sprites import Cell, Text, BestPoint, Point, NextBalls, Time, Play_Btn, HighScoreTable
from myLibs import isThread

class PlayingScene:
    def __init__(self, parent):
        self.parent = parent
        self.loadData()
        #self.reset()
        #self.run()

    def loadData(self):
        self.game_over = True
        self.isRunning = False #ignore events if it is True
        #self.all_gameobjs = pygame.sprite.Group()
        self.all_gameobjs = []
        self.cells = []
        self.text = Text()
        self.bestpoint = BestPoint() #update(point)
        self.point = Point() #addPoint(point)
        self.next_balls = NextBalls() #update(scene)
        self.time = Time()
        '''
        self.all_gameobjs.add(self.text)
        self.all_gameobjs.add(self.point)
        self.all_gameobjs.add(self.bestpoint)
        self.all_gameobjs.add(self.next_balls)
        self.all_gameobjs.add(self.time)
        '''
        self.all_gameobjs.extend([self.text, self.point, self.bestpoint, self.next_balls, self.time])
        for i in range(Setting.NUMBER_OF_CELLS):
            cell = Cell(i)
            self.cells.append(cell)
            #self.all_gameobjs.addcell(cell)
            self.all_gameobjs.append(cell)
        #self.all_gameobjs.draw(self.parent.screen)
        for obj in self.all_gameobjs:
            self.parent.screen.blit(obj.image, obj.rect)
        pygame.display.update()

    def reset(self):
        self.empty_cells = []
        self.selected = -1
        for i, cell in enumerate(self.cells):
            cell.removeBall()
            self.empty_cells.append(i)
        self.point.addPoint(-self.point.point)
        self.next_balls.update(self)
        self.next_balls.update(self)
        self.time.time = int(time.time())
        self.time.run()
        return
        for _ in range(24):
            self.next_balls.update(self)

    def run(self):
        print('run')
        while Events.checkEventsOfPlayingScene(self):
            print(time.time())
            if self.game_over:
                self.time.stop()
                self.parent.gameover_scene.run()
                if self.parent.gameover_scene.status == 'quit':
                    break
                else:
                    self.game_over = False
                    self.reset()
            self.parent.screen.fill(Setting.BACKGROUND_COLOR)
            #self.all_gameobjs.draw(self.parent.screen)
            for obj in self.all_gameobjs:
                self.parent.screen.blit(obj.image, obj.rect)
            pygame.display.update()
            self.parent.clock.tick(Setting.FPS)
        for cell in self.cells:
            cell.jumping = False
        self.time.stop()
    @isThread
    def findWay(self, start, end):
        self.isRunning = True
        result = None
        result1 = None
        result2 = None
        temp1 = [[start]]
        temp2 = [[end]]
        while True:
            temp = list(temp1)
            temp1 = []
            for way in temp:
                for cell in self.cells[way[-1]].neighbours:
                    if self.cells[cell].ball == 0 and cell not in way:
                        if cell == end:
                            result1 = way + [cell]
                        else:
                            temp1.append(way + [cell])
            temp = list(temp2)
            temp2 = []
            for way in temp:
                for cell in self.cells[way[0]].neighbours:
                    if self.cells[cell].ball == 0 and cell not in way:
                        if cell == start:
                            result2 = [cell] + way
                        else:
                            temp2.append([cell] + way)
            if result1:
                result = result1
                break
            elif result2:
                result = result2
                break
            if not (temp1 and temp2):
                break
        if result:
            self.moveBall(result)
        self.isRunning = False
    
    def moveBall(self, way):
        color = self.cells[self.selected].ball
        self.cells[self.selected].stopJumping()
        self.cells[self.selected].removeBall()
        self.empty_cells.append(self.selected)
        self.selected = -1
        for i in range(len(way)-1):
            self.cells[way[i]].image.blit(Images.img_balls[0], (0, 0))
            self.cells[way[i+1]].image.blit(Images.img_balls[color], (0, 0))
            time.sleep(0.02)
        self.cells[way[-1]].addBall(color)
        self.empty_cells.remove(way[-1])
        if not self.checkPoint(way[-1]):
            self.next_balls.update(self)

    def checkPoint(self, cell):
        cells = []
        for i in range(4):
            temp = []
            for c in self.cells[cell].lines[i][0]:
                if self.cells[c].ball == self.cells[cell].ball:
                    temp.append(c)
                else:
                    break
            for c in self.cells[cell].lines[i][1]:
                if self.cells[c].ball == self.cells[cell].ball:
                    temp.append(c)
                else:
                    break
            if len(temp)>=4:
                cells.extend(temp)
        if cells:
            cells.append(cell)
            i = len(cells) - 5
            self.point.addPoint(5 + (i+1)*i//2)
            if self.bestpoint.point < self.point.point:
                self.bestpoint.update(self.point.point)
            size = Setting.PIXEL_OF_X
            while size>0:
                for c in cells:
                    try:
                        self.cells[c].image.blit(Images.img_balls[0], (0, 0))
                        self.cells[c].image.blit(
                            pygame.transform.scale(Images.img_balls[self.cells[c].ball], (size, size)),
                            ((Setting.PIXEL_OF_X-size)//2, (Setting.PIXEL_OF_Y-size)//2)
                        )
                    except: pass
                size -= 10
                time.sleep(0.1)
            for c in cells:
                self.cells[c].removeBall()
                self.empty_cells.append(c)
            for i, c in enumerate(self.next_balls.next_cells):
                self.cells[c].addNext(self.next_balls.next_images[i])
            return True
        else:
            return False

class GameOverScene:
    def __init__(self, parent):
        self.parent = parent
        self.status = ''
        self.playbtn = Play_Btn()
        self.highscore_table = HighScoreTable()
        #self.all_gameobjs = pygame.sprite.Group()
        self.all_gameobjs = []
        #self.all_gameobjs.add(self.highscore_table)
        #self.all_gameobjs.add(self.playbtn)
        self.all_gameobjs.append(self.playbtn)
        #self.run()

    def run(self):
        self.highscore_table.update()
        self.parent.screen.blit(Setting.BACKGROUND_OF_GAMEOVER, (0, 0))
        #self.all_gameobjs.draw(self.parent.screen)
        for obj in self.all_gameobjs:
            self.parent.screen.blit(obj.image, obj.rect)
        pygame.display.update()
        while Events.checkEventsOfGameOverScene(self):
            self.parent.clock.tick(Setting.FPS)