import sys, socket, select, json
from packets import *

# create dictionary to map ip addresses to nicknames


def run_server(port):
    buffers = {} # map sockets to buffers
    names = {}
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
                    data = json.loads(data)
                    if data['type'] == 'hello': ## probably can extract this into function, use switch 
                        names[read_socket] = data['nick']
                        for client_socket in read_set:
                            if client_socket != listener:
                                connect_msg = (f"*** {names[read_socket]} has joined the chat").encode()
                                print(read_set)
                                client_socket.sendall(connect_msg)

                    elif data['type'] == 'chat':
                        for client_socket in read_set:
                            if client_socket != listener:
                                pass







# Sent to all when user joins
# {
#     "type": "join"
#     "nick": "[joiner's nickname]"
# }

# Sent to all when user leaves
# {
#     "type": "leave"
#     "nick": "[leaver's nickname]"
# }

# Sent to all when user sends msg
# {
#     "type": "chat"
#     "nick": "[sender nickname]"
#     "message": "[message]"
# }


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
