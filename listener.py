import socket

from connection import Connection


class Listener:
    def __init__(self, port, host, backlog=1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.settimeout(1.0)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(port={self.port}, host={self.host}, backlog={self.backlog})"

    def start(self):
        self.connection.bind((self.host, self.port))
        self.connection.listen(self.backlog)

    def stop(self):
        self.connection.close()

    def accept(self):
        while True:
            try:
                connection, _ = self.connection.accept()
            except TimeoutError:
                continue  # Allow escape (eg keyboardinterrupt)
            return Connection(connection)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()
