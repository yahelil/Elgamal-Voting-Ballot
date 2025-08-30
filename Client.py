import socket
import pickle
from encryption import encrypt_vote

HOST = 'localhost'
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Step 1: Receive public key
    data = s.recv(1024)
    p, g, y = pickle.loads(data)
    print(f"Received public key: p={p}, g={g}, y={y}")

    # Step 2: Cast vote
    # Step 2: Cast vote
    vote = int(input("Cast your vote (1 = Yes, 2 = No): "))
    if vote not in [1, 2]:
        raise ValueError("Invalid vote. Must be 1 or 2.")

    encrypted_vote, Key_E = encrypt_vote(vote, p, g, y)

    # Step 3: Send encrypted vote
    s.sendall(pickle.dumps((encrypted_vote, Key_E)))
    print("Vote sent.")