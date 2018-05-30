'''
Файл отвечающий за таблицы.
- генерирует таблицы
- первичное заполение таблицы кораблями (ручное,автоматик)
'''
from bin.menu import Menu
from random import randint
from copy import deepcopy   # copy - модуль поверхностного(.copy) и полного(.deepcopy) копирования объектов
''' класс создания таблицы и расстановка кораблей
GenTable - класс, отвечающий за построение таблиц
    attribute:
        __menu          отвечат за вывод меню выбора расстановки кораблей
        __item_table    вариант выбора по умолчанию
        up              символы для пустого поля
        __table         образец пустой таблицы
    method:
        menu_ship       пункт выбора расстановки кораблей
        view_table      вывод таблиц на экран
        get_table       возвращает копию пустой таблицы
        get_ships       возвращает кол-во кораблей с координатами
        ranking_manual  ручное распределение кораблей
        ranking_auto    автоматическое распределение кораблей на игрока
        dots_check      проверка точки вокруг своей оси. для установки палубы
        temp_coordinate пополняет массив координат для установки корабля      
'''
class GenTable:
    def __init__(self):
        self.__menu = Menu()
        self.__item_table = '0'

        #таблица
        self.up = list(10 * ' ')
        self.__table = {1: self.up[:], 2: self.up[:], 3: self.up[:], 4: self.up[:], 5: self.up[:],
                    6: self.up[:], 7: self.up[:], 8: self.up[:], 9: self.up[:], 10: self.up[:]}
        # число кораблей для игрока
        self.ships_count = []
        # вид палубы
        self.ship_symbol = '@'



    def menu_ship(self,table):
        self.__menu.choice_table()

        while self.__item_table != '1' and self.__item_table !='2':
            self.__item_table = input('=>')
            if self.__item_table == '0': return 1

        # выбор расстановки
        if int(self.__item_table) == 1:
            return self.ranking_auto(table)
        else:
            return self.ranking_manual(table)



    def view_table(self, table_a, table_b):
        '''Вывод таблиц по горизонту
            table_a - таблица кораблей
            table_b - таблица оппонента '''
        #print('Таблица кораблей' + 3 * '\t' + 'Таблица оппонента')
        print(3 * ' ', end='')

        # таблица кораблей
        for a in 'АБВГДЕЖЗИК':
            print(a, end=1 * ' ')
        print(end=6 * ' ')
        # таблица оппонента
        for a in 'АБВГДЕЖЗИК':
            print(a, end=1 * ' ')
        print()

        for i in table_a:
            if i != 10:
                print(i, end='  ')
            else:
                print(i, end=' ')

            if i == 10:
                print(' '.join(table_a[i]), 2 * ' ', i, ' '.join(table_b[i]))
                continue

            print(' '.join(table_a[i]), 2 * ' ', i, '', ' '.join(table_b[i]))



    def get_table(self):
        return deepcopy(self.__table)



    def get_ships(self):
        temp = deepcopy(self.ships_count)
        self.ships_count.clear()
        # установка первичных статусов состояния кораблей
        for ship in temp:
            for deck in ship:
                deck.append('g')
            ship.append('g')
        return temp



    def ranking_manual(self,table):
        print('\"в ручную\" -  в стадии разработки')
        return table



    def ranking_auto(self,table):
        # корабли
        # пример: x1 - однопалубный корабль
        ships = [
            [0,1,2,3],          # четрыехпалубный - 1 шт
            [0,1,2],[0,1,2],    # трехпалубный - 2 шт
            [0,1],[0,1],[0,1],  # двухпалубный - 3 шт
            [0],[0],[0],[0]     # однопалубный - 4 шт
        ]

        ''' Общая картина
        1 - [0,1,2,3,4,5,6,7,8,9]
        2 - [0,1,2,3,4,5,6,7,8,9]
        3 - [0,1,2,3,4,5,6,7,8,9]
        4 - [0,1,2,3,4,5,6,7,8,9]
        5 - [0,1,2,3,4,5,6,7,8,9]
        6 - [0,1,2,3,4,5,6,7,8,9]
        7 - [0,1,2,3,4,5,6,7,8,9]
        8 - [0,1,2,3,4,5,6,7,8,9]
        9 - [0,1,2,3,4,5,6,7,8,9]
        10 - [0,1,2,3,4,5,6,7,8,9]
        '''

        cnt=0
        # цикл while перебирает все корабли в сортировке с их количеством на тип.
        while cnt < len(ships):
            err = 0
            # получить точку установки корабля
            a, b = randint(1, 10), randint(0, 9)
            # выбор установки: горизонталь(0) или вертикаль(1)
            direction = randint(0, 1)
            # в какую сторону устанавливать: низ/право(0) или вверх/лево(1)
            direction_correct = randint(0, 1)


            if table[a][b] != self.ship_symbol:
                coordinates_ship = []
                for ship in ships[cnt]:
                    # вертикаль - вверх
                    if direction and direction_correct:
                        # если 1 ( размещение не возможно) то err=1
                        if self.temp_coordinate(a-ship,b,coordinates_ship,table):
                            err = 1; break
                    # вертикаль - вниз
                    elif direction and not direction_correct:
                        if self.temp_coordinate(a + ship,b,coordinates_ship,table):
                            err = 1; break
                    # горизонталь - лево
                    elif not direction and direction_correct:
                        if self.temp_coordinate(a,b - ship,coordinates_ship,table):
                            err = 1; break
                    # горизонталь - право
                    elif not direction and not direction_correct:
                        if self.temp_coordinate(a,b + ship,coordinates_ship,table):
                            err = 1; break
                # в случае успешного окончания, устанавливаем корабаль
                else:
                    self.ships_count.append(coordinates_ship)
                    for coordinate in coordinates_ship:
                       table[coordinate[0]][coordinate[1]] = self.ship_symbol
            else:
                continue

            # 1, если позиция для установки корабля не пригодна.
            if err:
                continue

            cnt+=1

        return table



    def temp_coordinate(self,a,b,coordinates_ship,table):
        if self.dots_check(a, b, table) == 1:
            return 1
        else:
            coordinates_ship.append([a, b])
            return 0



    def dots_check(self,a,b,table_cp):
        list_check = [
            [a, b+1],[a, b-1],
            [a-1, b],[a+1, b],
            [a+1, b+1],[a-1, b+1],
            [a+1, b-1],[a-1, b-1]
        ]

        for i in list_check:
            # проверка границ
            if a < 1 or a > 10 or  b < 0 or b > 9:
                return 1
            elif (i[0] <= 10 and i[0] >= 1) and (i[1] <= 9 and i[1] >= 0):
                if table_cp[i[0]][i[1]] == self.ship_symbol:
                    return 1
            else:
                continue

        return 0
