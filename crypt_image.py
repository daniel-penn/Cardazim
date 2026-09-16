from __future__ import annotations

import hashlib
import struct

from Crypto.Cipher import AES
from PIL import Image


class CryptImage:
    """
    Class that stores an encryptable image.
    Attributes:
        image: Encrypted or unencrypted PIL.Image.Image.
        key_hash: Hash of the aes key used to encrypt the image or None if it isn't encrypted.
    """
    DEFAULT_NONCE = b"arazim"

    def __init__(self, image: Image.Image, key_hash: bytes | None = None):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: str) -> CryptImage:
        return cls(Image.open(path))

    def encrypt(self, key_string: str):
        """
        Encrypt the image under a key derived from key_string.
        Sets self.key_hash to a hash of said derived key.
        """
        aes_key = hashlib.sha256(key_string.encode("utf-8")).digest()
        self.key_hash = hashlib.sha256(aes_key).digest()
        image_bytes = self.image.tobytes()

        cipher = AES.new(aes_key, AES.MODE_EAX, nonce=self.DEFAULT_NONCE)
        encrypted_image_bytes = cipher.encrypt(image_bytes)
        encrypted_image = Image.frombytes("RGB", self.image.size, encrypted_image_bytes)
        self.image = encrypted_image

    def decrypt(self, key_string: str):
        """
        Attempt to decrypt the image by deriving a key from key_string.
        Hashes key against key_hash to test for correctness. Only decrypts if hashes match.
        Returns True on success and False otherwise.
        """
        guessed_aes_key = hashlib.sha256(key_string.encode("utf-8")).digest()
        guessed_key_hash = hashlib.sha256(guessed_aes_key).digest()
        if guessed_key_hash != self.key_hash:
            # Guessed key is incorrect. Exit.
            return False

        # Guessed key is correct. Decrypt.
        encrypted_image_bytes = self.image.tobytes()
        cipher = AES.new(guessed_aes_key, AES.MODE_EAX, nonce=self.DEFAULT_NONCE)
        decrypted_image_bytes = cipher.decrypt(encrypted_image_bytes)
        decrypted_image = Image.frombytes("RGB", self.image.size, decrypted_image_bytes)
        self.image = decrypted_image

    def serialize(self) -> bytes:
        """
        Serialize the CryptImage into bytes via the following protocol:
        [height: int32][width: int32][image_bytes: height*width*3][key_hash]
        """
        height_bytes = struct.pack("<I", self.image.size[1])
        width_bytes = struct.pack("<I", self.image.size[0])
        image_bytes = self.image.tobytes()

        serialization = height_bytes + width_bytes + image_bytes
        if self.key_hash:
            serialization += self.key_hash
        return serialization

    @classmethod
    def deserialize(cls, serialization: bytes) -> CryptImage:
        """
        Alt init method to deserialize a CryptImage from serialized bytes.
        """

        height, width = struct.unpack_from("<II", serialization)
        image_length = width * height * 3
        image_end = 8 + image_length

        image = Image.frombytes("RGB", (width, height), serialization[8:image_end])
        key_hash = serialization[image_end:] or None
        return cls(image, key_hash)

    def _show(self):
        self.image.show()
