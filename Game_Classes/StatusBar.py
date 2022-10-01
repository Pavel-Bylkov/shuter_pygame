from Game_Classes.Color import Color
from Game_Classes.Text import Text
import pygame as pg
import math
class StatusBar:
    def __init__(self, center_x, center_y, width=50, height=10, max_value=100):
        self.color = Color.GREEN
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
        self.color = Color.GREEN if self.cur_value / self.max_value > 0.2 else Color.RED
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