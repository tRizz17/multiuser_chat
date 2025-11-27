# Example usage:
#
# python select_server.py 3490

import sys
import socket
import select

# create dictionary to map ip addresses to nicknames


def run_server(port):
    read_set = set()
    s = socket.socket()
    s.bind(("localhost", port))
    s.listen()
    read_set.add(s)
    while True:
        ready, _, _ = select.select(read_set, {}, {})

        for read_socket in ready:
            if read_socket == s:
                client_socket, client_addr = s.accept()
                read_set.add(client_socket)
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
