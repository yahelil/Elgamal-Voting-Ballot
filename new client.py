import socket
import random

def encrypt(x, p, g, b):
    i = random.randint(1, p - 2)    # random nonce
    kt = pow(g, i, p)               # temporary key
    km = pow(b, i, p)               # masking key
    y  = (x * km) % p               # encrypted message
    return (kt, y)

def main(server_host="127.0.0.1", server_port=5000):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_host, server_port))

    # Receive public parameters
    data = s.recv(1024).decode()
    p, g, b = map(int, data.split(","))
    print(f"[+] Received params: p={p}, g={g}, b={b}")

    # Get vote from user
    print("Enter your vote:")
    print("  1000 → Person 1")
    print("  2000 → Person 2")
    while True:
        try:
            x = int(input("Your vote (1000/2000): ").strip())
            if x in (1000, 2000):
                break
        except:
            pass
        print("Please enter 1000 or 2000.")

    # Encrypt and send
    kt, y = encrypt(x, p, g, b)
    s.send(f"{kt},{y}".encode())
    print(f"[+] Sent ciphertext: (kt={kt}, y={y})")
    s.close()

if __name__ == "__main__":
    main()
