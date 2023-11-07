import os
import http.server
import socketserver
import tkinter as tk
from tkinter import filedialog
import socket

class ServerUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Folder Server")

        self.folder_path = tk.StringVar(value=os.path.dirname(os.path.abspath(__file__)))

        tk.Label(master, text="Folder Path:").grid(row=0, column=0, sticky="e")
        tk.Entry(master, textvariable=self.folder_path, width=50).grid(row=0, column=1, columnspan=2)
        tk.Button(master, text="Browse", command=self.browse_folder).grid(row=0, column=3)

        tk.Button(master, text="Start Server", command=self.start_server).grid(row=1, column=1, columnspan=2)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)

    def start_server(self):
        folder_path = self.folder_path.get()

        if not os.path.exists(folder_path):
            tk.messagebox.showerror("Error", f"The specified folder '{folder_path}' does not exist.")
            return

        os.chdir(folder_path)

        port = find_available_port()

        ip_address = get_device_ip()

        handler = http.server.SimpleHTTPRequestHandler
        server_address = (ip_address, port)
        httpd = socketserver.TCPServer(server_address, handler)

        print(f"Serving on {ip_address}:{port}, and hosting the folder: {folder_path}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

def find_available_port(start_port=8000, max_attempts=100):
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) != 0:
                return port
    raise Exception("Could not find an available port.")

def get_device_ip():
    return socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    root = tk.Tk()
    server_ui = ServerUI(root)
    root.mainloop()
