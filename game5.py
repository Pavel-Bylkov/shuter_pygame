#!./venv/bin/python3
import pygame as pg
import random
import time
import sys
import math

from Game_Classes import *

# todo add give many and pay upgrades
# todo add store with weapon strangth, firrate, restore HP

# запускаем инициализацию pygame - настройка на наше железо
pg.init()
pg.font.init()





main_win = Window(Conf.win_width, Conf.win_height, Conf.title)
main_win.run()
