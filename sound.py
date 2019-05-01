import os
import pygame as pg
import logging as log
from resmgr import get_res

log.basicConfig(
    filename='ld44.log',
    filemode='w',
    level=log.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-6s %(message)s'
)
SELECT_SOUND = get_res(os.path.join('assets', 'select.wav'))
INCOME_SOUND = get_res(os.path.join('assets', 'income.wav'))
INTRO_SOUND = get_res(os.path.join('assets', 'intro2.wav'))
ERROR_SOUND = get_res(os.path.join('assets', 'error.wav'))

MUSIC_VOLUME = 0.05
EFFECTS_VOLUME = 0.03


class SoundSystem:
    def __init__(self):
        log.info("Starting sound system with: %s %s %s %s" % (SELECT_SOUND, INCOME_SOUND, INTRO_SOUND, ERROR_SOUND))
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.mixer.init()
        self.select = pg.mixer.Sound(SELECT_SOUND)
        self.select.set_volume(EFFECTS_VOLUME)
        self.income = pg.mixer.Sound(INCOME_SOUND)
        self.income.set_volume(EFFECTS_VOLUME)
        self.error = pg.mixer.Sound(ERROR_SOUND)
        self.error.set_volume(EFFECTS_VOLUME)

    def play_select(self):
        self.select.play()

    def play_income(self):
        self.income.play()

    def play_error(self):
        self.error.play()

    def play_intro(self):
        pg.mixer.music.load(INTRO_SOUND)
        pg.mixer.music.set_volume(MUSIC_VOLUME)
        pg.mixer.music.play()
