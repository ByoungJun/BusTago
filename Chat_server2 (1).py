# Socket, Select module import
from socket import *
from select import *
import sys
from time import ctime

# Setting Up  Host, Buffer, Port
HOST =""
PORT = 10022
BUF_SIZE = 1024
ADDR = (HOST, PORT)

# Make Socket instantation
serverSocket = socket(AF_INET, SOCK_STREAM)

# Server information binding
serverSocket.bind(ADDR)

# Listening for req
serverSocket.listen(10)
connection_list = [serverSocket]
print("=======================================")
print("Starting Server. (Port Num:%s)" % str(PORT))
print("=======================================")

# Loop for Communication
while connection_list:
    try:
        print("[INFO] Listening for Req")

        # release blocking per 10sec, receive by using Select Module
        read_socket, write_socket, error_socket = select(connection_list,[],[],10)

        for sock in read_socket:
            #new Connection
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                connection_list.append(clientSocket)
                print("[INFO][%s] new Connection with Client(%s)." % (ctime(), addr_info[0]))

                # reply to Client
                for socket_in_list in connection_list:
                    if socket_in_list != serverSocket and socket_in_list != sock:
                        try:
                            print()
                            # socket_in_list.send("[%s] welcome new Client.\n" % ctime())
                        except Exception as e:
                            socket_in_list.close()
                            connection_list.remove(socket_in_list)
        # from Client received new Data
            else:
                try:
                    data = sock.recv(BUF_SIZE)
                except Exception as e:
                    print("Error Occured!" + e.message)
                    data = ""
                if data:

                    print("[INFO][%s] Received data from Client" % ctime())
                    for socket_in_list in connection_list:
                        if socket_in_list != serverSocket and socket_in_list != sock:
                            try:
                                #                                socket_in_list.send("[%s] %s" % (ctime(), data))
                                socket_in_list.send("%s" % data);

                            except Exception as e:
                                print(e.message)
                                socket_in_list.close()
                                connection_list.remove(socket_in_list)
                                continue

                else:
                    connection_list.remove(sock)
                    sock.close()
                    print("[INFO][%s] disconnection User." % ctime())

    except KeyboardInterrupt:
        serverSocket.close()
        sys.exit()

