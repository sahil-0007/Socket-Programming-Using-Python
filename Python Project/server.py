import tkinter as tk
from tkinter import filedialog
import socket
import os
import subprocess
import sys

# Server Function
def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = server_ip_entry.get()
    server_port = int(server_port_entry.get())
    conn = None

    try:
        sock.bind((server_ip, server_port))
        sock.listen(1)
        print("Server started. Waiting for a connection...")

        while True:
            conn, addr = sock.accept()
            print("Connected to:", addr)

            try:
                # Receive the file name from the client as a byte string
                file_name = conn.recv(1024)
                file_name = file_name.decode('latin-1')  # Decode the file name to str
                print("Receiving file:", file_name)

                with open(file_name, 'wb') as file:
                    try:
                        data = conn.recv(1024)
                        while data:
                            file.write(data)
                            data = conn.recv(1024)
                    except socket.error as e:
                        print("Socket error:", e)
                        break

                print("File received successfully:", file_name)

                if os.name == 'nt':
                    os.startfile(file_name)  # Open the file using the default application
                elif os.name == 'posix':
                    opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
                    subprocess.call([opener, file_name])  # Open the file using the default application

            except socket.error as e:
                print("Socket error:", e)
                break

    except socket.error as e:
        print("Socket error:", e)

    finally:
        if conn:
            conn.close()
        sock.close()

# Create the main window
window = tk.Tk()
window.title("Server Application")

# Server UI elements
server_label = tk.Label(window, text="Server", font=("Arial", 24))
server_label.pack(pady=20)

server_ip_label = tk.Label(window, text="Server IP:", font=("Arial", 16))
server_ip_label.pack()
server_ip_entry = tk.Entry(window, font=("Arial", 16))
server_ip_entry.pack()

server_port_label = tk.Label(window, text="Server Port:", font=("Arial", 16))
server_port_label.pack()
server_port_entry = tk.Entry(window, font=("Arial", 16))
server_port_entry.pack()

start_button = tk.Button(window, text="Start Server", command=start_server, font=("Arial", 16))
start_button.pack(pady=20)

# Start the main loop
window.mainloop()
