from Game_Classes.Button import Button
from Game_Classes.Conf import Conf
from Game_Classes.Menu import Menu
from Game_Classes.ButtonGroup import ButtonGroup
from Game_Classes.Color import Color
from Game_Classes.Music import sounds
import sys
import pygame as pg
class SubMenu(Menu):
    def __init__(self, win, chapters, filename="",
                 pos=(Conf.win_width//2, Conf.win_height//2),
                 size=(Conf.win_width//4*3, Conf.win_height//4*3),
                 fill=(60, 60, 60), title="",
                 text_color=Color.WHITE):
        super().__init__(win, filename, pos, size, fill, title, text_color)
        self.surfaces = []
        self.colors = []
        self.cur_surface = None
        self.collect_widgets = ButtonGroup()
        listcolor = [Conf.option_act, Conf.option_notact]
        for i, chapter in enumerate(chapters):
            color = listcolor [1]
            self.surfaces.append(pg.Surface(size))
            width_button = size[0]//len(chapters)
            self.buttons.add(
                Button(pos=(width_button * i + self.rect.left + width_button//2,
                            self.rect.top + 100),
                       size=(width_button, 60), text=chapter, attr=i,
                       on_click=self.change_surface,
                       text_color=Color.BLACK, fill=color)
            )
            self.cur_surface = i
            self.colors.append(color)
            self.collect_widgets.append(ButtonGroup())

        self.add_button(
            Button(pos=(self.rect.centerx, self.rect.bottom - 100),
                   size=(150, 60), text="Back", on_click=self.stop,
                   text_color=Color.BLACK, fill=(20, 150, 20)))

    def change_surface(self, i):
        self.collect_widgets.hide()
        self.cur_surface = i
        self.collect_widgets[self.cur_surface].show()

    def add_button(self, button):
        self.buttons.add(button)

    def add_widget_to(self, widget, id):
        widget.hide()
        self.collect_widgets[id].append(widget)

    def add_text(self, text):
        self.text.add(text)

    def draw(self):
        if self.image is None:
            pg.draw.rect(self.win, self.fill, self.rect)
        else:
            self.win.blit(self.image, self.rect)
        self.title.reset(self.win)
        self.buttons.reset(self.win)
        self.text.reset(self.win)
        self.collect_widgets[self.cur_surface].reset(self.win)

    def run(self):
        self.play = True
        clock = pg.time.Clock()
        while self.play:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    sounds.control(event.key)
                    if event.key == pg.K_ESCAPE:
                        self.play = False
            sounds.update()
            self.draw()
            self.buttons.update(events)
            self.collect_widgets[self.cur_surface].update(events)
            pg.display.update(self.rect)
            clock.tick(60)