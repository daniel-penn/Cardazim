import struct
from typing import Self

from crypt_image import CryptImage


class Card:
    def __init__(
        self,
        name: str,
        creator: str,
        image: CryptImage,
        riddle: str,
        solution: str | None,
    ):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str:
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self) -> str:
        return f"""Card {self.name} by {self.creator}
Riddle: {self.riddle}
Solution: {self.solution if self.solution else "unsolved"}"""

    @classmethod
    def create_from_path(
        cls, name: str, creator: str, path: str, riddle: str, solution: str | None
    ):
        return cls(name, creator, CryptImage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:
        name_bytes = struct.pack(
            "<I", len(self.name.encode("utf-8"))
        ) + self.name.encode("utf-8")
        creator_bytes = struct.pack(
            "<I", len(self.creator.encode("utf-8"))
        ) + self.creator.encode("utf-8")
        crypt_image_data = self.image.serialize()
        crypt_image_bytes = struct.pack("<I", len(crypt_image_data)) + crypt_image_data
        riddle_bytes = struct.pack(
            "<I", len(self.riddle.encode("utf-8"))
        ) + self.riddle.encode("utf-8")
        serialization = name_bytes + creator_bytes + crypt_image_bytes + riddle_bytes
        return serialization

    @classmethod
    def deserialize(cls, serialization: bytes) -> Self:
        offset = 0

        def read_next_bytes() -> bytes:
            nonlocal offset

            length = struct.unpack_from("<I", serialization, offset)[0]
            offset += 4

            data = serialization[offset : offset + length]
            offset += length

            return data

        name = read_next_bytes().decode("utf-8")
        creator = read_next_bytes().decode("utf-8")
        image = CryptImage.deserialize(read_next_bytes())
        riddle = read_next_bytes().decode("utf-8")

        return cls(
            name=name, creator=creator, image=image, riddle=riddle, solution=None
        )



