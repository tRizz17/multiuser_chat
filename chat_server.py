import sys
import socket
import select
import json

# create dictionary to map ip addresses to nicknames


def run_server(port):
    buffers = {} # map sockets to buffers
    read_set = set()
    listener = socket.socket()
    listener.bind(("localhost", port))
    listener.listen()
    read_set.add(listener)
    while True:
        ready, _, _ = select.select(read_set, {}, {})

        for read_socket in ready:
            if read_socket == listener:
                client_socket, client_addr = listener.accept()
                read_set.add(client_socket)
                buffers[client_socket] = b''
                print(f"{client_addr}: connected")
            else:
                data = read_socket.recv(1024)
                if len(data) == 0:
                    read_socket.close()
                    read_set.remove(read_socket)
                    print(f"{client_addr}: disconnected")
                else:
                    print(f"{client_addr} {len(data)}: {data}")





#--------------------------------#
# Do not modify below this line! #
#--------------------------------#

def usage():
    print("usage: chat_server.py port", file=sys.stderr)

def main(argv):
    try:
        port = int(argv[1])
    except:
        usage()
        return 1

    run_server(port)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
