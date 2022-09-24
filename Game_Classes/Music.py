from Game_Classes import Conf
import pygame as pg
import time
class Music:
    def __new__(cls):
        """Реализация паттерна 'Сингелтон' - при попытке создать новый объект
        будет возвращаться ссылка на уже созданный"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Music, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        if not hasattr(self, 'sounds'):  # чтобы дважды не вызывался конструктор
            self.sounds = []
            self.volume = 0.2
            self.current_sound = None
            self.is_playing = False
            self.timer = time.time()
            self.channel = None

    def add(self, *filenames):
        for filename in filenames:
            self.sounds.append(pg.mixer.Sound(filename))

    def stop(self):
        if self.current_sound is not None:
            self.sounds[self.current_sound].stop()
            self.is_playing = False

    def play_current(self):
        if self.current_sound is not None:
            self.sounds[self.current_sound].set_volume(self.volume)
            self.channel = self.sounds[self.current_sound].play(loops=-1)
            self.is_playing = True

    def play(self, index=0):
        if self.sounds and index < len(self.sounds):
            self.stop()
            self.current_sound = index
            self.play_current()

    def play_next(self):
        if self.current_sound + 1 == len(self.sounds):
            self.play(0)
        else:
            self.play(self.current_sound + 1)

    def set_volume(self, volume):
        self.volume = volume
        if self.current_sound is not None:
            self.sounds[self.current_sound].set_volume(self.volume)

    def up_volume(self):
        self.volume += 0.05
        if self.volume > 1:
            self.volume = 1
        self.set_volume(self.volume)

    def down_volume(self):
        self.volume -= 0.05
        if self.volume < 0:
            self.volume = 0
        self.set_volume(self.volume)

    def control(self, key):
        if key == pg.K_p:
            if self.is_playing:
                self.channel.pause()
                self.is_playing = False
            else:
                self.channel.unpause()
                self.is_playing = True
        comand = {pg.K_t: self.stop, pg.K_l: self.play,
                  pg.K_n: self.play_next}
        if key in comand:
            comand[key]()
        comand2 = (pg.K_1, pg.K_2, pg.K_3, pg.K_4)
        if key in comand2:
            self.play(comand2.index(key))

    def update(self):
        if time.time() - self.timer > 0.1:
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                self.up_volume()
            elif keys[pg.K_DOWN]:
                self.down_volume()
            self.timer = time.time()
sounds = Music()  # создаем сингелтон объект для управления музыкой
sounds.add(*Conf.music)
sounds.play()