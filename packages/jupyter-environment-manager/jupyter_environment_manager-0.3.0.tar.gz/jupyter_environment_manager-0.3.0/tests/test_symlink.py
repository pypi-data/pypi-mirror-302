# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint: disable=redefined-outer-name

"""
Tests for the jupyter_environment_manager symlink module.

"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from jupyter_environment_manager.symlink import (
    apply_symlinks,
    create_lib64_symlink,
    create_python_version_symlink,
    extract_version_from_dir_name,
    get_site_packages_python_version,
    supports_symlink,
)


@pytest.fixture
def mock_venv_path(tmp_path: Path) -> Path:
    """Create a virtual environment directory at given (temporary) path."""
    venv_path = tmp_path / "test-env"
    venv_path.mkdir(parents=True, exist_ok=True)
    return venv_path


@pytest.mark.parametrize(
    "directory_name, prefix, expected_version",
    [
        ("python3.10.0", "python", "3.10.0"),
        ("python3.9.12", "python", "3.9.12"),
    ],
)
def test_extract_version_from_dir_name(directory_name, prefix, expected_version):
    """Test extract_version_from_dir_name function."""
    version = extract_version_from_dir_name(directory_name, prefix)
    assert version == expected_version


def test_extract_version_from_dir_name_invalid_version():
    """Test extract_version_from_dir_name function with invalid version."""
    with pytest.raises(ValueError):
        extract_version_from_dir_name("python3.10.invalid", "python")


@pytest.fixture
def venv_path(tmp_path):
    """Return a temporary directory for the virtual environment."""
    pyenv_lib = tmp_path / "lib" / "python3.10"
    pyenv_lib.mkdir(parents=True)
    return tmp_path


def test_get_site_packages_python_version(venv_path):
    """Test get_site_packages_python_version function."""
    version = get_site_packages_python_version(venv_path)
    assert version == "3.10"


def test_get_site_packages_python_version_no_python_dirs(tmp_path):
    """Test get_site_packages_python_version function with no Python directories."""
    with pytest.raises(FileNotFoundError):
        get_site_packages_python_version(tmp_path)


def test_get_site_packages_python_version_multiple_python_dirs(venv_path):
    """Test get_site_packages_python_version function with multiple Python directories."""
    pyenv_lib = venv_path / "lib" / "python3.9"
    pyenv_lib.mkdir(parents=True)
    with pytest.raises(ValueError):
        get_site_packages_python_version(venv_path)


def test_supports_symlink():
    """Test supports_symlink function."""
    assert supports_symlink()


@patch("jupyter_environment_manager.symlink.create_python_version_symlink")
@patch("jupyter_environment_manager.symlink.create_lib64_symlink")
def test_apply_symlinks(mock_create_lib64_symlink, mock_create_python_version_symlink, venv_path):
    """Test apply_symlinks function."""
    apply_symlinks(venv_path)
    mock_create_python_version_symlink.assert_called_once_with(venv_path)
    mock_create_lib64_symlink.assert_called_once_with(venv_path)


@pytest.mark.skip(reason="Need to fix this test")
@patch("jupyter_environment_manager.symlink.update_symlink")
def test_create_python_version_symlink(mock_update_symlink, mock_venv_path):
    """Test create_python_version_symlink function."""
    venv_path = mock_venv_path

    mock_version_info = MagicMock()
    mock_version_info.major = 3
    mock_version_info.minor = 10
    mock_version_info.micro = 0

    with patch("sys.version_info", mock_version_info):
        with patch(
            "jupyter_environment_manager.symlink.get_python_version_from_exe",
            return_value="3.10.0",
        ):
            with patch(
                "jupyter_environment_manager.symlink.get_site_packages_python_version",
                return_value="3.9.0",
            ):
                create_python_version_symlink(venv_path)
                assert mock_update_symlink.called


@patch("jupyter_environment_manager.symlink.update_symlink")
def test_create_lib64_symlink(mock_update_symlink, mock_venv_path):
    """Test create_lib64_symlink function."""
    venv_path = mock_venv_path
    pyenv_lib = venv_path / "lib"
    pyenv_lib64 = venv_path / "lib64"

    pyenv_lib.mkdir(parents=True, exist_ok=True)

    # Mock the 'exists' method to return True only for 'pyenv_lib' and False for 'pyenv_lib64'
    def mock_exists(path):
        if path == pyenv_lib:
            return True
        if path == pyenv_lib64:
            return False
        return path.exists()

    with patch.object(Path, "exists", mock_exists):
        create_lib64_symlink(venv_path)

    mock_update_symlink.assert_called_once_with(pyenv_lib64, "lib", target_is_directory=True)
