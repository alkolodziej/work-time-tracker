# main.py
from services.data_manager import DataManager
from services.analyzer import Analyzer
from models.entry import WorkEntry
from utils.validators import validate_date, validate_time, log_operation
import csv
import sys

# Zmienna globalna (przykład użycia zmiennej globalnej)
GLOBAL_USER = "admin"


def print_header():
    """Wyświetla nagłówek aplikacji w atrakcyjny sposób."""
    print("\n" + "=" * 50)
    print("      SYSTEM REJESTRACJI CZASU PRACY".center(50))
    print("=" * 50)


def print_menu():
    """Wyświetla menu główne."""
    menu = [
        "1. Dodaj wpis",
        "2. Wyświetl wszystkie wpisy",
        "3. Edytuj wpis",
        "4. Szukaj wpisu po dacie",
        "5. Analizuj czas pracy",
        "6. Zapisz dane",
        "7. Wygeneruj wykres",
        "8. Usuń wpis",
        "9. Pokaż sumę godzin (rekurencyjnie)",
        "10. Filtruj wpisy (funkcja wyższego rzędu)",
        "11. Operacje na stringach (dzielenie, wyszukiwanie)",
        "12. Eksport do CSV",
        "13. Import z CSV",
        "0. Wyjście"
    ]
    for item in menu:
        print(f" {item}")


@log_operation
def add_entry(data_manager):
    """Dodaje nowy wpis czasu pracy z walidacją i atrakcyjnym komunikatem."""
    print("\n--- Dodawanie nowego wpisu ---")
    date = input("Podaj datę (YYYY-MM-DD): ").strip()
    assert len(date) == 10, "Data powinna mieć 10 znaków (YYYY-MM-DD)"
    if not validate_date(date):
        print("❌ Niepoprawna data!")
        return
    start = input("Godzina rozpoczęcia (HH:MM): ").strip()
    if not validate_time(start):
        print("❌ Niepoprawny format godziny rozpoczęcia!")
        return
    end = input("Godzina zakończenia (HH:MM): ").strip()
    if not validate_time(end):
        print("❌ Niepoprawny format godziny zakończenia!")
        return
    entry = WorkEntry(date, start, end)
    data_manager.entries.append(entry)
    print("✅ Dodano wpis.")


def recursive_sum(entries, idx=0):
    """Rekurencyjnie sumuje czas pracy ze wszystkich wpisów."""
    if idx >= len(entries):
        return 0
    return entries[idx].duration() + recursive_sum(entries, idx + 1)


def filter_entries(entries, predicate):
    """Zwraca listę wpisów spełniających
    warunek predicate (funkcja jako argument)."""
    return [e for e in entries if predicate(e)]


@log_operation
def remove_entry(data_manager):
    """Usuwa wpis czasu pracy na podstawie numeru."""
    if not data_manager.entries:
        print("Brak wpisów do usunięcia.")
        return
    print("\n--- Usuń wpis ---")
    for i, e in enumerate(data_manager.entries):
        print(f"{i + 1}. {e}")
    try:
        index = int(input("Podaj numer wpisu do usunięcia: ")) - 1
        if 0 <= index < len(data_manager.entries):
            removed = data_manager.entries.pop(index)
            print(f"✅ Usunięto wpis: {removed}")
        else:
            print("❌ Niepoprawny indeks.")
    except Exception as e:
        print(f"Błąd usuwania: {e}")


@log_operation
def edit_entry(data_manager):
    """Edycja wybranego wpisu czasu pracy."""
    if not data_manager.entries:
        print("Brak wpisów do edycji.")
        return
    print("\n--- Edycja wpisu ---")
    for i, e in enumerate(data_manager.entries):
        print(f"{i + 1}. {e}")
    try:
        index = int(input("Podaj numer wpisu do edycji: ")) - 1
        if 0 <= index < len(data_manager.entries):
            entry = data_manager.entries[index]
            print(f"Edytujesz: {entry}")
            new_start = input("Nowa godzina rozpoczęcia (HH:MM): ").strip()
            if not validate_time(new_start):
                print("❌ Niepoprawny format godziny!")
                return
            new_end = input("Nowa godzina zakończenia (HH:MM): ").strip()
            if not validate_time(new_end):
                print("❌ Niepoprawny format godziny!")
                return
            entry.start = new_start
            entry.end = new_end
            print("✅ Zmieniono wpis.")
        else:
            print("❌ Niepoprawny indeks.")
    except Exception as e:
        print(f"Błąd edycji: {e}")


def string_operations_demo():
    """Pokazuje operacje na stringach: dzielenie, wyszukiwanie."""
    print("\n--- Operacje na stringach ---")
    s = input("Podaj tekst do demonstracji operacji na stringach: ")
    parts = s.split(" ")
    print(f"🔹 Podzielony tekst: {parts}")
    search = input("Podaj fragment do wyszukania: ")
    found = s.find(search)
    if found != -1:
        print(f"🔍 Znaleziono '{search}' na pozycji {found}")
    else:
        print(f"❌ Nie znaleziono '{search}' w tekście.")


def export_to_csv(entries, filename):
    """Eksportuje wpisy do pliku CSV."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "start", "end"])
            for e in entries:
                writer.writerow([e.date, e.start, e.end])
        print(f"✅ Wyeksportowano do pliku {filename}")
    except Exception as e:
        print(f"Błąd eksportu CSV: {e}")


def import_from_csv(data_manager, filename):
    """Importuje wpisy z pliku CSV."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if (
                        validate_date(row["date"]) and
                        validate_time(row["start"]) and
                        validate_time(row["end"])
                ):
                    data_manager.entries.append(
                        WorkEntry(row["date"], row["start"], row["end"]))
                    count += 1
        print(f"✅ Zaimportowano {count} wpisów z pliku {filename}")
    except Exception as e:
        print(f"Błąd importu CSV: {e}")


def print_entries(entries):
    """Ładnie wyświetla wszystkie wpisy."""
    if not entries:
        print("Brak wpisów do wyświetlenia.")
        return
    print("\n--- Lista wpisów ---")
    for i, e in enumerate(entries, 1):
        print(f"{str(i).rjust(2)}. {e}")


def main():
    # Zmienna lokalna (przykład)
    data_manager = DataManager("data/work_log.json")
    analyzer = Analyzer()

    while True:
        print_header()
        print_menu()
        choice = input("\nWybierz opcję: ").strip()
        if choice == "1":
            add_entry(data_manager)
        elif choice == "2":
            print_entries(data_manager.entries)
        elif choice == "3":
            edit_entry(data_manager)
        elif choice == "4":
            print("\n--- Wyszukiwanie wpisów po dacie ---")
            search_date = input(
                "Podaj datę do wyszukania (YYYY-MM-DD): ").strip()
            found = list(filter(lambda e: e.date ==
                         search_date, data_manager.entries))
            print_entries(found)
        elif choice == "5":
            analyzer.analyze(data_manager.entries)
        elif choice == "6":
            try:
                data_manager.save()
                print("✅ Dane zapisane.")
            except Exception as e:
                print(f"Błąd zapisu: {e}")
        elif choice == "7":
            analyzer.plot(data_manager.entries)
        elif choice == "8":
            remove_entry(data_manager)
        elif choice == "9":
            total = recursive_sum(data_manager.entries)
            print(f"\n🔢 Rekurencyjna suma godzin: {total:.2f}h")
        elif choice == "10":
            print("\n--- Filtruj wpisy ---")
            try:
                min_hours = float(
                    input("Pokaż wpisy z czasem pracy >= (godz): "))
                filtered = filter_entries(
                    data_manager.entries, lambda e: e.duration() >= min_hours)
                print_entries(filtered)
            except ValueError:
                print("❌ Podano niepoprawną wartość.")
        elif choice == "11":
            string_operations_demo()
        elif choice == "12":
            filename = input("Podaj nazwę pliku CSV do eksportu: ").strip()
            export_to_csv(data_manager.entries, filename)
        elif choice == "13":
            filename = input("Podaj nazwę pliku CSV do importu: ").strip()
            import_from_csv(data_manager, filename)
        elif choice == "0":
            print("\nDziękujemy za skorzystanie z systemu. Do zobaczenia!")
            sys.exit(0)
        else:
            print("❌ Niepoprawna opcja. Spróbuj ponownie.")


if __name__ == "__main__":
    main()
