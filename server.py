import socket


def run_server(ip, port):
    """
    Blocking process that listens to a port and IP and prints all data received.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((ip, port))
        while True:
            sock.listen()
            connection, _ = sock.accept()
            chunks = []
            while True:
                data = connection.recv(4096)
                if not data:
                    break
                chunks.append(data)
            received_data = b"".join(chunks)
            print(f"Received data: {received_data.decode('utf-8')}")
            connection.close()

if __name__ == '__main__':
    run_server('0.0.0.0',8080)