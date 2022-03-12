import pygame as pg
import random
import time

# todo Добавить режимы игр
# ToDo make it so that when rocket and ufo interact the ufo
# disappears and u get point not u lose game
# todo add give many and pay upgrades
# todo add levels and boss
# todo diff enemys and boss
# todo add store with weapon strangth, firrate, restore HP
# todo add controller spawn monsters with level limits


FPS = 20

coins = 0
level = 1

limits_levels = [10, 20, 30]
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
# подготавливаем картинку для геймовера
gameover = pg.transform.scale(pg.image.load("gameover.jpeg"), (win_width, win_height))
img_bull = pg.transform.scale(pg.image.load("fireball.png"), (15, 15))
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
        if keys[pg.K_t]:
            self.change_weapon()
        if self.cur_weapon == 1:
            if keys[pg.K_SPACE] and time.time() - self.reload > 0.15:
                self.bullets.add(
                    Bullet(x=self.rect.centerx, y=self.rect.top, speed=10,
                           power=random.randint(1, 2))
                )
                self.reload = time.time()
        else:
            if keys[pg.K_SPACE] and time.time() - self.reload > 0.5:
                self.bullets.add(
                    Bullet(x=self.rect.centerx, y=self.rect.top, speed=15,
                           power=random.randint(3, 5))
                )
                self.reload = time.time()

    def get_hit(self, power):
        self.health -= power
        if self.health <= 0:
            game_over()

    def reset(self, win):
        super().reset(win)
        self.bullets.draw(win)
        self.health_display.reset(win)

class Enemy(Base):
    def __init__(self, x, y, speed, health):
        super().__init__(x=x, y=y, speed=speed, img=img_enemy)
        self.health = health
        self.power = health
        self.health_display = Text(x=self.rect.x, y=(self.rect.y-15),
                                   text=f"{self.health}", font_size=20)

    def move(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-self.speed, self.speed)

    def update(self, player, bums, win):
        global coins

        self.move()
        self.health_display.change_pos(self.rect.x, self.rect.y - 15)
        if self.rect.y > win_height + 50:
            self.kill()
            player.get_hit(self.power)
        if pg.sprite.collide_rect(self, player):
            player.get_hit(self.power)
            self.health = 0
        coll = pg.sprite.spritecollide(self, player.bullets, True)
        if coll:
            for bull in coll:
                self.health -= bull.power
        if self.health <= 0:
            bums.add(
                Bum(self.rect.centerx, self.rect.centery)
            )
            self.kill()
            coins += self.power

        self.health_display.update(f"{self.health}")
        self.health_display.reset(win)


class Enemy2(Enemy):

    def move(self):
        self.rect.y += self.speed

class Bullet(Base):
    def __init__(self, x, y, speed, power):
        super().__init__(x=x, y=y, speed=speed, img=img_bull)
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


class Controller:
    def __init__(self):
        self.monsters1 = pg.sprite.Group()
        self.levels = {
            1: {1: 10},
            2: {1: 15, 2: 5},
            3: {1: 10, 2: 10}
        }
        self.level = 1
        self.timer = time.time()
        self.level_display = Text(x=20, y=5, text="LEVEL: 1", font_size=30)
        self.coins_display = Text(x=20, y=35, text="Coins: 0", font_size=30)

    def get_next_monster(self):
        level = self.levels[self.level]
        if len(level) == 0 and len(self.levels) > 0:
            del self.levels[self.level]
            self.level += 1
        if len(self.levels) == 0:
            game_win()
            return
        #todo error ValueError: min() arg is an empty sequence

        type = random.randint(min(level), max(level))
        self.levels[self.level][type] -= 1
        if self.levels[self.level][type] == 0:
            del self.levels[self.level][type]
        if type == 1:
            self.monsters1.add(
                Enemy(x=random.randint(3, win_width // 10 - 4) * 10,
                      y=random.randint(-500, -30),
                      speed=random.randint(3, 7), health=4)
            )
        elif type == 2:
            self.monsters1.add(
                Enemy2(x=random.randint(3, win_width // 10 - 4) * 10,
                      y=random.randint(-500, -30),
                      speed=random.randint(3, 7), health=10)
            )

    def update(self, hero, bums, window):
        if time.time() - self.timer >= 1:
            self.get_next_monster()
            self.timer = time.time()
        self.monsters1.update(hero, bums, window)
        self.monsters1.draw(window)
        self.level_display.update(f"LEVEL: {level}")
        self.level_display.reset(window)
        self.coins_display.update(f"Coins: {coins}")
        self.coins_display.reset(window)


def game_over():
    global finish

    finish = True
    window.blit(gameover, (0, 0))

def game_win():
    global finish

    finish = True
    win_display = Text(x=win_width//2, y=win_height//2, text="WIN",
                       font_size=150, color=GREEN_COLOR)
    win_display.reset(window)

# Создаем окошко
pg.display.set_caption("Shooter")  # Title у окна
window = pg.display.set_mode((win_width, win_height))

# создаем спрайты
hero = Hero(x=500, y=700, speed=12)

# чтобы работала группа, необходимо наследоваться от pg.sprite.Sprite
controller = Controller()


bums = pg.sprite.Group()

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
        # обновляем фон
        window.blit(background, (0, 0))

        hero.update()
        hero.reset(window)

        controller.update(hero, bums, window)

        bums.update()
        bums.draw(window)

        pg.display.update()

    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(FPS)