import socket

HOST = ''
PORT = 65432

# Create a socket object, connects to the server and calls s.sendall() to send its message.
# Lastly, it calls s.recv() to read the server`s reply and then prints it.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)

print('Received', repr(data))