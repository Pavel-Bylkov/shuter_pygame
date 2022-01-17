import pygame as pg
import random

# todo Добавить режимы игры
# Todo Добавить взрывы и стрельбу
# todo Добавить вывод информации на экран - текст
#ToDo make it so that when rocket and ufo interact the ufo
# disappears and u get point not u lose game


# запускаем инициализацию pygame - настройка на наше железо
pg.init()
pg.font.init()

# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"  # враг
img_over = "gameover.jpeg"
win_width, win_height = 1200, 800

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

class Hero(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 12
        self.image = pg.transform.scale(pg.image.load(img_hero), (60, 80))
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 400

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y -= self.speed
        if keys[pg.K_s]:
            self.rect.y += self.speed
        if keys[pg.K_a]:
            self.rect.x -= self.speed
        if keys[pg.K_d]:
            self.rect.x += self.speed

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



# Создаем окошко
pg.display.set_caption("Shooter")  # Title у окна
window = pg.display.set_mode((win_width, win_height))
back_img = pg.image.load(img_back)  # конвертация любого формата изображений в формат pygame
background = pg.transform.scale(back_img, (win_width, win_height))

# подготавливаем картинку для геймовера
gameover = pg.transform.scale(pg.image.load(img_over), (win_width, win_height))

# создаем спрайты
hero = Hero()

# создаем надписи на экране
score_display = Text(x=20, y=30, text="Score: 0", font_size=30)
score = 0

lives_display = Text(x=20, y=60, text="Lives: 3", font_size=30)
lives = 3

# чтобы работала группа, необходимо наследоваться от pg.sprite.Sprite
monsters = pg.sprite.Group()
for k in range(5):
    monsters.add(
        Enemy(x=random.randint(3, win_width // 10 - 3) * 10,
              y=random.randint(-500, -30),
              speed=random.randint(3, 7))
    )


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

        monsters.update()
        monsters.draw(window)

        score_display.update(f"Score: {score}")
        score_display.reset(window)
        lives_display.update(f"Lives: {lives}")
        lives_display.reset(window)

        if pg.sprite.spritecollide(hero, monsters, True):
            window.blit(gameover, (0, 0))
            finish = True

        pg.display.update()

    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(30)