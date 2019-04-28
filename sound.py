import pygame as pg

SELECT_SOUND = 'assets/select.wav'
INCOME_SOUND = 'assets/income.wav'
INTRO_SOUND = 'assets/intro2.wav'
ERROR_SOUND = 'assets/error.wav'


class SoundSystem:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.mixer.init()
        self.select = pg.mixer.Sound(SELECT_SOUND)
        self.income = pg.mixer.Sound(INCOME_SOUND)
        self.error = pg.mixer.Sound(ERROR_SOUND)

    def play_select(self):
        self.select.play()

    def play_income(self):
        self.income.play()

    def play_error(self):
        self.error.play()

    def play_intro(self):
        pg.mixer.music.load(INTRO_SOUND)
        pg.mixer.music.play()
