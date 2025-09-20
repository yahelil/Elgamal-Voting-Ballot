import socket
import pickle
from Group import Group
import random
from encryption import decrypt_vote

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
    s.connect((HOST, PORT))

    s.sendall(pickle.dumps((public_key, elements)))

    print("keys send")

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

for name, count in counters.items():
    print(f"{name.capitalize()} votes: {count}")
