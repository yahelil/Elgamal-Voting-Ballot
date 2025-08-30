import random

def encrypt_vote(m, p, g, y):

    i = random.randint(2, p - 2)
    Key_E = pow(g, i, p)
    K_M = pow(y, i, p)
    encrypted_vote = m * K_M % p
    return encrypted_vote, Key_E

def decrypt_vote(encrypted_vote, key, private_key, p):
    K_M = pow(key, private_key, p)
    K_M_inv = pow(K_M, -1, p)
    decrypted_vote = (encrypted_vote * K_M_inv) % p
    return decrypted_vote, key