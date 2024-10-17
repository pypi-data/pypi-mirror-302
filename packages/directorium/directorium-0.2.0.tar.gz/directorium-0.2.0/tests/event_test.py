import json
from datetime import date
from unittest import TestCase

from directorium.event import Color, Event, Rank


class TestEvent(TestCase):

    def setUp(self):
        with open("tests/data/2022.json", "r") as f:
            self.data = json.load(f)["Zelebrationen"]

    def test_parse(self):
        expected = Event(
            date=date(2022,1,1),
            title="1. Januar - Neujahr",
            comment="Hochfest der Gottesmutter Maria",
            lecture1="Num 6, 22-27",
            psalm="Ps 67 (66), 2-3.5.6 u. 8 (R: 2a)",
            lecture2="Gal 4, 4-7",
            gospel="Lk 2, 16-21",
            color=Color.WHITE,
            file="weihnachtszeit/oktavtag.htm",
            importance=3,
            rank=Rank.SOLEMNITY,
        )
        actual = Event.parse(self.data[0])
        self.assertEqual(actual, expected)

    def test_parse_pink_color(self):
        days = ["Dritter Adventssonntag", "Vierter Fastensonntag"]
        data = [d for d in self.data if d["Tl"] in days]
        for d in data:
            actual = Event.parse(d)
            self.assertEqual(actual.color, Color.ROSE)
