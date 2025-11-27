import sys, socket, threading, json
from chatui import init_windows, read_command, print_message, end_windows


def usage():
    print("usage: chat_client.py name host port", file=sys.stderr)

def connect_and_msg(name, host, port):
    s = socket.socket()
    s.connect((host, port))
    cmd = read_command(f"{name}> ")

# def receive_msgs()


def main(argv):
    init_windows()

    nickname = argv[1]
    host = argv[2]
    port = int(argv[3])

    connect_and_msg_thread = threading.Thread(target=connect_and_msg, args=(nickname, host, port))
    # receive_thread = threading.Thread(target= , arg= )
    connect_and_msg_thread.start()





if __name__ == "__main__":
    sys.exit(main(sys.argv))