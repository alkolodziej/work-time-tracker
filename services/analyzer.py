### services/analyzer.py
from collections import defaultdict
import matplotlib.pyplot as plt
from functools import reduce

class Analyzer:
    """Analizuje dane o czasie pracy."""

    def analyze(self, entries):
        """Wyświetla statystyki i analizę czasu pracy."""
        if not entries:
            print("Brak danych do analizy.")
            return

        # reduce - suma godzin (programowanie funkcyjne)
        total = reduce(lambda acc, e: acc + e.duration(), entries, 0)
        avg = total / len(entries)
        print(f"\nStatystyki czasu pracy:")
        print(f" - Łączny czas pracy: {total:.2f}h")
        print(f" - Średni czas na wpis: {avg:.2f}h")

        # słownik miesięcy, krotki, zbiór miesięcy (przykład użycia kontenerów)
        monthly = defaultdict(float)
        for e in entries:
            monthly[e.date[:7]] += e.duration()
        months = set(monthly.keys())  # zbiór miesięcy

        print("\nCzas pracy wg miesięcy:")
        for month, hours in monthly.items():
            tup = (month, hours)  # krotka
            print(f" - {tup[0]}: {tup[1]:.2f}h")

    def plot(self, entries):
        """Generuje i zapisuje wykres czasu pracy."""
        if not entries:
            print("Brak danych do wykresu.")
            return

        # Słownik z sumą godzin dla każdej daty
        daily = defaultdict(float)
        for e in entries:
            daily[e.date] += e.duration()

        dates = sorted(daily.keys())
        hours = [daily[d] for d in dates]

        # Tworzenie wykresu słupkowego
        plt.figure(figsize=(10, 5))
        plt.bar(dates, hours, color='skyblue')
        plt.xlabel("Data")
        plt.ylabel("Godziny pracy")
        plt.title("Czas pracy dzienny")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("data/work_plot.png")
        plt.show()
        print("Wykres zapisano jako data/work_plot.png")