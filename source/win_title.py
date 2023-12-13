'''в модуле: реализация класса WinTitleSquare одного квадратика в надписи 'WIN' на экране выигрыша'''

import pygame
from source.my_functions import scale_img, in_screen
from source.CONSTANTS import SCREEN_SIZE

# словарь {порядковый номер квадратика : его координата на экране}
dict_of_coordinates = { 1 : (256, 358),
                        2 : (268, 358),
                        3 : (316, 358),
                        4 : (328, 358),
                        5 : (364, 358),
                        6 : (376, 358),
                        7 : (388, 358),
                        8 : (400, 358),
                        9 : (412, 358),
                        10 : (424, 358),
                        11 : (460, 358),
                        12 : (472, 358),
                        13 : (520, 358),
                        14 : (532, 358),
                        15 : (256, 370),
                        16 : (268, 370),
                        17 : (316, 370),
                        18 : (328, 370),
                        19 : (388, 370),
                        20 : (400, 370),
                        21 : (460, 370),
                        22 : (472, 370),
                        23 : (484, 370),
                        24 : (520, 370),
                        25 : (532, 370),
                        26 : (256, 382),
                        27 : (268, 382),
                        28 : (292, 382),
                        29 : (316, 382),
                        30 : (328, 382),
                        31 : (388, 382),
                        32 : (400, 382),
                        33 : (460, 382),
                        34 : (472, 382),
                        35 : (484, 382),
                        36 : (496, 382),
                        37 : (520, 382),
                        38 : (532, 382),
                        39 : (256, 394),
                        40 : (268, 394),
                        41 : (280, 394),
                        42 : (292, 394),
                        43 : (304, 394),
                        44 : (316, 394),
                        45 : (328, 394),
                        46 : (388, 394),
                        47 : (400, 394),
                        48 : (460, 394),
                        49 : (472, 394),
                        50 : (496, 394),
                        51 : (508, 394),
                        52 : (520, 394),
                        53 : (532, 394),
                        54 : (256, 406),
                        55 : (268, 406),
                        56 : (280, 406),
                        57 : (304, 406),
                        58 : (316, 406),
                        59 : (328, 406),
                        60 : (388, 406),
                        61 : (400, 406),
                        62 : (460, 406),
                        63 : (472, 406),
                        64 : (508, 406),
                        65 : (520, 406),
                        66 : (532, 406),
                        67 : (256, 418),
                        68 : (268, 418),
                        69 : (316, 418),
                        70 : (328, 418),
                        71 : (388, 418),
                        72 : (400, 418),
                        73 : (460, 418),
                        74 : (472, 418),
                        75 : (520, 418),
                        76 : (532, 418),
                        77 : (256, 430),
                        78 : (268, 430),
                        79 : (316, 430),
                        80 : (328, 430),
                        81 : (364, 430),
                        82 : (376, 430),
                        83 : (388, 430),
                        84 : (400, 430),
                        85 : (412, 430),
                        86 : (424, 430),
                        87 : (460, 430),
                        88 : (472, 430),
                        89 : (520, 430),
                        90 : (532, 430)}

class WinTitleSquare():
    count = 0   # сквозной счетчик квадратиков

    img_black_square = pygame.image.load('images/WIN/black_square.png') # convert_alpha() и in_screen() в конструкторе первого квадратика

    def __init__(self):
        WinTitleSquare.count += 1
        self.count = WinTitleSquare.count

        if self.count == 1:
            WinTitleSquare.img_black_square = scale_img(WinTitleSquare.img_black_square.convert_alpha(), width=in_screen(13))

        self.rect = WinTitleSquare.img_black_square.get_rect()
        # координаты x и y данного квадратика по словарю координат
        self.rect.x = in_screen(dict_of_coordinates[self.count][0])
        self.y_float = in_screen(dict_of_coordinates[self.count][1])
        self.rect.y = self.y_float

        self.hit = False    # факт попадания пули
        self.h = 0          # расстояние от первоначального y до текущего y

    def update(self, bullets_list, WIN_list):
        '''отслеживание попадания bullet и ее удаление, изменение коордианты y при попадании'''
        # отслеживание попадания пули
        for bullet in bullets_list:
            if self.rect.colliderect(bullet):
                self.hit = True
                bullets_list.remove(bullet)

        # изменение координаты y
        if self.hit == True:
            self.h = self.rect.y - in_screen(dict_of_coordinates[self.count][1])    # текущая координата - начальная из словаря

            if self.rect.top < SCREEN_SIZE:     # если не вышла за экран
                # меняем сначала фиктивную float-координату а потом реальную
                self.y_float += in_screen(9.8) * (self.h + 1) / in_screen(60)    # +1 чтобы в начале сдвигалось не на 0
                self.rect.y = round(self.y_float)
            else:
                WIN_list.remove(self)           # иначе удаляем

    def output(self, screen):
        '''выводит данный квадратик (по вычисленным в __init__() и измененным в update() координатам)'''
        screen.blit(WinTitleSquare.img_black_square, self.rect)
