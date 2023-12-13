'''в модуле: реализация класса Bullet пули выпущенной пушкой'''

import pygame
from source.my_functions import scale_img, in_screen
from source.CONSTANTS import SCREEN_SIZE, SMALLFONT, SCREEN_FRAME, GunConst, BulletConst

class Bullet():
    '''класс ОДНОЙ пули пушки'''
    count_of_bullets_fired = 0          # количество выпущенных за раунд пуль
    speed_hor_from_moving_gun = 0.15 * GunConst.SPEED * SCREEN_SIZE / 800   # горизонтальная скорость пули при вылете из движещейся пушки (делаем ее равной 0.15 от скорости пушки) и ее масштабирование с учетом размера экрана (не in_screen() потому что не нужен round())
    speed_vert = BulletConst.SPEED_VERT * SCREEN_SIZE / 800  # отмасштабированная общая скорость по вертикали (не in_screen() потому что не нужен round())

    # .convert_alpha() и scale_img в конструкторе первой выпущенной пули
    img_regular = pygame.image.load('images/gun/bullet_green.png')
    img_win = pygame.image.load('images/gun/bullet_black.png')

    sound_shoot = pygame.mixer.Sound('sounds/gun_shoot.wav')

    def __init__(self, gun):
        if GunConst.PLAY_SOUND_OF_SHOOT == True:
            Bullet.sound_shoot.play()

        # первая выпущенная пуля инициализирует изображения
        if Bullet.count_of_bullets_fired == 0:
            Bullet.img_regular = scale_img(Bullet.img_regular.convert_alpha(), height=in_screen(18))
            Bullet.img_win = scale_img(Bullet.img_win.convert_alpha(), height=in_screen(18))
        Bullet.count_of_bullets_fired += 1

        # изображение по дефолту зеленое
        self.img = Bullet.img_regular

        # скорость по вертикали
        self.speed_vert = Bullet.speed_vert
        # скорость по горизонтали
        if gun.mov_direction == gun.mov_direction.RIGHT:
            self.speed_hor = Bullet.speed_hor_from_moving_gun
        elif gun.mov_direction == gun.mov_direction.LEFT:
            self.speed_hor = - Bullet.speed_hor_from_moving_gun
        else:
            self.speed_hor = 0

        self.rect = self.img.get_rect()
        # задание centerx
        self.centerx_float = gun.rect.centerx
        self.rect.centerx = self.centerx_float
        # задание top
        self.top_float = gun.rect.top
        self.rect.top = self.top_float

        self.number_of_current_overflight = 1 # номер пролета при рикошете (нужен только для "съедания" пули пушкой)


    def update(self, bullets_list, win):
        '''изменение координат x и y, при win: изменение цвета на черный, рикошет, удаление при выходе за экран'''
        # centerx
        self.centerx_float += self.speed_hor
        self.rect.centerx = round(self.centerx_float)
        # top
        self.top_float -= self.speed_vert
        self.rect.top = round(self.top_float)

        if win:
            self.img = Bullet.img_win   # делаем изображение черным

            # РИКОШЕТ ОТ ПОТОЛКА И ПОЛА (смена знака speed_vert)
            if self.rect.top <= 0:
                self.speed_vert = - Bullet.speed_vert   # не *= -1 чтобы не было зацикливанивания: пока пуля не отлетит от потолка скорость бесконечно будет умножаться на -1
                self.number_of_current_overflight += 1
            elif self.rect.bottom >= SCREEN_SIZE:
                self.speed_vert = Bullet.speed_vert
                self.number_of_current_overflight += 1
            # РИКОШЕТ ОТ ЛЕВОЙ И ПРАВОЙ СТЕН (смена знака speed_hor)
            if self.rect.left <= 0:
                self.speed_hor = Bullet.speed_hor_from_moving_gun
            elif self.rect.right >= SCREEN_SIZE:
                self.speed_hor = - Bullet.speed_hor_from_moving_gun
        else:       # чтобы удаление не срабатывало при win (при супер большой скорсоти пушки пули не успевают отрикошетить и сразу оказываются за пределами экрана)
            # удаление при выходе за экран
            if self.rect.bottom <= 0:           # если вышла за экран сверху
                bullets_list.remove(self)
            elif self.rect.top >= SCREEN_SIZE:  # если вышла за экран снизу
                bullets_list.remove(self)
            elif self.rect.right <= 0:          # если вышла за экран слева
                bullets_list.remove(self)
            elif self.rect.left >= SCREEN_SIZE: # если вышла за экран справа
                bullets_list.remove(self)

    def output(self, screen):
        '''выводит на экран изрбражение данной пули с учетом ее текущих координат'''
        screen.blit(self.img, self.rect)

    @classmethod
    def set_score_zero(cls):
        '''зануляет количество выпущенных пуль'''
        cls.count_of_bullets_fired = 0