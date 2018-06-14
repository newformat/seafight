'''
Файл, отвечающий за механику действий игрока
'''

# Игрок 1
class Player:
    '''
    table_1 - таблица игрока с кораблями
    table_2 - таблица оппонента для ударов
    '''
    def __init__(self):
        self.table_1 = {}
        self.table_2 = {}
        self.name = None
        self.ship_symbol = '@'  # вид палубы
        self.ships_count = None # корабли с координатами


    # принять удар
    def get_hit(self, coordinate):
        if self.table_1[coordinate[0]][coordinate[1]] == self.ship_symbol:
            return 0
        elif self.table_1[coordinate[0]][coordinate[1]] == '.' or self.table_1[coordinate[0]][coordinate[1]] == 'X':
            return -1
        else:
            return 1
    # отметка удара противника на таблице кораблей
    def modify_table(self,coordinate,label):
        self.table_1[coordinate[0]][coordinate[1]] = label
        return

    # отметка удара второй таблицы противника
    def modify_table_2(self, coordinate, label):
        self.table_2[coordinate[0]][coordinate[1]] = label
        return
