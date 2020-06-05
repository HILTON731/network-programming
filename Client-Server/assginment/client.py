import socket
import argparse

def run(port, host):
    i=1
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.connect((host,port))
        print("Press Enter if you finished typing message.")
        while True:
            msg=input("<message %d>: "%i)
            s.sendall(msg.encode())
            if msg=="exit":
                print("\n\nTerminate program!\n")
                break
            rMsg=s.recv(1024).decode()
            print("<received mesage %d>: "%i,rMsg)
            i+=1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="echo client.py -p port -i host")
    parser.add_argument('-p',help="port_number",required=True)
    parser.add_argument('-i',help="host_name", required=True)

    args = parser.parse_args()
    run(port=int(args.p), host=args.i)
