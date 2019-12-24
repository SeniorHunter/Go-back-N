# ---------------------------------------- #
# ------------ Packet Manager ------------ #
# ---------------------------------------- #

import socket
from UN import UN


class Packet:
    connection: socket
    is_EOC: bool
    un: UN

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
