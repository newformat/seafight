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

       # запуск режимов игры
       if item == 1:
           game.game_bot()
       elif item == 2:
           ''' lan режим '''
           # 1 - создать игру / 2 - найти игру
           menu.lan_menu()
           ch = ''
           while True:
               ch = input('=>')
               if ch == '1':
                   game.game_lan_server()
                   break
               elif ch == '2':
                   game.game_lan_client()
                   break
               else:
                   continue
       elif item == 3:
           print('Режим \'Игра по интернету\' в разработке..')
           continue
       else:
           continue
