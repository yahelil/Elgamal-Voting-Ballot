import socket
import pickle
from Group import Group
import random
from Encryption import decrypt_vote

HOST = 'localhost'
PORT = 65434

#Creating the cyclic group
def add_mod_5(a, b):
    return (a + b) % 5

elements = [0, 1, 2, 3, 4]
Group = Group(elements, add_mod_5)

# Key generation
g = Group.get_generator()
private_key = random.randint(1, 100)
public_key = Group.pow(g, private_key)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    """
        Establish a socket connection to a server.
        Send a pickled tuple containing a public key and elements.
        Receive pickled votes from the server.
    """

    s.connect((HOST, PORT))

    s.sendall(pickle.dumps((public_key, elements)))

    print("keys sent")

    votes = pickle.loads(s.recv(4096))


# Count the votes
print("\nCounting the votes...")
counters = {name: 0 for name in ["simon", "eden", "guy", "shira", "yaheli"]}

for vote in votes:
    num, encrypted_vote = vote[0], vote[1]
    decrypted_vote = decrypt_vote(Group, num, encrypted_vote, private_key)
    print(decrypted_vote)
    if decrypted_vote in counters:
        counters[decrypted_vote] += 1

max_count = 0
winner = None
for name, count in counters.items():
    if count > max_count:
        winner = name
        max_count = count
    elif count == max_count:
        winner = winner + ", " + name
    print(f"{name.capitalize()} votes: {count}")
print(f"Winners are {winner}")
