"""Создать дисплей и на нём с помощью модуля pygame.draw
нарисовать картинку из геометрических фигур. Создать округлую
зелёную  землю с помощью арки. С помощью прямоугольника и
треугольника нарисовать дом. Добавьте окружность для создания
солнца и окон домов. Лучики и перегородки окон можно сделать
 с помощью линий"""

import pygame as pg
import random
import sys  # модуль для выхода из игры и закрытия всех окон

pg.init()  # используется для старта модуля pygame
pg.display.set_caption("Pygame")  # задание заголовка окну
screen = pg.display.set_mode((800, 600), pg.RESIZABLE)  # создание поверхности с указанными размерами и параметрами
clock = pg.time.Clock()  # создаем экземпляр класса для управление времени(кадрами игры (fps))

play = True

def get_rand_color():
    return pg.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


rect_home = pg.Rect(350, 400, 100, 100)  # top_left_x, top_left_y, width, height
roof_home = ((350, 400), (400, 350), (450, 400))

rect_2 = pg.Rect(0, 0, 200, 100)  # top_left_x, top_left_y, width, height
rect_2.center = (100, 50)

# pg.display.flip() - обновление всего экрана
while play:  # основной цикл игры
    for event in pg.event.get():  # отслеживание всех событий которые происходят на игровом дисплее
        if event.type == pg.QUIT:  # если тип события = нажатию на крестик
            # play = False
            sys.exit()  # функция выхода из игры и закрытия всех окон
    screen.fill((60, 150, 30))

    pg.draw.circle(surface=screen, color=get_rand_color(), center=(400, 1500), radius=1050)

    pg.draw.rect(surface=screen, color=(30, 40, 150), rect=rect_home)

    pg.draw.polygon(surface=screen, color=(160, 40, 40), points=roof_home)

    pg.draw.rect(surface=screen, color=(30, 140, 150), rect=rect_2)

    # pg.draw.line()

    pg.display.update()  # - обновление части экрана, но если аргумент не указан, то обновляется весь
    clock.tick(1)  # устанавливаем максимальное указанное количество кадров


