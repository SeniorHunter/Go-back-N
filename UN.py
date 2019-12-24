# ---------------------------------------- #
# ---------- Unreliable Network ---------- #
# ---------------------------------------- #
import random
import socket


class UN:
    """A class to simulate an unreliable network.


        Attributes:

        DROP_PROBABILITY : float
            lost packet percentage
        connection : socket
            a TCP socket used for sending and receiving data


        Methods:

        send(packet)
            sends a packet through the Socket
        receive()
            receives a packet through the socket

    """
    DROP_PROBABILITY = 0.1  # receive through TCP with Drop Probability
    connection: socket

    def __init__(self, connection: socket):
        self.connection = connection

    def send(self, packet):
        """Sends the passed packet with the set drop probability

        """
        if random.random() >= self.DROP_PROBABILITY:
            self.connection.send(packet)
        return

    # receive from TCP
    def receive(self):
        """Receives the incoming packet from the socket and returns it

        :return: packet
        """
        packet = self.connection.recv(1024)
        return packet
