import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

# Move to the standard running dir.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from card import Card
from crypt_image import CryptImage
from listener import Listener

HOST = "127.0.0.1"
CLIENT_PATH = Path(__file__).resolve().parents[1] / "client.py"


def run_client_and_receive_card(card):
    with tempfile.NamedTemporaryFile(
        suffix=".png", dir=Path(__file__).parent
    ) as image_file:
        image_path = Path(image_file.name)

    try:
        card.image.image.save(image_path)

        with Listener(0, HOST) as listener:
            listener.start()
            port = listener.connection.getsockname()[1]

            result = subprocess.run(
                [
                    sys.executable,
                    str(CLIENT_PATH),
                    HOST,
                    str(port),
                    card.name,
                    card.creator,
                    str(image_path),
                    card.riddle,
                    card.solution or "",
                ],
                capture_output=True,
                text=True,
                timeout=2,
                check=True,
            )
            assert result.returncode == 0, result.stdout + result.stderr

            with listener.accept() as connection:
                return Card.deserialize(connection.receive_message())
    finally:
        image_path.unlink()


def assert_cards_match(sent, received):
    assert received.name == sent.name
    assert received.creator == sent.creator
    assert received.riddle == sent.riddle
    assert received.image.image.size == sent.image.image.size
    assert received.image.image.tobytes() == sent.image.image.tobytes()


def test_client_sends_card():
    card = Card(
        "CoolName",
        "Alice",
        CryptImage(Image.new("RGB", (2, 2), "orange")),
        "What is your name?",
        None,
    )

    assert_cards_match(card, run_client_and_receive_card(card))


def test_client_sends_card_with_unicode_and_varied_pixels():
    image = Image.new("RGB", (2, 1))
    image.putdata([(1, 2, 3), (250, 251, 252)])
    card = Card(
        "אחלה שפה בסך הכל ✨",
        "דניאל",
        CryptImage(image),
        "מה המסע שלך?",
        None,
    )

    assert_cards_match(card, run_client_and_receive_card(card))


def test_client_sends_card_with_larger_image():
    card = Card.create_from_path(
        "Large Image",
        "Bob",
        "./tests/bird.jpg",
        "What is the air-speed velocity of an unladen swallow?",
        "ThisDoesntGetSerializedAnyway",
    )

    assert_cards_match(card, run_client_and_receive_card(card))
