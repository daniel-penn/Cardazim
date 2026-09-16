import json
from pathlib import Path

from card import Card


class CardManager:
    def save(self, card: Card, dir_path=".") -> None:
        save_path = Path(f"{dir_path}/{self.get_identifier(card)}")
        save_path.mkdir(parents=True, exist_ok=True)
        card_info = {
            "name": card.name,
            "creator": card.creator,
            "riddle": card.riddle,
            "solution": card.solution,
            "image_path": f"{save_path!s}/card_image.jpg",
        }
        with open(f"{save_path!s}/metadata.json", "w", encoding="utf-8") as json_file:
            json.dump(card_info, json_file, indent=4)
        card.image.save_image(f"{save_path!s}/card_image.jpg")

    def get_identifier(self, card: Card) -> str:
        return f"{card.name}--{card.creator}"

    def load(self, identifier: str, database_path: str) -> Card:
        card_folder_path = Path(f"{database_path}/{identifier}")
        if not card_folder_path.exists():
            raise ValueError("Card not found")
        with open("metadata.json", "r") as file:
            card_data = json.load(file)
        return Card.create_from_path(
            name=card_data["name"],
            creator=card_data["creator"],
            path=card_data["image_path"],
            riddle=card_data["riddle"],
            solution=card_data.get("solution",None)
        )
