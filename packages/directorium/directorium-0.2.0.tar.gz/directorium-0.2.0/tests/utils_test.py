from datetime import date, datetime
from unittest import TestCase

from directorium import utils


class TestUtils(TestCase):

    easter_dates = [
        date(2015, 4, 5),
        date(2016, 3, 27),
        date(2017, 4, 16),
        date(2018, 4, 1),
        date(2019, 4, 21),
        date(2020, 4, 12),
        date(2021, 4, 4),
        date(2022, 4, 17),
        date(2023, 4, 9),
        date(2024, 3, 31),
        date(2025, 4, 20),
        date(2026, 4, 5),
        date(2027, 3, 28),
        date(2028, 4, 16),
        date(2029, 4, 1),
        date(2030, 4, 21),
    ]

    def test_easter_date_for_year_number(self):
        for d in self.easter_dates:
            self.assertEqual(utils.easter(d.year), d)

    def test_easter_date_for_date(self):
        for d in self.easter_dates:
            self.assertEqual(utils.easter(date(d.year, 3, 1)), d)

    def test_easter_date_for_datetime(self):
        for d in self.easter_dates:
            self.assertEqual(utils.easter(datetime(d.year, 3, 1, 12, 3, 5)), d)

    def test_normalize_date(self):
        self.assertEqual(utils.normalize_date(date(2020, 2, 29)), date(2020, 2, 29))
        self.assertEqual(utils.normalize_date(datetime(2020, 2, 29, 12, 3, 5)), date(2020, 2, 29))
        self.assertEqual(utils.normalize_date(2020, 5, 23), date(2020, 5, 23))
        with self.assertRaises(ValueError):
            utils.normalize_date(2020)
        with self.assertRaises(ValueError):
            utils.normalize_date(2020, 5)
