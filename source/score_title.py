'''в модуле: реализация класса ScoreTitleSumbol одного символа из надписи 'bullets : количество_выпущенных_пуль' '''
from source.my_functions import in_screen
from source.CONSTANTS import SCREEN_SIZE, SCREEN_FRAME, SMALLFONT
from source.bullet import Bullet

class ScoreTitleSumbol():
    count = 0                       # сквозной счетчик
    symbols_before_digits = ''      # к ней в своем конструкторе добавляется каждый символ который до двоеточия включительно
    colon_was_added = False         # факт передачи двоеточия в конструктор

    def __init__(self, gun_hp_height, symb):    # symb -- инициализирующий символ из main и update_digits() (напр. 'b', ':', '5')
        self.count = ScoreTitleSumbol.count
        ScoreTitleSumbol.count += 1

        self.symb = str(symb)

        # добавляем в symbols_before_digits данный символ если это двоеточие или те символы что до двоеточия
        if not ScoreTitleSumbol.colon_was_added:
            ScoreTitleSumbol.symbols_before_digits += self.symb
            if self.symb == ':':
                ScoreTitleSumbol.colon_was_added = True

        self.rect = SMALLFONT.render(self.symb, 'White', False).get_rect()
        # координаты x и y данного символа
        self.rect.x = - 1       # определяется в update() (который знает весь список score_list символов)
        self.y_float = SCREEN_FRAME + gun_hp_height - SMALLFONT.get_height()
        self.rect.y = self.y_float
        self.start_y = self.rect.y

        self.color = 'White'
        self.hit = False        # факт попадания пули
        self.h = 0              # расстояние от первоначального y до текущего y

    @classmethod
    def update_digits(cls, score_list, gun_hp_height):
        '''удаляет цифры счета из score_list и добавляет обновленные'''
        del score_list[len(ScoreTitleSumbol.symbols_before_digits):]
        for digit in str(Bullet.count_of_bullets_fired):
            score_list.append(ScoreTitleSumbol(gun_hp_height, digit))

    def update(self, bullets_list, score_list, gun_hp_height, win):
        '''
        not win: обновление элементов-цифр в score_list, обновление координат x,

        win: отслеживание попадания bullet и ее удаление, изменение коордианты y при попадании
        '''
        if not win:
            # обновление цифр в выводимой строке
            if score_list.index(self) == 0:  # первый выживший
                ScoreTitleSumbol.update_digits(score_list, gun_hp_height)
            # обновление координаты x в зависимости от значности числа пуль
            self.rect.x = SCREEN_SIZE - round(1.5 * SCREEN_FRAME) - (len(score_list) - score_list.index(self)) * self.rect.width
        else:
            self.color = 'Black'

            # отслеживание попадания пули
            for bullet in bullets_list:
                if self.rect.colliderect(bullet):
                    self.hit = True
                    bullets_list.remove(bullet)

            # изменение координаты y
            if self.hit == True:
                self.h = self.rect.y - self.start_y  # текущая координата - начальная

                if self.rect.top < SCREEN_SIZE:     # если не вышла за экран
                    # меняем сначала фиктивную float-координату а потом реальную
                    self.y_float += in_screen(9.8) * (self.h + 1) / in_screen(60)    # +1 чтобы в начале сдвигалось не на 0
                    self.rect.y = round(self.y_float)
                else:
                    score_list.remove(self)         # иначе удаляем

    def output(self, screen):
        '''вывод данного символа на экран по вычисленным в update() координатам'''
        screen.blit(SMALLFONT.render(self.symb, False, self.color), self.rect)