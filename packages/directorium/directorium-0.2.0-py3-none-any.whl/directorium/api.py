"""
Module containing different approaches on handling API data.

The idea is to have a common interface for different backends, that provide the
information of the API of http://www.eucharistiefeier.de. It is organized by
years so that the data may be cached.
"""

import json
import os
from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Any, Dict, List, Mapping, cast
from urllib.parse import urlencode

import requests
from platformdirs import user_data_dir

from . import utils

ApiEvent = Mapping[str, str | int]
"""Type alias for the event data returned by the API."""

ApiYear = Mapping[str, str | List[ApiEvent]]
"""Type alias for a whole year of events returned by the API."""


class Api(ABC):
    """An abstract class representing an API response.

    To simplify the implementation of various backends, this abstract class is
    used to define a common interface. The implementing classes should return
    the JSON-data returned by the API of http://www.eucharistiefeier.de.
    """

    @abstractmethod
    def get_year(self, year: int) -> ApiYear:
        """Should return the JSON-data for a given year.

        Args:
            year (int): The year for which to return the JSON-data.

        Returns:
            ApiYear: The JSON-data as provided by the API described above.
        """
        pass

    def get_date(
        self, year: int | date | datetime, month: int = 0, day: int = 0,
    ) -> List[ApiEvent]:
        """Returns a list of data for a given date.

        The data will be retrieved from the whole year of data provided.

        Args:
            year (int | date | datetime): Either a date to check or the year if
                month and day are also provided.
            month (int, optional): If the year is a number, the month must also
                be provided. Defaults to 0.
            day (int, optional): If the year is a number, the day must also be
                provided. Defaults to 0.

        Returns:
            List[ApiEvent]: As multiple events may be on the same day, a list is
                returned.
        """
        date = utils.normalize_date(year, month, day)
        data = self.get_year(date.year)["Zelebrationen"]
        data = cast(List[ApiEvent], data)
        date_param = date.strftime("%Y-%m-%d")
        return [d for d in data if d["Datum"] == date_param]


class RequestApi(Api):
    """An API using the requests library to fetch the data directly.

    This class directly trys to fetch all requested data directly from the web
    API. It doesn't implement any caching or file handling.

    Attributes:
        calendar (str | None): The calendar to use. If None, the default
            calendar is used. See the `kal`-parameter of the API.
    """

    def __init__(self, calendar: str | None = None):
        """Creates an API-handler.

        Args:
            calendar (str | None, optional): The regional calendar to use.
                Defaults to None.
        """
        self.calendar = calendar

    def _get_params(self, year: int) -> Dict[str, str]:
        """Internal method to prepare common parameters for the API.

        Args:
            year (int): The year to request.

        Returns:
            Dict[str, str]: Parameters to send as GET-parameters to the API.
        """
        return {
            "format": "jsonarray",
            "jahr": str(year),
            "info": "wdtrgflu",
            "dup": "e",
            "bahn": "j",
            "kal": self.calendar if self.calendar else "",
        }

    def _request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Internal method to request data from the API.

        Args:
            params (Dict[str, str]): The parameters to add as query parameters.

        Returns:
            Dict[str, Any]: The response of the API as a dictionary.
        """
        url = f"http://www.eucharistiefeier.de/lk/api.php?{urlencode(params)}"
        return requests.get(url, timeout=10).json()

    def get_year(self, year: int) -> ApiYear:
        """Returns the JSON-data for a given year.

        Args:
            year (int): The year for which to return the JSON-data.

        Returns:
            ApiYear: The JSON-data freshly requested from the API.
        """
        params = self._get_params(year)
        return self._request(params)

    def get_date(
        self, year: int | date | datetime, month: int = 0, day: int = 0,
    ) -> List[ApiEvent]:
        """Returns a list of data for a given date.

        This method is overwritten as to only request the data for the given
        date from the API instead of the whole year.

        Args:
            year (int | date | datetime): Either a date to check or the year if
                month and day are also provided.
            month (int, optional): If the year is a number, the month must also
                be provided. Defaults to 0.
            day (int, optional): If the year is a number, the day must also be
                provided. Defaults to 0.

        Returns:
            List[ApiEvent]: As multiple events may be on the same day, a list is
                returned.
        """
        date = utils.normalize_date(year, month, day)
        params = self._get_params(date.year)
        params["monat"] = str(date.month)
        params["tag"] = str(date.day)
        data = self._request(params)
        return data["Zelebrationen"]

    def get_date_from_year(
        self, year: int | date | datetime, month: int = 0, day: int = 0,
    ) -> List[ApiEvent]:
        """Returns a list of data for a given date.

        The data will be retrieved from the whole year of data provided. Useful
        if you want to enforce the use of the whole year of data. E.g. if the
        `get_year`-method is overwritten to use a cache.

        Args:
            year (int | date | datetime): Either a date to check or the year if
                month and day are also provided.
            month (int, optional): If the year is a number, the month must also
                be provided. Defaults to 0.
            day (int, optional): If the year is a number, the day must also be
                provided. Defaults to 0.

        Returns:
            List[ApiEvent]: As multiple events may be on the same day, a list is
                returned.
        """
        return super().get_date(year, month, day)


class FileApi(Api):
    """An api that reads the data from a file.

    This backend may be useful if you don't want to use an online API. This
    requires you to firstly download the data from the API and save it to a
    file. The file must contain the JSON-data of a whole year of events. An
    example code to create this files could be:

    ```python
    years = range(2020, 2026)
    api = RequestApi()
    for year in years:
        data = api.get_year(year)
        with open(f"path/{year}.json", "w") as f:
            json.dump(data, f)
    ```

    Attributes:
        format_path (str): A format string that is used to load the data for a
            given year. The year will be inserted into the string using the
            `%`-operator.
    """

    def __init__(self, format_path: str):
        """Creates the API-handler.

        Args:
            format_path (str): A format string that is used to load the data for
                a given year. The year will be inserted into the string using the
                `%`-operator.
        """
        self.format_path = format_path

    def get_year(self, year: int) -> ApiYear:
        """Returns the JSON-data for a given year.

        Args:
            year (int): The year for which to return the JSON-data.

        Returns:
            ApiYear: The JSON-data loaded from the file.
        """
        path = self.format_path % year
        with open(path, "r") as f:
            return json.load(f)


class CacheApi(RequestApi):
    """An API extension that caches requested data to a file.

    Additionally to the `RequestApi`, this class saves the data to a file after
    being loaded. This way, the data is only requested once and then saved to a
    file. If the data is requested again, it is loaded from the file instead of
    the API.

    Attributes:
        base_path (str): The base path where the files are saved. In the given
            directory, multiple JSON-files will be saved.
        calendar (str | None): The calendar to use. If None, the default
            calendar is used. See the `kal`-parameter of the API.
    """

    def __init__(self, base_path: str | None = None, calendar: str | None = None):
        """Creates an API-handler.

        Args:
            base_path (str | None, optional): The base path where the files are
                saved. In the given directory, multiple JSON-files will be
                created. If no path is given, a temporary directory according to
                the operating system is used. Defaults to None.
            calendar (str | None, optional): The regional calendar to use.
                Defaults to None.
        """
        super().__init__(calendar)
        if base_path is None:
            base_path = user_data_dir("directorium", False, ensure_exists=True)
        self.base_path = base_path

    def get_year(self, year: int) -> ApiYear:
        """Returns the JSON-data for a given year.

        Args:
            year (int): The year for which to return the JSON-data.

        Returns:
            ApiYear: The JSON-data out of the cached data or requested from the
                API if no local data is available.
        """
        cal_name = f".{self.calendar}" if self.calendar else ""
        path = f"{self.base_path}/{year}{cal_name}.json"

        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)

        data = super().get_year(year)
        with open(path, "w") as f:
            json.dump(data, f)
        return data

    def get_date(
        self, year: int | date | datetime, month: int = 0, day: int = 0,
    ) -> List[ApiEvent]:
        """Returns a list of data for a given date.

        The data will be retrieved from the whole year of data provided. This
        way caching of the yearly data is possible.

        Args:
            year (int | date | datetime): Either a date to check or the year if
                month and day are also provided.
            month (int, optional): If the year is a number, the month must also
                be provided. Defaults to 0.
            day (int, optional): If the year is a number, the day must also be
                provided. Defaults to 0.

        Returns:
            List[ApiEvent]: As multiple events may be on the same day, a list is
                returned.
        """
        return super().get_date_from_year(year, month, day)
