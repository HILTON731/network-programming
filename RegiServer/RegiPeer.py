import socket
import threading
import time

def peer_server():
    
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        host = socket.gethostname()
        port = 

def peer_client(port, host):

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("something")
        
        while True:
            msg = input()
            s.send(msg.encode())
            if msg == 'logoff':
                print("Terminate program")
                break
            rmsg=s.recv(1024).decode()
            print("<")

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
        regi = threading.Thread(target=rcvMsg, args=(sock,))
        regi.daemon = True
        regi.start()

        while True:
            msg = input()
            if msg == '/quit':
                sock.send(msg.encode())
                break
            sock.send(msg.encode())

runChat()