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
