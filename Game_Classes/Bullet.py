class Bullet(Base):
    def __init__(self, x, y, speed, power, img, direction=1):
        super().__init__(x=x, y=y, speed=speed, img=img)
        self.power = power
        self.direction = direction

    def update(self):
        if self.direction == 1:
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if self.rect.y < 0 or self.rect.y > Conf.win_height + 50:
            self.kill()

    @staticmethod
    def bullet_collide(sprite, bull_group):
        coll = pg.sprite.spritecollide(sprite, bull_group, True)
        for bull in coll:
            sprite.health -= bull.power