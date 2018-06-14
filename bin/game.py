'''
Модуль процесса игры
'''

from time import sleep
from random import randint

from bin.player import Player
from bin.bot import Bot
from bin.gentable import GenTable
from bin.network import *


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
        player.table_1 = gen_table.ranking_auto(player.table_1)
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




    ''' игра по LAN-сети '''
    # если мы сервер
    def game_lan_server(self):
        player = Player()
        player_2 = Player()
        gen_table = GenTable()

        # Задаем данные игроку
        # даем 2 таблицы игроку
        player.table_1 = gen_table.get_table()
        player.table_2 = gen_table.get_table()

        # даем 2 таблицы игроку_2
        player_2.table_1 = gen_table.get_table()
        player_2.table_2 = gen_table.get_table()


        # авто расстановка (игрок)
        player.table_1 = gen_table.ranking_auto(player.table_1)
        player.ships_count = gen_table.get_ships()

        # будем автоматически раскидывать корабли (игрок_2)
        player_2.table_1 = gen_table.ranking_auto(player_2.table_1)
        player_2.ships_count = gen_table.get_ships()

        # СЕТЕВАЯ ЧАСТЬ КОДА
        lserver = LanServer()
        if lserver.create_server():
            return 1

        # прогон первого запроса, получаем имя
        # accept request client and get data request and  init player_2.name
        print('Ждем игрока...')
        lserver.accept_request()
        player_2.name = lserver.get_request_data()

        # имя клиента - если 1, значит имя очень большое или маленькое
        while self.check_name(player_2.name):
            lserver.send_data('name=false')
            player_2.name = lserver.get_request_data()
        else:
            lserver.send_data('name=true')

        # имя сервера
        player.name = input('Введите имя => ')
        while self.check_name(player.name):
            player.name = input('Введите имя => ')

        # отправляем первичные данные клиенту
        # имя сервера               - player.name
        # таблицу кораблей клиента  - player_2.table_1
        # таблицу оппонента         - player_2.table_2
        lserver.send_data((
                player.name,
                player_2.table_1,
                player_2.table_2
            ))
        # получаем ответ, что все хорошо(true)
        if lserver.get_request_data() == True:
            print('Данные успешно отправлены;')
            print('Имя игрока_2:', player_2.name)
            print('Начинаем игру...')
        else:
            print('что-то пошло не так... game.py 225 строка.')



        walk = 0
        while len(player.ships_count) != 0 and len(player_2.ships_count) != 0:
            coordinate = None
            # Ход игрока
            if not walk:
                while type(coordinate) != list:
                    coordinate = self.coordinate_converter(
                        input('\n{0}: ходит =>'.format(player.name)))
                    if coordinate == -1:
                        # -------- сетевая роль сервер -> клиент ------------
                        lserver.send_data((player_2.table_1, player_2.table_2, 'exit_server'))
                        self.check_request(lserver)
                        # ---------------------------------------------------
                        return 0

                print()
                result = player_2.get_hit(coordinate)
                # попал
                if result == 0:
                    player.modify_table_2(coordinate, 'X')
                    player_2.modify_table(coordinate, 'X')
                    if self.status_install(player_2.ships_count, 'k', coordinate) == 'k':
                        self.dots_install(player.table_2, player_2.table_1, player_2.ships_count)
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        print('{0}: убил...'.format(player_2.name))
                        # -------- сетевая роль сервер -> клиент ------------
                        lserver.send_data((player_2.table_1,player_2.table_2,'убил...',walk))
                        self.check_request(lserver)
                        # ---------------------------------------------------
                        continue
                    else:
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        print('{0}: ранил...'.format(player_2.name))
                        # -------- сетевая роль сервер -> клиент ------------
                        lserver.send_data((player_2.table_1,player_2.table_2,'ранил...',walk))
                        self.check_request(lserver)
                        # ---------------------------------------------------
                        continue
                # сюда стреляли уже
                elif result == -1:
                    print('стреляли уже')
                    continue
                # не попал
                else:
                    # вывод (обновления) таблицы на консоль
                    player.modify_table_2(coordinate, '.')
                    player_2.modify_table(coordinate, '.')
                    gen_table.view_table(player.table_1, player.table_2)
                    print('\n{0}: мимо =Р\n'.format(player_2.name))
                    # -------- сетевая роль сервер -> клиент ------------
                    lserver.send_data((player_2.table_1, player_2.table_2, 'мимо =Р',walk))
                    self.check_request(lserver)
                    # ---------------------------------------------------

                walk = 1
            # Ход игрока_2
            else:
                while type(coordinate) != list:
                    # -------- сетевая роль сервер -> клиент ------------
                    lserver.send_data('get_coordinate')
                    str_coordinate = lserver.get_request_data()
                    # ---------------------------------------------------
                    print('\n{0}: ходит =>'.format(player_2.name))
                    coordinate = self.coordinate_converter(str_coordinate)

                    # ответить на запрос о том, что клиент успешно покинул игру.
                    if coordinate == -1:
                        # -------- сетевая роль сервер -> клиент ------------
                        lserver.send_data('exit_client')
                        self.check_request(lserver)
                        # ---------------------------------------------------
                        return 0
                else:
                    # если координаты корректны
                    lserver.send_data('coordinate_yes')
                    self.check_request(lserver)

                print()
                result = player.get_hit(coordinate)
                # попал
                if result == 0:
                    player_2.modify_table_2(coordinate, 'X')
                    player.modify_table(coordinate, 'X')
                    if self.status_install(player.ships_count, 'k', coordinate) == 'k':
                        self.dots_install(player_2.table_2, player.table_1, player.ships_count)
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        print('{0}: убил...'.format(player.name))
                        # -------- сетевая роль сервер -> клиент ------------
                        lserver.send_data((player_2.table_1, player_2.table_2, 'убил...',walk))
                        self.check_request(lserver)
                        # ---------------------------------------------------
                        continue
                    else:
                        # вывод (обновления) таблицы на консоль
                        gen_table.view_table(player.table_1, player.table_2)
                        print('{0}: ранил...'.format(player.name))
                        # -------- сетевая роль сервер -> клиент ------------
                        lserver.send_data((player_2.table_1, player_2.table_2, 'ранил...',walk))
                        self.check_request(lserver)
                        # ---------------------------------------------------
                        continue
                # сюда стреляли уже
                elif result == -1:
                    print('стреляли уже')
                    # -------- сетевая роль сервер -> клиент ------------
                    lserver.send_data((player_2.table_1, player_2.table_2, 'стреляли',walk))
                    self.check_request(lserver)
                    # ---------------------------------------------------
                    continue
                # не попал
                else:
                    # вывод (обновления) таблицы на консоль
                    player_2.modify_table_2(coordinate, '.')
                    player.modify_table(coordinate, '.')
                    gen_table.view_table(player.table_1, player.table_2)
                    print('\n{0}: мимо =Р\n'.format(player.name))
                    # -------- сетевая роль сервер -> клиент ------------
                    lserver.send_data((player_2.table_1, player_2.table_2, 'мимо =Р',walk))
                    self.check_request(lserver)
                    # ---------------------------------------------------
                walk = 0

        else:
            # 1 - игрок_1 вин / 2 - игрок_2 вин
            count_player = 0
            if len(player.ships_count):
                print('\n{0} выйграл! Поздравляю!'.format(player.name))
                count_player = 1
            else:
                print('\n{0} выиграл! Поздравляю!'.format(player_2.name))
                count_player = 2

            print('кол-во кораблей {0}\t'.format(player.name), len(player.ships_count))
            print('кол-во кораблей {0}\t'.format(player_2.name), len(player_2.ships_count))
            print()
            # -------- сетевая роль сервер -> клиент ------------
            lserver.send_data((player_2.table_1, player_2.table_2, count_player,'end_game'))
            self.check_request(lserver)
            lserver.socket_close()
            return 0
            # ---------------------------------------------------


    # если мы клиент
    def game_lan_client(self):
        table = GenTable()
        player_2 = Player()
        client = LanClient()
        player_enemy = None

        # коннект с сервером
        client.connected()

        # вводим имя
        player_2.name = input('введите имя => ')
        client.send_data(player_2.name)
        # если имя не соответствует требованию (не более 9 и не менее 2 символов на имя)
        while client.get_answer() == 'name=false':
            # вводим еще раз соответствуя требованиям
            player_2.name = input('введите имя => ')
            client.send_data(player_2.name)

        # получаем первичные ответные данные
        INFORMATION = client.get_answer()
        # тип данных должен быть кортежем
        if type(INFORMATION) == tuple:
            # отправляем серверу что все хорошо
            client.send_data(True)
        else:
            print('что-то не так.. exit(1)')
            exit(1)

        # инит данных
        player_enemy = INFORMATION[0]       # имя оппонента
        player_2.table_1 = INFORMATION[1]   # таблица кораблей
        player_2.table_2 = INFORMATION[2]   # таблица выстрелов


        # Вывод таблиц на экран
        print()
        table.view_table(player_2.table_1,player_2.table_2)
        # ответ запроса сервера
        result_request = client.get_answer()
        # игра не закончена
        while result_request[-1] != 'end_game':

            # выход во время игры
            if result_request in ['exit_client', 'exit_server']:
                print('выход из игры.. возврат в главное меню...')
                client.socket_close()
                return 0

            while result_request == 'get_coordinate':
                client.send_data(input('ваш ход => '))
                result_request = client.get_answer()
            else:
                if result_request == 'coordinate_yes':
                    client.send_data(True)
                    result_request = client.get_answer()

            # walk = 0 , ходит сервер (ничего не делаем)
            if (result_request[-2] in ['убил...', 'ранил...', 'мимо =Р']) and result_request[-1] == 0 :
                client.send_data(True)
                print()
                table.view_table(result_request[0],result_request[1])
                print(player_enemy,result_request[-2])
                result_request = client.get_answer()
                continue

            # walk = 1, ходит клиент
            if (result_request[-2] in ['убил...', 'ранил...', 'стреляли']) and result_request[-1] == 1 :
                client.send_data(True)
                table.view_table(result_request[0],result_request[1])
                print(player_enemy,result_request[-2])
                result_request = client.get_answer()
            elif result_request[-2] == 'мимо =Р':
                client.send_data(True)
                table.view_table(result_request[0],result_request[1])
                print(player_enemy,result_request[-2])
                result_request = client.get_answer()
        else:
            # lserver.send_data((player_2.table_1, player_2.table_2, count_player,'end_game'))
            # count_player - 1 ( player 1 win), 2 - (player 2 win)
            table.view_table(result_request[0],result_request[1])
            if result_request[-2] == 2:
                print(player_2.name,' выиграл!')
                print(player_enemy, 'проиграл!')
            else:
                print(player_2.name,'проиграл!')
                print(player_enemy, 'выйграл!')
            client.send_data(True)
            client.socket_close()

        return 0




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


    # получаем имя, проверяем валидность.
    def check_name(self, client_name):

        if len(client_name) < 2:
            print('Имя игрока меньше 2 символов!')
            return 1
        elif len(client_name) > 9:
            print('Имя игрока больше 9 символов!')
            return 1

        return 0

    # проверка, успешно ли пришел запрос на клиент
    def check_request(self, handle):
        if handle.get_request_data() != True:
            print('сообщение не долшо, аварийный выход')
            handle.socket_close()
            exit(1)
        else:
            return 0


