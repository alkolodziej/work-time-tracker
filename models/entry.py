# models/entry.py
from datetime import datetime


class WorkEntry:
    """Reprezentuje pojedynczy wpis czasu pracy."""

    def __init__(self, date, start, end):
        # Konstruktor klasy WorkEntry
        self.date = date
        self.start = start
        self.end = end

    def duration(self):
        """Zwraca liczbę godzin między start a end."""
        try:
            fmt = "%H:%M"
            tdelta = datetime.strptime(
                self.end, fmt) - datetime.strptime(self.start, fmt)
            return tdelta.total_seconds() / 3600
        except Exception as e:
            print(f"Błąd w obliczaniu czasu: {e}")
            return 0

    def to_dict(self):
        """Konwertuje wpis do słownika."""
        return {"date": self.date, "start": self.start, "end": self.end}

    @staticmethod
    def from_dict(d):
        """Tworzy wpis na podstawie słownika."""
        return WorkEntry(d["date"], d["start"], d["end"])

    def __str__(self):
        # Formatowanie stringa (przykład operacji na stringach)
        return (f"{self.date}: "
                f"{self.start} - "
                f"{self.end} "
                f"({self.duration():.2f}h)")


class ProjectWorkEntry(WorkEntry):
    """Wpis czasu pracy z informacją o
    projekcie (dziedziczenie po WorkEntry)."""

    def __init__(self, date, start, end, project):
        # Konstruktor klasy dziedziczącej
        super().__init__(date, start, end)
        self.project = project

    def to_dict(self):
        # Rozszerzenie metody bazowej
        d = super().to_dict()
        d["project"] = self.project
        return d

    @staticmethod
    def from_dict(d):
        # Tworzenie obiektu z dodatkowym polem
        return ProjectWorkEntry(d["date"], d["start"],
                                d["end"], d.get("project", ""))

    def __str__(self):
        # Formatowanie stringa z informacją o projekcie
        return (f"{self.date}: {self.start} - "
                f"{self.end} ({self.duration():.2f}h) "
                f"[Projekt: {self.project}]")
