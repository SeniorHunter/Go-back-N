import socket
import threading
import time
import Packet
import UN
from timer import Timer

PORT = 65432
HOST = '127.0.0.1'
SEND_FILE_PATH = b'send.jpg'
TIMEOUT = 0.5
windows_size = 4
PACKET_SIZE = 1000
number_of_packets = 0
packets = []
last_ack = -1
next_packet = 0
timer = Timer(TIMEOUT)
lock = threading.Lock()


def is_finished():
    return last_ack >= number_of_packets - 1


def is_send_window_complete():
    return not (next_packet - last_ack < windows_size and next_packet < number_of_packets)


def client(local_socket):
    global last_ack
    global next_packet
    global windows_size
    global lock

    to_buffer()
    receive_data_thread = threading.Thread(target=receive_data, args=(local_socket,))
    receive_data_thread.start()

    while not is_finished():
        while not is_send_window_complete():
            UN.send(Packet.encoder(next_packet, packets[next_packet]), local_socket)
            next_packet += 1
            time.sleep(0.0001)

        if is_finished():
            break

        if not timer.is_running():
            timer.start()

        while timer.is_running() and not timer.time_out():
            time.sleep(0.01)

        if timer.time_out():
            timer.stop()
            next_packet = last_ack


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
        print("file Error")
        return


def receive_data(local_socket):
    global last_ack
    global lock

    while not is_finished():
        ack, _ = Packet.decoder(UN.receive(local_socket))

        if ack >= last_ack:
            last_ack = ack
            timer.stop()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    client(sock)

