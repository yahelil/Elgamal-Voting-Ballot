import socket
import pickle
from GUI import launch_gui

HOST = 'localhost'
PORT = 65433

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    p, g, b = pickle.loads(data)

    launch_gui(s, p, g, b)
