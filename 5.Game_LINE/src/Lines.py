import pygame
import sys
from __images import Images
from __setting import Setting
from __scenes import PlayingScene, GameOverScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Lines')
        pygame.display.set_icon(Images.img_icon)
        Setting.setScreenToCenter(Setting.SCREEN_WIDTH, Setting.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode((Setting.SCREEN_WIDTH, Setting.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.loadScenes()
        print('1')
        self.playing_scene.run()
        print('2')
        pygame.quit()

    def loadScenes(self):
        print('load play')
        self.playing_scene = PlayingScene(self)
        print('load gameover')
        self.gameover_scene = GameOverScene(self)

def main():
    Game()


if __name__ == '__main__':
    main()