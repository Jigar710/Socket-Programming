import socket
import threading
import sqlite3
import time

# Database initialization and setup
def initialize_database():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                      (group_id TEXT, user_id TEXT, message TEXT, timestamp REAL)''')
    conn.commit()
    conn.close()

# Function to store a message in the database
def store_message(group_id, user_id, message):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    timestamp = time.time()
    cursor.execute("INSERT INTO messages VALUES (?, ?, ?, ?)", (group_id, user_id, message, timestamp))
    conn.commit()
    conn.close()

# Function to retrieve messages from the database for a specific group within the last 15 minutes
def retrieve_messages(group_id):
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    fifteen_minutes_ago = time.time() - (15 * 60)
    cursor.execute("SELECT user_id, message, timestamp FROM messages WHERE group_id=? AND timestamp > ?", (group_id, fifteen_minutes_ago))
    messages = cursor.fetchall()
    conn.close()
    return messages

# Function to handle client connections
def handle_client(client_socket, groups,user_id,group_id):
    try:
        # user_id = client_socket.recv(1024).decode()
        # group_id = client_socket.recv(1024).decode()
        print(user_id,group_id)

        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break

            # Store the message in the database
            store_message(group_id, user_id, message)

            # Relay the message to all clients in the same group
            for client in groups[group_id]:
                if client != client_socket:
                    client.send(f"{user_id}: {message}\n".encode())

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        if client_socket in groups[group_id]:
            groups[group_id].remove(client_socket)
            print(f"{user_id} has left group {group_id}")
            client_socket.close()

# Function to create or join a group
def join_group(client_socket, groups):
    user_id = client_socket.recv(1024).decode()
    group_id = client_socket.recv(1024).decode()
    
    if group_id not in groups:
        groups[group_id] = []
    
    groups[group_id].append(client_socket)
    print(f"{user_id} has joined group {group_id}")

    # Send chat history to the new client
    chat_history = retrieve_messages(group_id)
    print("###",chat_history)
    if(len(chat_history)>0):
        for message_data in chat_history:
            user, message, _ = message_data
            client_socket.send(f"{user}: {message}\n".encode())
    client_socket.send("Welcome to the chat!\n".encode())
    return user_id,group_id

def main():
    initialize_database()
    9
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8888))
    server.listen(5)
    
    print("Chat server is running...")
    
    groups = {}  # Dictionary to store groups and their members
    
    while True:
        client_socket, addr = server.accept()
        print("Accepted connection from", addr)
        
        # Ask the client to join a group or create a new one
        user_id,group_id = join_group(client_socket, groups)
        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, groups,user_id,group_id))
        client_handler.start()

if __name__ == "__main__":
    main()
