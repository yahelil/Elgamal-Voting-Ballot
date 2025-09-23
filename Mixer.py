import hashlib
import random
import socket
import pickle

from BulletinBoard import MAX_MIXES
from Group import Group
from Encryption import encrypt_vote

HOST = 'localhost'
PORT = 65434

def add_mod_5(a, b):
    return (a + b) % 5

def name_shortcut(name):
    match name:
        case "si":  return "simon"
        case "e":   return "eden"
        case "g":   return "guy"
        case "sh":  return "shira"
        case "y":   return "yaheli"
    return name

def reencrypt(encrypted_vote, r):
    """
        Mix two ciphertexts using a random value.
        Generate proofs.
        Return the mixed ciphertexts along with the proof.
    """

    if not hasattr(reencrypt, "cheat"):
        reencrypt.cheat = input("Cheat? (y or n) ")

    # Adding an option to cheat (Only to test verifier. Not in real life!)
    if reencrypt.cheat == "y":
        vote = name_shortcut(input("Vote: ").lower())
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
    """A simple sha256 hash"""

    hasher = b''.join(str(arg).encode() for arg in args)
    return int(hashlib.sha256(hasher).hexdigest(), 16)

def generate_proof(original, reencryption, v):
    """
        Generate a zero-knowledge proof of knowledge for a re-encryption operation.
    """

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
    """
        Establish a socket connection to a server. 
        Receive public_key, mixes, elements.
        Send processed data back.
    """

    sock.connect((HOST, PORT))

    data = sock.recv(4096)
    public_key, mixes, elements = pickle.loads(data)
    Group = Group(elements, add_mod_5)
    print(f"Mixer {len(mixes)}")

    mixed_votes = mix_two_ciphertexts(mixes[-1][0], mixes[-1][1])
    if len(mixes) == MAX_MIXES:
        print("No more mixes.")
    else:
        print("Done mixing.")
    sock.sendall(pickle.dumps(("mixer", mixed_votes)))

