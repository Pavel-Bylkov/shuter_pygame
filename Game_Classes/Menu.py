class Menu:
    def __init__(self, win, filename="",
                 pos=(Conf.win_width//2, Conf.win_height//2),
                 size=(Conf.win_width//2, Conf.win_height//2),
                 fill=(60, 60, 60), title="",
                 text_color=Color.WHITE):
        self.win = win
        self.image = None
        if filename:
            menu = pg.image.load(filename).convert()  # загрузка картинок для меню
            self.image = pg.transform.scale(menu, size)  # изменение размера
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = pg.Rect(0, 0, *size)
            self.rect.center = pos
        self.fill = fill
        self.title = Text(text=title, color=text_color, font_size=60,
                          x=self.rect.centerx, y=self.rect.top+40)
        self.title.set_italic(True)
        self.title.set_bold(True)
        self.buttons = ButtonGroup()
        self.text = Group()
        self.play = False

    def add_button(self, button):
        self.buttons.add(button)

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
            pg.display.update(self.rect)
            clock.tick(60)

    def stop(self):
        self.play = False