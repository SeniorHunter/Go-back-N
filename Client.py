import logging
import socket
import time
import Packet
from timer import Timer
from Packet import Packet

PORT = 65432
HOST = '127.0.0.1'
SEND_FILE_PATH = b'send.jpg'
TIMEOUT = 0.1
PACKET_SIZE = 700  # dont change this shit pls
WINDOW_SIZE = 10
number_of_packets = 0
packets = []
last_ack = -1
next_packet = 0
timer = Timer(TIMEOUT)
logger: logging


def initialize_logger():
    global logger
    # logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG", filename="server.log", filemode='w')
    logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG")
    logger = logging.getLogger()


def is_finished():
    return last_ack >= number_of_packets - 1


def is_send_window_complete():
    return not (next_packet - last_ack <= WINDOW_SIZE and next_packet < number_of_packets)


def client(local_socket):
    packet = Packet(local_socket)
    initialize_logger()

    global last_ack
    global next_packet

    to_buffer()

    while True:
        while not is_send_window_complete():
            packet.send_packet(next_packet, False, packets[next_packet])
            logging.info("send packet " + str(next_packet))
            next_packet += 1
            time.sleep(0.0001)

        if is_finished():
            break

        if not timer.is_running():
            timer.start()
            logging.info("timer start")

        while timer.is_running() and not timer.time_out():
            try:
                ack, is_EOT, _ = packet.receive_packet()
                if ack is not None:
                    logging.info("ack " + str(ack))
                    if ack >= last_ack:
                        last_ack = ack
                        timer.stop()
            except:
                pass

        if timer.time_out():
            logging.info("time out")
            timer.stop()
            next_packet = last_ack

        if is_finished():
            packet.send_packet(0, True)
            break


def to_buffer():
    global number_of_packets
    global packets

    try:
        data_file = open(SEND_FILE_PATH, "rb")
        while True:
            data = data_file.read(PACKET_SIZE)
            if not data:
                break
            else:
                packets.append(data)
                number_of_packets += 1
    except FileNotFoundError:
        print("File Error")
        return


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.settimeout(False)
    client(sock)
