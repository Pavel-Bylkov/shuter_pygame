import pygame as pg
import random
import time

# todo add give many and pay upgrades
# todo add level boss
# todo diff enemys and boss
# todo add store with weapon strangth, firrate, restore HP
# todo при смене оружия выводить сообщение или показывать на экране тип текущего оружия

FPS = 20

stop_spawn = False

# запускаем инициализацию pygame - настройка на наше железо
pg.init()
pg.font.init()

win_width, win_height = 1200, 800
# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
# конвертация любого формата изображений в формат pygame
back_img = pg.image.load(img_back)
background = pg.transform.scale(back_img, (win_width, win_height))
# герой
img_hero = pg.transform.scale(pg.image.load("rocket.png"), (60, 80))
# враг
img_enemy = pg.transform.scale(pg.image.load("ufo.png"), (70, 50))
img_enemy2 = pg.transform.scale(pg.image.load("ship.png"), (50, 60))
img_enemy3 = pg.transform.scale(pg.image.load("ship_star-wars.png"), (50, 60))
img_enemy4 = pg.transform.scale(pg.image.load("mandocruiser.png"), (60, 80))
# подготавливаем картинку для геймовера
gameover = pg.transform.scale(pg.image.load("gameover.jpeg"), (win_width, win_height))
img_bull = pg.transform.scale(pg.image.load("fire_blue.png"), (10, 10))
img_bull2 = pg.transform.scale(pg.image.load("blaster.png"), (15, 15))
img_bum = "Взрыв4.png"
images_for_bum = []
for i in range(1, 11):
    images_for_bum.append(
        pg.transform.scale(pg.image.load(img_bum), (i * 10, i * 10))
    )

# цвета
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
YELLOW_COLOR = (255, 255, 0)


class Text:
    def __init__(self, x, y, font=None, font_size=50, text="Test", color=WHITE_COLOR):
        # создаем шрифт
        self.font = pg.font.Font(font, font_size)
        # Картинка из шрифта
        self.color = color
        self.image = self.font.render(text, 1, self.color)
        self.x = x
        self.y = y

    def update(self, text):
        self.image = self.font.render(text, 1, self.color)

    def change_color(self, new_color):
        self.color = new_color

    def change_pos(self, x, y):
        self.x = x
        self.y = y

    def reset(self, win):
        win.blit(self.image, (self.x, self.y))

class Base(pg.sprite.Sprite):
    def __init__(self, x, y, speed, img, *args, **kwargs):
        super().__init__(*args)
        self.speed = speed
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Hero(Base):
    def __init__(self, x, y, speed):
        super().__init__(x=x, y=y, speed=speed, img=img_hero)
        self.bullets = pg.sprite.Group()
        self.reload = time.time()
        self.health = 100
        self.health_display = Text(x=20, y=90, text="Health: 100", font_size=30)
        self.cur_weapon = 1
        # 1 - blaster, 2 - fireball

    def change_weapon(self):
        if self.cur_weapon == 1:
            self.cur_weapon = 2
        else:
            self.cur_weapon = 1

    def fire(self):
        if self.cur_weapon == 1:
            if time.time() - self.reload > 0.15:
                self.bullets.add(
                    Bullet(x=self.rect.centerx, y=self.rect.top, speed=10,
                           power=1, img=img_bull)
                )
                self.reload = time.time()
        else:
            if time.time() - self.reload > 0.5:
                self.bullets.add(
                    Bullet(x=self.rect.centerx, y=self.rect.top, speed=15,
                           power=4, img=img_bull2)
                )
                self.reload = time.time()

    def update(self):
        self.bullets.update()
        self.health_display.update(f"Health: {self.health}")
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        if keys[pg.K_d]:
            self.rect.x += self.speed
        if keys[pg.K_r] or keys[pg.K_t]:
            self.change_weapon()
        if keys[pg.K_SPACE]:
            self.fire()

    def get_hit(self, power):
        self.health -= power

    def is_dead(self):
        return self.health <= 0

    def reset(self, win):
        super().reset(win)
        self.bullets.draw(win)
        self.health_display.reset(win)

class Enemy(Base):
    def __init__(self, x, y, speed, health, img):
        super().__init__(x=x, y=y, speed=speed, img=img)
        self.health = health
        self.power = health
        self.health_display = Text(x=self.rect.x, y=(self.rect.y-15),
                                   text=f"{self.health}", font_size=20)

    def move(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-self.speed, self.speed)

    def is_lose(self):
        if self.rect.y > win_height + 50:
            self.kill()
            return True
        return False

    def health_draw(self, win):
        self.health_display.reset(win)

    def update(self):
        self.move()
        self.health_display.change_pos(self.rect.x, self.rect.y - 15)
        self.health_display.update(f"{self.health}")



class Enemy2(Enemy):

    def move(self):
        self.rect.y += self.speed

class Bullet(Base):
    def __init__(self, x, y, speed, power, img):
        super().__init__(x=x, y=y, speed=speed, img=img)
        self.power = power

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Bum(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = images_for_bum[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.count = 0

    def update(self):
        self.count += 1
        if self.count == 10:
            self.kill()
        else:
            x = self.rect.centerx
            y = self.rect.centery
            self.image = images_for_bum[self.count]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.centery = y

    def reset(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


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
        if type == 1:
            return Enemy(x=random.randint(3, win_width // 10 - 4) * 10,
                      y=random.randint(-50, -10),
                      speed=4, health=4, img=img_enemy)
        elif type == 2:
            return Enemy2(x=random.randint(3, win_width // 10 - 4) * 10,
                      y=random.randint(-50, -10),
                      speed=7, health=2, img=img_enemy3)
        elif type == 3:
            return Enemy2(x=random.randint(3, win_width // 10 - 4) * 10,
                      y=random.randint(-50, -10),
                      speed=2, health=10, img=img_enemy2)
        elif type == 4:
            return Enemy2(x=random.randint(3, win_width // 10 - 4) * 10,
                      y=random.randint(-50, -10),
                      speed=2, health=12, img=img_enemy4)


class Controller:
    def __init__(self):
        # Создаем окошко
        pg.display.set_caption("Shooter")  # Title у окна
        self.window = pg.display.set_mode((win_width, win_height))
        # создаем спрайты
        self.hero = Hero(x=500, y=700, speed=12)
        self.monsters1 = pg.sprite.Group()
        self.bums = pg.sprite.Group()
        self.levels = [
            Level(1, {1: 5}),
            Level(2, {1: 7}),
            Level(3, {1: 5, 2: 5}),
            Level(4, {1: 10, 2: 5}),
            Level(5, {3: 5}),
            Level(6, {3: 5, 4: 3})
        ]
        self.cur_level = self.levels.pop(0)
        self.timer = time.time()
        self.pause = True
        self.pause_timer = time.time()
        self.coins = 0
        self.level_display = Text(x=20, y=5, text="LEVEL: 1", font_size=30)
        self.coins_display = Text(x=20, y=35, text="Coins: 0", font_size=30)
        self.result_display = None


    def draw(self):
        # обновляем фон
        self.window.blit(background, (0, 0))
        self.hero.reset(self.window)
        self.bums.draw(self.window)
        self.monsters1.draw(self.window)
        for monster in self.monsters1:
            monster.health_draw(self.window)
        self.level_display.reset(self.window)
        self.coins_display.reset(self.window)
        if self.pause:
            level_display = Text(x=win_width // 2 - 150, y=win_height // 2 - 50,
                                 text=f"LEVEL {self.cur_level.number}",
                                 font_size=150, color=GREEN_COLOR)
            level_display.reset(self.window)
        if finish:
            self.result_display.reset(self.window)

    def monsters_update(self):
        for monster in self.monsters1:
            monster.update()
            if monster.is_lose():
                self.hero.get_hit(monster.health)
            if pg.sprite.collide_rect(monster, self.hero):
                self.hero.get_hit(monster.health)
                monster.health = 0
            coll = pg.sprite.spritecollide(monster, self.hero.bullets, True)
            for bull in coll:
                monster.health -= bull.power
            if monster.health <= 0:
                self.bums.add(
                    Bum(monster.rect.centerx, monster.rect.centery)
                )
                self.coins += monster.power
                monster.kill()

    def update(self):
        if not self.pause:
            self.hero.update()
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
        global finish

        finish = True
        self.result_display = Text(x=win_width//2-250, y=win_height//2-50,
                                   text="GAME OVER",
                           font_size=150, color=RED_COLOR)

    def game_win(self):
        global finish

        finish = True
        self.result_display = Text(x=win_width//2-150, y=win_height//2-50, text="WIN",
                           font_size=150, color=GREEN_COLOR)



# чтобы работала группа, необходимо наследоваться от pg.sprite.Sprite
controller = Controller()


# переменная "игра закончилась": как только там True,
# в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна

clock = pg.time.Clock()
while run:
    # событие нажатия на кнопку Закрыть
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    if not finish:
        controller.update()
        controller.draw()
        pg.display.update()

    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(FPS)