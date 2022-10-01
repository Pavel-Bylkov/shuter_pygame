from Game_Classes.Base import Base
from Game_Classes.Conf import Conf
from Game_Classes.StatusBar import StatusBar
from Game_Classes.Text import Text
from Game_Classes.Images import Images
from Game_Classes.Weapon import Weapon
import pygame as pg
class Hero(Base):
    def __init__(self, x, y, speed):
        super().__init__(x=x, y=y, speed=speed, img=Images.hero)
        self.bullets = pg.sprite.Group()
        self.health = 100
        self.health_display = Text(x=Conf.win_width - 155, y=20, text="Health:", font_size=30)
        self.health_bar = StatusBar(0, 0, Conf.win_width-self.health_display.rect.right-10,
                                    height=20, max_value=self.health)
        self.health_bar.correct_pos(self.health_display.rect.right+5, self.health_display.rect.centery)
        self.cur_weapon = 0
        self.weapons = (
            Weapon(name=Conf.weapon_names[0], time_reload=0.15, speed=10, power=1, volume=900,
                   img=Images.bulls[0], mini_img=Images.weapon[0], mini_x=Conf.win_width - 100,
                   mini_y=80),
            Weapon(name=Conf.weapon_names[1], time_reload=0.5, speed=15, power=4, volume=300,
                   img=Images.bulls[1], mini_img=Images.weapon[1], mini_x=Conf.win_width - 100,
                   mini_y=80))
        # 1 - blaster, 2 - fireball

    def upgrade_weapon_reload(self, name, new_reload):
        for weapon in self.weapons:
            print(weapon.name, name)
            if weapon.name == name:
                weapon.time_for_reload = new_reload

    def upgrade_weapon_power(self, name, new_power):
        for weapon in self.weapons:
            if weapon.name == name:
                weapon.power = new_power

    def change_weapon(self):
        if self.cur_weapon == 0:
            self.cur_weapon = 1
        else:
            self.cur_weapon = 0

    def fire(self):
        if self.weapons[self.cur_weapon].reloaded():
            self.bullets.add(
                self.weapons[self.cur_weapon].fire(x=self.rect.centerx,
                                                   y=self.rect.top))

    def update(self, events):
        self.bullets.update()
        self.health_bar.update(self.health)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_SPACE]:
            self.fire()
        for e in events:
            if e.type == pg.KEYDOWN and e.key == pg.K_r:
                self.change_weapon()

    def get_hit(self, power):
        self.health -= power

    def is_dead(self):
        return self.health <= 0

    def reset(self, win):
        super().reset(win)
        self.bullets.draw(win)
        self.health_display.reset(win)
        self.health_bar.draw(win)
        self.weapons[self.cur_weapon].draw(win)