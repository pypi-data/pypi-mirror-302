# Templater

Templater is a Python project designed to create and manage templates for various purposes. This project includes features such as pre-commit hooks, tox for testing, loguru for logging, and pytest for unit testing.

## Features

- **Pre-commit hooks**: Ensure code quality before committing changes.
- **Tox**: Automate testing in multiple environments.
- **Loguru**: Simplify logging.
- **Pytest**: Write simple and scalable test cases.
- **Pytest-cov**: Measure code coverage.
- **Pytest-cov-html**: Generate HTML reports for code coverage.

## Installation

To install the dependencies, use [PDM](https://pdm.fming.dev/):

```sh
pdm install
```

## Usage

### Listing YAML Files

To list all YAML files in a directory:

```python
from src.templater.app import list_yaml_files

yaml_files = list_yaml_files("path/to/directory")
print(yaml_files)
```

### Selecting a YAML File

To select a YAML file from a list:

```python
from src.templater.app import select_yaml_file

selected_file = select_yaml_file(yaml_files)
print(selected_file)
```

### Executing a YAML File

To execute a YAML file:

```python
from src.templater.app import execute_yaml

execute_yaml("path/to/yaml/file.yaml")
```

## Testing

To run the tests, use [`pytest`](command:_github.copilot.openSymbolFromReferences?%5B%22%22%2C%5B%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Faratz%2FDocuments%2F_pyro%2Ftemplater%2Ftests%2Ftest_app.py%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A0%2C%22character%22%3A7%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Faratz%2FDocuments%2F_pyro%2Ftemplater%2Fpyproject.toml%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A11%2C%22character%22%3A5%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Faratz%2FDocuments%2F_pyro%2Ftemplater%2Ftemplates%2Ftest.yaml%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A6%2C%22character%22%3A117%7D%7D%2C%7B%22uri%22%3A%7B%22scheme%22%3A%22file%22%2C%22authority%22%3A%22%22%2C%22path%22%3A%22%2FUsers%2Faratz%2FDocuments%2F_pyro%2Ftemplater%2F.gitignore%22%2C%22query%22%3A%22%22%2C%22fragment%22%3A%22%22%7D%2C%22pos%22%3A%7B%22line%22%3A52%2C%22character%22%3A1%7D%7D%5D%2C%22e08ecd10-cd79-403c-8579-1dee39317bdb%22%5D "Go to definition"):

```sh
pytest
```

### Example Test

Here is an example test case for listing YAML files:

```python
import pytest
from unittest.mock import patch
from src.templater.app import list_yaml_files

@pytest.fixture
def mock_os_path_exists():
    with patch("os.path.exists") as mock_exists:
        yield mock_exists

@pytest.fixture
def mock_os_listdir():
    with patch("os.listdir") as mock_listdir:
        yield mock_listdir

def test_list_yaml_files_directory_not_exist(mock_os_path_exists):
    mock_os_path_exists.return_value = False
    result = list_yaml_files("non_existent_directory")
    assert result == []

def test_list_yaml_files_no_yaml_files(mock_os_path_exists, mock_os_listdir):
    mock_os_path_exists.return_value = True
    mock_os_listdir.return_value = ["file1.txt", "file2.doc"]
    result = list_yaml_files("some_directory")
    assert result == []

def test_list_yaml_files_with_yaml_files(mock_os_path_exists, mock_os_listdir):
    mock_os_path_exists.return_value = True
    mock_os_listdir.return_value = ["file1.yaml", "file2.yml", "file3.txt"]
    result = list_yaml_files("some_directory")
    assert result == ["file1.yaml", "file2.yml"]
```

## Project Structure

```
templater/
├── __pycache__/
├── .gitignore
├── .pdm-python
├── .pytest_cache/
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
│   └── v/
│       └── cache/
│           ├── lastfailed
│           ├── nodeids
│           └── stepwise
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── docs/
├── pdm.lock
├── pyproject.toml
├── README.md
├── src/
│   └── templater/
│       ├── __init__.py
│       ├── __pycache__/
│       └── app.py
├── templates/
│   ├── docs/
│   │   └── test.md
│   └── test.yaml
└── tests/
    ├── __init__.py
    ├── __pycache__/
    └── test_app.py
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Authors

- Andre Ratzenberger - [andre.ratzenberger@whiteduck.de](mailto:andre.ratzenberger@whiteduck.de)