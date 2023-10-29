import socket


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)  # Set a timeout for waiting for connections

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print("Connected to the peer.")
            return True
        except ConnectionRefusedError:
            print("Peer is not available.")
            return False

    def send_message(self, message):
        self.socket.send(message.encode())

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    host = 'localhost'
    port = 8000

    peers = []

    # Create and connect peers
    for i in range(1, 5):
        peer = Peer(host, port)
        if peer.connect():
            peers.append(peer)

    for i, peer in enumerate(peers):
        message = input(f"Peer {i + 1}, You: ")
        for other_peer in peers:
            if other_peer != peer:
                other_peer.send_message(message)

    # Close all connections
    for peer in peers:
        peer.close()
