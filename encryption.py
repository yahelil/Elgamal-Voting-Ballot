import random

def string_to_int(s):
    return int.from_bytes(s.encode(), 'big')

def int_to_string(n):
    byte_length = (n.bit_length() + 7) // 8
    return n.to_bytes(byte_length, 'big').decode()

def encrypt_vote(name, p, g, b):
    m = string_to_int(name)
    i = random.randint(2, p - 2)
    Key_E = pow(g, i, p)
    K_M = pow(b, i, p)
    encrypted_vote = (m * K_M) % p
    return encrypted_vote, Key_E

def decrypt_vote(encrypted_vote, key, private_key, p):
    K_M = pow(key, private_key, p)
    K_M_inv = pow(K_M, -1, p)
    decrypted_int = (encrypted_vote * K_M_inv) % p
    decrypted_name = int_to_string(decrypted_int)
    return decrypted_name, key