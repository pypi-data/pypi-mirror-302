"""Module containing the Event class and associated data types.

The event is a liturgical celebration with a date, title, comment, readings, and
more. It defines the color of the day and the rank of the celebration as an enum
to simplify the handling of the data.
"""

import enum
from dataclasses import dataclass
from datetime import date
from typing import Optional

from .api import ApiEvent


class Color(enum.Enum):
    """The color of the liturgical celebration."""

    NONE = enum.auto()
    WHITE = enum.auto()
    RED = enum.auto()
    GREEN = enum.auto()
    VIOLET = enum.auto()
    ROSE = enum.auto()


class Rank(enum.IntEnum):
    """The rank of a celebration. A higher rank has a higher priority."""

    NONE = 0
    COMMEMORATION = 1
    OPTIONAL_MEMORIAL = 2
    MEMORIAL = 3
    FEAST = 4
    SOLEMNITY = 5


@dataclass
class Event:
    """Smallest data unit of the liturgical calendar.

    An Event contains many information about a liturgical celebration like the
    date, title, comment, readings, color, rank, and more.
    """

    date: date
    """The date of the liturgical celebration."""

    title: str
    """A title for the liturgical celebration."""

    comment: str = ""
    """An additional comment explaining the celebration."""

    lecture1: str = ""
    """First lecture."""

    psalm: str = ""
    """Responsorial psalm."""

    lecture2: str = ""
    """Second lecture."""

    gospel: str = ""
    """The gospel of the day."""

    color: Optional[Color] = None
    """The liturgical color of the celebration."""

    file: str = ""
    """A path of the online shott with more information."""

    importance: int = 0
    """Importance of the celebration. Higher values have a higher priority."""

    rank: Rank = Rank.NONE
    """Liturgical rank of the celebration."""

    @staticmethod
    def parse(data: ApiEvent) -> "Event":
        """Parses the data from the API into an Event object.

        Args:
            data (ApiEvent): The data from the API.

        Returns:
            Event: The event containing all data from the API.
        """
        title = str(data.get("Tl"))
        colors = {
            "w": Color.WHITE,
            "r": Color.RED,
            "g": Color.GREEN,
            "v": Color.VIOLET,
            "": Color.NONE,
        }
        color = colors.get(str(data.get("Farbe")))
        rose_days = ["Dritter Adventssonntag", "Vierter Fastensonntag"]
        if title in rose_days:
            color = Color.ROSE
        ranks = {
            "H": Rank.SOLEMNITY,
            "F": Rank.FEAST,
            "G": Rank.MEMORIAL,
            "g": Rank.OPTIONAL_MEMORIAL,
            "Kommemoration": Rank.COMMEMORATION,
        }
        rank = ranks.get(str(data.get("Rang")), Rank.NONE)

        return Event(
            date=date.fromisoformat(str(data.get("Datum"))),
            title=title,
            comment=str(data.get("Bem")),
            lecture1=str(data.get("L1")),
            psalm=str(data.get("AP")),
            lecture2=str(data.get("L2")),
            gospel=str(data.get("EV")),
            color=color,
            file=str(data.get("Datei")),
            importance=int(data.get("Grad", 0)),
            rank=rank,
        )
