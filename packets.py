WORD_LEN_SIZE = 2
DATA_TO_RECV = 1


def packet_complete():
    if len(packet_buffer) > WORD_LEN_SIZE:
        packet_length_int = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], "big")
        if len(packet_buffer) >= packet_length_int + WORD_LEN_SIZE:
            return True
    return False


def get_next_word_packet(s):
    """
    Return the next word packet from the stream.

    The word packet consists of the encoded word length followed by the
    UTF-8-encoded word.

    Returns None if there are no more words, i.e. the server has hung
    up.
    """
    while True:
        if packet_complete():
            word_len_int = int.from_bytes(packet_buffer[:WORD_LEN_SIZE], "big")
            packet = packet_buffer[:word_len_int + WORD_LEN_SIZE]
            packet_buffer = packet_buffer[word_len_int + WORD_LEN_SIZE:]
            return packet

        data = s.recv(DATA_TO_RECV)

        if len(data) == 0:
            return None

        packet_buffer += data


def extract_word(word_packet):
    """
    Extract a word from a word packet.

    word_packet: a word packet consisting of the encoded word length
    followed by the UTF-8 word.

    Returns the word decoded as a string.
    """
    return word_packet[WORD_LEN_SIZE:].decode('utf-8')