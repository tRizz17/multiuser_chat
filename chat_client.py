import sys, socket, threading
from chatui import init_windows, read_command, print_message, end_windows

CHAT_THREADS = 2



def usage():
    print("usage: chat_client.py name host port", file=sys.stderr)

def launch_connection(name, host, port):
    s = socket.socket()
    s.connect((host, port))
    cmd = read_command()


def main(argv):
    init_windows()

    nickname = argv[1]
    host = argv[2]
    port = int(argv[3])

    launch_thread = threading.Thread(target=launch_connection, args=(nickname, host, port))
    launch_thread.start()


if __name__ == "__main__":
    sys.exit(main(sys.argv))