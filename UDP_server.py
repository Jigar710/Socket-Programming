import socket
import os
import time

def send_file_contents(client_socket, filename, substring,client_address):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                if substring in line:
                    client_socket.sendto(line.encode(), client_address)
    except FileNotFoundError:
        client_socket.sendto("File not found".encode(), client_address)
    
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("0.0.0.0", 8888))

    print("UDP Server is ready to receive file requests...")

    while True:
        data, client_address = server.recvfrom(1024)
        data = data.decode()
        if not data:
            continue

        # Split the received data into filename and substring
        filename, substring = data.split(',')
        
        send_file_contents(server, filename, substring,client_address)

        # Monitor the file for changes and send new content
        while True:
            time.sleep(1)
            with open(filename, 'r') as file:
                lines = file.readlines()
                server.sendto("New content:\n".encode(), client_address)
                for line in lines:
                    if substring in line:
                        server.sendto(line.encode(), client_address)

if __name__ == "__main__":
    main()
