import pickle
import socket
from Group import Group

HOST = 'localhost'
PORT = 65434

def add_mod_5(a, b):
    return (a + b) % 5

def verify_proof(original, reencryption, proof):
    A1, A2, c, t = proof
    g = Group.get_generator()

    b1 = Group.operation(reencryption[0][0], Group.inverse(original[0][0]))
    b2 = Group.operation(reencryption[0][1], Group.inverse(original[0][1]))

    lhs1 = Group.pow(g, t)
    rhs1 = Group.operation(A1, Group.pow(b1, c))

    lhs2 = Group.pow(public_key, t)
    rhs2 = Group.operation(A2, Group.pow(b2, c))

    return lhs1 == rhs1 and lhs2 == rhs2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    data = s.recv(4096)
    public_key, mixes, elements = pickle.loads(data)
    Group = Group(elements, add_mod_5)

    verified = True
    for i in range(2, len(mixes)):
        prev_cipher1, prev_cipher2, _ = mixes[i - 1][1]
        curr_cipher1, curr_cipher2, proof = mixes[i][1]

        verified = verify_proof((prev_cipher1, prev_cipher2), (curr_cipher1, curr_cipher2), proof)
        if not verified:
            print(f"The mixer {i - 1} cheated")
            break
    print(f"Mixers verified")
    s.sendall(pickle.dumps(("very", verified)))