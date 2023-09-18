import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except ConnectionError:
            print("Connection to the server is closed.")
            break

def send_messages(client_socket):
    while True:
        message = input("=>")
        client_socket.send(message.encode())
        if message.lower() == "exit":
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8888))

    # User input for user ID and group ID
    user_id = input("Enter your user ID: ")
    group_id = input("Enter the group ID you want to join: ")

    # Send user ID and group ID to the server
    client.send(user_id.encode())
    client.send(group_id.encode())

    # Receive and print the welcome message from the server
    welcome_message = client.recv(1024).decode()
    print(welcome_message)

    # Create separate threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    send_thread = threading.Thread(target=send_messages, args=(client,))

    # Start the threads
    receive_thread.start()
    send_thread.start()

    # Wait for both threads to finish
    receive_thread.join()
    send_thread.join()

    client.close()

if __name__ == "__main__":
    main()

