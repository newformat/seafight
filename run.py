#!/usr/bin/python3
# свои модули
from bin.menu import Menu
from bin.game import Game

# приветсвие
def welcome_print():
    cnt_shebang=36
    print(cnt_shebang*'#')
    print('# Добро пожаловать в \'Морской бой\' #')
    print(cnt_shebang*'#')
    return

# init modules bin.
menu = Menu()
game = Game()
# init var
item = -1

#run application
if __name__ == "__main__":
    welcome_print()

    while item != 0:
       menu.welcome()

       try: item = int(input('=>'))
       except:
           print('некорретный ввод')
           continue

       if item > menu.m_item or item < 0:
           print('такого пункта в меню нет.')
           continue

        # запуск режимов игры (набросок)
       # игра с ботом
       if item == 1:
           game.game_bot()
           #print('Режим \'игра с ботом\' в разработке..')
        # игра по LAN сети
       elif item == 2:
           print('Режим \'Игра по LAN\' в разработке..')
        # игра по Интернету
       elif item == 3:
           print('Режим \'Игра по интернету\' в разработке..')
        # пропускаем цикл.
       else:
           continue
