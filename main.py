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
renderer_small = Renderer("assets/tileset8x8.png", 'assets/big_skull.png', 8)


def update(world):
    world.update(sound_manager)
    pass


def render(world, status_bar, renderer):
    status_bar.fill((0, 0, 0))
    if world.render_status():
        renderer.render_line(status_bar, world.get_status(), 5.5, 0.5)
    world.render(renderer, renderer_small)
    pygame.display.flip()


def main():
    top_rect = (0, 0, WIN_TILE_SIZE * WIN_WIDTH, WIN_TILE_SIZE * 4)
    top_menu_screen = screen.subsurface(top_rect)

    field_rect = (0, WIN_TILE_SIZE * 4, WIN_TILE_SIZE * WIN_WIDTH, 80 * WIN_TILE_SIZE)
    field_screen = screen.subsurface(field_rect)

    world = World(field_screen, sound_manager)
    world.play_splash()
    while True:
        handle_events(world)
        if world.should_exit:
            terminate()
        update(world)
        render(world, top_menu_screen, renderer)
        clock.tick(FPS)


def handle_events(world):
    global grow
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            sound_manager.play_select()
            world.handle_input(event.key)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
