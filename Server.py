import socket
import random
import pickle
from encryption import decrypt_vote

HOST = 'localhost'
PORT = 65433

# Key generation
p = 2**64 - 59 # Choose any prime number big enough for a string value
g = 2 #Choose the modulo (my p)
private_key = random.randint(2, p - 2) # Bob's private key (Kprivate)
y = pow(g, private_key, p) # same as g^x mod p
public_key = (p, g, y)

votes = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening...")

    for i in range(6):
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            # Step 1: Send public key
            conn.sendall(pickle.dumps(public_key))

            # Step 2: Receive encrypted vote
            data = conn.recv(1024)

            vote = pickle.loads(data)
            votes.append(vote)
            print(f"Received vote: {vote}")


print("The voting is finished.\nCounting the votes...")
counters = {
    "simon": 0,
    "eden": 0,
    "guy": 0,
    "shira": 0,
    "yaheli": 0
}

for vote in votes:
    decrypted_vote, Key_E = decrypt_vote(vote[0], vote[1], private_key, p)

    if decrypted_vote in counters:
        counters[decrypted_vote] += 1


print(f"Simon votes: {counters['simon']}")
print(f"Eden votes: {counters['eden']}")
print(f"Guy votes: {counters['guy']}")
print(f"Shira votes: {counters['shira']}")
print(f"Yaheli votes: {counters['yaheli']}")
