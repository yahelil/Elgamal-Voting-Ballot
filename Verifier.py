import pickle
import random
import socket
from Group import Group

HOST = 'localhost'
PORT = 65434

def add_mod_5(a, b):
    return (a + b) % 5


def check_equality(original, reencryption):
    """Perform a proof verification based on the given proof and parameters."""

    A1, A2, c, r = proof
    g = Group.get_generator()

    b1 = Group.operation(reencryption[0], Group.inverse(original[0]))
    b2 = Group.operation(reencryption[1], Group.inverse(original[1])) # Assuming that m'1 and m1 are the same = public_key^r

    return Group.pow(g, r) == Group.operation(A1, Group.pow(b1, c)) and Group.pow(public_key, r) == Group.operation(A2, Group.pow(b2, c))

def verify_proof(original, reencryption):
    """The function takes the two votes before the mix and after, together with the proof
            Then Returns True or False based on whether the proof is correct"""

    # Checks if [(C1 ≈ C'1) ∨ (C1 ≈ C'2)]
    return check_equality(original[0], reencryption[0]) or check_equality(original[1], reencryption[0])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    """
        Establish a socket connection with the Bulletin Board.
        Receive public_key, mixes, elements.
        Perform a series of verifications on mixes using proofs.
    """

    s.connect((HOST, PORT))

    data = s.recv(4096)
    public_key, mixes, elements = pickle.loads(data)
    Group = Group(elements, add_mod_5)
    print(f"Verifying {len(mixes)} mixers...\n")

    # Check the validity of mixes and detect any cheating in the process.
    overall_proof = True
    cheater = None
    for i in range(1, len(mixes)):
        if i == 1:
            prev_cipher1, prev_cipher2 = mixes[i - 1]
        else:
            prev_cipher1, prev_cipher2, _ = mixes[i - 1]
        curr_cipher1, curr_cipher2, proof = mixes[i]

        verified = verify_proof((prev_cipher1, prev_cipher2), (curr_cipher1, curr_cipher2))
        if not verified:
            # if the current mixer cheated
            print(f"Mixer {i} cheated")
            if not cheater: cheater = i
            overall_proof = False
    print(f"Mixers verified: {overall_proof}")
    s.sendall(pickle.dumps(("very", overall_proof, cheater)))