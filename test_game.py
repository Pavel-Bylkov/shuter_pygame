import pygame as pg

pg.init()

win_width, win_height = 1200, 800

window = pg.display.set_mode((win_width, win_height))
run = True
clock = pg.time.Clock()
while run:
    # событие нажатия на кнопку Закрыть
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    window.fill((30, 200, 50))
    test = 565656 * 345
    pg.display.update()
#hello
    # цикл срабатывает каждую 0.05 секунд
    #time.delay(50)
    clock.tick(60)