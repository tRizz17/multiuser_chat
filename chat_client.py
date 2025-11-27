import sys, socket, threading, json
from chatui import init_windows, read_command, print_message, end_windows
from packets import *


def usage():
    print("usage: chat_client.py name host port", file=sys.stderr)

def connect_and_msg(name, host, port, s):

    init_msg = json.dumps({"type": "hello", "nick": f"{name}"}).encode('utf-8')
    s.send(init_msg)

    cmd = read_command(f"{name}> ")

def receive_msgs(s):

    data = s.recv(1024)
    decoded_data = data.decode()
    print_message(decoded_data)
    # while True:
    #     packet = get_next_word_packet(s)

    #     if packet is None:
    #         break

    #     received_msg = extract_word(word_packet)

    #     print_message(received_msg)

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