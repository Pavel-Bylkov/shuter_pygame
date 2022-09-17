import pygame as pg
import Game_Classes.Conf as Conf


def create_img(filename, width, height):
    """конвертация любого формата изображений в формат pygame"""
    return pg.transform.scale(pg.image.load(filename), (width, height))


class Images:
    background = create_img(Conf.back, Conf.win_width, Conf.win_height)
    gameover = create_img(Conf.gameover, Conf.win_width, Conf.win_height)
    bum = [create_img(Conf.img_bum, i * 10, i * 10) for i in range(1, 11)]
    hero = create_img(Conf.hero, *Conf.hero_size)
    enemies = [create_img(img, *size) for img, size in Conf.enemies]
    bulls = [create_img(img, *size) for img, size in Conf.bulls]
    weapon = [create_img(img, *size) for img, size in Conf.weapon]