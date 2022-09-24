import pygame as pg
class Base(pg.sprite.Sprite):
    def __init__(self, x, y, speed, img, *args, **kwargs):
        super().__init__(*args)
        self.speed = speed
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))

    def reset(self, win):
        win.blit(self.image, self.rect)
