# services/data_manager.py
import json
import os
from models.entry import WorkEntry


class DataManager:
    """Zarządza zapisem i odczytem wpisów czasu pracy."""

    def __init__(self, filepath):
        # Konstruktor klasy DataManager
        self.filepath = filepath
        self.entries = self.load()

    def load(self):
        """Wczytuje dane z pliku."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)
                # Tworzenie listy obiektów WorkEntry
                # na podstawie danych z pliku
                return [WorkEntry.from_dict(e) for e in data]
        except Exception as e:
            print(f"Błąd wczytywania danych: {e}")
            return []

    def save(self):
        """Zapisuje dane do pliku."""
        try:
            with open(self.filepath, "w") as f:
                # Zapis listy wpisów jako listy słowników
                json.dump([e.to_dict() for e in self.entries], f, indent=4)
        except Exception as e:
            print(f"Błąd zapisu danych: {e}")
