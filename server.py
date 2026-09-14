import argparse
import threading

from listener import Listener


def run_server(ip, port):
    """
    Blocking process that listens to a port and IP and prints all data received.
    """
    lock = threading.Lock()

    def handle_connection(connection):
        """
        Handle a single given connection. Currently prints data.
        """
        with connection:
            payload = connection.receive_message()
            with lock:
                print(f"Received data: {payload.decode('utf-8')}")

    with Listener(port, ip) as listener:
        listener.start()

        while True:
            connection = listener.accept()
            threading.Thread(
                target=handle_connection, args=(connection,), daemon=True
            ).start()


def get_args():
    parser = argparse.ArgumentParser(description="Launch a server.")

    parser.add_argument("server_ip", type=str, help="the server's listening ip")
    parser.add_argument("server_port", type=int, help="the server's listening port")
    return parser.parse_args()


def main():
    args = get_args()
    run_server(args.server_ip, args.server_port)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
