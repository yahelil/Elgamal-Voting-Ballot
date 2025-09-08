import socket
import pickle
from encryption import encrypt_vote


HOST = 'localhost'
PORT = 65434

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Step 1: Receive public key
    data = s.recv(1024)
    p, g, y = pickle.loads(data)
    print(f"Received public key: p={p}, g={g}, y={y}")

    # Step 2: Cast vote
    # Step 2: Cast vote
    vote = input("Cast your vote (Simon, Eden, Guy, Shira, Yaheli): ").lower()
    if vote not in ["simon", "eden", "guy", "shira", "yaheli"]:
        raise ValueError("Invalid vote. Must be Simon/Eden/Guy/Shira/Yaheli.")

    encrypted_vote, Key_E = encrypt_vote(vote, p, g, y)

    # Step 3: Send encrypted vote
    s.sendall(pickle.dumps((encrypted_vote, Key_E)))
    print("Vote sent.")
