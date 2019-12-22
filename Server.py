import socket
import Packet
import UN
import logging

PORT = 65432
HOST = '127.0.0.1'
RECEIVED_FILE_PATH = b'receive.jpg'

logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG", filename="server.log")
logger = logging.getLogger()


def server(connection):
    try:
        file = open(RECEIVED_FILE_PATH, "wb")  # create a file for received data
    except IOError:
        print("file error")
        return

    expected_number = 0
    while True:
        raw_data = UN.receive(connection)
        if not raw_data:
            break
        sequence_number, data = Packet.decoder(raw_data)
        logger.info("data number " + str(sequence_number) + " received")

        if expected_number == sequence_number:
            # send ack and write to file
            UN.send(Packet.encoder(sequence_number), connection)
            logger.info("Ack send: " + str(sequence_number))
            expected_number += 1
            file.write(data)
        else:
            # drop and send Ack(exp-num - 1)
            UN.send(Packet.encoder(expected_number - 1), connection)
            logger.info("(resubmit) Ack send: " + str(sequence_number))
    file.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    conn, addr = sock.accept()
    server(conn)
