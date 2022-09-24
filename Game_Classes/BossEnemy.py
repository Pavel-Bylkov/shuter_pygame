from Game_Classes import Weapon, Enemy, Conf, Images
import random
import pygame as pg
class Boss(Enemy):
    def __init__(self, x, y, speed, health, img, power):
        super().__init__(x, y, speed, health, img)
        self.bullets = pg.sprite.Group()
        self.fire_line = pg.Rect(self.rect.left, self.rect.bottom,
                                 self.rect.right - self.rect.left, Conf.win_height)
        if random.randint(0, 1):
            self.speed *= -1
        self.fps = 0
        self.weapon = Weapon(name=Conf.weapon_names[0], time_reload=0.3,
                             speed=10, power=power,
                             volume=1000, img=Images.bulls[0])
        self.left_radar = pg.Rect(self.rect.left-50, self.rect.bottom,
                                 50, Conf.win_height)
        self.right_radar = pg.Rect(self.rect.right+50, self.rect.bottom,
                                  50, Conf.win_height)

    def move(self):
        if 30 < self.rect.x + self.speed < Conf.win_width - 30:
            self.rect.x += self.speed
        else:
            self.speed *= -1
        if self.fps // 5 == 1:
            self.rect.y += 1
            self.fps = 0
        self.fps += 1

    def fire(self):
        if self.weapon.reloaded():
            self.bullets.add(self.weapon.fire(x=self.rect.centerx,
                                              y=self.rect.bottom, direction=0))

    def update_fire(self):
        self.fire_line.centerx = self.rect.centerx
        self.left_radar.right = self.rect.left
        self.right_radar.left = self.rect.right

    def change_move(self, hero):
        if self.speed < 0 and self.right_radar.colliderect(hero.rect):
            self.speed *= -1
        if self.speed > 0 and self.left_radar.colliderect(hero.rect):
            self.speed *= -1

    def update(self):
        super().update()
        self.bullets.update()

    def check_fire(self, hero):
        return self.fire_line.colliderect(hero.rect)

    def reset(self, win):
        # pg.draw.rect(win, (250, 200, 230), self.fire_line)
        # pg.draw.rect(win, (50, 200, 30), self.left_radar)
        # pg.draw.rect(win, (50, 20, 230), self.right_radar)
        self.bullets.draw(win)