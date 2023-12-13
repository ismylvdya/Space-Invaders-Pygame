'''в модуле: реализация класса Gun пушки, класса GunHp значка хп и перечисления MovDirectionEnum направления движения пушки'''

import pygame
from source.my_functions import scale_img, in_screen
from source.bullet import Bullet    # для бесконечных пуль
from source.CONSTANTS import SCREEN_SIZE, SCREEN_FRAME, GunConst as Const
from enum import Enum

class MovDirectionEnum(Enum):
    '''варианты направления движения пушки'''
    RIGHT = 'right'
    LEFT = 'left'
    STAY = 'stay'

class Gun():
    '''класс пушки'''
    # .convert_alpha() и scale_img в конструкторе
    img_regular = pygame.image.load('images/gun/green.png')
    img_hit = pygame.image.load('images/gun/white.png')
    img_transparency = pygame.image.load('images/gun/outline_green.png')
    img_death = pygame.image.load('images/gun/death.png')
    img_win = pygame.image.load('images/gun/black.png')

    sound_death = pygame.mixer.Sound('sounds/gun_death.wav')

    def __init__(self):
        # масштабирование изображений и их .convert_alpha()
        Gun.img_regular = scale_img(Gun.img_regular.convert_alpha(), width=in_screen(43))
        Gun.img_hit = scale_img(Gun.img_hit.convert_alpha(), width=in_screen(43))
        Gun.img_transparency = scale_img(Gun.img_transparency.convert_alpha(), width=in_screen(43))
        Gun.img_win = scale_img(Gun.img_win.convert_alpha(), width=in_screen(43))
        Gun.img_death = scale_img(Gun.img_death.convert_alpha(), width=in_screen(43))

        self.img = Gun.img_regular                      # по дефолту изображение зеленое

        # инициализация координат centerx и bottom
        self.rect = self.img.get_rect()
        self.rect.centerx = SCREEN_SIZE/2               # абсицисса центра пушки совпадает с центром экрана
        self.rect.bottom = SCREEN_SIZE - SCREEN_FRAME   # ордината низа пушки = низ экрана минус рамка

        self.mov_direction = MovDirectionEnum.STAY
        self.hp = Const.START_HP

        # если длительность анимации попадания (сумма всех тиков) больше длительности заморозке при проигрыше то длительность заморозки делаем равной длительность анимации попадания (чтоб она пролостью проигралась при заморозке) (используется только в main)
        self.duration_of_lose_freeze = max(Const.DURATION_OF_LOSE_FREEZE, 2*Const.DURATION_OF_FLASH_TICK*Const.NUMBER_OF_FLASH_CYCLES)
            
        self.hit_time = - 2 * Const.DURATION_OF_FLASH_TICK * Const.NUMBER_OF_FLASH_CYCLES - 1  # чтобы на старте время до полследнего попадания в пушку (hit_time) было больше чем длина всей анимации мигания (чтобы в намом начале не мигало белым без причины)
        self.lose_time = self.hit_time      # момент проигрыша (в мс). Начальное значение такое же по той же причине
        self.transparency = False           # если True то пули инопланетян проходят мимо

        # создание множества миллисекунд (с момента попадания) при которых gun должна быть белой
        self.set_of_white_ms = []
        for tick in range(Const.NUMBER_OF_FLASH_CYCLES):  # номер мигания
            #        00000         11111                    tick
            # green  WHITE  green  WHITE  green             GUN COLOUR
            # green  outli  GREEN  outli  GREEN  outli      GUN_HP COLOUR
            for ms in range((2 * tick) * Const.DURATION_OF_FLASH_TICK, (2 * tick + 1) * Const.DURATION_OF_FLASH_TICK):  # каждая миллисекунда в данном мигании
                self.set_of_white_ms.append(ms)

    def img_setter(self, win):
        '''меняет self.img в зависимости от win, self.transparency и set_of_white_ms'''
        if self.hp <= 0:       # не lose чтобы пушка не рассыпалась при касании инопланетянами низа экрана
            self.img = Gun.img_death
        elif not win:
            if self.transparency == False:
                if pygame.time.get_ticks() - self.hit_time in self.set_of_white_ms:
                    self.img = Gun.img_hit
                else:
                    self.img = Gun.img_regular
            else:
                self.img = Gun.img_transparency
        else:
            self.img = Gun.img_win


    def update(self, aliens_bullets_list, bullets_list, infinity_bullets, win):
        '''смена изображения, добавление пуль при infinity_bullets, изменение координат и mov_direction, соприкосновение с инопланетянами, их пулями и своими пулями (и их удаление), проигрыш звука смерти при попадании соответствующей пули'''
        self.img_setter(win)    # смена изображения

        if infinity_bullets == True:    # если зажата i
            bullets_list.append(Bullet(self)) # добавляем по пуле в bullets_list при каждом вызове gun.update()

        # изменение координаты x и mov_direction

        if self.mov_direction == MovDirectionEnum.RIGHT and self.rect.right < SCREEN_SIZE - SCREEN_FRAME:       # если нажимаем вправо ДО достижения правой границы
            self.rect.centerx += in_screen(Const.SPEED)
        elif self.mov_direction == MovDirectionEnum.RIGHT and self.rect.right >= SCREEN_SIZE - SCREEN_FRAME:    # если нажимаем вправо и ТЫКАЕТСЯ в правую границу
            self.mov_direction = MovDirectionEnum.STAY
        elif self.mov_direction == MovDirectionEnum.LEFT and self.rect.left > 0 + SCREEN_FRAME + 1:             # если нажимаем влево ДО достижения левой границы (+1 для визуала)
            self.rect.centerx -= in_screen(Const.SPEED)
        elif self.mov_direction == MovDirectionEnum.LEFT and self.rect.left <= 0 + SCREEN_FRAME + 1:            # если нажимаем влево и ТЫКАЕТСЯ в левую границу
            self.mov_direction = MovDirectionEnum.STAY

        # собприкосновение с aliens_bullet
        if self.transparency == False:              # если неуязвимости нет
            for aliens_bullet in aliens_bullets_list:   # перебираем каждую пулю инопланетян
                if self.rect.colliderect(aliens_bullet):    # если соприкосновение пушки с данной пулей
                    self.hit_time = pygame.time.get_ticks()
                    if self.hp == 1:
                        self.lose_time = self.hit_time
                        Gun.sound_death.play()
                    self.hp -= 1
                    aliens_bullets_list.remove(aliens_bullet)
        if win:
            self.transparency = False   # выключаем неуязвимость

            # собприкосновение со своими bullet
            for bullet in bullets_list:
                if self.rect.colliderect(bullet) and bullet.number_of_current_overflight > 1: # and ... чтобы это условие не срабатывало при вылете из пушки
                    bullets_list.remove(bullet)     # удаление пули


    def output(self, screen):
        '''выводит на экран изрбражение пушки с учетом ее текущих координат'''
        screen.blit(self.img, self.rect)


    def restart(self, bullets_list):
        '''удаление выпущенных пуль, возвращения аттрибутов к дефолтным значениям'''
        bullets_list.clear()
        self.rect.centerx = SCREEN_SIZE/2
        self.hp = Const.START_HP
        self.img = Gun.img_regular
        self.transparency = False
        self.hit_time = - 2 * Const.DURATION_OF_FLASH_TICK * Const.NUMBER_OF_FLASH_CYCLES - 1
        self.lose_time = self.hit_time

    def zero_hp(self):
        '''возвращает True если hp = 0'''
        if self.hp <= 0: # < чтобы если при hp=1 две пули попали в одном фрейме hp не ушла в минус
            return True     # lose = True
        else:
            return False

    def freeze(self):
        '''присваивает mov_direction-у значение STAY'''
        self.mov_direction = MovDirectionEnum.STAY


class GunHp():
    '''класс ОДНОГО значка хп'''
    count = 0   # сквозной счетчик объектов

    set_of_hp_green_ms = []  # множество миллисекунд (с момента попадания в gun) при которых gun_hp должно быть зеленой
    max_number_of_displayed_hp = Const.START_HP  # максимально возможное количество изображений gun_hp (чтоб больше трех hp не показывало если они не достигали до этого значения больше 3-ех)

    # .convert_alpha() и scale_img в конструкторе
    img_regular = Gun.img_regular
    img_outline = pygame.image.load('images/gun/outline_green.png')
    img_win = Gun.img_win
    img_outline_win = pygame.image.load('images/gun/outline_black.png')

    def __init__(self, gun):
        GunHp.count += 1
        self.count = GunHp.count    # порядковый номер данного gun_hp

        if self.count == 1:     # делает только первый gun_hp
            # масштабирование изображений и их .convert_alpha()
            GunHp.img_regular = scale_img(GunHp.img_regular.convert_alpha(), width=in_screen(43))
            GunHp.img_outline = scale_img(GunHp.img_outline.convert_alpha(), width=in_screen(43))
            GunHp.img_win = scale_img(GunHp.img_win.convert_alpha(), width=in_screen(43))
            GunHp.img_outline_win = scale_img(GunHp.img_outline_win.convert_alpha(), width=in_screen(43))

            # создание множества миллисекунд при которых gun_hp должна мигать зеленой (win: черной)
            for tick in range(Const.NUMBER_OF_FLASH_CYCLES):  # номер мигания
                #        00000         11111                    tick
                # green  WHITE  green  WHITE  green             GUN COLOUR
                # green  outli  GREEN  outli  GREEN  outli      GUN_HP COLOUR
                for ms in range((2 * tick + 1) * Const.DURATION_OF_FLASH_TICK, (2 * tick + 2) * Const.DURATION_OF_FLASH_TICK):
                    GunHp.set_of_hp_green_ms.append(ms)

        self.img = GunHp.img_regular    # по дефолту делаем зеленым

        self.rect = self.img.get_rect()
        # координаты x и y
        self.rect.x = SCREEN_FRAME + (self.count - 1) * (gun.rect.width + in_screen(18))
        self.y_float = SCREEN_FRAME
        self.rect.y = self.y_float

        self.filled = True  # True -> данный gun_hp закрашенный зеленый (win: черный)
        self.dead = False   # (для win) если в него попала пуля пушки

    def img_setter(self, win):
        '''меняет self.img в зависимости от win и self.filled'''
        if not win:
            if self.filled == True:
                self.img = GunHp.img_regular
            else:
                self.img = GunHp.img_outline
        else:
            if self.filled == True:
                self.img = GunHp.img_win
            else:
                self.img = GunHp.img_outline_win

    def update(self, win, gun, gun_hp_list, bullets_list):
        '''изменение изображения, синхронизация с gun.hp, переопределение self.filled, отслеживание попаданий пулями (и их удаление) и изменение координаты y'''
        self.img_setter(win)    # изменение изображения в зависимости от self.filled и win

        if not win:
            # увеличение максимально возможного количества изображений gun_hp (в случае попадания по положительному инопланетянину)
            if gun.hp > GunHp.max_number_of_displayed_hp:
                GunHp.max_number_of_displayed_hp = gun.hp
                gun_hp_list.append(GunHp(gun))

            # измнение self.filled для данного gun_hp в зависимости от gun.hp и set_of_hp_green_ms
            if self.count < gun.hp + 1:         # для тех кто ЛЕВЕЕ мигающего
                self.filled = True
            elif self.count == gun.hp + 1:      # для минающего
                if pygame.time.get_ticks() - gun.hit_time in GunHp.set_of_hp_green_ms:
                    self.filled = True
                else:
                    self.filled = False
            else:                               # для тех кто ПРАВЕЕ мигающего
                self.filled = False
        else:
            # отслеживание попаданий bullet-ами
            for bullet in bullets_list:
                if self.rect.colliderect(bullet):
                    self.dead = True   # -> теперь он падает
                    bullets_list.remove(bullet)
            if self.dead == True:
                # изменение координаты y
                self.h = self.rect.y - SCREEN_FRAME     # пройденное расстояние (SCREEN_FRAME -- начальная координата)

                if self.rect.top < SCREEN_SIZE:         # если не вышла за экран снизу
                    self.y_float += in_screen(9.8) * (self.h + 1) / in_screen(60) # изменение float-координаты y с ускорением (+1 чтобы в начале сдвигалось не на 0)
                    self.rect.y = round(self.y_float)
                else:                                   # иначе удаляем данный gun_hp
                    gun_hp_list.remove(self)

    def output_hp(self, screen):
        '''выводит на экран изрбражение данного gun_hp с учетом ее текущих координат'''
        if self.count <= GunHp.max_number_of_displayed_hp:  # максимально возможное количество изображений
            screen.blit(self.img, self.rect)

    @classmethod
    def restart(cls):
        '''возвращает максимально возможное количество изображений к 3'''
        cls.max_number_of_displayed_hp = Const.START_HP
