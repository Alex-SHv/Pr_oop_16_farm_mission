import json
from pathlib import Path


class Resources:
    def __init__(self, filename="resources/resources.json"):
        self.file_path = Path(filename)
        self.data = {}

        if not self.file_path.exists():
            self._create_default()

        self.load()

    def _create_default(self):
        self.data = {}
        with self.file_path.open("w", encoding="utf-8") as f:
             json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load(self):
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                self.data = json.load(f)
            if not isinstance(self.data, dict):
                raise ValueError("Очікувався словник у файлі")
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(f"Помилка читання або валідації: {e}")

    @property
    def start_money(self):
        return self.data["game"]["start_money"]

    @property
    def beds_count(self):
        return self.data["game"]["beds_count"]

    @property
    def plants(self):
        return self.data["plants"]

    @property
    def fertilizers(self):
        return self.data["fertilizers"]

    @property
    def images_path(self):
        return self.data["images"]["base_path"]
        


