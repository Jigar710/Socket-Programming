import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 8888))

    while True:
        request = input("Enter a command (e.g., GET key, PUT key value, DELETE key): ")
        client.send(request.encode())
        response = client.recv(1024).decode()
        print("Server response:", response)

if __name__ == "__main__":
    main()
