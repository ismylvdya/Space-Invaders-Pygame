'''в модуле: реализация класса Alien инопланетянина, класса AliensBullet его пули, класса Ufo НЛО и перечислений MovDirectionEnum и TypeEnum направлений движения и типов инопланетян'''

import pygame
from source.my_functions import scale_img, in_screen
import random
from source.progress_bars import ProgressBar
from source.CONSTANTS import SCREEN_SIZE, SCREEN_FRAME, SMALLFONT, AlienConst as Const
from enum import Enum

class MovDirectionEnum(Enum):
    '''варианты направления движения инопланетянина'''
    RIGHT = 'right'
    LEFT = 'left'
    STAY = 'stay'   # для Ufo за пределами экрана

class TypeEnum(Enum):
    '''типы инопланетянинов'''
    REGULAR = 'regular'     # белые
    NEGATIVE = 'negative'   # черные
    POSITIVE = 'positive'   # зеленые
    UFO = 'ufo'             # красный НЛО


class Alien():
    '''класс ОДНОГО инопланетянина'''
    count = 0                                   # количество созданных инопланетян
    start_numer_of_aliens = Const.NUMBER_HOR * Const.NUMBER_VERT
    mov_direction_hor = MovDirectionEnum.RIGHT  # общее направление движения для всех инопланетян
    start_y = 45                                # отсчет от SCREEN_FRAME
    distance_between_hor = None                 # определяется в конструкторе первого инопланетянина
    distance_between_vert = None                # определяется в конструкторе первого инопланетянина
    current_speed_hor = Const.START_SPEED_HOR
    speed_increase_at_the_end = Const.FINISH_SPEED_HOR / Const.START_SPEED_HOR
                                                # во ск раз увеличится скорость движения, анимации и звуков под конец по сравнению с начальной
    shoot_frequancy = Const.DEFAULT_SHOOTING_FREQUANCY
    number_of_negative = None                   # определяется в конструкторе первого инопланетянина
    number_of_positive = None                   # определяется в конструкторе первого инопланетянина
    number_of_created_negative = 0
    number_of_created_positive = 0

    # .convert_alpha() и scale_img в конструкторе первого инопланетянина (потому что для .convert_alpha() нужен объект(?) в котором он используется)
    img_regular_up = pygame.image.load('images/aliens/1_up.png')
    img_regular_down = pygame.image.load('images/aliens/1_down.png')
    img_regular_splash = pygame.image.load('images/aliens/white_splash.png')
    img_negative_up = pygame.image.load('images/aliens/2_up.png')
    img_negative_down = pygame.image.load('images/aliens/2_down.png')
    img_negative_splash = pygame.image.load('images/aliens/black_splash.png')
    img_positive_up = pygame.image.load('images/aliens/3_up.png')
    img_positive_down = pygame.image.load('images/aliens/3_down.png')
    img_positive_splash = pygame.image.load('images/aliens/green_splash.png')

    sound_tick = pygame.mixer.Sound('sounds/alien_tick.wav')
    sound_tick_duration = 850                  # длительность звука тикания инопланетян, зависящий от их численности (в секундах)
    sound_death = sound_shoot = pygame.mixer.Sound('sounds/alien_killed.wav')

    def __init__(self, gun_rect):
        self.count = Alien.count
        Alien.count += 1

        self.frame = round(SCREEN_FRAME + gun_rect.width/2) + in_screen(2)  # рамка по периметру экрана для инопланетян (чтобы пушка в крайнем положении не могла попасть в инопланетянина)

        if self.count == 0:     # делает только первый инопланетянин
            # масштабирование изображений и конвертирование .convert_aplha()
            Alien.img_regular_up = scale_img(Alien.img_regular_up.convert_alpha(),width=in_screen(43))
            Alien.img_regular_down = scale_img(Alien.img_regular_down.convert_alpha(),width=in_screen(43))
            Alien.img_regular_splash = scale_img(Alien.img_regular_splash.convert_alpha(),width=in_screen(43))
            Alien.img_negative_up = scale_img(Alien.img_negative_up.convert_alpha(),width=in_screen(43))
            Alien.img_negative_down = scale_img(Alien.img_negative_down.convert_alpha(),width=in_screen(43))
            Alien.img_negative_splash = scale_img(Alien.img_negative_splash.convert_alpha(),width=in_screen(43))
            Alien.img_positive_up = scale_img(Alien.img_positive_up.convert_alpha(),width=in_screen(43))
            Alien.img_positive_down = scale_img(Alien.img_positive_down.convert_alpha(),width=in_screen(43))
            Alien.img_positive_splash = scale_img(Alien.img_positive_splash.convert_alpha(),width=in_screen(43))

            # рандомный выбор количества негатиный и позитивных из промежутков NUMBER_OF_NEGATIVE и NUMBER_OF_POSITIVE
            Alien.number_of_negative = random.randint(Const.NUMBER_OF_NEGATIVE[0], Const.NUMBER_OF_NEGATIVE[1])
            Alien.number_of_positive = random.randint(Const.NUMBER_OF_POSITIVE[0], Const.NUMBER_OF_POSITIVE[1])

            # определение расстояний между инопланетянами по горизонтали и по вертикали (6% и 8% от свободного места)
            Alien.distance_between_hor = round(0.06 * (SCREEN_SIZE - 2 * self.frame - Const.NUMBER_HOR * Alien.img_regular_down.get_width()))
            Alien.distance_between_vert = round(0.08 * (SCREEN_SIZE - (SCREEN_FRAME + in_screen(Alien.start_y)) - (SCREEN_FRAME + gun_rect.height) - Const.NUMBER_VERT * Alien.img_regular_down.get_height()))

        self.type = TypeEnum.REGULAR    # по дефолту делаем инопланетянина обычным

        # P{данного инопланетянина делаем негативным} = \frac{number_of_negative - number_of_created_negative}{44 - self.count}
        p_numerator = Alien.number_of_negative - Alien.number_of_created_negative
        p_denominator = Alien.start_numer_of_aliens - self.count
        p = random.randint(1,p_denominator) # точка в простанстве возможных исходов -- из знаменателя
        if p in range(1, p_numerator + 1):  # если точка принадлежит подпространству благоприятных исходов (если она из числителя)
            self.type = TypeEnum.NEGATIVE
            Alien.number_of_created_negative += 1

        if self.type != TypeEnum.NEGATIVE: # чтобы негативные не заменялись на положительных
            # для положительных аналогично
            p_numerator = Alien.number_of_positive - Alien.number_of_created_positive
            p_denominator = Alien.start_numer_of_aliens - self.count
            p = random.randint(1, p_denominator)
            if p in range(1, p_numerator + 1):
                self.type = TypeEnum.POSITIVE
                Alien.number_of_created_positive += 1

        # присваивание img_down и img_splash инопланетянину в зависимости от типа
        if self.type == TypeEnum.REGULAR:
            self.img = Alien.img_regular_down
            self.img_splash = Alien.img_regular_splash
        elif self.type == TypeEnum.NEGATIVE:
            self.img = Alien.img_negative_down
            self.img_splash = Alien.img_negative_splash
        elif self.type == TypeEnum.POSITIVE:
            self.img = Alien.img_positive_down
            self.img_splash = Alien.img_positive_splash

        # координаты x и y (сначала высчитываются более плавные float координаты, а потом они присваиваются реальным координатам на экране)
        self.rect = self.img.get_rect()
        self.float_x = 0 + self.frame + (self.count % Const.NUMBER_HOR)*(self.rect.width + Alien.distance_between_hor)
        self.rect.x = round(self.float_x)
        self.float_y = float(SCREEN_FRAME + in_screen(Alien.start_y) + (self.count // Const.NUMBER_HOR)*(self.rect.height + Alien.distance_between_vert) + 1.5 * SMALLFONT.get_height())
        self.rect.y = round(self.float_y)

        self.dead = False
        self.hit_time = - Const.SPLASH_DURATION - 1 # такое значение чтобы в начале игры не было изображения splash

        self.down = True    # True -> изображение _down, False -> изображение _up
        self.duration_of_down_up_animation = random.randint(1000,5000)      # определяется рандомная частота изменения изображения (от 1 до 5 сек)
        self.start_animation_duration = self.duration_of_down_up_animation
        self.time_of_last_changing_img = pygame.time.get_ticks()     # последнее время изменения изображения
        self.time_of_last_play_tick_sound = pygame.time.get_ticks()     # последнее время проигрывания звука тика

    def timer_for_down_up(self):
        '''каждые self.duration_of_down_up_animation мс меняет self.down на противоположный'''
        if pygame.time.get_ticks() - self.time_of_last_changing_img >= self.duration_of_down_up_animation:
            self.time_of_last_changing_img = pygame.time.get_ticks()
            self.down = not self.down

    def img_setter(self):
        '''меняет self.img в зависимости от self.down и self.type'''
        if self.type == TypeEnum.REGULAR:
            self.img = Alien.img_regular_down if self.down==True else Alien.img_regular_up
        elif self.type == TypeEnum.NEGATIVE:
            self.img = Alien.img_negative_down if self.down==True else Alien.img_negative_up
        elif self.type == TypeEnum.POSITIVE:
            self.img = Alien.img_positive_down if self.down==True else Alien.img_positive_up

    def timer_for_sound(self):
        '''каждые Alien.sound_tick_duration с проигрывает Alien.sound_tick'''
        if pygame.time.get_ticks() - self.time_of_last_play_tick_sound >= Alien.sound_tick_duration:
            self.time_of_last_play_tick_sound = pygame.time.get_ticks()
            Alien.sound_tick.play()

    def update(self, aliens_list, bullets_list, aliens_bullet_list, gun, progr_bars_list):
        '''смена изображения, изменение направления движения и скорости, изменение его координат, соприкосновение с пулями (и их удаление) и пушкой, проигрыш звука смерти пушки при соответствующем соприкосновении с ней, стрельба, удаление'''
        if not self.dead:   # пока не попали, обновляется, иначе просто держим изобржаение splash нужное время и удаляется
            # анимация инопланетян
            self.timer_for_down_up()
            self.img_setter()
            # ритмичный звук инопланетян
            if aliens_list.index(self) == 0:  # делает первый из выживших
                self.timer_for_sound()

            # изменение направления движения если коснулись рамки
            if self.rect.right >= SCREEN_SIZE - self.frame: # справа
                Alien.mov_direction_hor = MovDirectionEnum.LEFT
            elif self.rect.left <= 0 + self.frame:          # слева
                Alien.mov_direction_hor = MovDirectionEnum.RIGHT

            # передвижение вправо / влево
            if Alien.mov_direction_hor == MovDirectionEnum.RIGHT:
                self.float_x += Alien.current_speed_hor * SCREEN_SIZE / 800  # не in_screen() потому что не нужен round()
            elif Alien.mov_direction_hor == MovDirectionEnum.LEFT:
                self.float_x -= Alien.current_speed_hor * SCREEN_SIZE / 800  # не in_screen() потому что не нужен round()
            self.rect.x = round(self.float_x)

            # движение вниз
            self.float_y += Const.SPEED_VERT * SCREEN_SIZE / 800 # не in_screen() потому что не нужен round()
            self.rect.top = round(self.float_y)

            # собприкосновение с bullet
            if not self.dead:
                for bullet in bullets_list: # перебираем все пули пушки
                    if self.rect.colliderect(bullet): # если соприкаснулись с данной пулей
                        if Const.PLAY_SOUND_OF_DEATH == True:
                            Alien.sound_death.play()

                        self.dead = True
                        self.hit_time = pygame.time.get_ticks()
                        self.img = self.img_splash  # изменение изобржаения на всплеск
                        bullets_list.remove(bullet)

                        # а если еще и был негативный инопланетянин то увеличиваем частоту стрельбы в 3 раза и создаем новый негативный прогрессбар
                        if self.type == TypeEnum.NEGATIVE:
                            Alien.shoot_frequancy /= Const.NEGATIVE_SHOOTING_FREQUANCY_INCREASE
                            progr_bars_list.append(ProgressBar(TypeEnum.NEGATIVE, Const.NEGATIVE_SHOOTING_DURATION, Const.NEGATIVE_SHOOTING_FREQUANCY_INCREASE))
                        # а если был позитивным инопланетянин то увеличиваем hp пушки
                        elif self.type == TypeEnum.POSITIVE:
                            gun.hp += 1

            # собприкосновение с gun
            if gun.transparency == False:   # если пушка не прозрачная
                if self.rect.colliderect(gun):
                    if Const.PLAY_SOUND_OF_DEATH == True:
                        Alien.sound_death.play()

                    self.dead = True
                    self.hit_time = pygame.time.get_ticks()
                    self.img = self.img_splash

                    gun.hit_time = pygame.time.get_ticks()  # для мигания пушки
                    if gun.hp == 1:
                        gun.sound_death.play()
                        gun.lose_time = gun.hit_time        # для замораживания после проигрыша
                    gun.hp -= 1

                    # а если еще и был негативный инопланетянин то увеличиваем частоту стрельбы в 3 раза
                    if self.type == TypeEnum.NEGATIVE:
                        Alien.shoot_frequancy /= Const.NEGATIVE_SHOOTING_FREQUANCY_INCREASE
                        progr_bars_list.append(ProgressBar(TypeEnum.NEGATIVE, Const.NEGATIVE_SHOOTING_DURATION, Const.NEGATIVE_SHOOTING_FREQUANCY_INCREASE))
                    # а если еще и был позитивным инопланетянин
                    elif self.type == TypeEnum.POSITIVE:
                        gun.hp += 1

            # стрельба
            p = random.randint(0, round(Alien.shoot_frequancy * (len(aliens_list) / (Alien.start_numer_of_aliens))))  # частота * (число_живых / 44 ) -- чтобы чем меньше живых оставалось тем больше была частота их стрельбы
            if p == 0:  # с вероятностью 1 / shoot_frequancy добавляем новую пулю в список пуль
                aliens_bullet_list.append(AliensBullet(self))
        else:       # если время всплеска истекло -- увеличиваем скорость движения, анимации и звука и удаляем инопланетянина. В противном случае просто продолжаем держать изображение всплеска
            if pygame.time.get_ticks() - self.hit_time >= Const.SPLASH_DURATION:
                # изменение speed_hor в зависимости от числа виживших
                Alien.current_speed_hor += (Const.FINISH_SPEED_HOR - Const.START_SPEED_HOR) / Alien.start_numer_of_aliens
                # изменение длительности звука тикания в зависимости от числа виживших
                Alien.sound_tick_duration = 150 + (850-150) * (1 - (Alien.start_numer_of_aliens - len(aliens_list)) / (Alien.start_numer_of_aliens))     # множитель (1-..):  1 при всех живых  ->  0 при всех мертвых
                # изменение длительности анимации ВСЕХ в зависимости от числа виживших
                for ali in aliens_list:
                    ali.duration_of_down_up_animation -= (ali.start_animation_duration - ali.start_animation_duration / Alien.speed_increase_at_the_end) / (Alien.start_numer_of_aliens)

                aliens_list.remove(self)

        if self.screen_bottom(): # если данный инопланетянин коснулся низа экрана то фиксируем новое время проигрыша -- чисто для замораживания
            gun.lose_time = pygame.time.get_ticks()


    def output(self, screen):
        '''выводит на экран изрбражение данного инопланетянина с учетом его текущих координат'''
        screen.blit(self.img, self.rect)

    def screen_bottom(self):
        '''возвращает True если данный инопланетянин коснулся низа экрана'''
        if self.rect.bottom >= SCREEN_SIZE:
            return True  # в main: lose = True
        else:
            return False

    @classmethod
    def restart(cls, aliens_bullet_list):
        '''удаляет все выпущенные пули, возвращает аттрибуты класса к дефолтным значениям'''
        aliens_bullet_list.clear()
        cls.count = 0
        cls.number_of_created_negative = 0
        cls.number_of_created_positive = 0
        cls.current_speed_hor = Const.START_SPEED_HOR
        cls.sound_tick_duration = 850
        cls.shoot_frequancy = Const.DEFAULT_SHOOTING_FREQUANCY
        cls.mov_direction_hor = MovDirectionEnum.RIGHT

    @classmethod
    def create_new_army(cls, aliens_bullet_list, number, gun_rect):
        '''возвращает список длиной number созданных им инопланетян с дефолтными характеристиками'''
        cls.restart(aliens_bullet_list)
        aliens_list = []
        for _ in range(number):
            aliens_list.append(cls(gun_rect))
        return aliens_list





class AliensBullet():
    '''класс ОДНОЙ пули инполанетянина'''
    count_of_bullets_fired = 0
    speed_hor = 0.15 * Alien.current_speed_hor * SCREEN_SIZE / 800     # горизонтальная скорость пули при вылете из движещегося инопланетянина (делаем ее равной 0.15 от текущей скорости инопланетянин)
    speed_vert = Const.BULLET_SPEED_VERT * SCREEN_SIZE / 800

    img = pygame.image.load('images/aliens/aliens_bullet.png')  # .convert_alpha() и scale_img в конструкторе первой выпущенной пули

    def __init__(self, alien):
        if AliensBullet.count_of_bullets_fired == 0:     # делает только первая выпущенная пуля
            # доопределение изображения пулей
            self.img = scale_img(AliensBullet.img.convert_alpha(), height=in_screen(18))
        AliensBullet.count_of_bullets_fired += 1

        # задание знака горизонтальной скорости данной пули
        if alien.mov_direction_hor == alien.mov_direction_hor.RIGHT:
            self.speed_hor = AliensBullet.speed_hor
        elif alien.mov_direction_hor == alien.mov_direction_hor.LEFT:
            self.speed_hor = - AliensBullet.speed_hor

        self.rect = self.img.get_rect()
        # задание centerx
        self.centerx_float = alien.rect.centerx
        self.rect.centerx = round(self.centerx_float)
        # задание bottom
        self.bottom_float = alien.rect.bottom
        self.rect.bottom = round(self.bottom_float)


    def update(self, aliens_bullets_list):
        '''изменение координат x и y, актулизация горизонтальной скорости, удаление при выходе за экран'''
        # centerx
        self.centerx_float += self.speed_hor
        self.rect.centerx = round(self.centerx_float)
        # bottom
        self.bottom_float += AliensBullet.speed_vert
        self.rect.bottom = round(self.bottom_float)

        # актулизация горизонтальной скорости
        AliensBullet.speed_hor = 0.15 * Alien.current_speed_hor * SCREEN_SIZE / 800

        # удаление при выходе за экран
        if self.rect.top >= SCREEN_SIZE:
            self.list = aliens_bullets_list
            self.list.remove(self)

    def output(self,screen):
        '''выводит на экран изрбражение данной пули с учетом ее текущих координат'''
        screen.blit(self.img, self.rect)





class Ufo():
    '''класс НЛО'''
    # .convert_alpha() и scale_img в конструкторе
    img = pygame.image.load('images/aliens/ufo.png')
    img_splash = pygame.image.load('images/aliens/red_splash.png')

    sound = pygame.mixer.Sound('sounds/ufo_highpitch.wav')
    sound_duration = sound.get_length() * 1000 - 10     # 10 для приемлимой склейке звука в цикле

    def __init__(self):
        Ufo.img = scale_img(Ufo.img.convert_alpha(), width=in_screen(55))
        Ufo.img_splash = scale_img(Ufo.img_splash.convert_alpha(), width=in_screen(43))

        self.mov_direction = random.choice([MovDirectionEnum.RIGHT,MovDirectionEnum.LEFT])  # появляется он слева или справа

        self.img = Ufo.img
        self.rect = self.img.get_rect()
        # задание координаты x в зависимости от направления движения
        if self.mov_direction == MovDirectionEnum.RIGHT:
            self.rect.right = 0
        elif self.mov_direction == MovDirectionEnum.LEFT:
            self.rect.left = SCREEN_SIZE
        self.float_x = self.rect.x
        # задание координаты y
        self.rect.y = SCREEN_FRAME + in_screen(Alien.start_y) + 1.5 * SMALLFONT.get_height()

        self.time_of_init = pygame.time.get_ticks()             # время создания объекта Ufo (для времени появления)
        self.visible_on_screen = False                          # становится True если хотя бы один пиксель НЛО виден на экране
        self.time_of_appearance = random.randint(2000, Const.MAX_TIME_FOR_UFO_APPEARANCE_MOMENT)
        self.time_of_last_play_sound = pygame.time.get_ticks()  # последнее время проигрывания звука

        self.dead = False
        self.hit_time = - Const.SPLASH_DURATION - 1     # такое значение чтобы в начале игры не было изображения splash

    def update(self, ufo_list, bullets_list, gun, progr_bars_list):
        '''изменение координаты x, удаление при выходе за экран и при соприкосновении с пулями (и их удаление)'''
        if not self.dead:   # пока не попали, обновляется, иначе просто держим изобржаение splash нужное время и удаляется
            if pygame.time.get_ticks() - self.time_of_init >= self.time_of_appearance:  # если прошло больше чем self.time_of_appearance мс
                # проигрыш пищащего звука
                if Const.PLAY_UFO_SOUND == True:
                    if pygame.time.get_ticks() - self.time_of_last_play_sound >= self.sound_duration:
                        self.time_of_last_play_sound = pygame.time.get_ticks()
                        Ufo.sound.play()

                # изменение координаты x
                if self.mov_direction == MovDirectionEnum.RIGHT:
                    self.float_x += Const.UFO_SPEED * SCREEN_SIZE / 800 # не in_screen() потому что не нужен round()
                    self.rect.x = round(self.float_x)
                    if self.rect.right > 0:
                        self.visible_on_screen = True
                elif self.mov_direction == MovDirectionEnum.LEFT:
                    self.rect.x = round(self.float_x)
                    self.float_x -= Const.UFO_SPEED * SCREEN_SIZE / 800 # не in_screen() потому что не нужен round()
                    if self.rect.left < SCREEN_SIZE:
                        self.visible_on_screen = True

                # удаление если вышел за экран
                if self.visible_on_screen == True: # если хоть пиксель уже был виден на экране (это условие нужно чтобы в самом начале, когда НЛО еще не вышел в пределы, не срабатывал выход за экран)
                    if self.rect.left >= SCREEN_SIZE or self.rect.right <= 0:   # если полностью вышло за пределы экрана
                        ufo_list.remove(self)

                # собприкосновение с bullet
                if self.visible_on_screen == True: # чтобы попадание пули не отслеживалось когда НЛО за пределами экрана
                    for bullet in bullets_list:
                        if self.rect.colliderect(bullet):
                            self.dead = True
                            self.hit_time = pygame.time.get_ticks()
                            self.img = Ufo.img_splash

                            gun.transparency = True     # делаем пушку неуязвимой (уязвимость возвращается прогрессбаром)
                            progr_bars_list.append(ProgressBar(TypeEnum.UFO, Const.GUN_TRANSPARENCY_DURATION))  # создаем новый красный прогрессбар

                            bullets_list.remove(bullet)     # удаление пули
        else:   # если время всплеска истекло -- удаляем. В противном случае просто продолжаем держать изображение всплеска
            if pygame.time.get_ticks() - self.hit_time >= Const.SPLASH_DURATION:
                ufo_list.remove(self)

    def output(self, screen):
        '''выводит на экран изрбражение НЛО с учетом его текущих координат'''
        screen.blit(self.img, self.rect)
