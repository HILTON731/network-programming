import socketserver
import socket
import threading
import time
import sys
import os

lock = threading.Lock()
now = time.strftime('[%y/%m/%d %H:%M:%S]',time.localtime(time.time()))

class PeerManager:
    def __init__(self):
        self.peers = {}

    def addPeer(self, peername, conn, addr):
        global tick
        if peername in self.peers:
            conn.send("Already connected..\n".encode())
            return None

        lock.acquire()
        self.peers[peername] = (conn, addr)
        lock.release()
        print(now,'{} request connect'.format(peername))
        return peername
    
    def removePeer(self, peername):
        if peername not in self.peers:
            return
        
        lock.acquire()
        del self.peers[peername]
        lock.release()

        print(now,peername,'Lost connection')


    def disconnect(self, peername, msg):
        self.removePeer(msg)

    def messageHandler(self, peername, msg):
        command = msg.split()
        if command[0] == 'disconnect':
            if command[1] == peerID:
                self.disconnect(peername, command[1])
                self.sendMessage('disconnecting',peername)
                return -1
            else: 
                self.sendMessage('Wrong argument',peername)
                return 1
        elif command[0] == 'talk' and command[1] == peerID:
            self.printMessage(peername,msg)
        if command == 'logoff':
            self.removePeer(peername)
            self.sendMessage('disconnecting',peername)
            return -1
    
    def sendMessage(self, msg, peername):
        conn, _ = self.peers.get(peername)
        conn.send(msg.encode())

    def printMessage(self, peername, msg):
        msg = msg.lstrip('talk {} '.format(peerID))
        print('{} Message from {}: {}'.format(now,peername,msg))
        # print(now,peername,':',msg)

class MyTCPHanler(socketserver.BaseRequestHandler):
    peerman = PeerManager()

    def handle(self):
        try:
            peername = self.registerPeername()            
            while True:
                msg = self.request.recv(1024)
                if self.peerman.messageHandler(peername, msg.decode()) == -1:
                    self.request.close()
                    break

        except Exception as e:
            print(e)

        self.peerman.removePeer(peername)

    def registerPeername(self):
        while True:
            peername = self.request.recv(1024).decode().strip()
            if self.peerman.addPeer(peername, self.request, self.client_address):
                return peername
                
class PeerServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer(PHOST, PPORT):
    try:
        server = PeerServer((PHOST, PPORT),MyTCPHanler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()

def access_peer(ip, port, sock):
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer.connect((ip, port))
        print(now,'Connect successfully')
        peer.send(peerID.encode())
        j = threading.Thread(target=rcvMsg, args=(peer,), daemon=True)
        j.start()
        while True:
            global data
            data = ''
            # msg = input(now+" {}: ".format(peerID))
            msg = input()
            if msg == '':
                continue
            elif msg == 'logoff':
                peer.send(msg.encode())
                sock.send(msg.encode())
                j.join()
                time.sleep(0.1)
                sys.exit()
            elif len(msg.split()) == 3 and msg.split()[0] == 'connect':
                print("Already in connection")
                data = 'null'
            elif len(msg.split()) == 2 and msg.split()[0] == 'disconnect':
                peer.send(msg.encode())
                time.sleep(0.3)
                if data.decode() == 'Wrong argument':
                    continue
                else:
                    j.join()
                    data = 'null'
                    print(now,"Disconnected")
                    break
            elif len(msg.split()) >= 3 and msg.split()[0] == 'talk':
                peer.send(msg.encode())
                data = 'null'
            else:    
                sock.send(msg.encode())
            while data == '':
                continue
    except KeyboardInterrupt:
        peer.send('logoff'.encode())
        sock.send('logoff'.encode())
        os._exit(-1)

    except socket.error:
        print("Wrong address")
    
    finally:
        peer.close()
        
def rcvMsg(sock):
    global data
    mainlock = threading.Lock()
    while True:
        try:
            mainlock.acquire()
            data = sock.recv(1024)
            if not data:
                break
            mainlock.release()
            print(data.decode())
            
        except:
            pass
    

HOST = 'localhost'
PORT = 9009
data = ''
tick = 0
peerID = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    
    sock.connect((HOST,PORT))
    PHOST, PPORT = sock.getsockname()

    t=threading.Thread(target=rcvMsg, args=(sock,), daemon=True)
    s=threading.Thread(target=runServer, args=(PHOST, PPORT,), daemon=True)

    t.start()
    s.start()
    while True:
        try:
            peerID = input(now+' loginID: ')
            if peerID == '':
                continue
            sock.send(peerID.encode())
            if peerID == 'logoff':
                t.join()
                s.join()
                time.sleep(0.1)
                sys.exit()
            time.sleep(0.1)
            if data.decode() == 'okay':
                break
        except KeyboardInterrupt:
            sock.send('logoff'.encode())
            os._exit(-1)

                    
    while True:
        data = ''
        try:
            # msg = input(now+" {}: ".format(peerID))
            msg = input()
            if msg == 'logoff':
                sock.send(msg.encode())
                time.sleep(0.1)
                sys.exit()
            elif len(msg.split()) == 3 and msg.split()[0] == 'connect' and msg.split()[2]:
                t = threading.Thread(target=access_peer, args=(msg.split()[1], int(msg.split()[2]), sock,))
                t.start()
                t.join()
                data = 'null'
            elif len(msg.split()) >= 2 and msg.split() == 'talk' or msg.split() == 'disconnect':
                print("Should connect peer first")
                data = 'null'
            elif msg == '':
                continue
            else:
                sock.send(msg.encode())
            while data == '':
                continue
        except KeyboardInterrupt:
            sock.send('logoff'.encode())
            os._exit(-1)
        