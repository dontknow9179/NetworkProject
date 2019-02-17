import socket
import threading

host = '127.0.0.1'
port = 65432

login = '0'
logout = '1'
broadcast = '2'
secret = '3'
failsend = '6'
repeated = '7'
overflow = '8'
disconnect = '9'


class Server:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.__socket.bind((host,port))
        self.__socket.listen(7)
        self.__clients = dict() #键为用户名
        print('Socket now listening.')

    def loginmessage(self,message):
        for client,conn in self.__clients.items():
            conn.send((login + message).encode('utf-8'))

    def logoutmessage(self,message):
        for client,conn in self.__clients.items():
            conn.send((logout + message).encode('utf-8'))

    def broadcast(self,message,source):
        #source = message[1:9]
        for client,conn in self.__clients.items():
            if client != source:
                conn.send((broadcast + message[1:]).encode('utf-8'))

    def secret(self,message,source):
        start = message.index('@') + 1
        end = message.index(' ')
        target = message[start:end]
        print(target)
        if target in self.__clients.keys():
            conn = self.__clients[target]

            conn.send(message.encode())
        else:
            conn = self.__clients[source]
            conn.send((failsend + "No User Found\n").encode())

    def receive(self,client):
        conn = self.__clients[client]
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if data.startswith(broadcast):
                    self.broadcast(data,client)
                elif data.startswith(secret):
                    print(data)
                    self.secret(data,client)
                elif data.startswith(logout):
                    del self.__clients[client]
                    conn.close()
                    #print(client + ' has left.')
                    self.logoutmessage(client)
                    break
            except ConnectionResetError:
                del self.__clients[client]
                conn.close()
                self.logoutmessage(client)
                print(client + ' has left somehow.')
                break

    def start(self):
        while True:
            try:
                conn,addr = self.__socket.accept()
                if len(self.__clients)< 7:
                    print('New connection created.',conn.fileno())
                    data = conn.recv(1024).decode('utf-8')
                    if data.startswith(login):
                        client = data[1:]
                        if client in self.__clients.keys():
                            conn.send(repeated.encode('utf-8'))
                            conn.close()
                        else:
                            self.__clients[client] = conn
                            self.loginmessage(client)
                            print(client)
                            thread = threading.Thread(target=self.receive,args=(client,))
                            thread.start()
                else:
                    conn.send(overflow.encode('utf-8'))
                    conn.close()
            except ConnectionError:
                for conn in self.__clients.values():
                    conn.send(disconnect.encode('utf-8'))
                    conn.close()
                self.__clients = {}
                print('Connection Error! Drop the chatroom.')

server = Server()
server.start()

