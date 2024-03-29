from Game_Classes.Conf import Conf
from Game_Classes.Color import Color
from Game_Classes.Text import Text
from Game_Classes.Music import sounds
from Game_Classes.Button import Button
from Game_Classes.Game import Game
from Game_Classes.Menu import Menu
from Game_Classes.SubMenu import SubMenu
import sys
import pygame as pg
class Window:
    def __init__(self, width, height, title, resizable=True) -> None:
        # Создаем окошко
        pg.display.set_caption(title)  # Title у окна
        if resizable:
            self.screen = pg.display.set_mode((width, height), pg.RESIZABLE)
        else:
            self.screen = pg.display.set_mode((width, height))
        self.width = width
        self.height = height
        self.game = Game(self)
        self.main_menu = Menu(win=self.screen, filename="images/futuristicmenuforpy.jpg",
                              title="Main Menu", text_color=(0, 0, 0))
        self.menu_controls = Menu(win=self.screen, filename="images/futuristicmenuforpy.jpg",
                                  title="Controls", text_color=(0, 0, 0))
        self.upgrade_menu = SubMenu(win=self.screen,
                                    chapters=['Weapon', 'Repair'],
                                    filename=Conf.upgrade_menu,
                                    title="Upgrade")
        self.config_menu()

    def config_menu(self):
        # main menu
        self.main_menu.add_button(
            Button(filename="",
                   pos=(Conf.win_width // 2, Conf.win_height // 2 - 40),
                   size=(150, 60), text="Controls", on_click=self.menu_controls.run,
                   text_color=Color.WHITE, fill_activ=(200, 50, 50), fill_not_activ=(200, 50, 50)))
        self.main_menu.add_button(
            Button(filename="",
                   pos=(Conf.win_width // 2, Conf.win_height // 2 + 60),
                   size=(150, 60), text="Quit", on_click=sys.exit,
                   text_color=Color.WHITE, fill_activ=(50, 200, 50), fill_not_activ=(50, 200, 50)))
        # menu controls
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 - 100,
                 font=None, font_size=30,
                 text=
                     "UP/DOWN ARROWS = VOLUME", color=Color.WHITE))
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 - 70,
                 font=None, font_size=30,
                 text="W,A,S,D = UP/LEFT/DOWN/RIGHT", color=Color.WHITE))
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 - 40,
                 font=None, font_size=30,
                 text="U = UPGRADES", color=Color.WHITE))
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 - 10,
                 font=None, font_size=30,
                 text="R = CHANGE WEAPON", color=Color.WHITE))
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 + 20,
                 font=None, font_size=30,
                 text="T = MUTE MUSIC", color=Color.WHITE))
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 + 50,
                 font=None, font_size=30,
                 text= "UP/DOWN ARROWS = VOLUME", color=Color.WHITE))
        self.menu_controls.add_text(
            Text(x=Conf.win_width // 2, y=Conf.win_height // 2 + 80,
                 font=None, font_size=30,
                 text="ESC = GO BACK/OPEN MENU", color=Color.WHITE))
        # menu upgrades
        # Weapuns id=0
        # weapon 1
        self.upgrade_menu.add_widget_to(
            Text(text=f"Fire speed for {Conf.weapon_names[1]} - 0.5 --> 0.3",
                 x=self.upgrade_menu.rect.centerx,
                 y=self.upgrade_menu.rect.centery - 100, color=Color.BLACK), id=0)
        self.upgrade_menu.add_widget_to(
            Button(pos=(Conf.win_width // 2, Conf.win_height // 2 - 50),
                   size=(150, 60), text="Cost:100",
                   attr={"type_upgrades": "weapon",
                         "choices": "reload", "name": Conf.weapon_names[1],
                         "attr": 0.3, "cost": 100},
                    on_click=self.game.pay_upgrades,
                   text_color=Color.WHITE, fill_activ=(50, 200, 50), fill_not_activ=(50, 200, 50)), id=0)
        # weapon 2
        self.upgrade_menu.add_widget_to(
            Text(text=f"Fire speed for {Conf.weapon_names[0]} - 0.15 --> 0.1",
                 x=self.upgrade_menu.rect.centerx,
                 y=self.upgrade_menu.rect.centery + 30, color=Color.BLACK), id=0)
        self.upgrade_menu.add_widget_to(
            Button(pos=(Conf.win_width // 2, Conf.win_height // 2 + 80),
                   size=(150, 60), text="Cost:75",
                   attr={"type_upgrades": "weapon",
                         "choices": "reload", "name": Conf.weapon_names[0],
                         "attr": 0.1, "cost": 75},
                   on_click=self.game.pay_upgrades,
                   text_color=Color.WHITE, fill_activ=(50, 200, 50), fill_not_activ=(50, 200, 50)), id=0)

        # Repairs id=1
        self.upgrade_menu.add_widget_to(
            Text(text=f"Health + 50",
                 x=self.upgrade_menu.rect.centerx,
                 y=self.upgrade_menu.rect.centery + 30, color=Color.BLACK), id=1)
        self.upgrade_menu.add_widget_to(
            Button(pos=(Conf.win_width // 2, Conf.win_height // 2 + 80),
                   size=(150, 60), text="Cost:100",
                   attr={"type_upgrades": "repair",
                         "choices": "health", "name": "",
                         "attr": 50, "cost": 100},
                   on_click=self.game.pay_upgrades,
                   text_color=Color.WHITE, fill_activ=(50, 200, 50), fill_not_activ=(50, 200, 50)), id=1)

    def resize(self):
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        # если где-то используется этот параметр, то его тоже нужно обновить
        Conf.win_width = self.width
        Conf.win_height = self.height
        self.game.on_resize()

    def run(self):
        # Основной цикл игры:
        run = True  # флаг сбрасывается кнопкой закрытия окна
        clock = pg.time.Clock()
        self.game.on_show()
        while run:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    run = False
                if e.type == pg.WINDOWSIZECHANGED:
                    self.resize()
                if e.type == pg.KEYDOWN:
                    sounds.control(e.key)
                    if e.key == pg.K_ESCAPE:
                        self.main_menu.run()
                    if e.key == pg.K_u:
                        self.upgrade_menu.run()
            sounds.update()
            self.game.on_update(events)
            self.game.on_draw()

            pg.display.update()
            clock.tick(Conf.FPS)
