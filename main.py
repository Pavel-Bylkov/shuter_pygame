import pygame as pg
import random

# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # враг
img_over = "gameover.jpeg"
win_width, win_height = 1200, 800


class Hero(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(img_hero), (60, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400
        

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= 10
        if keys[pg.K_s]:
            self.rect.y += 10
        if keys[pg.K_a]:
            self.rect.x -= 10
        if keys[pg.K_d]:
            self.rect.x += 10

    def reset(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.speed = speed
        self.image = pg.transform.scale(pg.image.load(img_enemy), (70, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-self.speed, self.speed)
        if self.rect.y > win_height:
            self.rect.y = -50
            self.rect.x = random.randint(30, win_height - 30)

    def reset(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

# запускаем инициализацию pygame - настройка на наше железо
pg.init()

# Создаем окошко
pg.display.set_caption("Shooter")  # Title у окна
window = pg.display.set_mode((win_width, win_height))
back_img = pg.image.load(img_back)  # конвертация любого формата изображений в формат pygame
background = pg.transform.scale(back_img, (win_width, win_height))

gameover = pg.transform.scale(pg.image.load(img_over), (win_width, win_height))

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

    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))

        hero.update()
        hero.reset(window)

        monster.update()
        monster.reset(window)

        # window.blit(gameover, (0, 0))

        pg.display.update()

    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(40)