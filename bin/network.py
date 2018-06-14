''' Модуль, отвечающий за работу сетевого режима игры '''
from socket import *
from pickle import dumps, loads


class LanServer:
    ''' Создать сетевую игру '''
    def __init__(self):
        # данные от сервера
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.host = ''              # хост
        self.port = 50007           # порт
        self.connection = None      # дескрипток сокета
        self.address = None         # ip клиента
        self.data = None            # данные запроса клиента

        # первичные данные от клиента
        self.client_name = None

    # создание сервера
    def create_server(self):
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
        except OSError as errno:
            print('ошибка = ',errno)
            return 1
    # ждем запрос от клиента
    def accept_request(self):
        self.connection, self.address = self.sock.accept()

    # получаем данные запроса
    def get_request_data(self):
        #self.accept_request()
        self.data = self.connection.recv(1024)
        self.check_data()
        self.data = loads(self.data)
        return self.data

    # есть ли данные?
    def check_data(self):
        if not self.data:
            print('данных нет. выход из игры')
            exit(1)
        else:
            return 0

    # ответ на запрос
    def send_data(self,data):
        data =  dumps(data)
        self.connection.send(data)

    # закрыть соединение с клиентом
    def socket_close(self):
        self.connection.close()



class LanClient(LanServer):
    ''' Найти сетевую игру '''
    #присоединится к серверу
    def connected(self):
        self.sock.connect((self.host,self.port))

    # отправить сообщение (переопределена от родителя)
    def send_data(self,data):
        self.data = data
        self.sock.send(dumps(self.data))

    def socket_close(self):
        self.sock.close()

    # получить ответ
    def get_answer(self):
        answer = self.sock.recv(1024)
        return loads(answer)


class Net:
    ''' игра через Интернет '''
    pass