# tests/test_entry.py
import unittest
from models.entry import WorkEntry
from utils.validators import validate_date, validate_time, log_operation
from services.data_manager import DataManager
import os
from models.entry import ProjectWorkEntry
import timeit


# Testy walidatorów i dekoratora
class TestValidators(unittest.TestCase):
    def test_validate_date_correct(self):
        self.assertTrue(validate_date("2024-06-01"))

    def test_validate_date_incorrect(self):
        self.assertFalse(validate_date("01-06-2024"))

    def test_validate_time_correct(self):
        self.assertTrue(validate_time("08:00"))

    def test_validate_time_incorrect(self):
        self.assertFalse(validate_time("800"))

    def test_log_operation_decorator(self):
        calls = []

        @log_operation
        def foo():
            calls.append(1)
            return 42
        result = foo()
        self.assertEqual(result, 42)
        self.assertEqual(len(calls), 1)


# Testy klasy WorkEntry
class TestWorkEntry(unittest.TestCase):
    def test_duration_valid(self):
        entry = WorkEntry("2024-01-01", "08:00", "16:00")
        self.assertEqual(entry.duration(), 8.0)

    def test_duration_invalid_format(self):
        entry = WorkEntry("2024-01-01", "invalid", "16:00")
        self.assertEqual(entry.duration(), 0)

    def test_to_dict(self):
        entry = WorkEntry("2024-01-01", "08:00", "16:00")
        expected = {"date": "2024-01-01", "start": "08:00", "end": "16:00"}
        self.assertEqual(entry.to_dict(), expected)

    def test_from_dict(self):
        data = {"date": "2024-01-01", "start": "08:00", "end": "16:00"}
        entry = WorkEntry.from_dict(data)
        self.assertEqual(entry.date, "2024-01-01")
        self.assertEqual(entry.start, "08:00")
        self.assertEqual(entry.end, "16:00")

    def test_duration_negative(self):
        entry = WorkEntry("2024-01-01", "16:00", "08:00")
        self.assertEqual(entry.duration(), -8)

    def test_duration_invalid_time(self):
        entry = WorkEntry("2024-01-01", "xx:yy", "16:00")
        self.assertEqual(entry.duration(), 0)


# Testy DataManagera
class TestDataManager(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(
            os.path.dirname(__file__))  # katalog "projekt"
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)

        self.test_file = os.path.join(data_dir, "test_data.json")
        self.manager = DataManager(self.test_file)
        self.manager.entries = [
            WorkEntry("2024-01-01", "08:00", "16:00"),
            WorkEntry("2024-01-02", "09:00", "17:00")
        ]

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        self.manager.save()
        new_manager = DataManager(self.test_file)
        self.assertEqual(len(new_manager.entries), 2)
        self.assertEqual(new_manager.entries[0].date, "2024-01-01")
        self.assertEqual(new_manager.entries[1].start, "09:00")


# Testy klasy dziedziczącej ProjectWorkEntry
class TestProjectWorkEntry(unittest.TestCase):
    def test_project_entry(self):
        entry = ProjectWorkEntry("2024-01-01", "08:00", "16:00", "TestProjekt")
        self.assertEqual(entry.project, "TestProjekt")
        d = entry.to_dict()
        self.assertEqual(d["project"], "TestProjekt")
        entry2 = ProjectWorkEntry.from_dict(d)
        self.assertEqual(str(entry2), str(entry))


# Test funkcjonalny (dodanie i usunięcie wpisu)
class TestFunctional(unittest.TestCase):
    def test_add_and_remove_entry(self):
        manager = DataManager(":memory:")
        entry = WorkEntry("2024-01-01", "08:00", "16:00")
        manager.entries.append(entry)
        self.assertEqual(len(manager.entries), 1)
        manager.entries.pop(0)
        self.assertEqual(len(manager.entries), 0)

# Test integracyjny (zapis/odczyt ProjectWorkEntry)
    def test_save_and_load_project_entry(self):
        base_dir = os.path.dirname(os.path.dirname(
            __file__))  # katalog główny projektu
        data_dir = os.path.join(base_dir, "data")
        # upewniamy się, że katalog istnieje
        os.makedirs(data_dir, exist_ok=True)

        test_file = os.path.join(data_dir, "test_project_entry.json")

        entry = ProjectWorkEntry("2024-01-01", "08:00", "16:00", "ProjX")
        manager = DataManager(test_file)
        manager.entries = [entry]
        manager.save()

        manager2 = DataManager(test_file)
        self.assertEqual(manager2.entries[0].date, "2024-01-01")

        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)


# Test wydajnościowy (timeit)
class TestPerformance(unittest.TestCase):
    def test_duration_performance(self):
        entry = WorkEntry("2024-01-01", "08:00", "16:00")
        duration = timeit.timeit(lambda: entry.duration(), number=10000)
        self.assertLess(duration, 1)  # powinno być szybkie

    # Test pamięci i jakości kodu – tylko szkielet (do uruchomienia z zewnątrz)
    def test_memory_usage(self):
        from memory_profiler import memory_usage
        entry = WorkEntry("2024-01-01", "08:00", "16:00")
        mem = memory_usage((entry.duration, ))
        assert max(mem) - min(mem) < 10  # MB

    def test_code_quality(self):
        import subprocess

        result = subprocess.run(
            [
                "flake8",
                "--exclude=.venv"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("\nFlake8 errors:\n" + result.stdout)

        assert result.returncode == 0, "Flake8 reported style violations"


if __name__ == "__main__":
    unittest.main()
