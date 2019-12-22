# ---------------------------------------- #
# ---------- Unreliable Network ---------- #
# ---------------------------------------- #
import random
import socket


DROP_PROBABILITY = 0  # receive through TCP with Drop Probability


def send(packet, connection: socket.socket):
    if random.randint(0, 1) >= DROP_PROBABILITY:
        connection.send(packet)
    return


# receive from TCP
def receive(connection: socket):
    packet = connection.recv(1024)
    return packet
