from Game_Classes.Color import Color
class Text:
    def __init__(self, x, y, font=None, font_size=50, text="Test", color=Color.WHITE):
        # создаем шрифт
        self.font = pg.font.Font(font, font_size)
        # Картинка из шрифта
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=(x, y))
        self.active = True

    def update(self, text, *args, **kwargs):
        if self.active and isinstance(text, str):
            x = self.rect.centerx
            y = self.rect.centery
            self.image = self.font.render(text, True, self.color)
            self.rect = self.image.get_rect(center=(x, y))

    def change_color(self, new_color):
        self.color = new_color

    def change_pos(self, x, y):
        self.rect.center = (x, y)

    def set_italic(self, value):
        self.font.set_italic(value)

    def set_bold(self, value):
        self.font.set_bold(value)

    def reset(self, win):
        if self.active:
            win.blit(self.image, self.rect)

    def hide(self):
        self.active = False

    def show(self):
        self.active = True