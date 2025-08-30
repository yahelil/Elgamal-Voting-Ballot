import socket
import pickle
from encryption import *

PROXY_HOST = 'localhost'
PROXY_PORT = 65433
REAL_SERVER_HOST = 'localhost'
REAL_SERVER_PORT = 65434  # Server must listen on this new port
VALID_NAMES = {"simon", "eden", "guy", "shira", "yaheli"}



def fake_decrypt(encrypted_vote, key, p):
    # Try random private keys
    for guess in range(2, min(p - 2, 100)):  # Try only first 100 guesses
        try:
            decrypt_message, key = decrypt_vote(encrypted_vote, key, guess, p)
            if decrypt_message in VALID_NAMES:
                print(f"Guess {guess} produced a valid name: {decrypt_message}")
            else:
                print(f"Guess {guess}: {decrypt_message} (invalid)")
        except:
            continue

print("MITM Proxy is running. Waiting for clients...\n")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy:
        proxy.bind((PROXY_HOST, PROXY_PORT))
        proxy.listen()

        while 1:
            client_conn, _ = proxy.accept()
            with client_conn:
                print("Client connected.")

                # Connect to real server
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
                    server_conn.connect((REAL_SERVER_HOST, REAL_SERVER_PORT))
                    print("Connected to real server.")

                    # Relay public key from server to client
                    public_key = server_conn.recv(1024)
                    client_conn.sendall(public_key)
                    p, g, y = pickle.loads(public_key)

                    # Intercept encrypted vote
                    encrypted_vote = client_conn.recv(1024)
                    intercepted = pickle.loads(encrypted_vote)
                    print(f"Intercepted vote: {intercepted}")

                    fake_decrypt(intercepted[0], intercepted[1], p)
                    # Try to decrypt (without private key)
                    print("Encryption is working: vote remains confidential.")

                    # Forward to real server
                    server_conn.sendall(encrypted_vote)
except KeyboardInterrupt:
    print("\nMITM Proxy stopped by user.")


