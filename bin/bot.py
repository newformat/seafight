'''
Файл отвечающий за логику и стратегию бота.
'''
import random

class Bot:
    ''' Bot - собственно сам бот.
    method:
        get_hit - принимает выстрел в поле table_1
        set_hit - формирует координаты для выстрела по player.table_1
        check_hand -  связывающий метод с seh_hit  выбора координаты для выстрела как проверка
        strategy_x - одна стратегия которая стреляет по полю вниз и в право.
        modify_table -  отметка удара противника на таблице кораблей
    '''
    def __init__(self):
        self.table_1 = {}
        self.table_2 = {}       # по сути нам он не нужен, но он используется методом game.dots_install для отметки корабля
        self.ship_symbol = '@'  # вид палубы
        self.ships_count = None # корабли с координатами
        self.temp_coordinats = [] # список истории ходов, чтоб определить например последнее попадание
        self.temp_status_2 = [] # список истории ходов, после того как ранили корабль
        self.moves = []         # список, в котором хранятся все ходы бота
        self.strikes = []       # список всех попаданий
        # для стратегий:
        self.a = 1
        self.b = 0
        self.rnd = random.randint(0,1)



    def get_hit(self, coordinate):
        if self.table_1[coordinate[0]][coordinate[1]] == self.ship_symbol:
            return 0
        elif self.table_1[coordinate[0]][coordinate[1]] == '.' or self.table_1[coordinate[0]][coordinate[1]] == 'X':
            return -1
        else:
            return 1



    def set_hit(self,status):
        result = None # нужна для координат выстрела в режиме статуса числом выше 2х
        # случайный выстрел или случайный выстрел т.к. последний корабль убит
        if status == -1 or status == 1:
            # чистка данных
            self.temp_coordinats.clear()
            self.temp_status_2.clear()
            self.strikes.clear()

            # stratery_x
            '''
            возможно из за этого кода выход за пределы массива
            if self.rnd == 0:
                self.a += 1
                self.b += 1
                if not self.strategy_x():
                    return [self.a, self.b]
                else:
                    self.a=1
                    self.b=0
            '''
            # история данных
            rcord =  [random.randint(1,10),random.randint(0,9)]
            self.temp_coordinats.append(rcord[:])
            self.moves.append(rcord[:])
            return self.temp_coordinats[-1]
        # ранил
        elif status == 2:
            # берем последние координаты
            coord = self.temp_coordinats[-1]
            # рандомно выбираем куда стрелять
            list_check = [
                [coord[0], coord[1] + 1], [coord[0], coord[1] - 1],
                [coord[0] - 1, coord[1]], [coord[0] + 1, coord[1]]
            ]

            for i in random.choice([list_check]):
                # проверка границ
                if (i[0] <= 10 and i[0] >= 1) and (i[1] <= 9 and i[1] >= 0):
                    # выбираем рандомную координату и возвращаем ее
                    # выбирать то, что еще не выбиралось
                    if not i in self.temp_status_2:
                        self.temp_status_2.append(i)
                        self.moves.append(i[:])
                        return i
                    continue
                else:
                    continue
            else:
                print('что-то не так, метод bot.set_hit')
                exit(1)
        # не первое попадание в корабль
        elif status > 2:
            # если первые числа координаты положительны, значит корабль распологается по горизонтали
            # вертикаль
            if self.temp_coordinats[-1][0] == self.temp_status_2[-1][0]:
                # тут чекаем горизонталь
                return self.check_hand(1,0,9)
            # горизонталь
            elif self.temp_coordinats[-1][1] == self.temp_status_2[-1][1]:
                # тут чекаем вертикаль
                return self.check_hand(0, 1, 10)
            else:
                print('что то тут не так. метод bot.set_hit(), сектор elif status > 2')
                exit(1)



    def check_hand(self,hid,up,down):
        temp=0
        inc=1
        while 1:
            if inc:
                temp = max(self.strikes)[:]
                temp[hid]+=1
            else:
                temp = min(self.strikes)[:]
                temp[hid]-=1

            if temp in self.strikes:
                if inc: inc = 0
                else: inc = 1
                continue

            self.temp_coordinats[-1] = temp[:]

            #1 смотрим, нет ли таких же координатов
            if not self.temp_coordinats[-1] in self.moves:
                #2 границы <-->
                if self.temp_coordinats[-1][hid] <= down and self.temp_coordinats[-1][hid] >= up:
                    self.moves.append(self.temp_coordinats[-1][:])
                    return self.temp_coordinats[-1]
                else:
                    if inc:inc = 0
                    else: inc = 1
                    continue
            else:
                if inc: inc = 0
                else: inc = 1
                continue


    # с верху вниз, с лева на право.
    def strategy_x(self):
        if self.a <=10 and self.b <=9:
            return 0
        else:
            return 1


    # отметка удара противника на таблице кораблей
    def modify_table(self,coordinate,label):
        self.table_1[coordinate[0]][coordinate[1]] = label

