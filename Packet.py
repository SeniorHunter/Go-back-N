# todo flag EOC
# todo move UN here
# todo remove thread
# todo file size
# todo sequence number can reset (% size)


# make a packet with sequence number and data (optional)
def encoder(sequence_number, data=b''):
    byte = sequence_number.to_bytes(6, byteorder="little", signed=True)
    return byte + data


# extract a packet
def decoder(packet):
    sequence_number = int.from_bytes(packet[:6], byteorder="little", signed=True)
    return sequence_number, packet[6:]
