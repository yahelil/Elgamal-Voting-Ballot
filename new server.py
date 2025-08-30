import socket
import threading
import hashlib
import json
import random
import sys
from typing import Tuple, List, Dict

# =========================
# Group / ElGamal helpers
# =========================

def mod_inv(a: int, p: int) -> int:
    # Since p is prime, use Fermat inverse: a^(p-2) mod p
    return pow(a, p - 2, p)

def reencrypt(ct: Tuple[int, int], g: int, b: int, p: int, s: int) -> Tuple[int, int]:
    kt, y = ct
    kt2 = (kt * pow(g, s, p)) % p
    y2  = (y  * pow(b, s, p)) % p
    return (kt2, y2)

def decrypt(ct: Tuple[int, int], d: int, p: int) -> int:
    kt, y = ct
    km = pow(kt, d, p)
    x = (y * mod_inv(km, p)) % p
    return x

def H_int(items: List[int], q: int, p: int) -> int:
    # Hash a sequence of integers to a challenge in Z_q
    m = hashlib.sha256()
    width = (p.bit_length() + 7) // 8
    for v in items:
        m.update(int(v).to_bytes(width, "big"))
    return int.from_bytes(m.digest(), "big") % q

# =========================
# Chaum–Pedersen EQ-of-Logs (non-interactive)
# Prove: log_g1(h1) = log_g2(h2) without revealing the log
# Verify equations:
#   g1^r == a1 * h1^c   and   g2^r == a2 * h2^c   (mod p)
# =========================

def cp_verify(g1, g2, h1, h2, a1, a2, c, r, p) -> bool:
    lhs1 = pow(g1, r, p)
    rhs1 = (a1 * pow(h1, c, p)) % p
    lhs2 = pow(g2, r, p)
    rhs2 = (a2 * pow(h2, c, p)) % p
    return lhs1 == rhs1 and lhs2 == rhs2

def cp_real_commit(g1, g2, h1, h2, q, p) -> Tuple[int, int, int]:
    # Choose blinding w and compute commitments a1 = g1^w, a2 = g2^w
    w = random.randrange(1, q)
    a1 = pow(g1, w, p)
    a2 = pow(g2, w, p)
    return w, a1, a2

def cp_real_respond(w, s, c, q) -> int:
    # r = w + c*s  mod q
    return (w + (c * s) % q) % q

def cp_simulate(g1, g2, h1, h2, q, p) -> Tuple[int, int, int, int]:
    # Pick random c_sim, r_sim and back-compute a1, a2 to satisfy checks
    c_sim = random.randrange(0, q)
    r_sim = random.randrange(0, q)
    # a1 = g1^r * (h1^-c)
    a1 = (pow(g1, r_sim, p) * pow(h1, (q - (c_sim % q)) % q, p)) % p
    a2 = (pow(g2, r_sim, p) * pow(h2, (q - (c_sim % q)) % q, p)) % p
    return a1, a2, c_sim, r_sim

# =========================
# 2x2 OR-proof builder (CDS-style)
# Inputs:
#   A,B  : input ciphertexts (pairs)
#   U,V  : output ciphertexts (pairs)
#   real_branch: "NS" if (A->U, B->V) , "SW" if (A->V, B->U)
#   s1,s2: re-encryption exponents used in the true mapping
# Params:
#   (p,g,b,q), and a comparator_id to domain-separate Fiat–Shamir
# Output: proof dict with both branches; verifier can check both
# =========================

def build_or_proof(A, B, U, V, real_branch, s1, s2, p, g, b, q, comparator_id: int) -> Dict:
    def targets(X, Y):
        (ktX, yX), (ktY, yY) = X, Y
        h1 = (ktX * mod_inv(ktY, p)) % p
        h2 = (yX  * mod_inv(yY,  p)) % p
        return (g, b, h1, h2)

    # Branch pairings
    NS_pairs = [(U, A), (V, B)]  # (A->U) and (B->V)
    SW_pairs = [(U, B), (V, A)]  # (B->U) and (A->V)

    real_pairs = NS_pairs if real_branch == "NS" else SW_pairs
    fake_pairs = SW_pairs if real_branch == "NS" else NS_pairs

    # --- REAL branch: prepare real commitments for its two relations
    (g1_r1, g2_r1, h1_r1, h2_r1) = targets(*real_pairs[0])
    (g1_r2, g2_r2, h1_r2, h2_r2) = targets(*real_pairs[1])

    w1, a1_r1, a2_r1 = cp_real_commit(g1_r1, g2_r1, h1_r1, h2_r1, q, p)
    w2, a1_r2, a2_r2 = cp_real_commit(g1_r2, g2_r2, h1_r2, h2_r2, q, p)

    # --- FAKE branch: simulate with a single shared branch-challenge c_fake
    (g1_f1, g2_f1, h1_f1, h2_f1) = targets(*fake_pairs[0])
    (g1_f2, g2_f2, h1_f2, h2_f2) = targets(*fake_pairs[1])

    c_fake = random.randrange(0, q)
    def resim(g1x, g2x, h1x, h2x, c_fixed):
        r = random.randrange(0, q)
        a1 = (pow(g1x, r, p) * pow(h1x, (q - c_fixed) % q, p)) % p
        a2 = (pow(g2x, r, p) * pow(h2x, (q - c_fixed) % q, p)) % p
        return a1, a2, r

    a1_f1, a2_f1, r_f1 = resim(g1_f1, g2_f1, h1_f1, h2_f1, c_fake)
    a1_f2, a2_f2, r_f2 = resim(g1_f2, g2_f2, h1_f2, h2_f2, c_fake)

    # --- Arrange commitments in a STABLE order for hashing: NS first, then SW
    # Decide which a’s belong to NS vs SW, depending on which branch is real
    if real_branch == "NS":
        a_NS = [(a1_r1, a2_r1), (a1_r2, a2_r2)]
        a_SW = [(a1_f1, a2_f1), (a1_f2, a2_f2)]
    else:
        a_NS = [(a1_f1, a2_f1), (a1_f2, a2_f2)]
        a_SW = [(a1_r1, a2_r1), (a1_r2, a2_r2)]

    # Compute global challenge C exactly like the verifier: NS-first then SW
    items = [
        comparator_id, p, g, b,
        A[0], A[1], B[0], B[1], U[0], U[1], V[0], V[1],
        a_NS[0][0], a_NS[0][1], a_NS[1][0], a_NS[1][1],
        a_SW[0][0], a_SW[0][1], a_SW[1][0], a_SW[1][1],
    ]
    C = H_int(items, q, p)

    # Split: C = c_real + c_fake (mod q)
    c_real = (C - c_fake) % q

    # Real responses (both relations in the real branch share c_real)
    r_real1 = cp_real_respond(w1, s1, c_real, q)
    r_real2 = cp_real_respond(w2, s2, c_real, q)

    # Package with stable branch layout (NS first, SW second)
    if real_branch == "NS":
        branch_NS = {
            "c": c_real,
            "pairs": [
                {"a1": a1_r1, "a2": a2_r1, "r": r_real1},
                {"a1": a1_r2, "a2": a2_r2, "r": r_real2},
            ],
        }
        branch_SW = {
            "c": c_fake,
            "pairs": [
                {"a1": a1_f1, "a2": a2_f1, "r": r_f1},
                {"a1": a1_f2, "a2": a2_f2, "r": r_f2},
            ],
        }
    else:
        branch_NS = {
            "c": c_fake,
            "pairs": [
                {"a1": a1_f1, "a2": a2_f1, "r": r_f1},
                {"a1": a1_f2, "a2": a2_f2, "r": r_f2},
            ],
        }
        branch_SW = {
            "c": c_real,
            "pairs": [
                {"a1": a1_r1, "a2": a2_r1, "r": r_real1},
                {"a1": a1_r2, "a2": a2_r2, "r": r_real2},
            ],
        }

    return {
        "C": C,
        "branch_NS": branch_NS,
        "branch_SW": branch_SW,
    }


def verify_or_proof(A, B, U, V, proof, p, g, b, q, comparator_id: int) -> bool:
    def targets(X, Y):
        (ktX, yX), (ktY, yY) = X, Y
        h1 = (ktX * mod_inv(ktY, p)) % p
        h2 = (yX  * mod_inv(yY,  p)) % p
        return (g, b, h1, h2)

    # --- Unpack proof
    C    = proof["C"]
    c_NS = proof["branch_NS"]["c"]
    c_SW = proof["branch_SW"]["c"]

    # NS branch (A->U, B->V)
    a1_NS1 = proof["branch_NS"]["pairs"][0]["a1"]
    a2_NS1 = proof["branch_NS"]["pairs"][0]["a2"]
    r_NS1  = proof["branch_NS"]["pairs"][0]["r"]

    a1_NS2 = proof["branch_NS"]["pairs"][1]["a1"]
    a2_NS2 = proof["branch_NS"]["pairs"][1]["a2"]
    r_NS2  = proof["branch_NS"]["pairs"][1]["r"]

    # SW branch (B->U, A->V)
    a1_SW1 = proof["branch_SW"]["pairs"][0]["a1"]
    a2_SW1 = proof["branch_SW"]["pairs"][0]["a2"]
    r_SW1  = proof["branch_SW"]["pairs"][0]["r"]

    a1_SW2 = proof["branch_SW"]["pairs"][1]["a1"]
    a2_SW2 = proof["branch_SW"]["pairs"][1]["a2"]
    r_SW2  = proof["branch_SW"]["pairs"][1]["r"]

    # --- Recompute Fiat–Shamir challenge exactly like the prover: NS then SW commits
    items = [
        comparator_id, p, g, b,
        A[0], A[1], B[0], B[1], U[0], U[1], V[0], V[1],
        a1_NS1, a2_NS1, a1_NS2, a2_NS2,
        a1_SW1, a2_SW1, a1_SW2, a2_SW2
    ]
    C_recomputed = H_int(items, q, p)
    if (c_NS + c_SW) % q != C_recomputed:
        return False

    # --- Build CP targets for each relation
    # NS relations: (A->U) and (B->V)
    (g1_NS1, g2_NS1, h1_NS1, h2_NS1) = targets(U, A)
    (g1_NS2, g2_NS2, h1_NS2, h2_NS2) = targets(V, B)

    # SW relations: (B->U) and (A->V)
    (g1_SW1, g2_SW1, h1_SW1, h2_SW1) = targets(U, B)
    (g1_SW2, g2_SW2, h1_SW2, h2_SW2) = targets(V, A)

    # --- Verify all four CP equations with the correct argument order
    ok_NS_1 = cp_verify(g1_NS1, g2_NS1, h1_NS1, h2_NS1, a1_NS1, a2_NS1, c_NS, r_NS1, p)
    ok_NS_2 = cp_verify(g1_NS2, g2_NS2, h1_NS2, h2_NS2, a1_NS2, a2_NS2, c_NS, r_NS2, p)

    ok_SW_1 = cp_verify(g1_SW1, g2_SW1, h1_SW1, h2_SW1, a1_SW1, a2_SW1, c_SW, r_SW1, p)
    ok_SW_2 = cp_verify(g1_SW2, g2_SW2, h1_SW2, h2_SW2, a1_SW2, a2_SW2, c_SW, r_SW2, p)

    return ok_NS_1 and ok_NS_2 and ok_SW_1 and ok_SW_2


# =========================
# Odd–Even Transposition Sorting Network (for any n)
# Each phase alternates comparing (0,1),(2,3),... then (1,2),(3,4),...
# We “sort” by hidden random tags; each comparator builds an OR-proof.
# =========================

def sorting_network_shuffle(ciphertexts: List[Tuple[int,int]], p, g, b, q) -> Tuple[List[Tuple[int,int]], List[Dict]]:
    n = len(ciphertexts)
    tags = [random.randrange(0, q) for _ in range(n)]
    proofs = []
    comp_id = 0

    # Work on a mutable copy
    C = list(ciphertexts)
    T = list(tags)

    for phase in range(n):
        start = 0 if phase % 2 == 0 else 1
        for i in range(start, n - 1, 2):
            j = i + 1

            # Decide order by hidden tags
            swap = T[i] > T[j]

            # Fresh re-encryption randomness for the chosen mapping
            s1 = random.randrange(1, q)
            s2 = random.randrange(1, q)

            A, B = C[i], C[j]
            if not swap:
                U = reencrypt(A, g, b, p, s1)
                V = reencrypt(B, g, b, p, s2)
                real_branch = "NS"
                # Tags stay as (T[i], T[j])
            else:
                U = reencrypt(B, g, b, p, s1)
                V = reencrypt(A, g, b, p, s2)
                real_branch = "SW"
                # Swap tags to achieve sorted-by-tag order
                T[i], T[j] = T[j], T[i]

            # Build proof for this 2x2 step
            proof = build_or_proof(A, B, U, V, real_branch, s1, s2, p, g, b, q, comp_id)

            # (Optional) Verify our own proof for sanity
            if not verify_or_proof(A, B, U, V, proof, p, g, b, q, comp_id):
                raise RuntimeError("Internal proof verification failed at comparator {}".format(comp_id))

            # Commit result into array and store proof
            C[i], C[j] = U, V
            proofs.append({
                "comparator_id": comp_id,
                "i": i, "j": j,
                "proof": proof
            })
            comp_id += 1

    return C, proofs

# =========================
# Server
# =========================

class VotingServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.host = host
        self.port = port

        # Tiny demo params — DO NOT USE IN PRODUCTION
        self.p = 7919             # prime modulus
        self.g = 5                # generator
        self.q = self.p - 1       # group order in Z_p*
        self.d = random.randint(1, self.p - 2)   # private key
        self.b = pow(self.g, self.d, self.p)     # public key

        self.ciphertexts = []

    def start(self):
        print(f"[+] Server keys: p={self.p}, g={self.g}, b={self.b}  (private d is hidden)\n")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"[+] Server listening on {self.host}:{self.port}")
        try:
            while len(self.ciphertexts) < 10:
                conn, addr = s.accept()
                with conn:
                    print(f"[+] Client connected: {addr}")
                    # Send public parameters
                    conn.send(f"{self.p},{self.g},{self.b}".encode())
                    data = conn.recv(4096).decode().strip()
                    kt, y = map(int, data.split(","))
                    self.ciphertexts.append((kt, y))
                    print(f"[+] Received ciphertext #{len(self.ciphertexts)}: (kt={kt}, y={y})")
            print("\n[+] 10 votes received. Building verifiable shuffle proof...")

            # Shuffle via odd-even network with ZK proofs
            mixed, proofs = sorting_network_shuffle(self.ciphertexts, self.p, self.g, self.b, self.q)

            print(f"[+] Generated {len(proofs)} 2x2 OR-proofs (one per comparator). Verifying...")

            # (Already self-verified inside; here we just report)
            ok = True
            if ok:
                print("[+] All per-step proofs verified locally.\n")

            # Decrypt final outputs and tally
            votes_p1 = 0
            votes_p2 = 0
            plaintexts = []
            for ct in mixed:
                x = decrypt(ct, self.d, self.p)
                plaintexts.append(x)
                if x == 1000:
                    votes_p1 += 1
                elif x == 2000:
                    votes_p2 += 1

            print("Decrypted votes (shuffled, unlinkable to senders):", plaintexts)
            print(f"Votes for Person 1 (1000): {votes_p1}")
            print(f"Votes for Person 2 (2000): {votes_p2}")
            if votes_p1 > votes_p2:
                print("🎉 Person 1 wins!")
            elif votes_p2 > votes_p1:
                print("🎉 Person 2 wins!")
            else:
                print("🤝 It's a tie!")

            # Save full proof bundle to a JSON file
            bundle = {
                "params": {"p": self.p, "g": self.g, "b": self.b, "q": self.q},
                "inputs": [{"kt": kt, "y": y} for (kt, y) in self.ciphertexts],
                "outputs": [{"kt": kt, "y": y} for (kt, y) in mixed],
                "proofs": proofs,
                "note": "Each comparator proof is an OR of two Chaum–Pedersen conjunctions."
            }
            with open("proofs.json", "w") as f:
                json.dump(bundle, f, indent=2)
            print("\n[+] Full shuffle proof written to proofs.json")
            print("[+] Server exiting.")
        finally:
            s.close()

if __name__ == "__main__":
    VotingServer().start()
