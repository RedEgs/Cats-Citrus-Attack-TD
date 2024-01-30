import socket
import select
import threading

class Server():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip_address, port))
        self.socket.listen(20)

    def run(self):
        self.client, address = self.socket.accept()
        self.client.send("CONNECTED TO CLIENT".encode())

    def close(self):
        self.client.close()


class Client():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip_address, port)) 
        print(self.socket.recv(1024).decode())

        
    