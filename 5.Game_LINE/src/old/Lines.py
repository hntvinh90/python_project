import pygame
import os
from __image import ImageString
from __game import Game

def main():
    X = 9
    Y = 9
    SIZE_IN_PIXEL = 70
    WIDTH = X * SIZE_IN_PIXEL
    HEIGHT = (Y+2) * SIZE_IN_PIXEL
    FPS = 30
    pygame.init()
    pygame.display.set_caption('Lines')
    pygame.display.set_icon(ImageString.img_icon)
    size_of_monitor = pygame.display.Info()
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' %((size_of_monitor.current_w-WIDTH)/2, (size_of_monitor.current_h-HEIGHT)/2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game(screen, X, Y, SIZE_IN_PIXEL)
    while True:
        screen.fill((200, 200, 200))
        if not game.update():
            pygame.quit()
            return
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    main()