from Game_Classes import Base, Text, Conf
import random
class Enemy(Base):
    def __init__(self, x, y, speed, health, img):
        super().__init__(x=x, y=y, speed=speed, img=img)
        self.health = health
        self.power = health
        self.health_display = Text(x=self.rect.centerx, y=(self.rect.top-15),
                                   text=f"{self.health}", font_size=20)

    def move(self):
        self.rect.y += self.speed
        self.rect.x += random.randint(-self.speed, self.speed)

    def is_lose(self):
        if self.rect.y > Conf.win_height + 50:
            self.kill()
            return True
        return False

    def health_draw(self, win):
        self.health_display.reset(win)

    def update(self):
        self.move()
        self.health_display.change_pos(x=self.rect.centerx, y=(self.rect.top-15))
        self.health_display.update(f"{self.health}")

    def is_dead(self):
        return self.health <= 0