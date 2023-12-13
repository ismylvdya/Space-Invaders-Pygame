'''в модуле: реализация класса ProgressBar одного прогрессбара'''

import pygame
from source.my_functions import scale_img, in_screen
from source.CONSTANTS import SCREEN_SIZE, SMALLFONT, SCREEN_FRAME
import source.alien as alien

class ProgressBar():
    '''класс ОДНОГО прогрессбара'''
    # определяются в конструкторе каждого соответствующего прогрессбара
    increase_coord_x = None     # координата x строки '3x'
    ufo_coord_x = None          # координата x значка НЛО

    # .convert_alpha() и scale_img в конструкторе каждого прогрессбара
    img_negative_outline = pygame.image.load('images/progr_bars/white_outline.png')
    img_negative_fill = pygame.image.load('images/progr_bars/white_fill.png')
    img_ufo_outline = pygame.image.load('images/progr_bars/red_outline.png')
    img_ufo_fill = pygame.image.load('images/progr_bars/red_fill.png')
    img_ufo = pygame.image.load('images/aliens/ufo.png')  # не alien.Ufo.img потому что тогда произойдет рекурсия в import-ах

    def __init__(self, type, duration, shooting_increase=-1):  # shooting_increase только для negative
        self.type = type
        self.time_created = pygame.time.get_ticks()
        self.duration = duration    # длительность прогрессбара (в мс)
        self.percent = 100          # процент в прогрессбаре (100 -> 0 в зависимости от пройденного времени)

        # определение и масштабирование изображений в зависимости от self.type
        if self.type == alien.TypeEnum.NEGATIVE:
            self.img_outline = scale_img(ProgressBar.img_negative_outline.convert_alpha(), width=in_screen(103), height=in_screen(22))
            self.img_fill = ProgressBar.img_negative_fill.convert_alpha() # не масштабируем потому что масштабирование все равно происходит в каждом фрейме в update()
        elif self.type == alien.TypeEnum.UFO:
            self.img_outline = scale_img(ProgressBar.img_ufo_outline.convert_alpha(), width=in_screen(103), height=in_screen(22))
            self.img_fill = ProgressBar.img_ufo_fill.convert_alpha()

        self.outline_rect = self.img_outline.get_rect()
        self.fill_rect = self.img_fill.get_rect()
        # координаты x двух изображений (координаты y определяются в update() т.к. они все равно меняются если верхний прогрессбар удаляется)
        self.outline_rect.x = SCREEN_SIZE - SCREEN_FRAME - in_screen(8) - self.img_outline.get_width() # -8 чтобы прогрессбар был заподлицо с score справа
        self.fill_rect.x = self.outline_rect.x

        # строка '3x' слева от прогрессбара (ее заполнение и определение координаты x)
        if type == alien.TypeEnum.NEGATIVE:
            self.shooting_increase = shooting_increase
            # определяем строку округленной до целого если дробная часть равна .0
            if self.shooting_increase == round(self.shooting_increase):
                self.str_neg_increase = str(round(self.shooting_increase)) + 'x'
            # иначе определяем с одним знаком после запятой
            else:
                self.str_neg_increase = str(round(self.shooting_increase, 1)) + 'x'
            ProgressBar.increase_coord_x = self.outline_rect.left - SMALLFONT.size(self.str_neg_increase)[0] - in_screen(10)
        # изображение маленького НЛО слева от прогрессбара (его масштабирование и определение координаты x)
        elif type == alien.TypeEnum.UFO:
            self.img_ufo = scale_img(ProgressBar.img_ufo.convert_alpha(), height=in_screen(22))
            ProgressBar.ufo_coord_x = self.outline_rect.left - self.img_ufo.get_width() - in_screen(10)


    def update(self, progr_bars_list, gun_hp_height):
        '''
        обновление координат y данного прогрессбара, расчет процента, масштабирование изображения-наполнителя, удаление если процент <= 0 \n
        ВОЗВРАЩАЕТ: \n
        в случае NEGATIVE 3 если время кончилось, иначе 1 \n
        в случае UFO False если время кончилось, иначе True
        '''
        bottom_of_score = SCREEN_FRAME + gun_hp_height  # координата низа надписи 'bullets : количество_выпущенных_пуль'
        # координаты y (расстояние между прогрессбарами = 0.5 от их высоты, расстояние от надписи до первого = 20)
        self.outline_rect.y = bottom_of_score + in_screen(20) + 1.5 * progr_bars_list.index(self) * self.outline_rect.height
        self.fill_rect.y = bottom_of_score + in_screen(20) + 1.5 * progr_bars_list.index(self) * self.outline_rect.height

        self.percent = 100 * (1 - (pygame.time.get_ticks() - self.time_created)/self.duration) # 100 -> 0 в зависимости от пройденного времени

        # сжатие изображения-наполнителя если percent > 0, иначе удаление прогрессбара и возврат нужных значений
        if self.percent > 0:  # не >= 0 чтобы ширина progr_bar_fill не дошла в конце до 0 (вызовет ошибку при масштабировании)
            self.img_fill = scale_img(self.img_fill, width=in_screen(103)*self.percent/100, height=in_screen(22)) # width не будет равно нулю так как в if percent > 0
            return 1           # интерпритируется как  1 если alien.TypeEnum.NEGATIVE (Alien.shoot_frequancy *=)  или как  True если alien.TypeEnum.UFO (gun.throughing =)
        else:
            progr_bars_list.remove(self)            # удаление данного прогрессбара
            if self.type == alien.TypeEnum.NEGATIVE:
                return self.shooting_increase       # возвращение множителя 3 для частоты стрельбы
            elif self.type == alien.TypeEnum.UFO:
                return False                        # возвращение фолса для прозрачности пушки

    def output(self, screen):
        '''вывод на экран данного прогрессбара и {'3x' или значка НЛО} перед ним по уже высчитанным в __init__() и update() координатам'''
        if self.type == alien.TypeEnum.NEGATIVE:
            screen.blit(SMALLFONT.render(self.str_neg_increase, False, 'White'), (
                ProgressBar.increase_coord_x,
                self.outline_rect.y))
        elif self.type == alien.TypeEnum.UFO:
            screen.blit(self.img_ufo, (
                ProgressBar.ufo_coord_x,
                self.outline_rect.y))

        screen.blit(self.img_outline, self.outline_rect)

        screen.blit(self.img_fill, self.fill_rect)

    @classmethod
    def restart(cls, progr_bars_list):
        '''очищает лист прогрессбаров'''
        progr_bars_list.clear()