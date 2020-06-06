import socketserver
import threading

HOST = ''
PORT = 9009
lock = threading.Lock()

class UserManager:

    def __init__(self):
        self.users = {}

    def addUser(self, username, conn, addr):
        if username in self.users:
            conn.send("Already registered..\n".encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()
        conn.send(addr.encode())
        print('--- joined users [%s] ---' %len(self.users))

        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        print('--- joined users [%s] ---' %len(self.users))
    
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
            conn, addr = value
            self.sendMessage(str(key)+'='+str(addr),username)

    def messageHandler(self, username, msg):
        # if msg[0] != '/':
        #     self.sendMessageToAll('[%s] %s'%(username, msg))
        #     return
        command = msg.strip()
        if command == 'logoff':
            self.removeUser(username)
            return -1
        elif command == 'online_users':
            self.online_users(username)
        else:
            self.help(username)

    def sendMessage(self, msg, username):
        conn, addr = self.users.get(username)
        conn.send(msg.encode())

class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        print('+++ [%s] connected +++'%self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)
        
        print('--- [%s] exit ---'%self.client_address[0])
        self.userman.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send('loginID:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.addUser(username, self.request, self.client_address):
                return username

class RegiServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print('--- Regiserver start ---')
    print('press ctrl-c if you wanna stop')

    try:
        server = RegiServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('--- Close server ---')
        server.shutdown()
        server.server_close()

runServer()