import logging
import time
import pygame

from field import Field
from pattern import predefined
from enum import Enum
from menu import Menu
from help import HelpScreen

TEN_MIL = 10000000

logging.basicConfig(
    filename='ld44.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-6s %(message)s'
)

FIELD_WIDGET_SIZE = 12
FIELD_WIDGET_DISTANCE = 1
FIELD_WIDGET_BORDER_COLOR = (0, 127, 255)
FIELD_WIDGET_FILL_COLOR = (0, 0, 0)
FIELD_DEF_SIZE = 20


class Mode(Enum):
    SPLASH = 1
    MAIN_MENU = 2
    HELP = 3
    OVERVIEW = 4
    FIELD_VIEW = 5
    SOW_VIEW = 6
    GAME_OVER = 7
    VICTORY = 8


class World:
    def __init__(self, screen, sound_mgr):

        self.field_index = {
            '1': Field('1', FIELD_DEF_SIZE, FIELD_DEF_SIZE, 0),
            '2': Field('2', FIELD_DEF_SIZE, FIELD_DEF_SIZE * 1.5, 10),
            '3': Field('3', FIELD_DEF_SIZE * 1.5, FIELD_DEF_SIZE * 1.5, 50),
            '4': Field('4', FIELD_DEF_SIZE * 2, FIELD_DEF_SIZE * 1.5, 100),
            '5': Field('5', FIELD_DEF_SIZE * 2, FIELD_DEF_SIZE * 2, 500),
            '6': Field('6', FIELD_DEF_SIZE * 2, FIELD_DEF_SIZE * 2.5, 1000),
            '7': Field('7', FIELD_DEF_SIZE * 2.5, FIELD_DEF_SIZE * 2.5, 10000),
            '8': Field('8', FIELD_DEF_SIZE * 3, FIELD_DEF_SIZE * 2.5, 100000),
            '9': Field('9', FIELD_DEF_SIZE * 3.5, FIELD_DEF_SIZE * 3.5, 1000000),
        }
        self.fields = [
            [
                self.field_index['1'],
                self.field_index['4'],
                self.field_index['7'],
            ],
            [
                self.field_index['2'],
                self.field_index['5'],
                self.field_index['8'],
            ],
            [
                self.field_index['3'],
                self.field_index['6'],
                self.field_index['9'],
            ],

        ]
        self.screen = screen
        self.is_open = False
        self.pause = True
        self.field_widgets = []
        self.field_frames = []
        # test all:
        # for i in self.field_index:
        #     field = self.field_index[i]
        #     field.unlock()
        #     field.add_cells(predefined['acorn'].get_moved_cells(10, 10))
        field = self.field_index['1']
        field.unlock()
        field.add_cells(predefined['acorn'].get_moved_cells(10, 10))

        self.currency = 0
        self.selected = ''
        self.is_selection_changed = False
        self.mode = Mode.SPLASH
        self.splash_end = 0
        self.main_menu = Menu()
        self.sound_manager = sound_mgr
        self.should_exit = False
        self.should_restart = False
        self.active_field = field
        self.help_screen = HelpScreen()
        self.prev_mode = Mode.MAIN_MENU
        self.next_ding = 1
        self.hunger = (100, 1)

    def update_ding(self):
        self.next_ding = int(self.currency * 1.1)

    def play_splash(self):
        self.sound_manager.play_intro()
        self.splash_end = time.time() + 5
        self.mode = Mode.SPLASH

    def update(self, sound_system):
        if self.mode == Mode.SPLASH:
            if time.time() >= self.splash_end:
                self.mode = Mode.MAIN_MENU
        if not self.pause:
            for row in self.fields:
                for field in row:
                    if not field.is_locked:
                        field.step()
                        self.currency += field.income
            if self.currency > self.next_ding:
                self.update_ding()
                sound_system.play_income()

            one_closed = False
            for i in self.field_index:
                if self.field_index[i].is_locked:
                    one_closed = True
                    break
            if not one_closed or self.currency > TEN_MIL:
                self.win()

            age_to_eat, quantity_to_eat = self.hunger
            if self.field_index['1'].age >= age_to_eat:
                if self.currency < quantity_to_eat:
                    self.game_over()
                self.currency -= quantity_to_eat
                self.update_hunger(age_to_eat)

    def game_over(self):
        self.mode = Mode.GAME_OVER
        self.pause = True

    def win(self):
        self.mode = Mode.VICTORY
        self.pause = True

    def update_hunger(self, age_to_eat):
        self.hunger = age_to_eat + 100, len(str(age_to_eat)) - 2

    def handle_input(self, key):
        if key == pygame.K_F1:
            self.to_help()

        if self.mode == Mode.OVERVIEW:
            self.handle_input_overview(key)
        elif self.mode == Mode.FIELD_VIEW:
            self.handle_input_overview(key)
        elif self.mode == Mode.SOW_VIEW:
            self.handle_input_sow(key)
        elif self.mode == Mode.SPLASH:
            self.handle_input_splash(key)
        elif self.mode == Mode.MAIN_MENU:
            self.handle_input_menu(key)
        elif self.mode == Mode.HELP:
            if key == pygame.K_ESCAPE:
                self.mode = self.prev_mode
        elif self.mode == Mode.VICTORY or self.mode == Mode.GAME_OVER:
            self.handle_end_screen(key)

    def to_help(self):
        self.pause = True
        self.prev_mode = self.mode
        self.is_open = False
        self.mode = Mode.HELP

    def handle_input_sow(self, key):
        if key == pygame.K_UP:
            self.active_field.move_cursor(0, -1)
        elif key == pygame.K_DOWN:
            self.active_field.move_cursor(0, 1)
        elif key == pygame.K_LEFT:
            self.active_field.move_cursor(-1, 0)
        elif key == pygame.K_RIGHT:
            self.active_field.move_cursor(1, 0)
        elif key == pygame.K_RETURN:
            if self.active_field:
                self.active_field.add_sowing_cell(self.active_field.cursor)
        elif key == pygame.K_s:
            logging.info("Attempting to sow...")
            if self.active_field.sowing_price < self.currency:
                self.currency -= self.active_field.sowing_price
                self.active_field.sow()
                self.mode = Mode.FIELD_VIEW
            else:
                logging.info("Not enough money: needed %d; have %d" % (self.active_field.sowing_price, self.currency))
                self.sound_manager.play_error()
        elif key == pygame.K_ESCAPE:
            self.active_field.cancel_sowing()
            self.start_overview_mode()

    def handle_input_splash(self, key):
        self.skip_splash()
        pass

    def render_status(self):
        return self.mode != Mode.SPLASH and self.mode != Mode.MAIN_MENU

    def skip_splash(self):
        self.splash_end = 0

    def handle_end_screen(self, key):
        self.should_restart = True
        pass

    def handle_input_menu(self, key):
        if key == pygame.K_UP:
            self.main_menu.prev()
            pass
        elif key == pygame.K_DOWN:
            self.main_menu.next()
            pass
        elif key == pygame.K_RETURN:
            act = self.main_menu.act()
            logging.debug("Next action is %s" % act)
            if 'about' == act:
                logging.debug("Showing about")
                self.play_splash()
                pass
            elif 'exit' == act:
                logging.debug("Exiting")
                self.should_exit = True
                pass
            elif 'cont' == act:
                logging.debug("Continuing")
                self.start_overview_mode()
            elif 'help' == act:
                logging.debug("Showing help")
                self.to_help()
            elif 'new' == act:
                logging.debug("Restarting")
                self.should_restart = True
                pass
            pass
        pass

    def handle_input_overview(self, key):
        if key == pygame.K_ESCAPE:
            self.mode = Mode.MAIN_MENU
            self.pause = True
            self.is_open = False
        elif key == pygame.K_1:
            self.select('1')
        elif key == pygame.K_2:
            self.select('2')
        elif key == pygame.K_3:
            self.select('3')
        elif key == pygame.K_4:
            self.select('4')
        elif key == pygame.K_5:
            self.select('5')
        elif key == pygame.K_6:
            self.select('6')
        elif key == pygame.K_7:
            self.select('7')
        elif key == pygame.K_8:
            self.select('8')
        elif key == pygame.K_9:
            self.select('9')
        elif key == pygame.K_BACKQUOTE:
            self.select('')
        elif key == pygame.K_v or key == pygame.K_RETURN:
            self.try_view()
        elif key == pygame.K_h:
            self.try_harvest()
        elif key == pygame.K_s:
            self.try_sow()
        elif key == pygame.K_u:
            self.try_unlock()
        # If you want to win quickly
        # elif key == pygame.K_F11:
        #     self.mode = Mode.GAME_OVER
        # elif key == pygame.K_F12:
        #     self.mode = Mode.VICTORY
        elif key == pygame.K_PAUSE or key == pygame.K_SPACE:
            self.pause = not self.pause

    def get_status(self):
        status = "$:" + '{:8d}'.format(self.currency)
        if self.pause:
            status += "   PAUSED"
        else:
            status += "       "
        return status + "   PRESS F1 FOR HELP"

    def start_overview_mode(self):
        self.mode = Mode.OVERVIEW
        self.is_open = False

    def select(self, id):
        if self.mode == Mode.FIELD_VIEW and id == '':
            self.start_overview_mode()
        if id != self.selected:
            self.selected = id
            self.is_selection_changed = True
        elif id != '':
            self.try_view()

    def try_view(self):
        if self.selected != '':
            self.mode = Mode.FIELD_VIEW
        pass

    def try_harvest(self):
        logging.info("Attempting to harvest %s!" % self.selected)
        if self.selected == '':
            logging.error("Cannot harvest what was not selected!")
            self.sound_manager.play_error()
        elif self.selected in self.field_index:
            field = self.field_index[self.selected]
            if field.is_locked:
                logging.error("Cannot harvest locked continent!")
                self.sound_manager.play_error()
            else:
                logging.info("Harvesting continent %s with %d cells" % (self.selected, len(field.cells)))
                self.sound_manager.play_income()
                self.currency += field.harvest()
                self.pause = True

        else:
            logging.error("Unknown continent %s!" % self.selected)
            self.sound_manager.play_error()
        pass

    def try_unlock(self):
        if self.selected == '':
            logging.error("Continent must be selected before unlocking")
            self.sound_manager.play_error()
        elif self.selected in self.field_index:
            field = self.field_index[self.selected]
            if not field.is_locked:
                logging.error("Continent %s is already unlocked!" % self.selected)
                self.sound_manager.play_error()
            else:
                if field.price < self.currency:
                    self.currency -= field.price
                    field.unlock()
                else:
                    logging.error("Not enough money to unlock - %d < %d" % (self.currency, field.price))
                    self.sound_manager.play_error()
        else:
            logging.error("Unknown continent %s!" % self.selected)
            self.sound_manager.play_error()
        pass

    def try_sow(self):
        if self.selected == '':
            logging.error("Continent must be selected before sowing")
            self.sound_manager.play_error()
        elif self.selected in self.field_index:
            field = self.field_index[self.selected]
            if field.is_locked:
                logging.error("Continent must be unlocked before sowing")
                self.sound_manager.play_error()
            elif len(field.cells) > 0:
                logging.error("Continent must be cleared before sowing")
                self.sound_manager.play_error()
            else:
                field.start_sowing()
                self.pause = True
                self.mode = Mode.SOW_VIEW
        else:
            logging.error("Unknown continent %s!" % self.selected)
            self.sound_manager.play_error()

    def render_selected(self, renderer):
        for c, row in enumerate(self.fields):
            for r, field in enumerate(row):
                if field.id == self.selected:
                    renderer.render_line(self.field_frames[c][r], ">Cont-t: " + field.id, 1, 1)
                else:
                    renderer.render_line(self.field_frames[c][r], " Cont-t: " + field.id, 1, 1)

    def render(self, renderer, renderer_small):
        if self.mode == Mode.SPLASH and time.time() < self.splash_end:
            renderer.render_splash(self.screen)
            pass
        elif self.mode == Mode.MAIN_MENU:
            renderer.render_menu(self.screen, self.main_menu)
            pass
        elif self.mode == Mode.HELP:
            renderer.render_help_screen(self.screen, self.help_screen)
            pass
        elif self.mode == Mode.OVERVIEW:
            # check state: main screen
            if not self.is_open:
                self.screen.fill((0, 0, 0))
                self.field_widgets = []
                for c, row in enumerate(self.fields):
                    line = []
                    line_frames = []
                    for r, field in enumerate(row):
                        x = FIELD_WIDGET_DISTANCE + c * (FIELD_WIDGET_DISTANCE + FIELD_WIDGET_SIZE)
                        y = FIELD_WIDGET_DISTANCE + r * (FIELD_WIDGET_DISTANCE + FIELD_WIDGET_SIZE)
                        rect = (x * renderer.tile_size,
                                y * renderer.tile_size,
                                FIELD_WIDGET_SIZE * renderer.tile_size,
                                FIELD_WIDGET_SIZE * renderer.tile_size)
                        fs = self.screen.subsurface(rect)
                        renderer.fill(fs, FIELD_WIDGET_BORDER_COLOR)
                        renderer.render_line(fs, " Cont-t: " + field.id, 1, 1)
                        line_frames.append(fs)
                        line.append(fs.subsurface(renderer.tile_size, 3 * renderer.tile_size, 10 * renderer.tile_size, 8  * renderer.tile_size))
                    self.field_widgets.append(line)
                    self.field_frames.append(line_frames)
                self.is_open = True

            if self.is_selection_changed:
                self.render_selected(renderer)
                self.is_selection_changed = False

            for c, row in enumerate(self.fields):
                for r, field in enumerate(row):
                    sfs = self.field_widgets[c][r]
                    renderer.fill(sfs, FIELD_WIDGET_FILL_COLOR)
                    renderer.render_multi_line(sfs, field.get_status(), 0, 0)

        elif self.mode == Mode.FIELD_VIEW:
            self.screen.fill((0, 0, 0))
            matching = self.field_index[self.selected]
            if matching.is_big:
                matching.render(renderer_small, self.screen)
            else:
                matching.render(renderer, self.screen)

        elif self.mode == Mode.SOW_VIEW:
            self.screen.fill((0, 0, 0))
            matching = self.field_index[self.selected]
            self.active_field = matching
            if matching.is_big:
                matching.render(renderer_small, self.screen)
            else:
                matching.render(renderer, self.screen)

        elif self.mode == Mode.GAME_OVER:
            renderer.render_gameover(self.screen)
            pass

        elif self.mode == Mode.VICTORY:
            renderer.render_victory(self.screen)
            pass
