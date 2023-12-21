'''модуль с константами, влияющими на геймплей, которые можно менять в угоду игроку'''

SCREEN_SIZE = 720               # размер квадратного экрана (в пикселях)
FRAMERATE = 80                  # фреймрейт (кадров в сек), влияет на скорость происходящего на экране

class GunConst():
    DURATION_OF_FLASH_TICK = 100        # длительность отображения каждого из цветов при мигании пушки от попадания пули (в мс)
    NUMBER_OF_FLASH_CYCLES = 2          # количество циклов мигания при попадании пули
    DURATION_OF_LOSE_FREEZE = 900       # длительность заморозки происходящего на экране при проигрыше (в мс)
    SPEED = 5                           # горизонтальная скорость пушки (округляется до int)
    START_HP = 3                        # начальное количество жизней
    PLAY_SOUND_OF_SHOOT = False

    BULLET_SPEED_VERT = 13              # вертикальная скорость наших пуль (учитывается float)

class AlienConst():
    NUMBER_HOR = 11                             # количество инопланетян по горизонтали (от 1 до 17 включительно)
    NUMBER_VERT = 4                             # количество инопланетян по вертикали (от 1 до 13 включительно)

    START_SPEED_HOR = 1.0                       # начальная горизонтальная скорость (учитывается float)
    FINISH_SPEED_HOR = 15.0                     # конечная горизонтальная скорость (при одном живом инопланетянине) (учитывается float)
    SPEED_VERT = 0.5                            # скорость опускания всех инопланетян (учитывается float)
    SPLASH_DURATION = 100                       # длительность анимации всплеска при попадании (мс)

    BULLET_SPEED_VERT = 13                      # вертикальная скорость пуль инопланетян (учитывается float)

    NUMBER_OF_NEGATIVE = (1, 3)                 # количество негативных инопланетян будет варьироваться от перового до второго числа включительно (первое должно быть <= второго)
    NUMBER_OF_POSITIVE = (0, 1)                 # количество позитивных инопланетян будет варьироваться от перового до второго числа включительно (первое должно быть <= второго)
    DEFAULT_SHOOTING_FREQUANCY = 2000           # вероятность выстрела каждым инопланетяниным в каждом фрейме = 1 к shoot_frequancy
    NEGATIVE_SHOOTING_FREQUANCY_INCREASE = 3.0  # во сколько раз увеличивается частота стрельбы при попадании в негативного инопланетянина
    NEGATIVE_SHOOTING_DURATION = 3000           # длительность учащенной стрельбы (мс)

    UFO_SPEED = 1.5                             # горизонтальная скорость НЛО
    GUN_TRANSPARENCY_DURATION = 7000            # длительность неуязвимости пушки при попадании в НЛО (мс)
    MAX_TIME_FOR_UFO_APPEARANCE_MOMENT = 20000  # максимлаьный момент времени (с начала раунда) в который НЛО может появиться

    PLAY_SOUND_OF_DEATH = False
    PLAY_UFO_SOUND = False




SCREEN_FRAME = round(10 * SCREEN_SIZE / 800)        # рамка по периметру экрана, за которую ничто, кроме пуль, не заходит

import pygame
pygame.init()

SMALLFONT = pygame.font.Font('fonts/PublicPixel.ttf', round(22 * SCREEN_SIZE / 800))    # шрифт для вывода количества выпущенных пуль, highscore и надписи 3x около прогрессбара
# размер каждого символа (с учетом расстояния между символами) -- 22x22 (на экране 800x800). Отдельных расстояний между символами нет