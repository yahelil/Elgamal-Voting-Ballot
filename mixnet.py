import random

def reencrypt(ciphertext, p, g, b):
    """Re-encrypts an ElGamal ciphertext with fresh randomness."""
    c1, c2 = ciphertext
    i = random.randint(2, p - 2)
    K_E = pow(g, i, p)
    K_M = pow(b, i, p)
    new_c1 = (c1 * K_E) % p
    new_c2 = (c2 * K_M) % p
    return (new_c1, new_c2), i

def mix_two_ciphertexts(C1, C2, p, g, y):
    """Re-encrypts and permutes two ciphertexts, returns output and proof."""
    C1_re, r1 = reencrypt(C1, p, g, y)
    C2_re, r2 = reencrypt(C2, p, g, y)

    if random.choice([True, False]):
        permuted = [C1_re, C2_re]
        permutation = 0
    else:
        permuted = [C2_re, C1_re]
        permutation = 1

    proof = {
        "C1": C1,
        "C2": C2,
        "C1'": permuted[0],
        "C2'": permuted[1],
        "r1": r1,
        "r2": r2,
        "perm": permutation
    }

    return permuted[0], permuted[1], proof

def verify_mix_proof(proof, p, g, b):
    """Verifies that the output ciphertexts are valid re-encryptions of the inputs."""
    def verify_reenc(C_orig, C_new, r):
        c1_orig, c2_orig = C_orig
        c1_new, c2_new = C_new
        K_E = pow(g, r, p)
        K_M = pow(b, r, p)
        expected_c1 = (c1_orig * K_E) % p
        expected_c2 = (c2_orig * K_M) % p
        return expected_c1 == c1_new and expected_c2 == c2_new

    if proof["perm"] == 0:
        return verify_reenc(proof["C1"], proof["C1'"], proof["r1"]) and \
               verify_reenc(proof["C2"], proof["C2'"], proof["r2"])
    else:
        return verify_reenc(proof["C2"], proof["C1'"], proof["r1"]) and \
               verify_reenc(proof["C1"], proof["C2'"], proof["r2"])