# Projekt zaliczeniowy – Języki skryptowe (Python)

**Tytuł projektu:** Ewidencja czasu pracy
**Autorzy:** Alan Kołodziej, Błażej Knap
**Data oddania:** 21.06.2025

---

## 1. Strona tytułowa
- **Nazwa uczelni:** Politechnika Świętokrzyska
- **Nazwa przedmiotu:** Języki skryptowe
- **Prowadzący:** Dr. inż. Dariusz Michalski
- **Tytuł projektu:** Ewidencja czasu pracy
- **Autorzy:** Alan Kołodziej, Błażej Knap
- **Grupa studencka:** 2ID12B
- **Data oddania:** 21.06.2025

---

## 2. Opis projektu

### Cel projektu
Celem projektu było stworzenie aplikacji umożliwiającej ewidencjonowanie czasu pracy, analizę przepracowanych godzin oraz generowanie raportów i wizualizacji.

### Funkcje aplikacji
- Dodawanie, edycja i usuwanie wpisów czasu pracy
- Analiza przepracowanych godzin
- Eksport danych do pliku CSV
- Generowanie wykresów
- Walidacja danych wejściowych

### Zakres funkcjonalny
- Obsługa plików JSON i CSV
- Prosta obsługa przez terminal
- Testy jednostkowe dla kluczowych komponentów

---

## 3. Struktura projektu

### Opis plików i folderów
- `main.py` – główny moduł uruchamiający aplikację i menu
- `models/entry.py` – definicja klasy Entry reprezentującej pojedynczy wpis czasu pracy
- `services/analyzer.py` – analiza danych, generowanie statystyk i wykresów
- `services/data_manager.py` – zarządzanie danymi, odczyt/zapis plików
- `utils/validators.py` – funkcje walidujące dane wejściowe
- `tests/test_entry.py` – testy jednostkowe klasy Entry
- `data/` – przykładowe dane, pliki JSON, CSV, wykresy
- `export.csv` – przykładowy plik eksportu
- `README.md` – dokumentacja projektu

### Krótkie omówienie klas/modułów
- **Entry (models/entry.py):** Klasa reprezentująca pojedynczy wpis czasu pracy (data, godziny, opis).
- **Analyzer (services/analyzer.py):** Moduł do analizy danych i generowania wykresów.
- **DataManager (services/data_manager.py):** Moduł do zarządzania odczytem i zapisem danych.
- **validators (utils/validators.py):** Funkcje do walidacji poprawności danych wejściowych.

---

## 4. Technologie i biblioteki
- **Python 3.x**
- **json** – obsługa plików danych
- **datetime** – operacje na datach i godzinach
- **os** – operacje na plikach i katalogach
- **csv** – eksport danych
- **matplotlib** – generowanie wykresów (jeśli użyto)
- **unittest** – testy jednostkowe

---

## 5. Sposób działania programu

### Instrukcja uruchomienia
1. Upewnij się, że masz zainstalowanego Pythona 3.x.
2. Uruchom program poleceniem:
   ```
   python main.py
   ```
3. Postępuj zgodnie z instrukcjami w menu.

### Przykładowe dane wejściowe/wyjściowe
- **Wejście:**  
  Data: 2025-06-21  

- **Wyjście:**  
  Zapis do pliku JSON/CSV, wyświetlenie statystyk, wygenerowanie wykresu.
---

## 6. Przykłady kodu (z wyjaśnieniem)

### Fragment funkcji funkcyjnej
```python
# utils/validators.py
def validate_date(date_str):
    """Waliduj datę w formacie YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
```
*Walidacja daty.*

### Fragment klasy
```python
# models/entry.py
class WorkEntry:
    def __init__(self, date, start, end):
        # Konstruktor klasy WorkEntry
        self.date = date
        self.start = start
        self.end = end
```
*Klasa reprezentująca wpis czasu pracy.*

### Obsługa wyjątków
```python
# services/data_manager.py
try:
    with open(filename, 'r') as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []
```
*Bezpieczne wczytywanie danych z pliku.*

---

## 7. Testowanie
- Testy jednostkowe w pliku `tests/test_entry.py`
- Sprawdzanie poprawności danych wejściowych
- Obsługa przypadków granicznych (np. godziny spoza zakresu, błędny format daty)

---

## 8. Wnioski
- Udało się zaimplementować kompletną aplikację do ewidencji czasu pracy z analizą i eksportem danych.
- Można byłoby rozbudować aplikację o interfejs graficzny lub obsługę wielu użytkowników.
- Rozwinięto umiejętności pracy z plikami, testowania, programowania obiektowego i funkcyjnego w Pythonie.

---
