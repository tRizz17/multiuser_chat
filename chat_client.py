import sys, socket, threading, json
from chatui import init_windows, read_command, print_message, end_windows
from packets import *

MSG_LEN_SIZE = 2

def usage():
    print("usage: chat_client.py name host port", file=sys.stderr)

def connect_and_msg(name, host, port, s):
    init_packet = client_json_packet('hello', name=name)
    s.sendall(init_packet)

    while True:
        cmd = read_command(f"{name}> ")
        stripped_cmd = cmd.lstrip('>')
        packet = client_json_packet('chat', message=stripped_cmd)
        s.sendall(packet)

def receive_msgs(s):

    while True:
        buffer = b''
        encoded_data = get_next_word_packet(s, buffer)
        data = extract_msg(encoded_data)
        data = json.loads(data)
        match data['type']:
            case 'join':
                join_msg = f"** {data['nick']} has joined the chat"
                print_message(join_msg)

            case 'chat':
                msg = data['chat']
                name_and_msg = f"{data['nick']}: {msg}"
                print_message(name_and_msg)

            case 'leave':
                pass



def main(argv):
    init_windows()

    nickname = argv[1]
    host = argv[2]
    port = int(argv[3])

    s = socket.socket()
    s.connect((host, port))

    connect_and_msg_thread = threading.Thread(target=connect_and_msg, args=(nickname, host, port, s)).start()
    receive_thread = threading.Thread(target=receive_msgs , args=(s,)).start()



if __name__ == "__main__":
    sys.exit(main(sys.argv))