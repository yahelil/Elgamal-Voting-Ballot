import tkinter as tk
from tkinter import messagebox
import socket
import pickle
from encryption import encrypt_vote

# Candidate list
CANDIDATES = ["Simon", "Eden", "Guy", "Shira", "Yaheli"]

# Server connection info (connects to MITM proxy)
HOST = 'localhost'
PORT = 65434

# Connect to server and get public key
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    p, g, y = pickle.loads(data)

    # GUI setup
    def submit_vote():
        selected = vote_var.get()
        if selected == "":
            messagebox.showwarning("No Selection", "Please select a candidate before voting.")
        else:
            encrypted_vote, Key_E = encrypt_vote(selected.lower(), p, g, y)
            s.sendall(pickle.dumps((encrypted_vote, Key_E)))
            messagebox.showinfo("Vote Submitted", f"You voted for {selected}.")
            root.destroy()

    root = tk.Tk()
    root.title("Secure Voting Ballot")
    root.geometry("300x300")
    root.resizable(False, False)

    tk.Label(root, text="Cast Your Vote", font=("Helvetica", 16, "bold")).pack(pady=10)

    vote_var = tk.StringVar(value="")
    for name in CANDIDATES:
        tk.Radiobutton(root, text=name, variable=vote_var, value=name, font=("Helvetica", 12)).pack(anchor="w", padx=20)

    tk.Button(root, text="Submit Vote", command=submit_vote, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=20)

    root.mainloop()