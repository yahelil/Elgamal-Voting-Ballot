import socket
import random
import pickle
from encryption import decrypt_vote

HOST = 'localhost'
PORT = 65434

# Key generation
p = 2**64 - 59 # Choose any prime number big enough for a string value
g = 60
private_key = random.randint(2, p - 2) # Bob's private key (K_private)
b = pow(g, private_key, p) # same as g^x mod p
public_key = (p, g, b)

votes = []

print("Server is running. Waiting for votes...\n")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(2)

        while True:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue

            with conn:
                print(f"Connected by {addr}")

                # Step 1: Send public key
                conn.sendall(pickle.dumps(public_key))

                # Step 2: Receive encrypted vote
                data = conn.recv(1024)

                vote = pickle.loads(data)
                votes.append(vote)
                print(f"Received vote: {vote}")
except KeyboardInterrupt:
    print("\nVoting ended by user.")


print("\nCounting the votes...")
counters = {name: 0 for name in ["simon", "eden", "guy", "shira", "yaheli"]}

for vote in votes:
    decrypted_vote, Key_E = decrypt_vote(vote[0], vote[1], private_key, p)

    if decrypted_vote in counters:
        counters[decrypted_vote] += 1

for name, count in counters.items():
    print(f"{name.capitalize()} votes: {count}")

