import os, csv, tempfile
from src.letterboxd_csv import DiaryRow, HEADERS
from src.utils import append_row, ensure_csv

def test_append_and_headers():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "out.csv")
        ensure_csv(path)
        row = DiaryRow(Date="2025-01-01", Name="Test Movie", Year=2024, Rating="4.5")
        append_row(path, row)
        with open(path, newline="", encoding="utf-8") as f:
            rdr = list(csv.DictReader(f))
            assert rdr[0]["Name"] == "Test Movie"
            assert rdr[0]["Year"] == "2024"
