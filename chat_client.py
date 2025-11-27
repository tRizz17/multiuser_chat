import sys, socket
from chatui import init_windows, read_command, print_message, end_windows



def usage():
    print("usage: chat_client.py host port", file=sys.stderr)

def main(argv):
    init_windows()

    host = argv[1]
    port = int(argv[2])


    s = socket.socket()
    s.connect((host, port))
    cmd = read_command()


if __name__ == "__main__":
    sys.exit(main(sys.argv))