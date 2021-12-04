import pygame as pg

# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры

# запускаем инициализацию pygame - настройка на наше железо
pg.init()

# Создаем окошко
win_width, win_height = 1200, 800
pg.display.set_caption("Shooter")  # Title у окна
window = pg.display.set_mode((win_width, win_height))
back_img = pg.image.load(img_back)  # конвертация любого формата изображений в формат pygame
background = pg.transform.scale(back_img, (win_width, win_height))

# переменная "игра закончилась": как только там True,
# в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True  # флаг сбрасывается кнопкой закрытия окна

clock = pg.time.Clock()
while run:
    # событие нажатия на кнопку Закрыть
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    if not finish:
        # обновляем фон
        window.blit(background, (0, 0))

        pg.display.update()

    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(60)