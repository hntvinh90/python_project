import pygame

class GameScreen:
    def __init__(self, title=None, pos=None, size=None, fps=None, icon=None):
        pygame.init()
        self.setTitle(title if title else 'Games')
        self.setPosition()

    def setTitle(self, title):
        pygame.display.set_caption(title)