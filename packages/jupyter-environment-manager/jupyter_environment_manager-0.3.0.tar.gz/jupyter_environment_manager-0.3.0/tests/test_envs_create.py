# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint: disable=redefined-outer-name,protected-access

"""
Tests for the jupyter_environment_manager envs_create module.

"""
import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest
from qbraid_core.services.environments.paths import DEFAULT_LOCAL_ENVS_PATH
from tornado.web import Application

from jupyter_environment_manager.envs_create import CreateCustomEnvironmentHandler


@pytest.fixture
def handler():
    """Return CreateCustomEnvironmentHandler instance."""
    application = Application()
    request = MagicMock()
    return CreateCustomEnvironmentHandler(application, request)


@patch("jupyter_environment_manager.envs_create.update_state_json")
@patch("jupyter_environment_manager.envs_create.create_local_venv")
@patch("jupyter_environment_manager.envs_create.create_qbraid_env_assets")
def test_post_creates_custom_environment(
    mock_create_qbraid_env_assets, mock_create_local_venv, mock_update_state_json, handler
):
    """Test post method creates custom environment."""
    input_data = {
        "slug": "test-env",
        "name": "Test Environment",
        "prompt": "Test Prompt",
        "kernelName": "Test Kernel",
        "image": None,
    }
    handler.get_json_body = MagicMock(return_value=input_data)
    handler.current_user = "test_user"
    handler._transforms = []

    handler.post()

    mock_create_qbraid_env_assets.assert_called_once_with(
        "test-env",
        "Test Environment",
        "Test Kernel",
        os.path.join(str(DEFAULT_LOCAL_ENVS_PATH), "test-env"),
        None,
    )
    mock_create_local_venv.assert_called_once_with(
        str(DEFAULT_LOCAL_ENVS_PATH / "test-env"), "Test Prompt", sys.executable
    )
    mock_update_state_json.assert_called_once_with(DEFAULT_LOCAL_ENVS_PATH / "test-env", 0, 0)


@patch("jupyter_client.kernelspec.KernelSpecManager")
def test_post_creates_kernel_json(mock_kernel_spec_manager, handler):
    """Test post method creates kernel.json file."""
    input_data = {
        "slug": "test-env",
        "name": "Test Environment",
        "prompt": "Test Prompt",
        "kernelName": "Test Kernel",
        "image": None,
    }
    handler.get_json_body = MagicMock(return_value=input_data)
    handler.current_user = "test_user"
    handler._transforms = []

    handler.post()

    mock_kernel_spec_manager_instance = mock_kernel_spec_manager.return_value
    mock_kernel_spec_manager_instance.get_all_specs.return_value = {
        "python3": {
            "spec": {"argv": ["python"], "display_name": "Python 3"},
            "resource_dir": str(
                DEFAULT_LOCAL_ENVS_PATH / "test-env" / "kernels" / "python3_test-env"
            ),
        }
    }
    kernel_json_path = os.path.join(
        str(DEFAULT_LOCAL_ENVS_PATH),
        "test-env",
        "kernels",
        "python3_test-env",
        "kernel.json",
    )
    with open(kernel_json_path, "r", encoding="utf-8") as file:
        kernel_data = json.load(file)

    if os.name == "nt":
        python_exec_path = os.path.join(
            str(DEFAULT_LOCAL_ENVS_PATH), "test-env", "pyenv", "Scripts", "python.exe"
        )
    else:
        python_exec_path = os.path.join(
            str(DEFAULT_LOCAL_ENVS_PATH), "test-env", "pyenv", "bin", "python"
        )

    assert kernel_data["argv"][0] == python_exec_path
    assert kernel_data["display_name"] == "Test Kernel"
