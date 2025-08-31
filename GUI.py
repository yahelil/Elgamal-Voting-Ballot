import tkinter as tk
from tkinter import messagebox
from encryption import encrypt_vote
import pickle

CANDIDATES = ["Simon", "Eden", "Guy", "Shira", "Yaheli"]

def launch_gui(sock, p, g, b):
    root = tk.Tk()
    root.title("Secure Voting Ballot")
    root.geometry("400x500")
    root.resizable(False, False)

    tk.Label(root, text="Cast Your Vote", font=("Helvetica", 16, "bold")).pack(pady=10)

    vote_var = tk.StringVar(value="")
    for name in CANDIDATES:
        tk.Radiobutton(root, text=name, variable=vote_var, value=name, font=("Helvetica", 12)).pack(anchor="w", padx=20)

    canvas = tk.Canvas(root, width=300, height=200, bg="white")
    canvas.pack(pady=10)
    box = canvas.create_rectangle(100, 150, 200, 180, fill="#444", outline="black")
    ballot = canvas.create_rectangle(120, 20, 180, 50, fill="#ddd", outline="black")
    canvas.itemconfigure(ballot, state='hidden')

    def animate_ballot(vote):
        canvas.itemconfigure(ballot, state='normal')
        stamp = canvas.create_oval(140, 30, 160, 50, fill="red", outline="")
        stamp_text = canvas.create_text(150, 40, text=vote, fill="white", font=("Helvetica", 10, "bold"))
        root.update()
        root.after(200)
        for scale in [1.2, 1.4, 1.2, 1.0]:
            canvas.scale(stamp, 150, 40, scale, scale)
            canvas.scale(stamp_text, 150, 40, scale, scale)
            root.update()
            root.after(100)
        for _ in range(20):
            canvas.move(ballot, 0, 5)
            canvas.move(stamp, 0, 5)
            canvas.move(stamp_text, 0, 5)
            root.update()
            root.after(50)
        messagebox.showinfo("Vote Submitted", f"You voted for {vote_var.get()}.")
        root.destroy()

    def submit_vote():
        selected = vote_var.get()
        if selected == "":
            messagebox.showwarning("No Selection", "Please select a candidate before voting.")
        else:
            encrypted_vote, Key_E = encrypt_vote(selected.lower(), p, g, b)
            sock.sendall(pickle.dumps((encrypted_vote, Key_E)))
            animate_ballot(selected)

    tk.Button(root, text="Submit Vote", command=submit_vote, font=("Helvetica", 12), bg="#4CAF50", fg="white").pack(pady=10)
    root.mainloop()