'''в модуле: реализация класса Bullet пули выпущенной пушкой'''

import pygame
from source.my_functions import scale_img, in_screen
from source.CONSTANTS import SCREEN_SIZE, GunConst

class bcolors:
    '''для вывода ошибков в except'''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Bullet():
    '''класс ОДНОЙ пули пушки'''
    score = 0          # количество выпущенных на данный момпнт пуль (обнуляется при новом раунде)
    speed_hor_from_moving_gun = 0.15 * GunConst.SPEED * SCREEN_SIZE / 800   # горизонтальная скорость пули при вылете из движещейся пушки (делаем ее равной 0.15 от скорости пушки) и ее масштабирование с учетом размера экрана (не in_screen() потому что не нужен round())
    speed_vert = GunConst.BULLET_SPEED_VERT * SCREEN_SIZE / 800  # отмасштабированная общая скорость по вертикали (не in_screen() потому что не нужен round())
    highscore = None            # определяется при чтении из highscore.txt

    # .convert_alpha() и scale_img в конструкторе первой выпущенной пули
    img_regular = pygame.image.load('images/gun/bullet_green.png')
    img_win = pygame.image.load('images/gun/bullet_black.png')

    sound_shoot = pygame.mixer.Sound('sounds/gun_shoot.wav')

    def __init__(self, gun):
        if GunConst.PLAY_SOUND_OF_SHOOT == True:
            Bullet.sound_shoot.play()

        # первая выпущенная пуля инициализирует изображения
        if Bullet.score == 0:
            Bullet.img_regular = scale_img(Bullet.img_regular.convert_alpha(), height=in_screen(18))
            Bullet.img_win = scale_img(Bullet.img_win.convert_alpha(), height=in_screen(18))
        Bullet.score += 1

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
    def read_highscore_txt(cls):
        '''обновляет переменную Bullet.highscore, перечитывая highscore.txt'''
        try:
            with open('source/highscore.txt', 'r') as f:
                try:
                    cls.highscore = f.readlines()[0]  # на всякий случай считываем только первую строку
                except:
                    print(f"{bcolors.FAIL}error reading the first line from the file{bcolors.ENDC}")  # если пустой файл
                    cls.highscore = None
        except:
            print(f"{bcolors.FAIL}error opening the file{bcolors.ENDC}")     # если файла нет
            cls.highscore = None