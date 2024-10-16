# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Tests for the jupyter_environment_manager envs_list module.

"""
from unittest.mock import mock_open, patch

import pytest

from jupyter_environment_manager.envs_list import (
    _uri_to_filepath,
    extract_package_version,
    extract_short_hash,
    get_pip_list,
    process_requirements_line,
    rewrite_requirements_file,
)


def test_uri_to_filepath_valid():
    """Test that valid file URIs are correctly converted to file paths."""
    uri = "file:///Users/example/Documents/testfile.txt"
    expected_path = "/Users/example/Documents/testfile.txt"
    assert (
        _uri_to_filepath(uri) == expected_path
    ), "The URI should be converted to a local file path correctly."


def test_uri_to_filepath_invalid():
    """Test that invalid URIs raise a ValueError."""
    uri = "http:///example.com/testfile.txt"
    with pytest.raises(ValueError) as exc_info:
        _uri_to_filepath(uri)
    assert "Invalid URI" in str(exc_info.value), "A ValueError should be raised for non-file URIs."


def test_extract_short_hash_valid():
    """Test that the short hash is correctly extracted from a valid git URI."""
    git_url = "git+https://github.com/user/repo.git@1234567890abcdef1234567890abcdef12345678"
    line = f"example-package @ {git_url}"
    expected_hash = "1234567"
    assert extract_short_hash(line) == expected_hash


def test_extract_short_hash_invalid():
    """Test that an invalid hash raises a ValueError."""
    git_url = "git+https://github.com/user/repo.git@invalidhash"
    line = f"example-package @ {git_url}"
    with pytest.raises(ValueError):
        extract_short_hash(line)


def test_extract_package_version_with_semver():
    """Test that the package version is correctly extracted from a valid package string."""
    string = "example-package==1.2.3"
    assert extract_package_version(string) == "1.2.3"


def test_extract_package_version_git_editable():
    """Test extracting the package version from a valid package string."""
    base_url = "git+https://github.com/user/repo.git"
    git_hash = "1234567890abcdef1234567890abcdef12345678"
    egg_info = "#egg=example-package"
    git_url = f"{base_url}@{git_hash}{egg_info}"
    string = f"-e {git_url}"
    assert extract_package_version(string) == "1234567"


def test_extract_package_version_with_hash():
    """Test that the package version is correctly extracted from a valid package string."""
    git_url = "git+https://github.com/user/repo.git@1234567890abcdef1234567890abcdef12345678"
    string = f"example-package @ {git_url}"
    with patch("jupyter_environment_manager.envs_list.extract_short_hash", return_value="1.0.0"):
        assert extract_package_version(string) == "1.0.0"


def test_extract_package_version_none():
    """Test that None is returned for an invalid package string."""
    string = "example-package"
    assert extract_package_version(string) is None


def test_process_requirements_line_valid():
    """Test that a valid requirements line is correctly processed."""
    git_url = "git+https://github.com/user/repo.git@1234567890abcdef1234567890abcdef12345678"
    line = f"example-package @ {git_url}"
    with patch(
        "jupyter_environment_manager.envs_list.extract_package_version", return_value="1.0.0"
    ):
        assert process_requirements_line(line) == "example-package==1.0.0\n"


def test_process_requirements_line_editable_package():
    """Test processing a valid editable package line."""
    base_url = "git+https://github.com/user/repo.git"
    git_hash = "1234567890abcdef1234567890abcdef12345678"
    egg_info = "#egg=example-package"
    git_url = f"{base_url}@{git_hash}{egg_info}"
    line = f"-e {git_url}"
    expected = "example-package==1234567\n"
    with patch(
        "jupyter_environment_manager.envs_list.extract_package_version", return_value="1234567"
    ):
        assert process_requirements_line(line) == expected


def test_process_requirements_line_invalid():
    """Test that an invalid requirements line returns None."""
    line = ""
    assert process_requirements_line(line) is None


def test_rewrite_requirements_file():
    """Test that the requirements file is correctly rewritten."""
    mock_file = mock_open()
    with patch("builtins.open", mock_file), patch("subprocess.Popen") as mock_popen:
        mock_popen.return_value.__enter__.return_value.stdout = iter(["package==1.0.0\n"])
        rewrite_requirements_file("dummy_path", "python")

    mock_file().write.assert_called_with("package==1.0.0\n")


def test_get_pip_list_exists():
    """Test that the pip list is correctly extracted from a requirements file."""
    mock_file = mock_open(read_data="package==1.0.0\n")
    with patch("builtins.open", mock_file):
        result = get_pip_list("dummy_path")
    assert result == ["package==1.0.0"]


def test_get_pip_list_not_found():
    """Test that an empty list is returned if the requirements file does not exist."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = get_pip_list("dummy_path")
    assert result == []
