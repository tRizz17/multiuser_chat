import json

MSG_LEN_SIZE = 2
DATA_TO_RECV = 1


def packet_complete(packet_buffer):
    if len(packet_buffer) > MSG_LEN_SIZE:
        packet_length_int = int.from_bytes(packet_buffer[:MSG_LEN_SIZE], "big")
        if len(packet_buffer) >= packet_length_int + MSG_LEN_SIZE:
            return True
    return False


def get_next_word_packet(s, packet_buffer):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    while True:
        if packet_complete(packet_buffer):
            word_len_int = int.from_bytes(packet_buffer[:MSG_LEN_SIZE], "big")
            packet = packet_buffer[:word_len_int + MSG_LEN_SIZE]
            packet_buffer = packet_buffer[word_len_int + MSG_LEN_SIZE:]
            return packet

        data = s.recv(DATA_TO_RECV)

        if len(data) == 0:
            return None

        packet_buffer += data


def extract_msg(packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    return packet[MSG_LEN_SIZE:].decode('utf-8')



def client_json_packet(type, message=None, name=None):

    match type:
        case 'hello':
            init_msg = json.dumps({"type": "hello", "nick": f"{name}"}).encode('utf-8')
            msg_len = len(init_msg)
            msg_len_bytes = msg_len.to_bytes(MSG_LEN_SIZE, "big")
            init_packet = msg_len_bytes + init_msg
            return init_packet

        case 'chat':
            msg_json = json.dumps({"type": "chat", "chat": f"{message}"}).encode('utf-8')
            msg_json_len = len(msg_json)
            msg_json_len_bytes = msg_json_len.to_bytes(MSG_LEN_SIZE, "big")
            packet = msg_json_len_bytes + msg_json
            return packet



def server_json_packet(type, message=None, name=None):
    
    match type:

        case 'chat':
            msg_json = json.dumps({"type": "chat", "nick": f"{name}", "chat": f"{message}"}).encode('utf-8')
            msg_json_len = len(msg_json)
            msg_json_len_bytes = msg_json_len.to_bytes(MSG_LEN_SIZE, "big")
            packet = msg_json_len_bytes + msg_json
            return packet

        case 'join':
            msg_json = json.dumps({"type": "join", "nick": f"{name}"}).encode('utf-8')
            msg_json_len = len(msg_json)
            msg_json_len_bytes = msg_json_len.to_bytes(MSG_LEN_SIZE, "big")
            packet = msg_json_len_bytes + msg_json
            return packet

        case 'leave':
            pass


