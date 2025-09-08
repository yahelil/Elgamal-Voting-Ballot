import socket
import random
import pickle
from encryption import decrypt_vote
from Group import Group
from mixnet import reencrypt

HOST = 'localhost'
PORT = 65434

#Creating the cyclic group
def add_mod_5(a, b):
    return (a + b) % 5

elements = [0, 1, 2, 3, 4]
G = Group(elements, add_mod_5)
G.show_structure()

# Key generation
g = G.get_generator()
private_key = random.randint(1, 100)
print(f"Private key: {private_key}")
public_key = G.pow(g, private_key)
print(f"Public key: {public_key}")

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
                conn.sendall(pickle.dumps((elements, public_key)))

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
    num, encrypted_vote = vote[0], vote[1]
    decrypted_vote = decrypt_vote(G, num, encrypted_vote, private_key)
    print(decrypted_vote)
    if decrypted_vote in counters:
        counters[decrypted_vote] += 1

for name, count in counters.items():
    print(f"{name.capitalize()} votes: {count}")

print("\nReencrypting votes...")

reencrypt(Group, votes[0])
