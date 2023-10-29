import threading
import peer
import hospital
import time

max_value = 2048
hos_port = 8000

print("Starting hospital")
# threading.Thread(target=hospital.Hospital(port=8000, max=max_value), daemon=False).start()
hospital_thread = threading.Thread(target=hospital.Hospital, args=(hos_port, max_value))
hospital_thread.daemon = False
hospital_thread.start()

time.sleep(1)

P_PORTS = [5001, 5002, 5003]

print("Starting peers")
p0 = peer.Peer(port=(P_PORTS[0]), max=max_value, h_port=hos_port)
p1 = peer.Peer(port=(P_PORTS[1]), max=max_value, h_port=hos_port)
p2 = peer.Peer(port=(P_PORTS[2]), max=max_value, h_port=hos_port)

for p in [p0, p1, p2]:
    print(f"Starting {p.port}")
    p.deal()
    thread = threading.Thread(target=p.peer_socket_stuff, daemon=False)
    thread.start()

time.sleep(3)

for p in [p0, p1, p2]:
    p.send_aggregate_values(p_ports=P_PORTS)
    time.sleep(1)

print(f"p0 {p0.s}, p1 {p1.s}, p2 {p2.s} summed to {p0.s + p1.s + p2.s}")
