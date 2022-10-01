from Game_Classes.Conf import Conf
from Game_Classes.Text import Text
from Game_Classes.Music import sounds
from Game_Classes.Bullet import Bullet
from Game_Classes.StatusBar import StatusBar
import time
import pygame as pg
class Weapon:
    def __init__(self, name, time_reload, speed, power, volume, img,
                 mini_img=None, mini_x=0, mini_y=0):
        self.name = name
        self.title = Text(text=f"Weapon: {name}", x=0, y=0, font_size=30)
        self.time_for_reload = time_reload
        self.speed = speed
        self.power = power
        self.reload = time.time()
        self.volume = volume
        self.img = img
        self.sound = pg.mixer.Sound(Conf.sound[name])
        if mini_img is not None:
            self.mini_img = mini_img
            self.rect = self.mini_img.get_rect(center=(mini_x, mini_y))
            self.title.change_pos(self.rect.centerx, self.rect.top)
            self.display_volume = StatusBar(self.rect.centerx, self.rect.bottom,
                                            width=self.title.rect.width, height=20,
                                            max_value=volume)
            self.speed_title = Text(text=f"Speed: {time_reload}", x=mini_x,
                                    y=self.display_volume.rect.bottom+30, font_size=30)
            self.power_title = Text(text=f"Power: {power}", x=mini_x,
                                    y=self.display_volume.rect.bottom + 70, font_size=30)

    def draw(self, win):
        if self.mini_img is not None:
            self.speed_title.update(f"Speed: {self.time_for_reload}")
            self.power_title.update(f"Power: {self.power}")
            win.blit(self.mini_img, self.rect)
            self.title.reset(win)
            self.display_volume.update(self.volume)
            self.display_volume.draw(win)
            self.speed_title.reset(win)
            self.power_title.reset(win)

    def reloaded(self):
        if self.volume == 0:
            return False
        return time.time() - self.reload > self.time_for_reload

    def fire(self, x, y, direction=1):
        bullet = Bullet(x=x, y=y, speed=self.speed, power=self.power, img=self.img,
                        direction=direction)
        self.reload = time.time()
        self.volume -= 1
        self.sound.set_volume(sounds.volume /4)
        self.sound.play()
        return bullet
