import socket
import threading
import tkinter as tk
import time

# Constants
DEFAULT_IP = '127.0.0.1'
DEFAULT_SENDER_PORT = 12345
DEFAULT_RECEIVER_PORT = 54321
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("P2P Chat Setup")
        self.create_widgets()  # Create GUI elements

    def create_widgets(self):
        # Label and Entry for IP Address
        self.ip_label = tk.Label(self.root, text="Enter IP Address:")
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack(pady=5)
        self.ip_entry.insert(0, DEFAULT_IP)  # Set default IP

        # Label and Entry for Sender Port
        self.sender_port_label = tk.Label(self.root, text="Enter Sender Port:")
        self.sender_port_label.pack(pady=5)
        self.sender_port_entry = tk.Entry(self.root)
        self.sender_port_entry.pack(pady=5)
        self.sender_port_entry.insert(0, str(DEFAULT_SENDER_PORT))  # Set default sender port

        # Label and Entry for Receiver Port
        self.receiver_port_label = tk.Label(self.root, text="Enter Receiver Port:")
        self.receiver_port_label.pack(pady=5)
        self.receiver_port_entry = tk.Entry(self.root)
        self.receiver_port_entry.pack(pady=5)
        self.receiver_port_entry.insert(0, str(DEFAULT_RECEIVER_PORT))  # Set default receiver port

        # Button to start the chat with user-specified settings
        self.start_button = tk.Button(self.root, text="Start Chat", command=self.start_chat)
        self.start_button.pack(pady=10)

    def start_chat(self):
        ip = self.ip_entry.get()
        sender_port = int(self.sender_port_entry.get())
        receiver_port = int(self.receiver_port_entry.get())
        self.root.destroy()  # Close the setup GUI

        # Function to receive messages
        def receive_messages():
            connection, address = receiver_socket.accept()
            print(f"Connected to {address}")

            while True:
                received_message = connection.recv(1024).decode('utf-8')
                if not received_message:
                    break
                message_listbox.insert(tk.END, f"Received message: {received_message}")

        # Create a socket for receiving messages
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver_socket.bind((ip, receiver_port))
        receiver_socket.listen(1)

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.start()

        # Create a socket for sending messages
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        max_attempts = 6  # Number of connection attempts, this should give it 30 seconds
        for attempt in range(max_attempts):
            try:
                # Connect the sender to the receiver
                sender_socket.connect((ip, sender_port))
                break  # If connection is successful, exit the loop
            except ConnectionRefusedError:
                if attempt == max_attempts - 1:
                    print("Connection Refused after multiple attempts.")
                    return
                else:
                    print(f"Connection Refused. Retrying in 5 seconds... (Attempt {attempt + 1}/{max_attempts})")
                    time.sleep(5)  # Wait for 5 seconds before retrying


        # Create the Tkinter GUI for the chat
        chat_root = tk.Tk()
        chat_root.title("P2P Chat")

        message_listbox = tk.Listbox(chat_root, height=15, width=50)
        message_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        message_entry = tk.Entry(chat_root, width=40)
        message_entry.pack(pady=10, fill=tk.BOTH, expand=True)

        def send_message():
            message = message_entry.get()
            sender_socket.send(message.encode('utf-8'))
            message_listbox.insert(tk.END, f"Sent message: {message}")
            message_entry.delete(0, tk.END)

        send_button = tk.Button(chat_root, text="Send", command=send_message, width=10)
        send_button.pack()

        chat_root.mainloop()  # Start the chat GUI

        # Close the sockets
        sender_socket.close()
        receiver_socket.close()

def main():
    root = tk.Tk()
    app = ChatApp(root)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.mainloop()

if __name__ == "__main__":
    main()
