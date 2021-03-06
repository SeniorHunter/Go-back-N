import socket
from UN import UN


class Packet:
    """Encodes or decodes the packets

    Attributes:

    is_EOC : bool
        flag to determine the end of connection

    Methods:
    send_packet(sequence_number, is_EOT: bool, data=b'')
        assembles the packet by appending the sequence number , EOC flag and the data and then sends it using
        the un instance
    receive_packet()
        extracts the packet and retrieves the sequence number , EOC flag then the data and returns them


    """
    connection: socket
    un: UN
    is_EOC: bool

    def __init__(self, connection):
        self.connection = connection
        self.un = UN(connection)

    # make a packet with sequence number and data (optional)
    def send_packet(self, sequence_number, is_EOT: bool, data=b''):
        seq_byte = sequence_number.to_bytes(6, byteorder="little", signed=True)
        EOT_byte = is_EOT.to_bytes(1, byteorder="little", signed=False)
        self.un.send(seq_byte + EOT_byte + data)

    # extract a packet
    def receive_packet(self):
        packet = self.un.receive()
        sequence_number = int.from_bytes(packet[:6], byteorder="little", signed=True)
        is_EOT = int.from_bytes(packet[6:7], byteorder="little", signed=False)
        return sequence_number, is_EOT, packet[7:]
