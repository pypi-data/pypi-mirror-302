# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint:disable=too-few-public-methods,no-member,unused-argument

"""
Tests for the jupyter_environment_manager kernels module.

"""
import json
import unittest
from asyncio import iscoroutinefunction
from pathlib import Path
from unittest import mock
from unittest.mock import patch

import pytest
from tornado.escape import json_encode
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Application

from jupyter_environment_manager.kernels import ToggleEnvKernelHandler, get_kernels


class TestGetKernels:
    """Test get_kernels function."""

    @mock.patch("jupyter_client.kernelspec.KernelSpecManager")
    def test_get_kernels(self, mock_kernel_spec_manager):
        """Test get_kernels function."""

        mock_kernel_spec_manager.return_value.get_all_specs.return_value = {
            "python3": {"spec": {"argv": ["/usr/bin/python3"]}},
            "python3_qbraid": {"spec": {"argv": ["/usr/bin/python3"]}},
            "invalid_kernel": {"spec": {"argv": ["/invalid/path"]}},
        }

        kernels = get_kernels()

        assert "python3" in kernels
        assert "python3_qbraid" not in kernels
        assert "invalid_kernel" not in kernels


class TestToggleEnvKernelHandler(unittest.TestCase):
    """Test ToggleEnvKernelHandler class."""

    def get_app(self):
        """Return a tornado.web.Application instance."""
        return Application(
            [
                (r"/toggle-env", ToggleEnvKernelHandler),
            ]
        )

    @pytest.hookimpl(tryfirst=True)
    def pytest_pyfunc_call(pyfuncitem):
        """Custom pytest function call hook."""
        funcargs = pyfuncitem.funcargs
        testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}

        if not iscoroutinefunction(pyfuncitem.obj):
            pyfuncitem.obj(**testargs)

    @patch("jupyter_environment_manager.kernels.get_kernels")
    @patch("jupyter_environment_manager.kernels.get_env_path")
    @patch("os.path.exists")
    @patch("os.listdir")
    async def test_toggle_env_kernel(
        self,
        mock_listdir,
        mock_path_exists,
        mock_get_env_path,
        mock_get_kernels,
    ):
        """Test ToggleEnvKernelHandler.post method."""
        mock_get_env_path.return_value = "/mock/path"
        mock_listdir.return_value = ["kernel1", "kernel2"]
        mock_path_exists.return_value = True
        mock_get_kernels.return_value = {"kernel1"}

        body = json_encode({"slug": "test-env"})
        async with AsyncHTTPClient() as http_client:
            response = await http_client.fetch(
                self.get_url("/toggle-env"), method="POST", body=body
            )

        self.assertEqual(response.code, 200)
        response_data = json.loads(response.body)
        self.assertEqual(response_data, {})

        mock_listdir.assert_called_with("/mock/path/kernels")
        mock_get_kernels.assert_called_once()

    @patch("qbraid_core.services.environments.kernels.add_kernels")
    @patch("qbraid_core.services.environments.kernels.remove_kernels")
    def test_toggle_env_kernels_with_valid_path(self, mock_remove_kernels, mock_add_kernels):
        """Test toggle_env_kernels method with a valid path."""
        slug_path = Path("/valid/path")
        result = ToggleEnvKernelHandler.toggle_env_kernels(slug_path)
        self.assertEqual(result["status"], 404)

    @patch("qbraid_core.services.environments.kernels.add_kernels")
    @patch("qbraid_core.services.environments.kernels.remove_kernels")
    def test_toggle_env_kernels_with_invalid_path(self, mock_remove_kernels, mock_add_kernels):
        """Test toggle_env_kernels method with an invalid path."""
        slug_path = Path("/invalid/path")
        result = ToggleEnvKernelHandler.toggle_env_kernels(slug_path)
        self.assertEqual(result["status"], 404)

    @patch("qbraid_core.services.environments.kernels.add_kernels")
    @patch("qbraid_core.services.environments.kernels.remove_kernels")
    def test_toggle_env_kernels_with_failure(self, mock_remove_kernels, mock_add_kernels):
        """Test toggle_env_kernels method with a failure in adding/removing kernels."""
        mock_add_kernels.side_effect = Exception("Failed to add kernel")
        slug_path = Path("/valid/path")
        result = ToggleEnvKernelHandler.toggle_env_kernels(slug_path)
        self.assertEqual(result["status"], 404)


if __name__ == "__main__":
    unittest.main()
