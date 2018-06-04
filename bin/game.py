'''
Модуль процесса игры
'''

from time import sleep
from random import randint

from bin.player import Player
from bin.bot import Bot
from bin.gentable import GenTable

class Game:
    ''' Game - отвечает за процесс игры
    method:
        game_bot                игра с ботом
        coordinate_converter    конвертация данных координат для массива (напр. Б1 - > 2,0)
        dots_install            установка точек вокруг пораженного корабля
        status_check            проверка на статусы, состояние кораблей
        status_install          установка статуса палубы
    '''
    def __init__(self):
        self.abc = 'АБВГДЕЖЗИК'


    ''' Режимы игры '''
    def game_bot(self):
        bot = Bot()
        player = Player()
        gen_table = GenTable()

        # Задаем данные игрокам
        # даем 2 таблицы боту
        bot.table_1 = gen_table.get_table()
        bot.table_2 = gen_table.get_table()
        # даем 2 таблицы игроку
        player.table_1 = gen_table.get_table()
        player.table_2 = gen_table.get_table()

        # выбор расстановки корабля для игрока
        # кол-во кораблей с координатами на игрока
        player.table_1 = gen_table.menu_ship(player.table_1)
        player.ships_count = gen_table.get_ships()

        # бот будет автоматически раскидывать корабли
        bot.table_1 = gen_table.ranking_auto(bot.table_1)
        bot.ships_count = gen_table.get_ships()

        # true если вернет число вместо списка, значит назад в главное меню.
        if type(player.table_1) == int:
            return 1

        # Судьба первого хода
        # 0 - начинает игрок
        # 1 - начинает бот
        print('Кто первый? секундочку...\n')
        sleep(1)
        walk = randint(0,1)

        # формат хода напр. Б9
        # кол-во кораблей не равно нулю
        status=-1 # переменная действует как статус для бота, ранил(2) он или убил(1)
        while len(player.ships_count) != 0  and len(bot.ships_count) != 0:
            coordinate = None
            # Ход игрока
            if not walk:
                while type(coordinate) != list:
                    coordinate = self.coordinate_converter(input('\nИгрок: ходит =>')) #[randint(1,10),randint(0,9)] (для теста)
                    if coordinate == -1: return 0

                print()
                result = bot.get_hit(coordinate)
                # попал
                if result == 0:
                    player.modify_table_2(coordinate, 'X')
                    bot.modify_table(coordinate,'X')
                    if self.status_install(bot.ships_count,'k',coordinate) == 'k':
                        self.dots_install(player.table_2,bot.table_1, bot.ships_count)
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        print('Бот: убил...')
                        continue
                    else:
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        print('Бот: ранил...')
                        continue
                # сюда стреляли уже
                elif result == -1:
                    print('стреляли уже')
                    continue
                # не попал
                else:
                    # вывод (обновления) таблицы на консоль
                    player.modify_table_2(coordinate, '.')
                    bot.modify_table(coordinate,'.')
                    gen_table.view_table(player.table_1, player.table_2)
                    print('\nБот: мимо =Р\n')

                walk = 1
            # Ход бота
            else:
                # координаты для удара
                coordinate = bot.set_hit(status)
                # игрок получает удар
                result = player.get_hit(coordinate)

                # сюда стреляли уже
                if result == -1:
                    continue

                print('Бот: хожу...\n')
                sleep(1)

                # попал
                if result == 0:
                    # если бот попал, то записываем в table_1 к игроку
                    player.modify_table(coordinate, 'X')

                    # если корабль имеет статус = k, значит подох.
                    if self.status_install(player.ships_count,'k',coordinate) == 'k':
                        # записываем попадание.
                        bot.strikes.append(coordinate[:])
                        # если корабль подох, то отмечаем его вокруг точками на таблице игрока
                        self.dots_install(player.table_1,bot.table_2, player.ships_count)
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        status = 1 # для координат, убит
                        print('Бот: убил твой корабль')
                        print('Бот: снова хожу')
                        continue
                    # ранил
                    else:
                        # записываем попадание.
                        bot.strikes.append(coordinate[:])
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)

                        if status != 2 and  status < 2:
                            status = 2 # статус для координат, ранил
                        # если статус больше 2. значит бот ищет как его добить
                        else:
                            status+=1

                        print('Бот: ранил твой корабль')
                        print('Бот: снова хожу')
                        continue
                # не попал
                else:
                    player.modify_table(coordinate, '.')
                    # вывод (обновления) таблицы на консоль
                    gen_table.view_table(player.table_1, player.table_2)
                    print('\nБот: промах\n')

                # вывод (обновления) таблицы на консоль
                gen_table.view_table(player.table_1, player.table_2)
                walk = 0
        else:
            if len(player.ships_count):
                print('\nИгрок выйграл! Поздравляю!')
            else:
                print('\nБот выиграл! Поздравляю!')

            print('кол-во кораблей игрока\t',len(player.ships_count))
            print('кол-во кораблей бота\t',len(bot.ships_count))
            print()



    # игра по LAN-сети
    def game_lan(self):
        return



    # игра по интернету
    def game_eth(self):
        return


    # ###### ОСТАЛЬНЫЕ МЕТОДЫ #######
    def coordinate_converter(self,coordinate):
        temp_coordinate = []

        # если 0, то выход из цикла игры
        if coordinate == '0': return -1

        # если пустая строка, то по новой.
        if coordinate == '': return 1

        ch = 0
        for i in self.abc:
            if coordinate[0].upper() == i:
                temp_coordinate.append(ch)
                break
            ch += 1
        else: return 1

        if len(coordinate) == 3:
            try:
                if coordinate[-2:] == '10':
                    temp_coordinate.append(int(coordinate[-2:]))
                else: return 1
            except ValueError: return 1
        elif len(coordinate) == 2:
            try:
                temp_coordinate.append(int(coordinate[1]))
            except ValueError: return 1
        else: return 1

        temp_coordinate.reverse()
        return temp_coordinate



    def dots_install(self,table,table_2,ships):
        # проверяем, есть ли дохлый корабль?
        result = self.status_check(ships)
        if result != None:
            for duck in ships[result][:-1]:
                temp_coord = []
                for coord in duck:
                    # координата убитого корабля
                    temp_coord.append(coord)

                list_check = [
                    [temp_coord[0], temp_coord[1] + 1], [temp_coord[0], temp_coord[1] - 1],
                    [temp_coord[0] - 1, temp_coord[1]], [temp_coord[0] + 1, temp_coord[1]],
                    [temp_coord[0] + 1, temp_coord[1] + 1], [temp_coord[0] - 1, temp_coord[1] + 1],
                    [temp_coord[0] + 1, temp_coord[1] - 1], [temp_coord[0] - 1, temp_coord[1] - 1]
                ]

                for i in list_check:
                    # проверка границ
                    if (i[0] <= 10 and i[0] >= 1) and (i[1] <= 9 and i[1] >= 0):
                        if table[i[0]][i[1]] == 'X':
                            continue
                        else:
                            table[i[0]][i[1]] = '.'
                            table_2[i[0]][i[1]] = '.'
                    else:
                        continue
                # чистка временного списка для новых координат
                temp_coord.clear()
            else:
                ships.pop(result)
        else:
            print('что-то пошло не так, метод dots_install')
            exit(1)



    def status_check(self,ships):
        # проверка на статусы
        cnt=0
        for status_ship in ships:
            if status_ship[-1] == 'k':
                return cnt
            cnt+=1
        return None



    def status_install(self, ships, status,coord):
        for sh in ships:
            for s in sh:
                if s[0] == coord[0] and s[1] == coord[1]:
                    s[-1] = status
        # Обновление статусов кораблей
        for status_ship in ships:
            deck_number = 0
            # перебор палуб корабля
            for sh in status_ship:
                if sh[-1] == 'k':
                    deck_number +=1
            # все ли палубы убиты или частично?
            if len(status_ship) - 1 == deck_number:
                status_ship[-1] = 'k'
                return 'k'
            elif deck_number > 0:
                status_ship[-1] = 'w'
