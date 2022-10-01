from Game_Classes.Images import Images
from Game_Classes.Conf import Conf
from Game_Classes.Music import sounds
import pygame as pg
class Bum(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = Images.bum[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.count = 0
        self.sound = pg.mixer.Sound(Conf.sound["bum"])
        self.sound.set_volume(sounds.volume)
        self.sound.play()

    def update(self):
        self.count += 1
        if self.count == 10:
            self.kill()
        else:
            x = self.rect.centerx
            y = self.rect.centery
            self.image = Images.bum[self.count]
            self.rect = self.image.get_rect(center=(x, y))

    def reset(self, win):
        win.blit(self.image, self.rect)