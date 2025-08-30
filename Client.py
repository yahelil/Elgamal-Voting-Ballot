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
    root = tk.Tk()
    root.title("Secure Voting Ballot")
    root.geometry("400x500")
    root.resizable(False, False)

    tk.Label(root, text="Cast Your Vote", font=("Helvetica", 16, "bold")).pack(pady=10)

    vote_var = tk.StringVar(value="")
    for name in CANDIDATES:
        tk.Radiobutton(root, text=name, variable=vote_var, value=name, font=("Helvetica", 12)).pack(anchor="w", padx=20)

    # Canvas for animation
    canvas = tk.Canvas(root, width=300, height=200, bg="white")
    canvas.pack(pady=10)

    # Draw ballot box
    box = canvas.create_rectangle(100, 150, 200, 180, fill="#444", outline="black")

    # Create ballot rectangle (hidden until vote)
    ballot = canvas.create_rectangle(120, 20, 180, 50, fill="#ddd", outline="black")
    canvas.itemconfigure(ballot, state='hidden')

    def animate_ballot():
        canvas.itemconfigure(ballot, state='normal')
        for _ in range(20):
            canvas.move(ballot, 0, 5)
            root.update()
            root.after(50)
        messagebox.showinfo("Vote Submitted", f"You voted for {vote_var.get()}.")
        root.destroy()

    def submit_vote():
        selected = vote_var.get()
        if selected == "":
            messagebox.showwarning("No Selection", "Please select a candidate before voting.")
        else:
            encrypted_vote, Key_E = encrypt_vote(selected.lower(), p, g, y)
            s.sendall(pickle.dumps((encrypted_vote, Key_E)))
            animate_ballot()

    tk.Button(root, text="Submit Vote", command=submit_vote, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)

    root.mainloop()