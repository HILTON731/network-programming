import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost).
PORT = 65432        # Port to listen on (non-privileged ports are > 1023).

#loopback interface: virtual network interface that your computer uses to communicate with itself.

# Creates a socket object that supports the context manager type --> no need to call s.close().
# AF_INET: Internet address family for IPv4.
# SOCK_STREAM: Socket type for TCP, the protocol that willl be used to transport our messages in the network.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.bind((HOST,PORT)) # Associate the socket with a specific network interface and port.
    s.listen()  # Enables a server to accept() connections.
    conn, addr = s.accept() # Blocks and waits for an incoming connection.
                            # conn: new socket object representing the connection.
                            # addr: tuple holding the address of the client.
    with conn: # The with statement is used with conn to automatically close the socket at the end of the block.
        print('Connected by', addr)
        while True:
            data = conn.recv(1024) # Reads whatever data the client sends.
            if not data: # conn.recv() returns an empty bytes object, b''.
                break
            conn.sendall(data) # Echoes it back.