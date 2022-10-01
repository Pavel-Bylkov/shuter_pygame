from Game_Classes.BaseEnemy import Enemy
class Enemy2(Enemy):
    def move(self):
        self.rect.y += self.speed