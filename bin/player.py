'''
Файл, отвечающий за механику действий игрока
'''

# Игрок 1
class Player:
    '''
    table_1 - таблица игрока с кораблями
    table_2 - таблица оппонента для ударов
    methods:
        modify_table    отметка удара противника на таблице кораблей
        modify_table_2  отметка удара второй таблицы противника
        get_hit         принять удар

    '''
    def __init__(self):
        self.table_1 = {}
        self.table_2 = {}
        self.name = None
        self.ship_symbol = '@'  # вид палубы
        self.ships_count = None # корабли с координатами


    def get_hit(self, coordinate):
        if self.table_1[coordinate[0]][coordinate[1]] == self.ship_symbol:
            return 0
        elif self.table_1[coordinate[0]][coordinate[1]] == '.' or self.table_1[coordinate[0]][coordinate[1]] == 'X':
            return -1
        else:
            return 1


    def modify_table(self,coordinate,label):
        self.table_1[coordinate[0]][coordinate[1]] = label
        return


    def modify_table_2(self, coordinate, label):
        self.table_2[coordinate[0]][coordinate[1]] = label
        return
