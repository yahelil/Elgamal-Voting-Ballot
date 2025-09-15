import socket
import pickle

HOST = 'localhost'
PORT = 65434
MAX_VOTES = 2

votes = []
mixes = []

print("Server is running. Waiting for admin...\n")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(10)

        admin_conn, admin_addr = s.accept()
        data = admin_conn.recv(4096)
        public_key, elements = pickle.loads(data)

        print("Admin is connected, public key was received...\n")

        while len(votes) < MAX_VOTES:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue

            with conn:
                print(f"Connected by {addr}")

                # Step 1: Send public key
                conn.sendall(pickle.dumps((public_key, elements)))

                # Step 2: Receive encrypted vote
                data = conn.recv(4096)

                vote = pickle.loads(data)
                votes.append(vote)
        mixes.append((votes[0], votes[1]))
        print("Finished voting...")
        num_of_mixes = int(input("How many mixers do you have? "))
        while len(mixes) < num_of_mixes + 1:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            with conn:
                print(f"Connected by {addr}")

                # Step 1: Send public key
                conn.sendall(pickle.dumps((public_key, mixes, elements)))

                # Step 2: Receive encrypted vote
                data = conn.recv(4096)
                mixed_votes = pickle.loads(data) # the two votes mixed and the proof
                if mixed_votes[0] == "mixer":
                    mixes.append(mixed_votes[1])
        votes = [mixes[-1][0], mixes[-1][1]]
        admin_conn.sendall(pickle.dumps(votes))
except KeyboardInterrupt:
    print("\nVoting ended by user.")
