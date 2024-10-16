# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint: disable=protected-access,redefined-outer-name

"""
Tests for the jupyter_environment_manager envs_state module.

"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import tornado.web

from jupyter_environment_manager.config_logger import get_logger
from jupyter_environment_manager.envs_state import InstallStatusHandler, PostInstallSetupHandler

logger = get_logger(__name__)


@pytest.fixture
def install_status_handler() -> InstallStatusHandler:
    """Fixture for InstallStatusHandler."""
    application = tornado.web.Application()
    request = MagicMock()
    return InstallStatusHandler(application, request)


@pytest.fixture
def post_install_setup_handler() -> PostInstallSetupHandler:
    """Fixture for PostInstallSetupHandler."""
    application = tornado.web.Application()
    request = MagicMock()
    return PostInstallSetupHandler(application, request)


@patch("jupyter_environment_manager.envs_state.install_status_codes")
def test_install_status_handler(mock_install_status_codes, install_status_handler):
    """Test InstallStatusHandler GET method."""
    handler = install_status_handler
    handler.current_user = "test_user"
    handler._transforms = []
    handler.get_query_argument = MagicMock(return_value="test-env")
    mock_install_status_codes.return_value = {"complete": 1, "success": 1}

    def mock_finish(data):
        handler._write_buffer.append(data)
        handler.finish = MagicMock(side_effect=mock_finish)
        handler.get()
        mock_install_status_codes.assert_called_once_with("test-env")
        handler.finish.assert_called_once()
        assert handler._write_buffer, "Write buffer is empty"
        assert json.loads(handler._write_buffer[0]) == {"complete": 1, "success": 1}


@patch("jupyter_environment_manager.envs_state.install_status_codes")
@patch("jupyter_environment_manager.symlink.apply_symlinks")
@patch("jupyter_environment_manager.envs_state.get_env_path")
def test_post_install_setup_handler_success(
    mock_get_env_path,
    mock_apply_symlinks,  # pylint: disable=unused-argument
    mock_install_status_codes,
    post_install_setup_handler,
):
    """Test PostInstallSetupHandler POST method for success scenario."""
    handler = post_install_setup_handler
    handler.current_user = "test_user"
    handler._transforms = []
    handler.get_json_body = MagicMock(return_value={"slug": "test-env"})
    mock_install_status_codes.return_value = {"complete": 1, "success": 1}
    mock_get_env_path.return_value = Path.home() / ".qbraid/qbraid/environments/test-env/"

    def mock_finish(data):
        handler._write_buffer.append(data)

    handler.finish = MagicMock(side_effect=mock_finish)
    handler.post()
    mock_install_status_codes.assert_called_once_with("test-env")
    assert handler._write_buffer, "Write buffer is empty"
    assert json.loads(handler._write_buffer[0]) == {
        "status": 202,
        "message": "Applying symlinks to environment test-env in background.",
    }


@patch("jupyter_environment_manager.envs_state.install_status_codes")
def test_post_install_setup_handler_failure(mock_install_status_codes, post_install_setup_handler):
    """Test PostInstallSetupHandler POST method for failure scenario."""
    handler = post_install_setup_handler
    handler.current_user = "test_user"
    handler._transforms = []
    handler.get_json_body = MagicMock(return_value={"slug": "test-env"})
    mock_install_status_codes.return_value = {"complete": 0, "success": 0}

    def mock_finish(data):
        handler._write_buffer.append(data)

    handler.finish = MagicMock(side_effect=mock_finish)
    handler.post()
    mock_install_status_codes.assert_called_once_with("test-env")

    assert handler._write_buffer, "Write buffer is empty"
    assert json.loads(handler._write_buffer[0]) == {
        "status": 400,
        "message": "Invalid request: install status values complete and success must be 1 (True).",
    }
