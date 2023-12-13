'''в модуле: реализация моих функций scale_img() и in_screen()'''

import pygame
from source.CONSTANTS import SCREEN_SIZE

def scale_img(image, width=-1, height=-1):
    '''возвращает новый image с новой width или height, но с тем же соотношением сторон. Если указывается и width и height, то оригинальное соотношение сторон не учитывается'''
    if width == -1 and height > 0:
        return pygame.transform.scale(image, (image.get_width()/image.get_height() * height , height))
    elif height == -1 and width > 0:
        return pygame.transform.scale(image, (width, image.get_height() / image.get_width() * width))
    elif width > 0 and height > 0:
        return pygame.transform.scale(image, (width, height))
    else:
        return None

def in_screen(value):
    '''возвращает число, отмасштабированное с учетом SCREEN_SIZE. В данную функцию подаются числа, ориентированные на SCREEN_SIZE = 800'''
    return round(value * SCREEN_SIZE / 800)