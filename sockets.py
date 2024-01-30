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
        print("waiting for client")

    def run(self):
        self.client, address = self.socket.accept()
        self.client.send("CONNECTED TO CLIENT".encode())

        self.input = input("Message to send: ")
        self.client.send(self.input.encode())

    def close(self):
        self.client.close()


class Client():
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip_address, port)) 
        #print(self.socket.recv(1024).decode())

    def run(self):
        print(self.socket.recv(1024))
        


choice = input("c or s?: ")


if choice == "s":
    ip_input = input("Input your IP4V: ")
    port_input = input("Input your port: ")
    server = Server(ip_input, int(port_input))
    while True:
        server.run()

if choice == "c":
    ip_input = input("Input server IP4V: ")
    port_input = input("Input your port: ")
    client = Client(ip_input, int(port_input))
    while True:
        client.run()


