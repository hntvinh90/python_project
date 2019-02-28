import pygame
from __setting import Setting
from myLibs import isThread

class Events:

    #@isThread
    @staticmethod
    def checkEventsOfPlayingScene(scene):
        if scene.isRunning:
            pygame.event.get()
            return True
        #scene.isRunning = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                left, top = event.pos
                top -= Setting.HEIGHT_FOR_INFO
                x = left//Setting.PIXEL_OF_X
                y = top//Setting.PIXEL_OF_Y
                if x>=0 and y>=0:
                    cell = y*Setting.X_CELLS_NUMBER + x
                    if scene.selected == cell:
                        scene.cells[scene.selected].stopJumping()
                        scene.selected = -1
                    else:
                        if scene.cells[cell].ball == 0:
                            if scene.selected != -1:
                                scene.findWay(scene.selected, cell)
                        else:
                            if scene.selected != -1:
                                scene.cells[scene.selected].stopJumping()
                            scene.cells[cell].startJumping()
                            scene.selected = cell
        #scene.isRunning = False
        return True

    @staticmethod
    def checkEventsOfGameOverScene(scene):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene.status = 'quit'
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (x>scene.playbtn.rect.x 
                    and x<scene.playbtn.rect.x+scene.playbtn.rect.width
                    and y>scene.playbtn.rect.y 
                    and y<scene.playbtn.rect.y+scene.playbtn.rect.height
                ):
                    scene.status = ''
                    return False
        return True