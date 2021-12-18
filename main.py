import pygame as pg
import random

# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # враг
win_width, win_height = 1200, 800


class Hero:
    def __init__(self):
        self.x = 500
        self.y = 400
        self.image = pg.transform.scale(pg.image.load(img_hero), (60, 80))

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.y -= 10
        if keys[pg.K_s]:
            self.y += 10
        if keys[pg.K_a]:
            self.x -= 10
        if keys[pg.K_d]:
            self.x += 10

    def reset(self, win):
        win.blit(self.image, (self.x, self.y))


class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pg.transform.scale(pg.image.load(img_enemy), (70, 50))

    def update(self):
        self.y += self.speed
        self.x += random.randint(-self.speed, self.speed)
        if self.y > win_height:
            self.y = -50
            self.x = random.randint(30, win_height - 30)

    def reset(self, win):
        win.blit(self.image, (self.x, self.y))

# запускаем инициализацию pygame - настройка на наше железо
pg.init()

# Создаем окошко
pg.display.set_caption("Shooter")  # Title у окна
window = pg.display.set_mode((win_width, win_height))
back_img = pg.image.load(img_back)  # конвертация любого формата изображений в формат pygame
background = pg.transform.scale(back_img, (win_width, win_height))

# создаем спрайты
hero = Hero()

monster = Enemy(x=win_width//2, y=0, speed=5)

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
        # if e.type == pg.KEYDOWN:
        #     if e.key == pg.K_w:
        #         hero_y -= 10
        #     if e.key == pg.K_s:
        #         hero_y += 10
        #     if e.key == pg.K_a:
        #         hero_x -= 10
        #     if e.key == pg.K_d:
        #         hero_x += 10

    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))

        hero.update()
        hero.reset(window)

        monster.update()
        monster.reset(window)

        pg.display.update()

    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(40)