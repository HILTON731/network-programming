import socket

HOST = '127.0.0.1'
PORT = 65432

# Create a socket object, connects to the server and calls s.sendall() to send its message.
# Lastly, it calls s.recv() to read the server`s reply and then prints it.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024) # bufsize argument of 1024 used above is the maximum amount of data to be received at once.
                        # send() returns the number of bytes sent, shich may be less than the size of the data passed in.

print('Received', repr(data))