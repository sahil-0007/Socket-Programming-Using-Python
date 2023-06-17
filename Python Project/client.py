import tkinter as tk
from tkinter import filedialog
import socket
import os

# Client Function
def send_files():
    file_paths = filedialog.askopenfilenames()
    server_ip = server_ip_entry.get()
    server_port = int(server_port_entry.get())

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            sock.connect((server_ip, server_port))
            sock.sendall(file_name.encode())

            with open(file_path, 'rb') as file:
                data = file.read(1024)
                while data:
                    sock.sendall(data)
                    data = file.read(1024)

            print("File sent successfully:", file_name)

        except socket.error as e:
            print("Socket error:", e)

        finally:
            sock.close()

# Create the main window
window = tk.Tk()
window.title("Client Application")

# Client UI elements
client_label = tk.Label(window, text="Client", font=("Arial", 24))
client_label.pack(pady=20)

server_ip_label = tk.Label(window, text="Server IP:", font=("Arial", 16))
server_ip_label.pack()
server_ip_entry = tk.Entry(window, font=("Arial", 16))
server_ip_entry.pack()

server_port_label = tk.Label(window, text="Server Port:", font=("Arial", 16))
server_port_label.pack()
server_port_entry = tk.Entry(window, font=("Arial", 16))
server_port_entry.pack()

send_button = tk.Button(window, text="Select Files", command=send_files, font=("Arial", 16))
send_button.pack(pady=20)

# Start the main loop
window.mainloop()
