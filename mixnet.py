import random


def reencrypt(Group, public_key, encrypted_vote):
    r = random.randint(1, 100)
    g = Group.get_generator()
    pow_public_key = Group.pow(public_key, r)
    return Group.operation(Group.pow(g, r), encrypted_vote[0]), Group.operation(pow_public_key, encrypted_vote[1])

def mix_two_ciphertexts(Group, public_key, C1, C2):
    num, D1 = reencrypt(Group, public_key, C1)
    num, D2 = reencrypt(Group, public_key, C2)
    if random.choice([True, False]):
        return D1, D2
    else:
        return D2, D1



def verify_mix_proof(proof, p, g, b):
    pass