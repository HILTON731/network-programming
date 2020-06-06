import socketserver
import socket
import threading
import time

lock = threading.Lock()
now = time.strftime('[%y/%m/%d %H:%M:%S]',time.localtime(time.time()))

class PeerManager:
    def __init__(self):
        self.peers = {}

    def addPeer(self, peername, conn, addr):
        if peername in self.peers:
            conn.send("Already connected..\n".encode())
            return None

        lock.acquire()
        self.peers[peername] = (conn, addr)
        lock.release()
        print(now,'Connect successfully')
        return peername
    
    def removePeer(self, peername):
        if peername not in self.peers:
            return
        
        lock.acquire()
        del self.peers[peername]
        lock.release()

        print(now,' ',peername,'disconnected')

    def messageHandler(self, peername, msg):
        command = msg.split()
        if command[0] == 'disconnect' and command[1] == peerID:
            self.removePeer(peername)
            return -1
        if command[0] == 'talk' and command[1] == peerID:
            self.printMessage(peername,command)
        if command == 'logoff':
            self.removePeer(peername)
    
    def printMessage(self, peername, command):
        msg = ' '.join(command[2:])
        print(peername,': ',msg)

class MyTCPHanler(socketserver.BaseRequestHandler):
    peerman = PeerManager()

    def handle(self):
        try:
            peername = self.registerPeername()
            msg = self.request.recv(1024)
            while msg:
                if self.peerman.messageHandler(peername, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)
        self.peerman.removePeer(peername)

    def registerPeername(self):
        while True:
            peername = self.request.recv(1024).decode()
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


def rcvMsg(sock):
    
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            pass

def access_peer(ip, port, sock):
    peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        peer.connect((ip, port))
        print(now,'Connect successfully')
        peer.send(peerID.encode())
        while True:
            input(now+" {}: ".format(peerID))
            if msg == 'logoff':
                peer.send(msg.encode())
                time.sleep(1)
                sock.send(msg.encode())
                return
            if len(msg.split()) == 3 and msg.split()[0] == 'connect':
                print("Already in connection")
            if len(msg.split()) == 2 and msg.split()[0] == 'disconnect':
                peer.send(msg.encode())
                break
            if len(msg.split()) >= 3 and msg.split()[0] == 'talk':
                peer.send(msg.encode())
            else:    
                sock.send(msg.encode())
    except socket.error:
        print("Wrong address")
    finally:
        peer.close()
        

HOST = 'localhost'
PORT = 9009

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    
    sock.connect((HOST,PORT))
    PHOST, PPORT = sock.getsockname()

    
    threading.Thread(target=runServer, args=(PHOST, PPORT,), daemon=True).start()

    while True:
        peerID = input(now+' loginID: ')
        sock.send(peerID.encode())
        time.sleep(1)
        if sock.recv(1024).decode() == 'okay':
            break

    threading.Thread(target=rcvMsg, args=(sock,), daemon=True).start()
    
    while True:
        msg = input(now+" {}: ".format(peerID))
        if msg == 'logoff':
            sock.send(msg.encode())
            break
        if len(msg.split()) == 3 and msg.split()[0] == 'connect':
            t = threading.Thread(target=access_peer, args=(msg.split()[1], int(msg.split()[2]), sock,))
            t.start()
            t.join()
            print(now,"Disconnect successfully")
        if len(msg.split()) <= 3 and msg.split()[0] == 'talk' or msg.split()[0] == 'disconnect':
            print("Should connect peer first")
        else:
            sock.send(msg.encode())
        
