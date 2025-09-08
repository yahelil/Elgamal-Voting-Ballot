import random
from Server import public_key


def reencrypt(Group, encrypted_vote):
    r = random.randint(1, 100)
    g = Group.get_generator()
    pow_public_key = Group.pow(public_key, r)
    return Group.operation(Group.pow(g, r), encrypted_vote[0]), Group.operation(pow_public_key, encrypted_vote[1])

def mix_two_ciphertexts(C1, C2, p, g, y):
    pass

def verify_mix_proof(proof, p, g, b):
    pass