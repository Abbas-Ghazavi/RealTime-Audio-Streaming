import socket
import tkinter as tk
from tkinter import scrolledtext
import threading

HOST = '127.0.0.1'
PORT = 5000

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((HOST, PORT))

BUFFER_SIZE = 65536

root = tk.Tk()
root.title("UDP Server Output")

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(padx=10, pady=10)

def update_ui(message):
    output_text.insert(tk.END, message + '\n')
    output_text.yview(tk.END)

def receive_data():
    while True:
        try:
            data, addr = server_sock.recvfrom(BUFFER_SIZE)
            message = f"Received {len(data)} bytes from {addr}"
            print(message)
            update_ui(message)

        except Exception as e:
            error_message = f"Error: {e}"
            print(error_message)
            update_ui(error_message)

data_thread = threading.Thread(target=receive_data, daemon=True)
data_thread.start()

root.mainloop()
