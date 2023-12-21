'''в модуле: реализация класса ScoreTitleSumbol одного символа из надписи 'bullets : количество_выпущенных_пуль' '''
from source.my_functions import in_screen
from source.CONSTANTS import SCREEN_SIZE, SCREEN_FRAME, SMALLFONT
from source.bullet import Bullet

class ScoreTitleSumbol():
    count = 0                               # сквозной счетчик
    symbols_before_digits_in_score = ''     # к ней в своем конструкторе добавляется каждый символ который до двоеточия включительно
    colon_was_added = False                 # факт передачи двоеточия в конструктор

    def __init__(self, from_screenframe_to_bottom_title, symb, row):
        '''symb -- инициализирующий символ из main и update_digits() (напр. 'b', ':', '5'), row -- ряд в котором строит данный символ (0 -> первая строка, 1 -> вторая строка)'''
        self.count = ScoreTitleSumbol.count
        ScoreTitleSumbol.count += 1

        self.symb = str(symb)
        self.row = row

        # добавляем в symbols_before_digits_in_score данный символ если это двоеточие или те символы что до двоеточия
        if self.row == 0:   # только для первой строки (для 'bullets:123')
            if not ScoreTitleSumbol.colon_was_added:
                ScoreTitleSumbol.symbols_before_digits_in_score += self.symb
                if self.symb == ':':
                    ScoreTitleSumbol.colon_was_added = True

        self.rect = SMALLFONT.render(self.symb, 'White', False).get_rect()
        # координаты x и y данного символа
        self.rect.x = - 1       # определяется в update() (который знает весь список score_list символов)
        self.y_float = SCREEN_FRAME + from_screenframe_to_bottom_title - SMALLFONT.get_height() + self.row * 1.5 * SMALLFONT.get_height()
        self.rect.y = self.y_float
        self.start_y = self.rect.y

        self.color = 'White'
        self.hit = False        # факт попадания пули
        self.h = 0              # расстояние от первоначального y до текущего y

    @classmethod
    def update_digits(cls, symb_list, old_highscore=-1):    # old_highdcore -- только для symb_list = highscore_list
        '''удаляет цифры после ':' из symb_list и добавляет обновленные'''
        if symb_list[0].row == 0:   # для score_list
            del symb_list[len(ScoreTitleSumbol.symbols_before_digits_in_score):]
            for digit in str(Bullet.score):
                symb_list.append(ScoreTitleSumbol(symb_list[0].rect.y - SCREEN_FRAME + SMALLFONT.get_height() - symb_list[0].row * 1.5 * SMALLFONT.get_height(), digit, 0))
        elif symb_list[0].row == 1: # для highscore_list
            # (почему тут мы просто удалем n элементов с конца на кажном фрейме а в score_list мы в начале вычисляем количество букв до цифр -- потому что во втором случае значность числа меняется отностельно часто поэтому каждый раз пересчитывать значность на пред выстреле и на следующем не рационально)
            del symb_list[-len(str(old_highscore)):]   # удаляет последние Bullet.highscore элементов
            for digit in str(Bullet.highscore):
                symb_list.append(ScoreTitleSumbol(symb_list[0].rect.y - SCREEN_FRAME + SMALLFONT.get_height() - symb_list[0].row * 1.5 * SMALLFONT.get_height(), digit, 1))

    def update_x(self, symb_list):
        '''обновление координаты x данного символа из symb_list в зависимости от значности score и highscore'''
        # длины чисел в первой и второй строке
        len_score = len(str(Bullet.score))
        len_highscore = len(str(Bullet.highscore))
        delta = 0  # на сколько символов данной строке нужно сдвинуться влево чтобы двоеточия были друг под другом
        if self.row == 0 and len_score < len_highscore:  # если первой строке нужно двинуться влево
            delta = len_highscore - len_score
        elif self.row == 1 and len_score > len_highscore:  # если второй строке нужно двинуться влево
            delta = len_score - len_highscore

        self.rect.x = SCREEN_SIZE - round(1.5 * SCREEN_FRAME) - ((len(symb_list) - symb_list.index(self)) + delta) * self.rect.width

    def update(self, bullets_list, symb_list, win):
        '''
        not win: обновление элементов-цифр в score_list, обновление координат x для всех символов в score_list и highscore_list,

        win: (для всех символов в score_list и highscore_list) отслеживание попадания bullet и ее удаление, изменение коордианты y при попадании
        '''
        if not win:
            if self.row == 0:   # только для score_list
                # обновление цифр в score
                if symb_list.index(self) == 0:  # делает только первый из score_list
                    ScoreTitleSumbol.update_digits(symb_list)

            self.update_x(symb_list)
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

                if self.rect.top < SCREEN_SIZE:     # если не вышла за экран снизу
                    # меняем сначала фиктивную float-координату а потом реальную
                    self.y_float += in_screen(9.8) * (self.h + 1) / in_screen(60)    # +1 чтобы в начале сдвигалось не на 0
                    self.rect.y = round(self.y_float)
                else:
                    symb_list.remove(self)         # иначе удаляем

    def output(self, screen):
        '''вывод данного символа на экран по вычисленным в update() координатам и цветом'''
        screen.blit(SMALLFONT.render(self.symb, False, self.color), self.rect)

    @classmethod
    def update_highscore_and_txt_and_titles(cls, score_list, highscore_list):
        '''
        вызывается единоразово в начале win_run()

        если мы побили рекорд:

        - обновляет переменную highscore

        - записывает в highscore.txt текущий highscore

        (если значение в highscore.txt было не валидно (или если файла не существовало) то (создает файл и) перезаписывает в файл текущее значение вып. пуль)

        обновляет цифры в highscore_list

        вызывает update_x() для всех символов из highscore_list и score_list
        '''

        old_highscore = Bullet.highscore  # нужно чтобы update_digits() знал сколько удалять цифр с конца highscore_list

        # Bullet.highscore равно None в случае если в txt было пусто или его не существовало
        if Bullet.highscore is not None and Bullet.highscore.isdigit():  # and если первая строка txt это чисто цифры (т.е. не отрицательный инт)
            if Bullet.score < int(Bullet.highscore):
                Bullet.highscore = Bullet.score
                with open('source/highscore.txt', 'w') as f:  # стирает файл при открытии
                    f.write(str(Bullet.highscore))  # не переходит на след строку к отличие от print(.., file=f)
        else:
            Bullet.highscore = Bullet.score
            with open('source/highscore.txt', 'w') as f:
                f.write(str(Bullet.highscore))  # не переходит на след строку к отличие от print(.., file=f)

        ScoreTitleSumbol.update_digits(highscore_list, old_highscore)   # не в первом if-е чтобы update_digits() вызывался в т.ч. в невалидных случаях

        for symb in highscore_list:
            symb.update_x(highscore_list)
        for symb in score_list:
            symb.update_x(score_list)