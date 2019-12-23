import socket as Socket
import Packet
import logging
from Packet import Packet

PORT = 65432
HOST = '127.0.0.1'
RECEIVED_FILE_PATH = b'receive.jpg'
logger: logging


def initialize_logger():
    global logger
    # logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG", filename="server.log", filemode='w')
    logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG")
    logger = logging.getLogger()


def open_file():
    try:
        return open(RECEIVED_FILE_PATH, "wb")  # create a file for received data
    except IOError:
        logging.debug("file error")
        return


def server(connection):
    packet = Packet(connection)
    initialize_logger()
    file = open_file()

    expected_number = 0
    while True:
        sequence_number, is_EOT, data = packet.receive_packet()
        if is_EOT:
            logging.info("EOT received, finishing connection...")
            packet.send_packet(-1, True)
            break
        logger.info("data number " + str(sequence_number) + " received")

        if expected_number == sequence_number:
            # send ack and write to file
            packet.send_packet(sequence_number, False)
            logger.info("Ack send: " + str(sequence_number))
            expected_number += 1
            file.write(data)
        else:
            # drop and send Ack(exp-num - 1)
            packet.send_packet((expected_number - 1), False)
            logger.info("(resubmit) Ack send: " + str(sequence_number))
    logging.info("saving file...")
    file.close()


with Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM) as socket:
    socket.bind((HOST, PORT))
    socket.listen()
    socket, _ = socket.accept()
    server(socket)




