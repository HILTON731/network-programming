# Client-Server program
This program was created with reference to several blogs.<br>
Need two terminal to run this program smoothly.(One for server the other for client)<br>
The document below is based on the Window, Python 3.7.6.

## Run on single computer

### 1. Run server.py in the terminal.

```
server.py -p <port_number><br>
```
option explain
>-p: Port number, required option. Need to put your port number after option.

### 2. Run client.py in another terminal.

```
client.py -p <port_number> -i <host_name>
```
option explain
>-p: Port number, required option. Need to put your port number same as before.<br>
>-i: Host name, required option. Put your server`s ip(IPv4) after option.

### 3. Type message you want to change From the terminal where the client is running and press Enter.
>client
```
<message 1>: This is data communication class!!
```
>result
```
<message 1>: This is data communication class!!
<received message 1>: !!ssalc noitacinummoc atad si sihT
```

### 4. Type "exit" if you want to terminate this program
>client
```
<message 1>: exit
```
>result
```
<message 1>: exit

Terminate program!

```
