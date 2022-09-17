
class Conf:
    win_width = 1200
    win_height = 800
    title = "Shooter"
    # фон игры
    back = "images/galaxy.jpg"
    # герой
    hero = "images/rocket.png"
    hero_size = (60, 80)
    # враг
    enemies = (("images/ufo.png", (70, 50)), ("images/ship.png", (50, 60)),
               ("images/ship_star-wars.png", (50, 60)), ("images/mandocruiser.png", (60, 80)))
    gameover = "images/gameover.jpeg"
    # пули
    bulls = ("images/fire_blue.png", (10, 10)), ("images/fireball.png", (20, 20))
    # взрыв
    img_bum = "images/Взрыв4.png"
    music = ("Sound/gamesound.wav", "Sound/cowboy.wav",
             "Sound/happy.wav", "Sound/sample.wav")
    weapon = ("images/rocket2.png", (60, 60)), ("images/rocket3.png", (60, 60))
    weapon_names = ("Rocket", "Stinger")
    sound = {
        weapon_names[0]: "sounds/laser2.wav", weapon_names[1]: "sounds/laser4.wav",
        "lose": "Sound/point.wav", "bum": "sounds/explosion1.wav",
        "change_level": "sounds/upgrade1.wav", "pay": "sounds/cost.mp3",
        "win": "sounds/money.mp3", "gameover": "sounds/gameover1.wav"}
    FPS = 20
    upgrade_menu = "images/dogan-karakus-hud-1.jpg"
