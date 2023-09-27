#This code has not yet been tested
#It's meant to be an update to the other file

import socket
import threading
import time
import miniupnpc

# Constants
DEFAULT_SENDER_PORT = 12345
DEFAULT_RECEIVER_PORT = 54321

def open_port(upnp, port):
    upnp.discoverdelay = 10
    upnp.discover()
    upnp.selectigd()
    upnp.addportmapping(port, 'TCP', socket.gethostbyname(socket.gethostname()), port, 'Chat Port', '')

def receive_messages(receiver_socket):
    connection, address = receiver_socket.accept()
    print(f"Connected to {address}")

    while True:
        received_message = connection.recv(1024).decode('utf-8')
        if not received_message:
            break
        print(f"Received message: {received_message}")

def main():
    sender_port = DEFAULT_SENDER_PORT
    receiver_port = DEFAULT_RECEIVER_PORT

    # Configure UPnP for port forwarding
    upnp = miniupnpc.UPnP()
    open_port(upnp, sender_port)
    open_port(upnp, receiver_port)

    # Get the public IP address
    public_ip = upnp.externalipaddress()

    # Create a socket for receiving messages
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_socket.bind((public_ip, receiver_port))
    receiver_socket.listen(1)

    # Start a thread to receive messages
    receive_thread = threading.Thread(target=receive_messages, args=(receiver_socket,))
    receive_thread.start()

    # Create a socket for sending messages
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remote_ip = input("Enter the remote public IP address: ")

    max_attempts = 6
    for attempt in range(max_attempts):
        try:
            # Connect the sender to the receiver
            sender_socket.connect((remote_ip, sender_port))
            break
        except ConnectionRefusedError:
            if attempt == max_attempts - 1:
                print("Connection Refused after multiple attempts.")
                return
            else:
                print(f"Connection Refused. Retrying in 5 seconds... (Attempt {attempt + 1}/{max_attempts})")
                time.sleep(5)

    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        sender_socket.send(message.encode('utf-8'))

    # Close the sockets
    sender_socket.close()
    receiver_socket.close()

if __name__ == "__main__":
    main()
