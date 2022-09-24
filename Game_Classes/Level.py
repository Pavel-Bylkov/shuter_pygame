class Level:
    def __init__(self, number, n_type):
        self.number = number
        self.n_type = n_type

    def __len__(self):
        return len(self.n_type)

    def is_end_level(self):
        return len(self.n_type) == 0

    def get_next_monster(self):
        types = list(self.n_type.keys())
        random.shuffle(types)
        type = types.pop()
        self.n_type[type] -= 1
        if self.n_type[type] == 0:
            del self.n_type[type]
        x = random.randint(3, Conf.win_width // 10 - 4) * 10
        y = random.randint(-50, -10)
        new_enemy = {
            1: Enemy(x=x, y=y, speed=4, health=4, img=Images.enemies[0]),
            2: Enemy2(x=x, y=y, speed=7, health=2, img=Images.enemies[2]),
            3: Enemy2(x=x, y=y, speed=2, health=10, img=Images.enemies[1]),
            4: Boss(x=x, y=10, speed=2, health=50, img=Images.enemies[3], power=3),
            5: Boss(x=x, y=10, speed=2, health=100, img=Images.enemies[3], power=5)}
        return new_enemy[type]