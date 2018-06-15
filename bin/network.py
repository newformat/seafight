''' Модуль, отвечающий за работу сетевого режима игры '''
from socket import *
from pickle import dumps, loads
from subprocess import check_output

class LanServer:
    ''' Создать сетевую игру
    attribute: помечены ниже
    methods:
        create_server       создание сервера
        accept_request      ждем запрос от клиента
        get_request_data    получаем данные запроса
        check_data          есть ли данные от запроса
        send_data           ответ на запрос
        socket_close        закрыть соединение с клиентом
        print_errors        вывод ошибки исключений на экран
        get_ip              получить ip адресс локальной машины(для сервера)(не срботает на Windows)
    '''
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = ''              # хост
        self.port = 50007           # порт
        self.connection = None      # дескрипток сокета
        self.address = None         # ip клиента
        self.data = None            # данные запроса клиента
        self.client_name = None     # первичные данные от клиента


    def create_server(self):
        self.get_ip()
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
        except OSError as errno:
            self.print_errors(errno,'Порт [{0}] занят'.format(str(self.port)))
            return 1


    def accept_request(self):
        self.sock.settimeout(120)
        print('Ваш IP:',self.host)
        print('Ожидание сервера 120 сек.')
        try:
            self.connection, self.address = self.sock.accept()
            self.sock.settimeout(None)
        except:
            print('Время истекло... выход в главное меню')
            return 1


    def get_request_data(self):
        self.data = self.connection.recv(1024)
        if self.check_data():
            return -1
        self.data = loads(self.data)
        return self.data


    def check_data(self):
        if not self.data:
            print('даныых нет, закрываюсь.')
            return 1
        else:
            return 0


    def send_data(self,data):
        data =  dumps(data)
        self.connection.send(data)


    def socket_close(self):
        self.connection.close()


    def print_errors(self, handle, message):
        print('\n{0}, err_code=[{1}]'.format(message,str(handle.errno)))


    def get_ip(self):
        self.host = check_output(['hostname', '-I']).decode().strip()



class LanClient(LanServer):
    ''' Найти сетевую игру
    methods:
        connected   присоединится к серверу
        check_ip    проверка ip адреса на формат
        get_answer  получить ответ
    '''

    def connected(self):
        self.sock.settimeout(10)
        while True:
            self.host = self.check_ip(input('Введите ip адрес сервера =>'))
            if type(self.host) != str:
                continue

            try:
                print('немного ожидания...')
                self.sock.connect((self.host,self.port))
                print('успешно подключились к хосту')
                self.sock.settimeout(None)
                break
            except ConnectionRefusedError as errno:
                self.print_errors(errno,'сервер не найден')
                return 1
            except OSError as err:
                self.print_errors(err,'неверный адрес')
                return 1
        return 0


    def send_data(self,data):
        self.data = data
        try:
            self.sock.send(dumps(self.data))
        except ConnectionResetError as err:
            self.print_errors(err,'сброс соединения')
            # по хорошему бы пробросить везде в коде game.py условия чтоб выходило в главное меню.
            exit(1)

    def socket_close(self):
        self.sock.close()


    def get_answer(self):
        try:
            answer = self.sock.recv(1024)
            return loads(answer)
        except ConnectionResetError as err:
            self.print_errors(err,'сервер отключился')
            return 1
        except EOFError:
            print('сервер отвалился')
            return 1


    def check_ip(self,str_ip):
        try:
            inet_aton(str_ip)
        except OSError:
            print('неверный формат ip адреса')
            return 1
        return str_ip



class Net:
    ''' игра через Интернет '''
    pass