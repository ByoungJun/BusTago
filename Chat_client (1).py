# Sokcet Moudle Import

from socket import *
from select import select
import sys

# Setting Up Host, Port, Buffer size
HOST = '52.68.197.141'
PORT = 10022
ADDR = (HOST,PORT)
BUF_SIZE = 1024
# new Socket Module
clientSocket = socket(AF_INET, SOCK_STREAM)

# Connection with Server
try:
    clientSocket.connect(ADDR)
except Exception as e:
    print("Can't connect Server(%s:%s)" % ADDR)
    sys.exit()
print("Connect Complet! (%s:%s)" % ADDR)

def prompt():
    sys.stdout.flush()

# Loop for Chatting
while True:
    try:
        connection_list = [sys.stdin, clientSocket]

        read_socket, write_socket,error_socket = select(connection_list,[],[],10)

        for sock in read_socket:
            if sock == clientSocket:
                data = sock.recv(BUF_SIZE)
                if not data:
                    print("disconnecting...(%s:%s)" % ADDR)
                    clientSocket.close()
                    sys.exit()
                else:
                    print("%s" % data) 
                    prompt()
            else:
                message = sys.stdin.readline()
                clientSocket.send(message)
                prompt()
    except KeyboardInterrupt:
        clientSocket.close()
        sys.exit()
