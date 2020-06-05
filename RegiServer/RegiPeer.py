import socket
from threading import Thread
import sys
import time
import threading
import sys

HOST = 'localhost'
PORT = 9009

def rcvMsg(sock):
    
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            pass

def runChat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        t = Thread(target=rcvMsg, args=(sock,))
        t.daemon = True
        t.start()

        while True:
            msg = input()
            if msg == 'logoff':
                sock.send(msg.encode())
                break
            sock.send(msg.encode())

runChat()




class Server(threading.Thread):
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Server started successfully")
        hostname=socket.gethostbyname(socket.getfqdn())
        port=int(input('port:'))
        self.sock.bind((hostname,port))
        self.sock.listen(1)
        print("Listening on port %d"%port)
        (clientname,address)=self.sock.accept()
        print("Connection from %s"%str(address))
        while True:
            chunk = clientname.recv(1024)
            print(str(address),":",chunk)

class Client(threading.Thread):
    def connect(self,host,port):
        self.sock.connect((host, port))
    def client(self, host, port, msg):
        sent=self.sock.send(msg)
        print("Sent")
    def run(self):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            host=input("Enter the hostname >>")
            port=int(input("Enter the port >>"))
        except EOFError:
            print("Error")
            return 1

        print("Connecting")
        s=''
        self.connect(host,port)
        print("Connected")
        while 1:
            print("Waiting for message")
            msg = input('>>')
            if msg == 'exit':
                break
            if msg == '':
                continue
            print("Sending")
            self.client(host,port,msg)
        return -1
if __name__=='__main__':
    runChat()
    srv=Server()
    srv.daemon=True
    print("Starting server")
    srv.start()
    time.sleep(1)
    print("Starting client")
    cli=Client()
    print("Started successfully")
    cli.start()