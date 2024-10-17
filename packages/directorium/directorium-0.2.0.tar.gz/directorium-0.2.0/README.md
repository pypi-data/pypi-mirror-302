[![Tests](https://github.com/matthiasgi/directorium/workflows/Testing%20code/badge.svg)](https://github.com/matthiasgi/directorium/actions?query=workflow:"Testing+code")
[![Build documentation](https://github.com/MatthiasGi/directorium/actions/workflows/docs.yml/badge.svg)](https://github.com/MatthiasGi/directorium/actions/workflows/docs.yml)
[![Publish Package](https://github.com/matthiasgi/directorium/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/matthiasgi/directorium/actions?query=workflow:"Upload+Python+Package")

[![GitHub release](https://img.shields.io/github/release/matthiasgi/directorium?include_prereleases=&sort=semver&color=blue)](https://github.com/matthiasgi/directorium/releases/)
[![License](https://img.shields.io/badge/License-MIT-blue)](#license)
[![issues - directorium](https://img.shields.io/github/issues/matthiasgi/directorium)](https://github.com/matthiasgi/directorium/issues)

# directorium

A wrapper package for the public API of https://eucharistiefeier.de/lk/. It is able to provide information from the liturgical calendar such as liturgical color and lectures. To start with the package just run:
```shell
pip install directorium
```

## Getting started

A sample usage would be:
```python
from datetime import date
from directorium import Directorium

directorium = Directorium.from_request()
today = date.today()
events = directorium.get(today)
print(events)
```

## Documentation

An automatically created documentation is available on [the GitHub Pages of this project](https://matthiasgi.github.io/directorium/).

## Contributing
You're more than invited to contribute to this project. Any kind of help is appreciated. Just open an issue or a pull request.

1. Fork the project
2. Add a python environment with `python -m venv .venv`
3. Activate the environment with `source .venv/bin/activate`
4. Install the development dependencies with `pip install -e .[development]`
5. Install the pre-commit hooks with `pre-commit install`
6. Create a new branch
7. Make your changes (remember to add tests!) and commit them
8. Install the test dependencies with `pip install -e .[test]`
9. Run the tests with `pytest`
10. Push your changes and open a pull request

## Acknowledgments
Thanks a lot to the [Salesians of Don Bosco](https://www.donbosco.de/) for providing the API!

## License

Released under [MIT](/LICENSE) by [@matthiasgi](https://github.com/matthiasgi).
