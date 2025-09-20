import socket
import pickle
from encryption import encrypt_vote
from Group import Group


HOST = 'localhost'
PORT = 65434

def add_mod_5(a, b):
    return (a + b) % 5

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Step 1: Receive public key
    data = s.recv(4096)
    public_key, elements = pickle.loads(data)
    group = Group(elements, add_mod_5)

    # Step 2: Cast vote
    # Step 2: Cast vote
    vote = input("Cast your vote (Simon, Eden, Guy, Shira, Yaheli): ").lower()

    match vote:
        case "si": vote = "simon"
        case "e": vote = "eden"
        case "g": vote = "guy"
        case "sh": vote = "shira"
        case "y": vote = "yaheli"

    if vote not in ["simon", "eden", "guy", "shira", "yaheli"]:
        raise ValueError("Invalid vote. Must be Simon/Eden/Guy/Shira/Yaheli.")

    num, encrypt_vote = encrypt_vote(vote, group, public_key)

    # Step 3: Send encrypted vote
    s.sendall(pickle.dumps((num, encrypt_vote)))
    print("Vote sent.")
