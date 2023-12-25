import pygame
import source.controls as controls
from source.gun import Gun, GunHp
from source.alien import TypeEnum as AlienTypeEnum, Alien, AliensBullet, Ufo
from source.progress_bars import ProgressBar
from source.win_title import WinTitleSquare
from source.score_title import ScoreTitleSymbol
from source.bullet import Bullet
from source.CONSTANTS import SCREEN_SIZE, FRAMERATE, AlienConst
from typing import List


def main_run(infinity_bullets):
    '''реализация цикла основной игры и инициализация переменных которые нужны только для него'''
    lose = False
    win = False

    # инициализация списка пуль инопланетян, создание самих инопланетян и НЛО, инициализация списка прогрессбаров
    aliens_bullet_list: List[AliensBullet] = []     # аннотация (здесь и далее) чтобы пайчарм выводил подсказки при наведении на методы объектов AliensBullet
    aliens_list: List[Alien] = Alien.create_new_army(aliens_bullet_list, AlienConst.NUMBER_VERT * AlienConst.NUMBER_HOR, gun.rect)
    ufo_list: List[Ufo] = [Ufo()]      # лист с одним объектом вместо просто объекта -- чтобы была возможность удалить объект Ufo
    progr_bars_list: List[ProgressBar] = []

    bullets_list.clear()

    while not win:          # цикл по каждому фрейму
        pygame.time.Clock().tick(FRAMERATE)  # фрэймрейт (по умолчанию 80)
        pygame.display.flip()   # обновление всех объектов на экране

        # отслеживание НАЖАТИЯ КНОПОК управления и стрельбы, закрытия игры
        if controls.events(gun, bullets_list, lose) == controls.EventsEnum.INFINITY_BULLETS:  # если нажали i
            infinity_bullets = not infinity_bullets     # замена флага бесконечных пуль на противоположный

        screen.fill((0, 0, 0))  # ЦВЕТ ФОНА (черный)

        # после закрашивания экрана: !!!

        # BULLET
        for bullet in bullets_list:     # проходимся по каждой пуле в списке пуль
            if not lose:    # здесь и далее update() не вызывается в случае lose чтобы производилась заморозка на пол секунды происходящего на экране
                bullet.update(bullets_list, False)
            bullet.output(screen)

        # НАДПИСЬ 'bullets : Bullet.score'
        for symb in score_list:
            symb.update(bullets_list, score_list, False)
            symb.output(screen)

        # НАДПИСЬ 'highscore: Bullet.highscore'
        for symb in highscore_list:
            symb.update(bullets_list, highscore_list, False)
            symb.output(screen)

        # ALIENS BULLETS
        for aliens_bullet in aliens_bullet_list:
            if not lose:
                aliens_bullet.update(aliens_bullet_list)
            aliens_bullet.output(screen)

        # GUN
        gun.update(aliens_bullet_list, bullets_list, infinity_bullets, False)
        gun.output(screen)
        if gun.zero_hp():
            lose = True

        # GUN_HP
        for gun_hp in gun_hp_list:
            gun_hp.update(False, gun, gun_hp_list, bullets_list)    # у gun и gun_hp update() вызывается даже в случае lose чтобы во время заморозки производилось их мигание
            gun_hp.output_hp(screen)

        # ALIENS
        for alien in aliens_list:
            if not lose:
                alien.update(aliens_list, bullets_list, aliens_bullet_list, gun, progr_bars_list)
                if alien.screen_bottom():   # если данный alien коснулся низа экрана
                    lose = True
            alien.output(screen)

        # UFO
        for ufo in ufo_list:
            if not lose:
                ufo.update(ufo_list, bullets_list, gun, progr_bars_list)
            ufo.output(screen)

        # PROGRESS BARS
        for pr_bar in progr_bars_list:
            if not lose:
                if pr_bar.type == AlienTypeEnum.NEGATIVE:   # для белых прогрессбаров
                    Alien.shoot_frequancy *= pr_bar.update(progr_bars_list, gun_hp_height)
                elif pr_bar.type == AlienTypeEnum.UFO:      # для красных прогрессбаров
                    gun.transparency = pr_bar.update(progr_bars_list, gun_hp_height)
            pr_bar.output(screen)

        if lose:
            if pygame.time.get_ticks() - gun.lose_time <= gun.duration_of_lose_freeze: # пока не прошло duration_of_lose_freeze мс
                gun.freeze()        # держим пушку неподвижной (lose при этом остается равен True)
            else:
                gun.restart(bullets_list)
                GunHp.restart()
                aliens_list = Alien.create_new_army(aliens_bullet_list, AlienConst.NUMBER_VERT * AlienConst.NUMBER_HOR,gun.rect)
                ufo_list = [Ufo()]  # тем самым создаем новый объект Ufo => с новыми дефолтными аттрибутами
                ProgressBar.restart(progr_bars_list)
                Bullet.score = 0
                lose = False
        elif len(aliens_list) == 0:
            win = True


def win_run(infinity_bullets):
    '''реализация цикла экрана выигрыша и инициализация переменных которые нужны только для него'''

    # обновление Bullet.highscore, highscore.txt и надписей highscore_list и score_list
    ScoreTitleSymbol.update_highscore_and_txt_and_titles(score_list, highscore_list)

    # инициализация разрушаемой надписи 'WIN'
    win_list: List[WinTitleSquare] = []
    for _ in range(90):
        win_list.append(WinTitleSquare())

    while True:
        pygame.time.Clock().tick(FRAMERATE)
        pygame.display.flip()

        # отслеживание НАЖАТИЯ КНОПОК управления и стрельбы, закрытия игры
        if controls.events(gun, bullets_list, False) == controls.EventsEnum.INFINITY_BULLETS:  # если нажата i
            infinity_bullets = not infinity_bullets

        # BACKGROUND
        screen.fill((0, 207, 0))    # ЦВЕТ ФОНА (зеленый)

        # после закрашивания экрана: !!!

        # BULLET
        for bullet in bullets_list:
            bullet.update(bullets_list, True)
            bullet.output(screen)

        # GUN
        gun.update([], bullets_list, infinity_bullets, True)
        gun.output(screen)

        # GUN_HP
        for gun_hp in gun_hp_list:
            gun_hp.update(True, gun, gun_hp_list, bullets_list)
            gun_hp.output_hp(screen)

        # НАДПИСЬ 'bullets : Bullet.score'
        for symb in score_list:
            symb.update(bullets_list, score_list, True)
            symb.output(screen)

        # НАДПИСЬ 'highscore: Bullet.highscore'
        for symb in highscore_list:
            symb.update(bullets_list, highscore_list, True)
            symb.output(screen)

        # НАДПИСЬ WIN
        for win_square in win_list:
            win_square.update(bullets_list, win_list)
            win_square.output(screen)


pygame.init()
pygame.display.set_caption('Space invaders')                        # Titlebar окна
pygame.display.set_icon(pygame.image.load('images/app_icon.png'))   # иконка приложения
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))        # инициализация экрана и его размеров

# иициализация пушки и пуль
gun = Gun()
bullets_list: List[Bullet] = []
infinity_bullets = False    # True -> поток бесконечных пуль

# инициализация значков хп
gun_hp_list: List[GunHp] = []
for _ in range(gun.hp):
    gun_hp_list.append(GunHp(gun))
gun_hp_height = gun_hp_list[0].rect.height

# инициализация счета выпущенных пуль и хайскора
Bullet.read_highscore_txt()
score_list: List[ScoreTitleSymbol] = []
highscore_list: List[ScoreTitleSymbol] = []
for symb in 'bullets:':         # все что после ':' не учитывается
    score_list.append(ScoreTitleSymbol(gun_hp_height, symb, 0))
for symb in 'highscore:' + str(Bullet.highscore):
    highscore_list.append(ScoreTitleSymbol(gun_hp_height, symb, 1))

# ОСНОВНОЙ ЦИКЛ ИГРЫ
main_run(infinity_bullets)

# ЦИКЛ ЭКРАНА ВЫИГРЫША
win_run(infinity_bullets)