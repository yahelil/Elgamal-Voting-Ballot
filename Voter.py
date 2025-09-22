import socket
import pickle
from encryption import encrypt_vote
from Group import Group


HOST = 'localhost'
PORT = 65434

def add_mod_5(a, b):
    return (a + b) % 5

def name_shortcut(name):
    match name:
        case "si":  return "simon"
        case "e":   return "eden"
        case "g":   return "guy"
        case "sh":  return "shira"
        case "y":   return "yaheli"
    return name


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    """
        Establish a socket connection to a server.
        Receive public_key, elements. 
        Unpack the received data using pickle. 
        Create a group with the elements.
        Prompt the user to cast a vote. 
        Map the user input to the full names of the candidates. 
        Encrypt the vote using the group and public key.
        Send the encrypted vote to the server.
    """

    s.connect((HOST, PORT))

    # Receive public key
    data = s.recv(4096)
    public_key, elements = pickle.loads(data)
    group = Group(elements, add_mod_5) # creates the group

    # accepts a vote
    vote = input("Cast your vote (Simon, Eden, Guy, Shira, Yaheli): ").lower()
    name_shortcut(vote)
    while vote not in ["simon", "eden", "guy", "shira", "yaheli"]:
        print("Invalid vote. Must be Simon/Eden/Guy/Shira/Yaheli.")
        vote = input("Cast your vote (Simon, Eden, Guy, Shira, Yaheli): ").lower()
        name_shortcut(vote)

    num, encrypt_vote = encrypt_vote(vote, group, public_key)

    # Send encrypted vote
    s.sendall(pickle.dumps((num, encrypt_vote)))
    print("Vote sent.")
