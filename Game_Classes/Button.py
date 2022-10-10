from Game_Classes.Conf import Conf
from Game_Classes.Text import Text
from Game_Classes.Color import Color
import pygame as pg
class Button:
    def __init__(self, filename="",
                 pos=(Conf.win_width//2, Conf.win_height//2),
                 size=(Conf.win_width//4, Conf.win_height//10),
                 on_click=(lambda: None), text="", attr=None,
                 text_color=Color.WHITE, fill_not_activ=(0, 0, 0),
                 fill_activ=(60, 60, 60), active=False, visible=True):
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
        self.fill_not_activ = fill_not_activ
        self.fill_activ = fill_activ
        self.on_click = on_click
        self.visible = visible
        self.active = active
        self.attr = attr

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def reset(self, win):
        if self.visible:
            if self.image is None and not self.active:
                pg.draw.rect(win, self.fill_not_activ, self.rect)
                pg.draw.rect(win, (0, 0, 0), self.rect, 1)
            elif self.image is None and self.active:
                pg.draw.rect(win, self.fill_activ, self.rect)
                pg.draw.rect(win, (0, 0, 0), self.rect, 1)
            else:
                win.blit(self.image, self.rect)
            self.text.reset(win)

    def not_active(self):
        self.active = False

    def update(self, events):
        if self.visible:
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.rect.collidepoint(*event.pos):
                        self.active = True
                        if self.attr is None:
                            result = self.on_click()
                        elif isinstance(self.attr, list):
                            result = self.on_click(*self.attr)
                        elif isinstance(self.attr, dict):
                            result = self.on_click(**self.attr)
                        else:
                            result = self.on_click(self.attr)
                        if result is not None and not result:
                            self.fill_not_activ = (120, 120, 120)