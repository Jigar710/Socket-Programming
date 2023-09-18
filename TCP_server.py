import socket
import threading
import time

class KeyValueStore:
    def __init__(self):
        self.data = {}
        self.ttl = {}

    def put(self, key, value, ttl=0):
        self.data[key] = value
        if ttl > 0:
            self.ttl[key] = time.time() + ttl

    def get(self, key):
        if key in self.data:
            if key in self.ttl and self.ttl[key] < time.time():
                del self.data[key]
                return None
            return self.data[key]
        else:
            return None

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            if key in self.ttl:
                del self.ttl[key]

def handle_client(client_socket, kv_store):
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            break

        parts = request.split()
        if len(parts) < 2:
            response = "Invalid request."
        else:
            command = parts[0]
            key = parts[1]

            if command == "GET":
                value = kv_store.get(key)
                if value is not None:
                    response = f"Value for {key}: {value}"
                else:
                    response = f"Key not found: {key}"

            elif command == "PUT":
                if len(parts) < 3:
                    response = "Invalid PUT request."
                else:
                    value = parts[2]
                    ttl = 0
                    if len(parts) >= 4:
                        ttl = int(parts[3])
                    kv_store.put(key, value, ttl)
                    response = f"Stored {key}: {value}"

            elif command == "DELETE":
                kv_store.delete(key)
                response = f"Deleted key: {key}"

            else:
                response = "Invalid command."

        client_socket.send(response.encode())

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 8888))
    server.listen(5)

    kv_store = KeyValueStore()

    while True:
        client_socket, addr = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, kv_store))
        client_handler.start()

if __name__ == "__main__":
    main()
