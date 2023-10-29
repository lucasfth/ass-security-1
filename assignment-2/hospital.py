import socket
import ssl
import sys
import struct
import threading


class Hospital:
    def __init__(self, port, max):
        # print("Hospital starting...")
        self.port = port
        self.max = max
        self.aggregate_values = []
        # print("Starting socket stuff")
        threading.Thread(target=self.socket_stuff(), daemon=False).start()

    # Aggregate values summed
    def aggregate(self):
        if len(self.aggregate_values) < 3:
            return
        aggregate = sum(self.aggregate_values)
        print(f"Hospitals aggregate sum: {aggregate}")
        sys.exit()

    # Socket stuff
    def socket_stuff(self):
        # print("Hospital socket stuff starting...")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("localhost", self.port))
        s.listen(5)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile="server_cert.pem", keyfile="server_key.pem")

        s = context.wrap_socket(s)

        # Recieve message from 4 clients
        for _ in range(4):
            # print("Hospital waiting for connection...")
            client, address = s.accept()
            data = client.recv(8)
            unpacked = (struct.unpack('!Q', data)[0])
            client.close()
            self.aggregate_values.append(unpacked)
            # print(f"Hospital received {unpacked} from {address}")

            if (len(self.aggregate_values) == 3):
                self.aggregate()
