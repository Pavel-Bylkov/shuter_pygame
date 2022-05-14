#!./venv/bin/python3
import pygame as pg
import random
import time
import sys
import math

# todo add give many and pay upgrades
# todo add store with weapon strangth, firrate, restore HP

# запускаем инициализацию pygame - настройка на наше железо
pg.init()
pg.font.init()


def create_img(filename, width, height):
    """конвертация любого формата изображений в формат pygame"""
    return pg.transform.scale(pg.image.load(filename), (width, height))


class Conf:
    win_width = 1200
    win_height = 800
    title = "Shooter"
    # фон игры
    back = "galaxy.jpg"  
    # герой
    hero = "rocket.png"
    hero_size = (60, 80)
    # враг
    enemies = (("ufo.png", (70, 50)), ("ship.png", (50, 60)),
               ("ship_star-wars.png", (50, 60)), ("mandocruiser.png", (60, 80)))
    gameover = "gameover.jpeg"
    # пули
    bulls = ("fire_blue.png", (10, 10)), ("fireball.png", (20, 20))
    # взрыв
    img_bum = "Взрыв4.png"
    music = ("Sound/gamesound.wav", "Sound/cowboy.wav",
             "Sound/happy.wav", "Sound/sample.wav")
    weapon = ("rocket2.png", (60, 60)), ("rocket3.png", (60, 60))
    weapon_names = ("Rocket", "Stinger")
    sound = {
        weapon_names[0]: "sounds/laser2.wav", weapon_names[1]: "sounds/laser4.wav",
        "lose": "Sound/point.wav", "bum": "sounds/boom.mp3",
        "change_level": "sounds/upgrade1.wav",
        "win": "sounds/money.mp3", "gameover": "sounds/gameover1.wav"}
    FPS = 20


class Images:
    background = create_img(Conf.back, Conf.win_width, Conf.win_height)
    gameover = create_img(Conf.gameover, Conf.win_width, Conf.win_height)
    bum = [create_img(Conf.img_bum, i * 10, i * 10) for i in range(1, 11)]
    hero = create_img(Conf.hero, *Conf.hero_size)
    enemies = [create_img(img, *size) for img, size in Conf.enemies]
    bulls = [create_img(img, *size) for img, size in Conf.bulls]
    weapon = [create_img(img, *size) for img, size in Conf.weapon]


# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Text:
    def __init__(self, x, y, font=None, font_size=50, text="Test", color=WHITE):
        # создаем шрифт
        self.font = pg.font.Font(font, font_size)
        # Картинка из шрифта
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, text):
        x = self.rect.centerx
        y = self.rect.centery
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=(x, y))

    def change_color(self, new_color):
        self.color = new_color

    def change_pos(self, x, y):
        self.rect.center = (x, y)

    def set_italic(self, value):
        self.font.set_italic(value)

    def set_bold(self, value):
        self.font.set_bold(value)

    def reset(self, win):
        win.blit(self.image, self.rect)


class Base(pg.sprite.Sprite):
    def __init__(self, x, y, speed, img, *args, **kwargs):
        super().__init__(*args)
        self.speed = speed
        self.image = img
        self.rect = self.image.get_rect(center=(x, y))

    def reset(self, win):
        win.blit(self.image, self.rect)


class StatusBar:
    def __init__(self, center_x, center_y, width=50, height=10, max_value=100):
        self.color = GREEN
        self.text = Text(text=f" {max_value}", color=self.color,
                         x=center_x, y=center_y, font_size=height+2)
        self.rect = pg.Rect(center_x - width//2, center_y - height//2,
                            width - self.text.rect.width, height)
        self.max_value = max_value
        self.cur_value = max_value
        self.text.rect.left = self.rect.right

    def correct_pos(self, left, center_y):
        self.rect.centery = center_y
        self.rect.left = left
        self.text.rect.left = self.rect.right
        self.text.rect.centery = center_y

    def update(self, new_value):
        self.cur_value = new_value
        self.color = GREEN if self.cur_value / self.max_value > 0.2 else RED
        self.text.update(f" {new_value}")
        self.text.change_color(self.color)

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect, width=1)
        rect = pg.Rect(self.rect.x, self.rect.y,
                       self.rect.width//10, self.rect.height)
        start_x = self.rect.x
        for i in range(math.ceil(self.cur_value / self.max_value * 10)):
            rect.x = start_x + self.rect.width//10 * i
            pg.draw.rect(win, self.color, rect)
        self.text.reset(win)


class Weapon:
    def __init__(self, name, time_reload, speed, power, volume, img,
                 mini_img=None, mini_x=0, mini_y=0):
        self.name = Text(text=f"Weapon: {name}", x=0, y=0, font_size=30)
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
            self.name.change_pos(self.rect.centerx, self.rect.top)
            self.display_volume = StatusBar(self.rect.centerx, self.rect.bottom,
                                            width=self.name.rect.width, height=20,
                                            max_value=volume)

    def draw(self, win):
        if self.mini_img is not None:
            win.blit(self.mini_img, self.rect)
            self.name.reset(win)
            self.display_volume.update(self.volume)
            self.display_volume.draw(win)

    def reloaded(self):
        if self.volume == 0:
            return False
        return time.time() - self.reload > self.time_for_reload

    def fire(self, x, y, direction=1):
        bullet = Bullet(x=x, y=y, speed=self.speed, power=self.power, img=self.img,
                        direction=direction)
        self.reload = time.time()
        self.volume -= 1
        self.sound.set_volume(sounds.volume - 0.2)
        self.sound.play()
        return bullet


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


class Enemy(Base):
    def __init__(self, x, y, speed, health, img):
        super().__init__(x=x, y=y, speed=speed, img=img)
        self.health = health
        self.power = health
        self.health_display = Text(x=self.rect.centerx, y=(self.rect.top-15),
                                   text=f"{self.health}", font_size=20)

    def move(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-self.speed, self.speed)

    def is_lose(self):
        if self.rect.y > Conf.win_height + 50:
            self.kill()
            return True
        return False

    def health_draw(self, win):
        self.health_display.reset(win)

    def update(self):
        self.move()
        self.health_display.change_pos(x=self.rect.centerx, y=(self.rect.top-15))
        self.health_display.update(f"{self.health}")

    def is_dead(self):
        return self.health <= 0


class Enemy2(Enemy):
    def move(self):
        self.rect.y += self.speed


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


class Bullet(Base):
    def __init__(self, x, y, speed, power, img, direction=1):
        super().__init__(x=x, y=y, speed=speed, img=img)
        self.power = power
        self.direction = direction

    def update(self):
        if self.direction == 1:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if self.rect.y < 0 or self.rect.y > Conf.win_height + 50:
            self.kill()

    @staticmethod
    def bullet_collide(sprite, bull_group):
        coll = pg.sprite.spritecollide(sprite, bull_group, True)
        for bull in coll:
            sprite.health -= bull.power


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


class Level:
    def __init__(self, number, n_type):
        self.number = number
        self.n_type = n_type

    def __len__(self):
        return len(self.n_type)

    def is_end_level(self):
        return len(self.n_type) == 0

    def get_next_monster(self):
        types = list(self.n_type.keys())
        random.shuffle(types)
        type = types.pop()
        self.n_type[type] -= 1
        if self.n_type[type] == 0:
            del self.n_type[type]
        x = random.randint(3, Conf.win_width // 10 - 4) * 10
        y = random.randint(-50, -10)
        new_enemy = {
            1: Enemy(x=x, y=y, speed=4, health=4, img=Images.enemies[0]),
            2: Enemy2(x=x, y=y, speed=7, health=2, img=Images.enemies[2]),
            3: Enemy2(x=x, y=y, speed=2, health=10, img=Images.enemies[1]),
            4: Boss(x=x, y=10, speed=2, health=50, img=Images.enemies[3], power=3),
            5: Boss(x=x, y=10, speed=2, health=100, img=Images.enemies[3], power=5)}
        return new_enemy[type]


class Game:
    def __init__(self, window):
        self.window = window
        self.scr = window.screen
        self.width = window.width
        self.height = window.height
        # создаем спрайты
        self.hero = Hero(x=500, y=700, speed=12)
        self.monsters1 = pg.sprite.Group()
        self.bums = pg.sprite.Group()
        self.levels = [
            Level(1, {1: 5}),
            Level(2, {1: 7}),
            Level(3, {1: 5, 2: 5}),
            Level(4, {1: 10, 2: 5}),
            Level(5, {3: 5, 4: 1}),
            Level(6, {3: 10, 5: 1})
        ]
        self.cur_level = self.levels.pop(0)
        self.timer = time.time()
        self.pause = True
        self.pause_timer = time.time()
        self.coins = 0
        self.level_display = Text(x=50, y=25, text="LEVEL: 1", font_size=30)
        self.coins_display = Text(x=55, y=55, text="Coins: 0", font_size=30)
        self.result_display = None
        self.finish = False

    def on_show(self):
        """Выполняется один раз при запуске или переключении вида"""
        self.finish = False

    def on_draw(self):
        # обновляем фон
        self.scr.blit(Images.background, (0, 0))
        self.hero.reset(self.scr)
        self.bums.draw(self.scr)
        self.monsters1.draw(self.scr)
        for monster in self.monsters1:
            monster.health_draw(self.scr)
            monster.reset(self.scr)
        self.level_display.reset(self.scr)
        self.coins_display.reset(self.scr)
        if self.pause:
            level_display = Text(x=self.width // 2, y=self.height // 2,
                                 text=f"LEVEL {self.cur_level.number}",
                                 font_size=150, color=GREEN)
            level_display.reset(self.scr)
        if self.finish:
            self.result_display.reset(self.scr)

    def monsters_update(self):
        for monster in self.monsters1:
            monster.update()
            if isinstance(monster, Boss):
                monster.change_move(self.hero)
                monster.update_fire()
                if monster.check_fire(self.hero):
                    monster.fire()
                Bullet.bullet_collide(self.hero, monster.bullets)
            if monster.is_lose():
                self.hero.get_hit(monster.health)
            if pg.sprite.collide_rect(monster, self.hero):
                self.hero.get_hit(monster.health)
                monster.health = 0
            Bullet.bullet_collide(monster, self.hero.bullets)
            if monster.is_dead():
                self.bums.add(
                    Bum(monster.rect.centerx, monster.rect.centery)
                )
                self.coins += monster.power
                monster.kill()

    def on_update(self, events):
        if not self.pause:
            self.hero.update(events)
            self.bums.update()
            if time.time() - self.timer >= random.randint(1, 3):
                self.timer = time.time()
                if len(self.cur_level) == 0:
                    if len(self.monsters1) == 0 and len(self.levels) != 0:
                        self.level_change()
                else:
                    self.monsters1.add(self.cur_level.get_next_monster())
            if (len(self.levels) == 0 and self.cur_level.is_end_level()
                    and len(self.monsters1) == 0):
                self.game_win()
            else:
                self.monsters_update()
        elif time.time() - self.pause_timer >= 2:
            self.pause = False
        if self.hero.is_dead():
            self.game_over()
        self.level_display.update(f"LEVEL: {self.cur_level.number}")
        self.coins_display.update(f"Coins: {self.coins}")

    def level_change(self):
        self.cur_level = self.levels.pop(0)
        self.pause = True
        self.pause_timer = time.time()

    def game_over(self):
        self.finish = True
        self.result_display = Text(x=self.width//2, y=self.height//2,
                                   text="GAME OVER", font_size=150, color=RED)

    def game_win(self):
        self.finish = True
        self.result_display = Text(x=self.width//2, y=self.height//2,
                                   text="WIN", font_size=150, color=GREEN)

    def on_resize(self):
        self.width = self.window.width
        self.height = self.window.height


class Button:
    def __init__(self, win, filename="",
                 pos=(Conf.win_width//2, Conf.win_height//2),
                 size=(Conf.win_width//4, Conf.win_height//10),
                 on_click=(lambda: None), text="",
                 text_color=WHITE, fill=(0, 0, 0)):
        self.win = win
        self.image = None
        if filename:
            menu = pg.image.load(filename)  # загрузка картинок для меню
            self.image = pg.transform.scale(menu, size)  # изменение размера
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = pg.Rect(0, 0, *size)
            self.rect.center = pos
        self.text = Text(text=text, color=text_color, font_size=40,
                         x=self.rect.centerx, y=self.rect.centery)
        self.fill = fill
        self.on_click = on_click

    def draw(self):
        if self.image is None:
            pg.draw.rect(self.win, self.fill, self.rect)
        else:
            self.win.blit(self.image, self.rect)
        self.text.reset(self.win)

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.rect.collidepoint(*event.pos):
                    self.on_click()


class Menu:
    def __init__(self, win, filename="",
                 pos=(Conf.win_width//2, Conf.win_height//2),
                 size=(Conf.win_width//2, Conf.win_height//2),
                 fill=(60, 60, 60), title="",
                 text_color=WHITE):
        self.win = win
        self.image = None
        if filename:
            menu = pg.image.load(filename)  # загрузка картинок для меню
            self.image = pg.transform.scale(menu, size)  # изменение размера
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = pg.Rect(0, 0, *size)
            self.rect.center = pos
        self.fill = fill
        self.title = Text(text=title, color=text_color, font_size=60,
                          x=self.rect.centerx, y=self.rect.top+40)
        self.title.set_italic(True)
        self.title.set_bold(True)
        self.buttons = ButtonGroup()

    def add_button(self, button):
        self.buttons.add(button)

    def draw(self):
        if self.image is None:
            pg.draw.rect(self.win, self.fill, self.rect)
        else:
            self.win.blit(self.image, self.rect)
        self.title.reset(self.win)
        self.buttons.draw()

    def run(self):
        play = True
        clock = pg.time.Clock()
        while play:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    sounds.control(event.key)
                    if event.key == pg.K_ESCAPE:
                        play = False
            sounds.update()
            self.draw()
            self.buttons.update(events)
            pg.display.update(self.rect)
            clock.tick(60)


class Popup(Menu):
    def __init__(self, win, filename="",
                 pos=(Conf.win_width//2, Conf.win_height//2),
                 size=(Conf.win_width//2, Conf.win_height//2),
                 fill=(60, 60, 60), title="",
                 text_color=WHITE):
        super(Popup, self).__init__(win, filename, pos, size, fill, title,text_color)

    def new_metod(self):
        pass

class ButtonGroup(list):
    def add(self, button) -> None:
        if isinstance(button, Button):
            super().append(button)
        else:
            raise TypeError("Type must be is Button")

    def draw(self, *args, **kwargs):
        for button in self:
            button.draw(*args, **kwargs)

    def update(self, *args, **kwargs):
        for button in self:
            button.update(*args, **kwargs)


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


class Window:
    def __init__(self, width, height, title, resizable=True) -> None:
        # Создаем окошко
        pg.display.set_caption(title)  # Title у окна
        if resizable:
            self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)
        else:
            self.screen = pg.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.game = Game(self)
        self.main_menu = Menu(win=self.screen, filename="base_menu.png",
                              title="Main Menu", text_color=(0, 0, 0))
        self.menu_settings = Menu(win=self.screen, filename="base_menu.png",
                                  title="Settings", text_color=(0, 0, 0))
        self.main_menu.add_button(
            Button(win=self.screen, filename="",
                   pos=(Conf.win_width//2, Conf.win_height//2 - 40),
                   size=(150, 60), text="Settings", on_click=self.menu_settings.run,
                   text_color=WHITE, fill=(200, 50, 50)))
        self.main_menu.add_button(
            Button(win=self.screen, filename="",
                   pos=(Conf.win_width//2, Conf.win_height//2 + 60),
                   size=(150, 60), text="Quit", on_click=sys.exit,
                   text_color=WHITE, fill=(50, 200, 50)))

    def resize(self):
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        # если где-то используется этот параметр, то его тоже нужно обновить
        Conf.win_width = self.width
        Conf.win_height = self.height
        self.game.on_resize()

    def run(self):
        # Основной цикл игры:
        run = True  # флаг сбрасывается кнопкой закрытия окна
        clock = pg.time.Clock()
        self.game.on_show()
        while run:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    run = False
                if e.type == pg.WINDOWSIZECHANGED:
                    self.resize()
                if e.type == pg.KEYDOWN:
                    sounds.control(e.key)
                    if e.key == pg.K_ESCAPE:
                        self.main_menu.run()
            sounds.update()
            self.game.on_update(events)
            self.game.on_draw()

            pg.display.update()
            clock.tick(Conf.FPS)


sounds = Music()  # создаем сингелтон объект для управления музыкой
sounds.add(*Conf.music)
sounds.play()

main_win = Window(Conf.win_width, Conf.win_height, Conf.title)
main_win.run()
