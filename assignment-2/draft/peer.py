import socket
import threading


class Peer:
    def __init__(self, host, portin, portout):
        self.host = host
        self.portin = portin
        self.portout = portout
        self.insocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, peer_host, peer_port):
        try:
            connection = self.outsocket.connect((peer_host, peer_port))
            print(f"Connected to {peer_host}:{peer_port}")
            return connection
        except socket.error as e:
            print(f"Failed to connect to {peer_host}:{peer_port}. Error: {e}")

    def listen(self):
        self.insocket.bind((self.host, self.portin))
        self.insocket.listen()
        print(f"Listening for connections on {self.host}:{self.portin}")

        while True:
            connection, address = self.insocket.accept()
            print(f"Accepted connection from {address}")

    def send_data(self, data, peer_host, peer_port):

        connection = self.connect(peer_host, peer_port)

        try:
            connection(data.encode())
        except socket.error as e:
            print(f"Failed to send data. Error: {e}")

        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()


host = "localhost"
p1i = 5000
p1o = 8001
p2i = 5001
p2o = 8002
p3i = 5002
p3o = 8003

p1 = Peer(host, p1i, p2o)
p2 = Peer(host, p2i, p2o)
p3 = Peer(host, p3i, p2o)

p1.start()
p2.start()
p3.start()

p1.send_data("Hello", host, p2i)
