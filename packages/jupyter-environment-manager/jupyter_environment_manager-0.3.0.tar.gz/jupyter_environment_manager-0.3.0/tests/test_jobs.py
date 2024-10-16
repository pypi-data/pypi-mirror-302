# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint:disable=redefined-outer-name

"""
Tests for the jupyter_environment_manager jobs module.

"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import tornado.web

from jupyter_environment_manager.jobs import (
    QuantumJobsHandler,
    flip_include_sys_packages,
    quantum_jobs_supported_enabled,
    safe_set_include_sys_packages,
)


@pytest.fixture
def app():
    """Return a tornado.web.Application instance with QuanJobsHandler."""
    return tornado.web.Application([(r"/quantum-jobs", QuantumJobsHandler)])


@pytest.fixture
def mock_quantum_lib_proxy_state(monkeypatch):
    """Return a MagicMock instance for quantum_lib_proxy_state."""
    mock_state = MagicMock()
    monkeypatch.setattr("jupyter_environment_manager.jobs.quantum_lib_proxy_state", mock_state)
    return mock_state


@pytest.fixture
def mock_env_path(tmp_path, monkeypatch):
    """Return a temporary environment path."""
    env_path = tmp_path / "test-env"
    env_path.mkdir()
    monkeypatch.setattr(
        "qbraid_core.services.environments.paths.get_default_envs_paths",
        lambda: [tmp_path],
    )
    yield env_path
    monkeypatch.undo()


@pytest.mark.parametrize(
    "supported, enabled, expected_output",
    [
        (True, True, (True, True)),
        (True, False, (True, False)),
        (False, True, (False, True)),
        (False, False, (False, False)),
    ],
)
def test_quantum_jobs_supported_enabled(supported, enabled, expected_output, mock_env_path):
    """Test quantum_jobs_supported_enabled function."""
    mock_state = {"supported": supported, "enabled": enabled}
    with patch(
        "jupyter_environment_manager.jobs.quantum_lib_proxy_state",
        return_value=mock_state,
    ):
        assert quantum_jobs_supported_enabled(mock_env_path.name) == expected_output


@pytest.mark.parametrize(
    "python_exe, pyvenv_cfg, expected_output",
    [
        (sys.executable, Path("/path/to/pyvenv.cfg"), False),
        (Path("/path/to/python"), Path("/path/to/pyvenv.cfg"), True),
    ],
)
def test_flip_include_sys_packages(python_exe, pyvenv_cfg, expected_output, monkeypatch):
    """Test flip_include_sys_packages function."""
    monkeypatch.setattr(
        "jupyter_environment_manager.jobs.python_paths_equivalent",
        lambda x, y: str(x) == str(y),
    )
    monkeypatch.setattr(
        "jupyter_environment_manager.jobs.extract_include_sys_site_pkgs_value",
        lambda x: True,
    )
    assert flip_include_sys_packages(python_exe, pyvenv_cfg) == expected_output


@patch("jupyter_environment_manager.jobs.set_include_sys_site_pkgs_value")
def test_safe_set_include_sys_packages(mock_set_include_sys_site_pkgs_value):
    """Test safe_set_include_sys_packages function."""
    safe_set_include_sys_packages(True, "/path/to/pyvenv.cfg")
    mock_set_include_sys_site_pkgs_value.assert_called_once_with(True, "/path/to/pyvenv.cfg")

    mock_set_include_sys_site_pkgs_value.side_effect = Exception("Test exception")
    safe_set_include_sys_packages(False, "/path/to/pyvenv.cfg")
    mock_set_include_sys_site_pkgs_value.assert_called_with(False, "/path/to/pyvenv.cfg")
