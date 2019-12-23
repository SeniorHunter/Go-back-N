import logging
import socket as Socket
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
packet: Packet


def client(connection):
    global packet
    packet = Packet(connection)
    initialize_logger()

    global last_ack
    global next_packet

    to_buffer()

    while True:
        while not is_send_window_complete():
            logging.info("send packet " + str(next_packet))
            send_window()

        if is_finished():
            break

        if not timer.is_running():
            timer.start()
            logging.info("timer start")

        while timer.is_running() and not timer.time_out():
            receive_ack()

        if timer.time_out():
            logging.info("time out")
            timer.stop()
            next_packet = last_ack

        if is_finished():
            packet.send_packet(0, True)
            break


def send_window():
    global next_packet
    packet.send_packet(next_packet, False, packets[next_packet])
    next_packet += 1
    time.sleep(0.0001)


def receive_ack():
    global last_ack
    try:
        ack, _, _ = packet.receive_packet()
        if ack is not None:
            logging.info("ack " + str(ack))
            if ack >= last_ack:
                last_ack = ack
                timer.stop()
    except:
        pass


def initialize_logger():
    global logger
    # logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG", filename="server.log", filemode='w')
    logging.basicConfig(format='%(asctime)-15s - %(message)s', level="DEBUG")
    logger = logging.getLogger()


def is_finished():
    return last_ack >= number_of_packets - 1


def is_send_window_complete():
    return not (next_packet - last_ack <= WINDOW_SIZE and next_packet < number_of_packets)


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


with Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM) as socket:
    socket.connect((HOST, PORT))
    socket.settimeout(False)
    client(socket)
