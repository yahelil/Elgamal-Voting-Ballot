import socket
import pickle

HOST = 'localhost'
PORT = 65444
MAX_VOTES = 2
MAX_MIXES = 5

votes = []
mixes = []

print("Server is running. Waiting for admin...\n")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(30)

        # Connecting to Admin
        admin_conn, admin_addr = s.accept()
        data = admin_conn.recv(4096)
        public_key, elements = pickle.loads(data)

        print("Admin is connected, public key was received...\n")

        #Connecting to MAX_VOTES voters and receiving MAX_VOTES encrypted votes
        while len(votes) < MAX_VOTES:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue

            with conn:
                print(f"Connected by {addr}")

                # Send public key
                conn.sendall(pickle.dumps((public_key, elements)))

                # Receive encrypted vote
                data = conn.recv(4096)

                vote = pickle.loads(data)
                votes.append(vote)

        # Starts mixing and verifying
        mixes.append((votes[0], votes[1]))
        last_time = False
        print("Finished voting...")
        while True:
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            with conn:
                # Send public key and the current mixes
                conn.sendall(pickle.dumps((public_key, mixes, elements)))

                # Receive re-encrypted votes or the verifier's response
                data = conn.recv(4096)
                response = pickle.loads(data) # the two votes mixed and the proof

                if response[0] == "mixer": # if mixer connected appends the re-encrypted votes (with the proof)
                    if last_time:
                        print("Mixing is over. Only verifying!")
                        continue
                    else:
                        print(f"Mixer {len(mixes)} connected")
                        mixes.append(response[1])

                if response[0] == "very" and not response[1]: # if verifier
                    print(f"Verifier connected")
                    if not response[1]: # At least one mixer cheated
                        print("Beware a mixer cheated!!!")
                        # An option to remove all faulty re-encrypted votes from mixes
                        if input("Want to overrule him? (y for yes, n for no) ") == "y":
                            tmp = []
                            for i in range(response[2]):
                                tmp.append(mixes[i])
                            mixes = tmp
                            if len(mixes) <= MAX_MIXES:
                                last_time = False
            # if MAX_MIXES reached ask whether to verify more or not
            if len(mixes) >= MAX_MIXES + 1:
                if input("Voting finished. Want to verify one last time? (y for yes, n for no)") == "n" or last_time:
                    # if not stop and send results to Admin
                    # else continues to accept another verifier
                    break
                else:
                    last_time = True

        votes = [mixes[-1][0], mixes[-1][1]] # the final re-encrypted votes
        admin_conn.sendall(pickle.dumps(votes))
except KeyboardInterrupt:
    print("\nVoting ended by user.")
