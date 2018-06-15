'''
Файл меню, отвечает за вывод информации о пунктах меню.
'''
class Menu:
    def __init__(self):
        self.m_item = 2 # кол-во пунктов меню


    def welcome(self):
        print()
        print('Главное меню:')
        print('1 - игра с ботом')
        print('2 - игра по LAN ')
        print('0 - выход')
        #print('3 - игра по Интернету')

    # подменю пункта "игра с ботом", ...
    def choice_table(self):
        print()
        print('Размещение кораблей:')
        print('1 - авто')
        #print('2 - в ручную')
        print('0 - отмена')

    # заморожено
    def ranking_manual_print(self):
        print('тут придумать метод ввода ручной установки кораблей')


    def lan_menu(self):
        print()
        print('1 - создать игру')
        print('2 - найти игру')