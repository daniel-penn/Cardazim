import argparse
import sys

from connection import Connection


def send_data(server_ip, server_port, data: bytes):
    """
    Send data to server in address (server_ip, server_port).
    """
    with Connection.connect(server_ip, server_port) as connection:
        connection.send_message(data)


def get_args():
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print("Done.")
    except Exception as error:  # noqa: BLE001
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
