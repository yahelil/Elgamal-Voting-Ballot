import hashlib
import random
import socket
import pickle
from Group import Group
from Voter import name_shortcut
from encryption import encrypt_vote

HOST = 'localhost'
PORT = 65434

def add_mod_5(a, b):
    return (a + b) % 5

def reencrypt(encrypted_vote, r):
    # Adding an option to cheat (Only to test verifier. Not in real life!)
    if input("Cheat? (y or n)") == "y":
        vote = input("Vote: ").lower()
        name_shortcut(vote)
        encrypted_vote = encrypt_vote(vote, Group, public_key)
    # Then re-encrypt
    g = Group.get_generator()
    pow_public_key = Group.pow(public_key, r)
    return Group.operation(Group.pow(g, r), encrypted_vote[0]), Group.operation(pow_public_key, encrypted_vote[1]) # (g^(r'+r), pk^r' * m)

def mix_two_ciphertexts(C1, C2):
    r = random.randint(1, Group.order-1)
    D1 = reencrypt(C1, r)
    D2 = reencrypt(C2, r)
    pi = generate_proof((C1, C2), (D1, D2), r)
    # After re-encrypting every vote randomly choose whether mix or not
    if random.choice([True, False]):
        return D1, D2, pi
    else:
        return D2, D1, pi

def hash_challenge(*args):
    # A simple sha256 hash
    hasher = b''.join(str(arg).encode() for arg in args)
    return int(hashlib.sha256(hasher).hexdigest(), 16)

def generate_proof(original, reencryption, v):
    g = Group.get_generator()
    y = public_key
    b1 = Group.operation(reencryption[0][0], Group.inverse(original[0][0]))  # g^r
    b2 = Group.operation(reencryption[0][1], Group.inverse(original[0][1]))  # pk^r

    s = random.randint(1, Group.order - 1)
    A1 = Group.pow(g, s)
    A2 = Group.pow(y, s)

    c = hash_challenge(g, y, b1, b2, A1, A2) % Group.order # Create the challenge with its hash value
    r = (s + c * v) % Group.order

    return A1, A2, c, r

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    data = sock.recv(4096)
    public_key, mixes, elements = pickle.loads(data)
    Group = Group(elements, add_mod_5)

    mixed_votes = mix_two_ciphertexts(mixes[-1][0], mixes[-1][1])
    sock.sendall(pickle.dumps(("mixer", mixed_votes)))

