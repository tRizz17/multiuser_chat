import sys, socket, select, json
from packets import *


def run_server(port):
    buffers = {} # map sockets to buffers
    names = {}
    read_set = set()
    listener = socket.socket()
    listener.bind(("localhost", port))
    listener.listen()
    print(f"Server listening on port {port}..")
    read_set.add(listener)

    while True:
        ready, _, _ = select.select(read_set, {}, {})

        for read_socket in ready:
            if read_socket == listener:
                client_socket, client_addr = listener.accept()
                read_set.add(client_socket)
                buffers[client_socket] = b''
            else:
                    encoded_data = get_next_word_packet(read_socket, buffers[read_socket])
                    data = extract_msg(encoded_data)
                    if data == b'':
                        read_socket.close()
                        read_set.remove(read_socket)
                        for client_socket in read_set:
                            if client_socket != listener:
                                connect_msg = (f"*** {names[read_socket]} has left the chat").encode()
                                client_socket.sendall(connect_msg)
                        
                    else:
                        data = json.loads(data)
                        match data['type']:
                            case 'hello':
                                names[read_socket] = data['nick']
                                for client_socket in read_set:
                                    if client_socket != listener:
                                        connect_msg = server_json_packet('join', name=data['nick'])
                                        client_socket.sendall(connect_msg)

                            case 'chat':
                                for client_socket in read_set:
                                    if client_socket != listener:
                                        msg = server_json_packet('chat', data['chat'], names[read_socket])
                                        client_socket.sendall(msg)


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
