import socket
import random
import pickle
from encryption import decrypt_vote

HOST = 'localhost'
PORT = 65433

# Key generation
p = 467 # Choose any prime number
g = 2 #Choose the modulo (my p)
private_key = random.randint(2, p - 2) # Bob's private key (Kprivate)
y = pow(g, private_key, p) # same as g^x mod p
public_key = (p, g, y)

votes = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server listening...")

    for i in range(5):
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
counter_1 = 0
counter_2 = 0

for vote in votes:
    decrypted_vote, Key_E = decrypt_vote(vote[0], vote[1], private_key, p)
    print(f"Decrypted vote: {decrypted_vote}")

    if decrypted_vote == 1:
        counter_1 += 1
    elif decrypted_vote == 2:
        counter_2 += 1

print(f"Yes votes (1): {counter_1}")
print(f"No votes (2): {counter_2}")
