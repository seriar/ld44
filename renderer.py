import pygame
import logging
from random import randint

logging.basicConfig(
    filename='ld44.log',
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
        'exclam': tileset[48],
        'colon': tileset[38],
        'pipe': tileset[38 + 2],
        'plus': tileset[38 + 3],
        'dash': tileset[38 + 4],
        'back_quote': tileset[52],
        'tilda': tileset[53],
        'border': tileset[62],
        'comma': tileset[36],
        'dot': tileset[37],
        'currency': tileset[51],
        'selected': tileset[46],
        'ghost': tileset[59],
        'add': tileset[58],
        'remove': tileset[57],
        'alive': tileset[60:63],
    }


class Renderer:
    def __init__(self, filename, splash, gameover, win, pixels, scale=1):
        self.tilemap = tile_map(load_tileset(filename, pixels, pixels, scale))
        self.scale = scale
        self.tile_size = pixels * scale
        self.splash = load_image(splash)
        self.splash_text = "Your life is currency"
        self.gameover = load_image(gameover)
        self.gameover_text = "..."
        self.victory = load_image(win)
        self.victory_text = "You won. Welcome to new Eden!"
        self.alpha = 0

        self.up = True
        self.done = False

    def fill(self, screen, color):
        screen.fill(color)

    def reset_gameover(self):
        self.up = True
        self.done = False
        self.reset_alpha()

    def reset_alpha(self):
        self.alpha = 0

    def render_multi_line(self, screen, lines, x, y):
        cy = y
        for line in lines:
            self.render_line(screen, line, x, cy)
            cy = cy + 1

    def render_cells(self, screen, cells):
        screen.fill((0, 0, 0))
        for cell in cells:
            t = self.tilemap['alive'][randint(0, len(self.tilemap['alive']) - 1)]
            screen.blit(t, (cell.x * self.tile_size, cell.y * self.tile_size))

    def render_template_cells(self, screen, cells, cursor):
        screen.fill((0, 0, 0))
        for cell in cells:
            logging.debug("Rendering ghost cell %d %d" % (cell.x, cell.y))
            screen.blit(self.tilemap['ghost'], (cell.x * self.tile_size, cell.y * self.tile_size))
        if cursor in cells:
            logging.debug("Rendering remove cursor %d %d" % (cursor.x, cursor.y))
            screen.blit(self.tilemap['remove'], (cursor.x * self.tile_size, cursor.y * self.tile_size))
        else:
            logging.debug("Rendering add cursor %d %d" % (cursor.x, cursor.y))
            screen.blit(self.tilemap['add'], (cursor.x * self.tile_size, cursor.y * self.tile_size))

    def render_image(self, screen, img, x, y):
        screen.blit(img, (x, y))

    def render_splash(self, screen):
        w, h = screen.get_size()
        iw, ih = self.splash.get_size()
        screen.fill((0, 0, 0))
        x = (w - iw) / 2
        y = (h - ih) / 2
        tx = (w / self.tile_size - len(self.splash_text)) / 2
        ty = (y + ih) / self.tile_size + 1
        self.render_image(screen, self.splash, x + randint(0, 1), y + randint(0, 4))
        self.render_line(screen, "Hew Home. New Tomb", tx, ty)
        self.render_line(screen, self.splash_text, tx - 1.5, ty + 3)
        self.render_line(screen, "by seriar 2019", tx + 15, ty + 7)

    def render_victory(self, screen):
        w, h = screen.get_size()
        iw, ih = self.victory.get_size()
        screen.fill((0, 0, 0))
        x = (w - iw) / 2
        y = (h - ih) / 2
        tx = (w / self.tile_size - len(self.victory_text)) / 2
        ty = (y + ih) / self.tile_size + 1

        if self.alpha < 255:
            self.alpha += 1

        vicpic = pygame.Surface((iw, ih))
        vicpic.set_alpha(self.alpha)
        vicpic.blit(self.victory, (0, 0))
        barren = pygame.Surface((iw, ih))
        barren.set_alpha(255 - self.alpha)
        barren.blit(self.gameover, (0, 0))

        self.render_image(screen, barren, x, y)
        self.render_image(screen, vicpic, x, y)
        self.render_line(screen, self.victory_text, tx, ty)

    def render_gameover(self, screen):
        w, h = screen.get_size()
        iw, ih = self.gameover.get_size()
        screen.fill((0, 0, 0))
        x = (w - iw) / 2
        y = (h - ih) / 2
        tx = (w / self.tile_size - len(self.gameover_text)) / 2
        ty = (y + ih) / self.tile_size + 1

        vicpic = pygame.Surface((iw, ih))
        vicpic.set_alpha(self.alpha)
        vicpic.blit(self.victory, (0, 0))
        barren = pygame.Surface((iw, ih))
        barren.set_alpha(255 - self.alpha)
        barren.blit(self.gameover, (0, 0))

        if not self.done:
            if self.up:
                if self.alpha < 127:
                    self.alpha += 1
                else:
                    self.up = False
            else:
                if self.alpha > 0:
                    self.alpha -= 1
                else:
                    self.up = True
                    self.done = True

        self.render_image(screen, barren, x, y)
        self.render_image(screen, vicpic, x, y)
        self.render_line(screen, self.gameover_text, tx, ty)

    def render_menu(self, screen, menu):
        w, h = screen.get_size()
        iw, ih = menu.get_size_with_selection()
        screen.fill((0, 0, 0))
        x = (w / self.tile_size - iw) / 2
        y = (h / self.tile_size - ih) / 2
        self.render_multi_line(screen, menu.get_options_with_selection(), x, y)

    def render_help_screen(self, screen, help):
        w, h = screen.get_size()
        iw, ih = help.get_size()
        screen.fill((0, 0, 0))
        x = (w / self.tile_size - iw) / 2
        y = (h / self.tile_size - ih) / 2
        self.render_multi_line(screen, help.message, x, y)

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
            elif ord(c) == ord('`'):
                character = self.tilemap['back_quote']
            elif ord(c) == ord('~'):
                character = self.tilemap['tilda']
            elif ord(c) == ord('-'):
                character = self.tilemap['dash']
            elif ord(c) == ord('|'):
                character = self.tilemap['pipe']
            elif ord(c) == ord('+'):
                character = self.tilemap['plus']
            elif ord(c) == ord('.'):
                character = self.tilemap['dot']
            elif ord(c) == ord('!'):
                character = self.tilemap['exclam']
            elif ord(c) == ord(','):
                character = self.tilemap['comma']
            else:
                character = self.tilemap['space']
            pix_x = int(cx * self.tile_size)
            pix_y = int(y * self.tile_size)
            screen.blit(character, (pix_x, pix_y))
            cx = cx + 1
