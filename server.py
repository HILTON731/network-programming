import socket
import argparse

def run_server(port=65432):
    host = ''

    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)

        conn, addr = s.accept()
        with conn:
            msg = conn.recv(1024)

            rMsg = reversMsg(msg.decode())
            print(rMsg)

            conn.sendall(rMsg.encode())
def reversMsg(str):
    size = len(str)
    reverseStr = ''
    for i in range(size-1, -1, -1):
        reverseStr+=str[i]

    return reverseStr

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Echo server -p port")
    parser.add_argument('-p', help="port number", required=True)

    args = parser.parse_args()
    run_server(port=int(args.p))