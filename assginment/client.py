import socket
import argparse

def run(port, host):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.connect((host,port))
        
        while True:
            msg=input()
            if msg=="exit":
                break
            s.sendall(msg.encode())
            rMsg=s.recv(1024).decode()
            print(rMsg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="echo client.py -p port -i host")
    parser.add_argument('-p',help="port_number",required=True)
    parser.add_argument('-i',help="host_name", required=True)

    args = parser.parse_args()
    run(port=int(args.p), host=args.i)
