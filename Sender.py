import logging
import socket as Socket
import time
import Packet
from Timer import Timer
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
    """The file is divided to packets and gets sent. Until the window size is reached, packets are sent.
    As long as a timeout doesn't happen the client keeps receiving acknowledgement, otherwise the client
    will retransmit from the last received ack. Process ends when all the packets are sent.

    Attributes:
    packet : Packet
    last_ack : int
        number of the last packet confirmed by server.
    next_packet : int
        number of the packet to be sent

    Methods:
    initialize_logger()
    to_buffer()
        saves the divided file

    """
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
    """Packets are assembled and sent

    """
    global next_packet
    packet.send_packet(next_packet, False, packets[next_packet])
    next_packet += 1
    time.sleep(0.0001)


def receive_ack():
    """The ack sent by the server is checked; if the sequence is correct, the acknowledgement is saved
        and timer is stopped

    """
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
    """Is called to check if the file is fully sent

    """
    return last_ack >= number_of_packets - 1


def is_send_window_complete():
    """Is called to check if a complete window is sent

    :return: boolean
    """
    return not (next_packet - last_ack <= WINDOW_SIZE and next_packet < number_of_packets)


def to_buffer():
    """The file which is going to be sent is divided in packet size parts and is saved to a list

    Attributes:
    number_of_packets : int
    packets : list

    """
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
