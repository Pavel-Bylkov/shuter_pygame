class Game:
    def __init__(self, window):
        self.window = window
        self.scr = window.screen
        self.width = window.width
        self.height = window.height
        # создаем спрайты
        self.hero = Hero(x=500, y=700, speed=12)
        self.monsters1 = pg.sprite.Group()
        self.bums = pg.sprite.Group()
        self.levels = [
            Level(1, {1: 5}),
            Level(2, {1: 7}),
            Level(3, {1: 5, 2: 5}),
            Level(4, {1: 10, 2: 5}),
            Level(5, {3: 5, 4: 1}),
            Level(6, {3: 10, 5: 1})
        ]
        self.cur_level = self.levels.pop(0)
        self.timer = time.time()
        self.pause = True
        self.pause_timer = time.time()
        self.coins = 0
        self.level_display = Text(x=50, y=25, text="LEVEL: 1", font_size=30)
        self.coins_display = Text(x=55, y=55, text="Coins: 0", font_size=30)
        self.result_display = None
        self.finish = False
        self.sound_pay = pg.mixer.Sound(Conf.sound["pay"])

    def pay_upgrades(self, type_upgrades, choices, name, attr, cost):
        if self.coins - cost < 0:
            return False
        self.coins -= cost
        self.sound_pay.set_volume(sounds.volume / 2)
        self.sound_pay.play()
        if type_upgrades == 'weapon':
            if choices == "power":
                self.hero.upgrade_weapon_power(name, attr)
            if choices == "reload":
                self.hero.upgrade_weapon_reload(name, attr)
        if type_upgrades == 'repair':
            pass
        return True

    def on_show(self):
        """Выполняется один раз при запуске или переключении вида"""
        self.finish = False

    def on_draw(self):
        # обновляем фон
        self.scr.blit(Images.background, (0, 0))
        self.hero.reset(self.scr)
        self.bums.draw(self.scr)
        self.monsters1.draw(self.scr)
        for monster in self.monsters1:
            monster.health_draw(self.scr)
            monster.reset(self.scr)
        self.level_display.reset(self.scr)
        self.coins_display.reset(self.scr)
        if self.pause:
            level_display = Text(x=self.width // 2, y=self.height // 2,
                                 text=f"LEVEL {self.cur_level.number}",
                                 font_size=150, color=Color.GREEN)
            level_display.reset(self.scr)
        if self.finish:
            self.result_display.reset(self.scr)

    def monsters_update(self):
        for monster in self.monsters1:
            monster.update()
            if isinstance(monster, Boss):
                monster.change_move(self.hero)
                monster.update_fire()
                if monster.check_fire(self.hero):
                    monster.fire()
                Bullet.bullet_collide(self.hero, monster.bullets)
            if monster.is_lose():
                self.hero.get_hit(monster.health)
            if pg.sprite.collide_rect(monster, self.hero):
                self.hero.get_hit(monster.health)
                monster.health = 0
            Bullet.bullet_collide(monster, self.hero.bullets)
            if monster.is_dead():
                self.bums.add(
                    Bum(monster.rect.centerx, monster.rect.centery)
                )
                self.coins += monster.power
                monster.kill()

    def on_update(self, events):
        if not self.pause:
            self.hero.update(events)
            self.bums.update()
            if time.time() - self.timer >= random.randint(1, 3):
                self.timer = time.time()
                if len(self.cur_level) == 0:
                    if len(self.monsters1) == 0 and len(self.levels) != 0:
                        self.level_change()
                else:
                    self.monsters1.add(self.cur_level.get_next_monster())
            if (len(self.levels) == 0 and self.cur_level.is_end_level()
                    and len(self.monsters1) == 0):
                self.game_win()
            else:
                self.monsters_update()
        elif time.time() - self.pause_timer >= 2:
            self.pause = False
        if self.hero.is_dead():
            self.game_over()
        self.level_display.update(f"LEVEL: {self.cur_level.number}")
        self.coins_display.update(f"Coins: {self.coins}")

    def level_change(self):
        self.cur_level = self.levels.pop(0)
        self.pause = True
        self.pause_timer = time.time()

    def game_over(self):
        self.finish = True
        self.result_display = Text(x=self.width//2, y=self.height//2,
                                   text="GAME OVER", font_size=150, color=Color.RED)

    def game_win(self):
        self.finish = True
        self.result_display = Text(x=self.width//2, y=self.height//2,
                                   text="WIN", font_size=150, color=Color.GREEN)

    def on_resize(self):
        self.width = self.window.width
        self.height = self.window.height