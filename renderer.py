import pygame
import logging
from random import randint

logging.basicConfig(
    filename='log/ld44.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-6s %(message)s'
)

def load_image(filename, scale=1):
    image = pygame.image.load(filename).convert_alpha()
    return pygame.transform.scale(image, (256, 256))

def load_tileset(filename, width, height, scale=1):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tileset = []
    for x in range(0, int(image_width / width)):
        for y in range(0, int(image_height / height)):
            rect = (x * width, y * height, width, height)
            tile = image.subsurface(rect)
            if scale != 1:
                tile = pygame.transform.scale(tile, (width * scale, height * scale))
            tileset.append(tile)
    return tileset


def tile_map(tileset):
    return {
        'numbers': tileset[0:10],
        'alphabet': tileset[10:37],
        'space': tileset[47],
        'colon': tileset[38],
        'border': tileset[62],
        'currency': tileset[51],
        'selected': tileset[46],
        'dead': tileset[61],
        'alive': tileset[63],
    }


class Renderer:
    def __init__(self, filename, splash, pixels, scale=1):
        self.tilemap = tile_map(load_tileset(filename, pixels, pixels, scale))
        self.scale = scale
        self.tile_size = pixels * scale
        self.splash = load_image(splash)
        self.splash_text = "Your life is currency"

    def fill(self, screen, color):
        screen.fill(color)

    def render_multi_line(self, screen, lines, x, y):
        cy = y
        for line in lines:
            self.render_line(screen, line, x, cy)
            cy = cy + 1

    def render_cells(self, screen, cells):
        screen.fill((0, 0, 0))
        w, h = screen.get_size()
        for cell in cells:
            screen.blit(self.tilemap['alive'], (cell.x * self.tile_size, cell.y * self.tile_size))

    def render_image(self, screen, img, x, y):
        screen.blit(img, (x, y))

    def render_splash(self, screen, x, y, alpha):
        w, h = screen.get_size()
        iw, ih = self.splash.get_size()
        screen.fill((0, 0, 0))
        x = (w - iw) / 2
        y = (h - ih) / 2
        tx = (w / self.tile_size - len(self.splash_text)) / 2
        ty = (y + ih) / self.tile_size + 1
        self.render_image(screen, self.splash, x + randint(0, 1), y + randint(0, 4))
        self.render_line(screen, self.splash_text, tx, ty)
        logging.info("Setting alpha %d" % alpha)

    def render_line(self, screen, text, x, y):
        # screen.fill((0, 0, 0))
        # limit in size
        # text = text[0:WIN_WIDTH]
        cx = x
        for c in text:
            if c.isalpha():
                character = self.tilemap['alphabet'][ord(c.upper()) - 65]
            elif c.isdigit():
                character = self.tilemap['numbers'][ord(c) - 48]
            elif ord(c) == ord(' '):
                character = self.tilemap['space']
            elif ord(c) == ord(':'):
                character = self.tilemap['colon']
            elif ord(c) == ord('#'):
                character = self.tilemap['border']
            elif ord(c) == ord('>'):
                character = self.tilemap['selected']
            elif ord(c) == ord('$'):
                character = self.tilemap['currency']
            else:
                character = self.tilemap['space']
            pix_x = int(cx * self.tile_size)
            pix_y = int(y * self.tile_size)
            screen.blit(character, (pix_x, pix_y))
            cx = cx + 1
