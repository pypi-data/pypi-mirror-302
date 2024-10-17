import json
from datetime import date
from unittest import TestCase

from directorium import Directorium
from directorium.api import CacheApi, FileApi, RequestApi
from directorium.directorium import Season
from directorium.event import Event


class TestDirectorium(TestCase):

    def setUp(self):
        with open("tests/data/2022.json", "r") as f:
            self.data = json.load(f)["Zelebrationen"]
        self.api = FileApi("tests/data/%s.json")

    def test_get(self):
        directorium = Directorium(self.api)
        expected = [Event.parse(self.data[0])]
        actual = directorium.get(date(2022, 1, 1))
        self.assertEqual(expected, actual)

    def test_get_multiple(self):
        directorium = Directorium(self.api)
        expected = [Event.parse(d) for d in self.data[7:10]]
        actual = directorium.get(date(2022, 1, 7))
        self.assertEqual(expected, actual)

    def test_season(self):
        directorium = Directorium(self.api)
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(directorium.season(date(2022, 1, 1)), Season.CHRISTMAS)
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(directorium.season(date(2022, 2, 5)), Season.ORDINARY)
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(directorium.season(date(2022, 3, 21)), Season.LENT)
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(directorium.season(date(2022, 4, 18)), Season.EASTER)

    def test_get_season(self):
        self.assertEqual(Directorium.get_season(date(2022, 1, 1)), Season.CHRISTMAS)
        self.assertEqual(Directorium.get_season(date(2022, 2, 5)), Season.ORDINARY)
        self.assertEqual(Directorium.get_season(date(2022, 3, 21)), Season.LENT)
        self.assertEqual(Directorium.get_season(date(2022, 4, 18)), Season.EASTER)

    def test_factory_methods(self):
        directorium = Directorium.from_request("koeln")
        self.assertIsInstance(directorium.api, RequestApi)
        self.assertEqual(directorium.api.calendar, "koeln")
        directorium = Directorium.from_file("tests/data/%s.json")
        self.assertIsInstance(directorium.api, FileApi)
        self.assertEqual(directorium.api.format_path, "tests/data/%s.json")
        directorium = Directorium.from_cache("tests/data/", "koeln")
        self.assertIsInstance(directorium.api, CacheApi)
        self.assertEqual(directorium.api.base_path, "tests/data/")
        self.assertEqual(directorium.api.calendar, "koeln")

    def tet_default_get_parameter_is_today(self):
        directorium = Directorium.from_request("koeln")
        self.assertEqual(directorium.get(), directorium.get(date.today()))
        self.assertEqual(directorium.season(), directorium.season(date.today()))
