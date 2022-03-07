import socket
import sys #for running system commands that is the cmds we run on cmd etc.

#Create socket(allow two computers to connect)
def sock_create():
    try:
        global host
        global port
        global s
        host = ""#this usually contains the IP address but we leave it blank as we are listening to our own machine
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error:" + str(msg))

#bind socket to port and wait for connection from client
def sock_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port :" + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket Binding error : "+str(msg)+"\n"+"Retrying....")
        sock_bind()

#Establishing connection
def sock_accept():
    conn,address=s.accept()
    print("Connection has been established : | "+"IP "+str(address[0])+" | PORT "+str(address[1]))
    send_cmds(conn)
    conn.close()

#Send commands
def send_cmds(conn):
    while True:
        cmd=input()
        if cmd=="quit":
            conn.close()
            s.close()
            sys.exit()
        if(len(str.encode(cmd))>0):
            conn.send(str.encode(cmd))
            client_response=str(conn.recv(1024),'utf-8')
            print(client_response,end=" ")

def main():
    sock_create()
    sock_bind()
    sock_accept()

main()


