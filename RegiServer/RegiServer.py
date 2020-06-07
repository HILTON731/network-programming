import socketserver
import threading
import time

HOST = ''
PORT = 9009
lock = threading.Lock()
now = time.strftime('[%y/%m/%d %H:%M:%S]',time.localtime(time.time()))

class UserManager:

    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            print(now,' Attempt to register')
            conn.send("Already registered..".encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()
        conn.send(str(addr).encode())
        print(now,' {} users joined' .format(len(self.users)))

        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        print(now,' {} users joined' .format(len(self.users)))
    
    def help(self, username):
        text = """
        - help : lookup commands
        - online_users: send a request to the regiServer, get back a list of all online peers and display them on the screen
        - connect [ip] [port] : request to chat with peer with the given IP and port
        - disconnect [peer] : end your chat session with the listed peer
        - talk [peer] [message] : send a message to the peer that you\'ve already initiated a chat with via the connect command
        - logoff : send a message (notification) to regiServer for logging off the chat system
        """
        self.sendMessage(text,username)
        

    def online_users(self, username):
        for key, value in self.users.items():
            _, addr = value
            self.sendMessage(str(key)+'='+str(addr),username)

    def messageHandler(self, username, msg):
        command = msg.strip()
        if command == 'logoff':
            self.removeUser(username)
            return -1
        elif command == 'online_users':
            self.online_users(username)
            return
        elif command == 'help':
            self.help(username)
            return
        else:
            self.sendMessage('Command not available',username)
            return

    def sendMessage(self, msg, username):
        conn, _ = self.users.get(username)
        conn.send(msg.encode())

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        print(now,' {} connect'.format(self.client_address))

        try:
            username = self.registerUsername()
            if username == -1:
                self.request.close()
                print(now,' {} exit'.format(self.client_address))
                return
            msg = self.request.recv(1024)
            while msg:
                print(now,' {} request command \'{}\''.format(self.client_address,msg.decode()))
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)
        
        print(now,' {} exit'.format(self.client_address))
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            username = self.request.recv(1024)
            username = username.decode().strip()
            if username == 'logoff':
                return -1
            if self.userman.addUser(username, self.request, self.client_address):
                self.request.send('okay'.encode())
                return username

class RegiServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print(now,' Regiserver start')
    print('press ctrl-c if you wanna stop')

    try:
        server = RegiServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print(now,' Close server')
        server.shutdown()
        server.server_close()

runServer()