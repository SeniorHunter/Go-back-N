# ---------------------------------------- #
# ---------- Unreliable Network ---------- #
# ---------------------------------------- #
import random
import socket


class UN:
    DROP_PROBABILITY = 0  # receive through TCP with Drop Probability
    connection: socket

    def __init__(self, connection: socket):
        self.connection = connection

    def send(self, packet):
        if random.random() >= self.DROP_PROBABILITY:
            self.connection.send(packet)
        return

    # receive from TCP
    def receive(self):
        packet = self.connection.recv(1024)
        return packet
