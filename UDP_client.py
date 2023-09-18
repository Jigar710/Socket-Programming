import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ("127.0.0.1", 8888)

    filename = input("Enter the filename you want to read: ")
    substring = input("Enter the substring you want to filter (Press Enter to read all lines): ")

    data = f"{filename},{substring}"
    client.sendto(data.encode(), server_address)

    while True:
        data, _ = client.recvfrom(1024)
        print(data.decode())

    client.close()

if __name__ == "__main__":
    main()
