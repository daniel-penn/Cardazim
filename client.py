import argparse
import sys

from card import Card
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
    parser.add_argument("name", type=str, help="the card name")
    parser.add_argument("creator", type=str, help="the card creator")
    parser.add_argument("path", type=str, help="the card image path")
    parser.add_argument("riddle", type=str, help="the card riddle")
    parser.add_argument("solution", type=str, help="the card riddle solution")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        card = Card.create_from_path(args.name, args.creator, args.path, args.riddle, args.solution)
        card_data = card.serialize()
        send_data(args.server_ip, args.server_port, card_data)
        print("Done.")
    except Exception as error:  # noqa: BLE001
        print(f"ERROR: {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
