import argparse
import socket


def run_server(ip, port):
    """
    Blocking process that listens to a port and IP and prints all data received.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((ip, port))
        sock.listen()
        sock.settimeout(1)

        while True:
            try:
                connection, _ = sock.accept()
            except socket.timeout:
                continue  # Loop, allowing keyboard interrupts to register.
            chunks = []
            while True:
                data = connection.recv(4096)
                if not data:
                    break
                chunks.append(data)
            received_data = b"".join(chunks)
            print(f"Received data: {received_data.decode('utf-8')}")
            connection.close()


def get_args():
    parser = argparse.ArgumentParser(description="Launch a server.")
    
    parser.add_argument("server_ip", type=str,
                         help="the server's listening ip")
    parser.add_argument("server_port", type=int,
                         help="the server's listening port")
    return parser.parse_args()


def main():
    args = get_args()
    run_server(args.server_ip, args.server_port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass