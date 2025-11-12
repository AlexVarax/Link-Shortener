from socket import *
from _thread import *
import sqlite3 as sql
import json
import DataLayer.DB_Connect

class Server:
    def __init__(self, ip, port, base_name):
        print(f"server ip: {ip}\nServer port: {port}\n")
        #self.data_name = data_name
        self.ser = socket(AF_INET, SOCK_STREAM)
        self.ser.bind((ip, port))
        self.ser.listen(3)

    def start_server(self):
        while True:
            user, addr = self.ser.accept()
            print(f'CLIENT CONNECT:\n IP:{addr[0]} PORT:{addr[1]} ')
            self.listen(user)

    def sender(self, user, text):
        user.send(text.encode('utf-8'))
        pass

    def listen(self, user):
        self.sender(user, "YOU ARE CONNECTED!")
        is_work = True

        while is_work:
            try:
                data = user.recv(1024)
                self.sender(user, 'getted')
            except Exception as e:
                data = ""
                is_work = False

            if len(data) > 0:
                msg = data.decode('utf-8')
                if msg == 'disonnect':
                    self.sender(user, "YOU DISCONNECT")
                    user.close()
                    is_work = False
                else:
                    DataLayer.DB_Connect.connection
            else:
                print('CLIENT DISCONNECT!')
                is_work = False     

