import socket
import argparse
import time

def run_server(port=65432):
    i=1
    print("Waiting for connect: ")
    
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        host =''
        s.bind((host,port))
        s.listen(1)
        conn, addr = s.accept()
        
        with conn:
            while True:
                msg = conn.recv(1024).decode()
                if msg=="exit":
                    print("\n\nTerminate program!\n")
                    break
                print("<receive message %d>: "%i,msg)
                rMsg = reverseStr(msg)
                print("<send message %d>: "%i,rMsg)
                conn.sendall(rMsg.encode())
                i+=1
            
def reverseStr(msg):
    size = len(msg)
    reverse=''
    for i in range(size-1, -1, -1):
        reverse+=msg[i]
    return reverse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="echo server.py -p port")
    parser.add_argument('-p',help="port_number",required=True)
    args=parser.parse_args()

    run_server(port=int(args.p))