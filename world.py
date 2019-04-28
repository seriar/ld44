import logging
import time
import pygame

from field import Field
from pattern import predefined
from enum import Enum


logging.basicConfig(
    filename='log/ld44.log',
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
    OVERVIEW = 3
    FIELD_VIEW = 4

class World:
    def __init__(self, screen):
        self.fields = [[Field('1', FIELD_DEF_SIZE, FIELD_DEF_SIZE),
                        Field('4', FIELD_DEF_SIZE, FIELD_DEF_SIZE),
                        Field('7', FIELD_DEF_SIZE, FIELD_DEF_SIZE)],
                       [Field('2', FIELD_DEF_SIZE, FIELD_DEF_SIZE),
                        Field('5', FIELD_DEF_SIZE, FIELD_DEF_SIZE),
                        Field('8', FIELD_DEF_SIZE, FIELD_DEF_SIZE)],
                       [Field('3', FIELD_DEF_SIZE, FIELD_DEF_SIZE),
                        Field('6', FIELD_DEF_SIZE, FIELD_DEF_SIZE),
                        Field('9', FIELD_DEF_SIZE, FIELD_DEF_SIZE)]
                       ]
        self.screen = screen
        self.is_open = False
        self.field_widgets = []
        self.field_frames = []
        field = self.fields[0][0]
        field.unlock()
        field.add_cells(predefined['acorn'].get_moved_cells(10, 10))
        self.currency = 0
        self.selected = ''
        self.is_selection_changed = False
        self.mode = Mode.SPLASH
        self.splash_end = time.time() + 5
        self.alpha = 0.0


    def update(self, sound_system):
        coin = False
        if self.mode == Mode.SPLASH:
            if time.time() >= self.splash_end:
                self.mode = Mode.OVERVIEW
            if self.alpha < 255:
                self.alpha = self.alpha + 1
        for row in self.fields:
            for field in row:
                if not field.is_locked and field.is_running:
                    field.step()
                    self.currency += field.income
                    if (field.income > 0):
                        coin = True
        if coin:
            sound_system.play_income()

    def get_status(self):
        return "$:" + str(self.currency)

    def select(self, id):
        if self.mode == Mode.FIELD_VIEW and id == '':
            self.mode = Mode.OVERVIEW
            self.is_open = False
        if id != self.selected:
            self.selected = id
            self.is_selection_changed = True
        elif id != '':
            self.try_view()

    def try_view(self):
        self.mode = Mode.FIELD_VIEW
        pass

    def try_harvest(self):
        pass

    def try_unlock(self):
        pass

    def toggle_start(self):
        for row in self.fields:
            for field in row:
                if not field.is_locked:
                    field.is_running = not field.is_running

    def render_selected(self, renderer):
        for c, row in enumerate(self.fields):
            for r, field in enumerate(row):
                if field.id == self.selected:
                    renderer.render_line(self.field_frames[c][r], ">Field: " + field.id, 1, 1)
                else:
                    renderer.render_line(self.field_frames[c][r], " Field: " + field.id, 1, 1)

    def render(self, renderer):
        if self.mode == Mode.SPLASH and time.time() < self.splash_end:
            renderer.render_splash(self.screen, 0, 0, 255 - self.alpha)
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
                        renderer.render_line(fs, " Field: " + field.id, 1, 1)
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
            matching = []
            for row in self.fields:
                for field in row:
                    if field.id == self.selected:
                        matching.append(field)
            if len(matching) == 0:
                logging.error("Window not found %s" % self.selected)
            elif len(matching) == 1:
                matching[0].render(renderer, self.screen)
            else:
                logging.warning("Multiple matching found -%d" % len(matching))

