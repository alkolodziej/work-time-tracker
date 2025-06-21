# System rejestracji czasu pracy

## Cel
Aplikacja do ewidencji i analizy czasu pracy z obsługą plików, wyjątków, OOP, programowania funkcyjnego i testów.

## Autorzy
Grupa 12B:
Alan Kołodziej
Błażej Knap

## Uruchamianie
```bash
python main.py
```

## Przykładowe dane wejściowe
```
2024-06-01, 08:00, 16:00
2024-06-02, 09:00, 17:00
```

## Przykładowe dane wyjściowe
```
2024-06-01: 08:00 - 16:00 (8.00h)
2024-06-02: 09:00 - 17:00 (8.00h)
```

## Diagram klas (tekstowy)
```
WorkEntry
 ├── date
 ├── start
 ├── end
 ├── duration()
 ├── to_dict()
 ├── from_dict()
 └── __str__()

ProjectWorkEntry (dziedziczy po WorkEntry)
 ├── project
 ├── to_dict()
 ├── from_dict()
 └── __str__()
```

## Struktura modułów
```
main.py
models/
  entry.py
services/
  data_manager.py
  analyzer.py
utils/
  validators.py
tests/
  test_entry.py
```
