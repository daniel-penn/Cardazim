import socket
import struct


class Connection:
    def __init__(self, connection: socket.socket):
        self.connection = connection

    def __repr__(self) -> str:
        """
        Example:
        <Connection from 127.0.0.1:1234 to 127.0.0.1:8080>
        """
        own_ip, own_port = self.connection.getsockname()
        dest_ip, dest_port = self.connection.getpeername()
        return f"<{type(self).__name__} from {own_ip}:{own_port} to {dest_ip}:{dest_port}>"

    def send_message(self, data: bytes | str):
        if isinstance(data, str):
            data = data.encode("utf-8")
        data_length = struct.pack("<I", len(data))
        self.connection.sendall(data_length + data)

    
    def _receive_exactly(self, byte_count: int) -> bytes:
        chunks = []
        bytes_received = 0

        while bytes_received < byte_count:
            chunk = self.connection.recv(byte_count - bytes_received)
            if not chunk:
                raise ConnectionError(
                    "Connection closed before the complete message was received"
                )
            chunks.append(chunk)
            bytes_received += len(chunk)

        return b"".join(chunks)

    def receive_message(self) -> bytes:
        """Receive and return one message."""
        message_length = struct.unpack("<I", self._receive_exactly(4))[0]
        return self._receive_exactly(message_length)

    @classmethod
    def connect(cls, host, port):
        new_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_connection.connect((host,port))
        return cls(new_connection)

    def close(self):
        self.connection.close()

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.close()
