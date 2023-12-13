'''в модуле: реализация функции event(), отслеживающей нажатия пользователя на кнопки, и перечисления EventsEnum возможных возвращаемых функуией event() событий'''

import pygame
import sys
from source.bullet import Bullet
from enum import Enum

class EventsEnum(Enum):
    '''варианты возвращаемых событий со стороны пользователя'''
    INFINITY_BULLETS = 'infinity_bullets'

def events(gun, bullets_list, lose):   # вызывается на каждой итерации бесконечного while в main
    '''отслеживает нажатия на клавиши: влево,вправо -> меняет mov_direction пушки, стрельба -> добавляет в bullets_list новую пулю, i -> возвращает INFINITY_BULLETS'''
    for event in pygame.event.get(): #  отслеживаем со стороны игрока ВСЕ возможные события event
        # нажатие на крестик, cmd+Q, cmd+W
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:    # если событие это нажатие на какую-либо клавишу
            # нажатие вправо
            if event.key in [pygame.K_RIGHT, pygame.K_d]:   # если нажатая клавиша это вправо или D
                if not lose:
                    gun.mov_direction = gun.mov_direction.RIGHT
            # нажатие влево
            elif event.key in [pygame.K_LEFT, pygame.K_a]:    # если нажатая клавиша это влево или A
                if not lose:
                    gun.mov_direction = gun.mov_direction.LEFT
            # стрельба
            if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_w]:  # если нажатая клавиша это пробел, вверх или W
                if not lose:
                    bullets_list.append(Bullet(gun))        # создание новой пули в списке пуль

        if event.type == pygame.KEYUP:      # если событие это отпускание какой-либо клавиши
            # если отпускается правая и при этом нажата левая
            if event.key in [pygame.K_d, pygame.K_RIGHT] and gun.mov_direction == gun.mov_direction.LEFT:
                if not lose:
                    gun.mov_direction = gun.mov_direction.LEFT
            # если отпускается левая и при этом нажата правая
            elif event.key in [pygame.K_a, pygame.K_LEFT] and gun.mov_direction == gun.mov_direction.RIGHT:
                if not lose:
                    gun.mov_direction = gun.mov_direction.RIGHT
            # если просто отпускается клавиша вправо/влево
            elif event.key in [pygame.K_d, pygame.K_RIGHT, pygame.K_a, pygame.K_LEFT]:
                gun.mov_direction = gun.mov_direction.STAY

        # нажатие на i
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                if not lose:
                    return EventsEnum.INFINITY_BULLETS

