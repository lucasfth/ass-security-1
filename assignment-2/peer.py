import socket
import random
import struct
import ssl
import time


class Peer:
    def __init__(self, port, max, h_port):
        self.port = port
        # print(f"{self.port} starting...")
        self.max = max
        self.h_port = h_port
        self.aggregate_values = []

    def deal(self):
        self.s = random.randint(1, self.max)
        s1 = random.randint(1, self.max)
        s2 = random.randint(1, self.max)
        # s3 = self.s - (s1 + s2)
        s3 = self.s + self.max - ((s1 + s2) % self.max)

        self.aggregate_to_send = [s1, s2]
        self.aggregate_values.append(s3)

        # print(f"{self.port} secret {self.s} and aggregate values {self.aggregate_to_send} and {s3}")

    def peer_socket_stuff(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", self.port))
        s.listen(5)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

        s = context.wrap_socket(s)

        # print(f"{self.port} waiting for connection...")

        # Recieve from the 2 other peers
        for _ in range(2):
            peer, address = s.accept()
            data = peer.recv(8)
            unpacked = (struct.unpack('!Q', data)[0])
            peer.close()
            self.aggregate_values.append(unpacked)
            # print(f"{self.port} received {unpacked} from {address}")

        # Send aggregated value to hospital
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect(("localhost", self.h_port))

        h_port = context.wrap_socket(s)

        data = struct.pack('!Q', (sum(self.aggregate_values) % self.max))

        # print(f"{self.port} sum {sum(self.aggregate_values) % self.max} lst {self.aggregate_values} to hospital")

        h_port.send(data)

        time.sleep(1)
        h_port.close()

    def send_aggregate_values(self, p_ports):
        n = 0
        for port in p_ports:
            if port == self.port:
                continue
            # print(f"{self.port} sending {self.aggregate_to_send[n]} to {port}")

            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect(("localhost", port))

            p_port = context.wrap_socket(s)

            data = struct.pack('!Q', self.aggregate_to_send[n])

            p_port.send(data)
            n += 1
            time.sleep(1)
            p_port.close()
