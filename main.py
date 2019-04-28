import sys
import pygame
import pygame.locals
import logging
import time
from world import World
from renderer import Renderer
from sound import SoundSystem

logging.basicConfig(
    filename='log/ld44.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-6s %(message)s'
)

WIN_WIDTH = 80
WIN_HEIGHT = 84
WIN_TILE_SIZE = 8

offset_x = 30
offset_y = 30

FPS = 40

sound_manager = SoundSystem()
pygame.init()
# logo = pygame.image.load('assets/logo32x32.png')
logo = pygame.image.load('assets/big_skull.png')
pygame.display.set_icon(logo)
screen = pygame.display.set_mode((WIN_WIDTH * WIN_TILE_SIZE, WIN_HEIGHT * WIN_TILE_SIZE))
screen.fill((0, 0, 0))


pygame.display.set_caption('Your life is currency')

grow = False

pygame.key.set_repeat(1, 50)
clock = pygame.time.Clock()
renderer = Renderer("assets/tileset8x8.png", 'assets/big_skull.png', 8, 2)


def update(world):
    world.update(sound_manager)
    pass


def render(world, status_bar, renderer):
    renderer.render_line(status_bar, world.get_status(), 5.5, 0.5)
    world.render(renderer)
    pygame.display.flip()


def main():
    # splash
    # start/menu screen
    sound_manager.play_intro()
    top_rect = (0, 0, WIN_TILE_SIZE * WIN_WIDTH, WIN_TILE_SIZE * 4)
    top_menu_screen = screen.subsurface(top_rect)

    field_rect = (0, WIN_TILE_SIZE * 4, WIN_TILE_SIZE * WIN_WIDTH, 80 * WIN_TILE_SIZE)
    field_screen = screen.subsurface(field_rect)

    world = World(field_screen)
    while True:
        handle_events(world)
        update(world)
        render(world, top_menu_screen, renderer)
        clock.tick(FPS)


def handle_events(world):
    global grow
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            terminate()
        elif event.type == pygame.KEYDOWN:
            sound_manager.play_select()
            if event.key == pygame.K_SPACE:
                world.toggle_start()
            elif event.key == pygame.K_1:
                world.select('1')
            elif event.key == pygame.K_2:
                world.select('2')
            elif event.key == pygame.K_3:
                world.select('3')
            elif event.key == pygame.K_4:
                world.select('4')
            elif event.key == pygame.K_5:
                world.select('5')
            elif event.key == pygame.K_6:
                world.select('6')
            elif event.key == pygame.K_7:
                world.select('7')
            elif event.key == pygame.K_8:
                world.select('8')
            elif event.key == pygame.K_9:
                world.select('9')
            elif event.key == pygame.K_BACKQUOTE:
                world.select('')
            elif event.key == pygame.K_v or pygame.K_RETURN:
                world.try_view()
            elif event.key == pygame.K_h:
                world.try_harvest()
            elif event.key == pygame.K_u:
                world.try_unlock()

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
