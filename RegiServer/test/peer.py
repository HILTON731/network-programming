import socket
from threading import Thread
import sys
import time
import threading
import sys
lock = threading.Lock()

class Server(threading.Thread):
    def run(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("Server started successfully")
        lock.acquire()
        hostname=input('host:')
        port=int(input('port:'))
        lock.release()
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
            lock.acquire()
            host=input("Enter the hostname >>")
            port=int(input("Enter the port >>"))
            lock.release()
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
    srv=Server()
    srv.daemon=True
    print("Starting server")
    srv.start()
    time.sleep(1)
    print("Starting client")
    cli=Client()
    print("Started successfully")
    cli.start()