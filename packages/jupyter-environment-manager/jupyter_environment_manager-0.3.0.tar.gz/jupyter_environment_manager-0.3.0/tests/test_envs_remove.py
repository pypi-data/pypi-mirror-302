# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Tests for the jupyter_environment_manager envs_remove module.

"""

import json
import shutil
import tempfile
import unittest

import pytest
from jupyter_server.serverapp import ServerApp
from qbraid_core.services.environments.paths import DEFAULT_LOCAL_ENVS_PATH
from qbraid_core.system.filemanager import FileManager

from jupyter_environment_manager.envs_remove import UninstallEnvironmentHandler


class UninstallEnvironmentHandlerTest(unittest.TestCase):
    """Test UninstallEnvironmentHandler class."""

    def get_app(self):
        """Return a tornado.web.Application instance."""
        self.server_app = ServerApp()  # pylint: disable=attribute-defined-outside-init
        return self.server_app.web_app

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.temp_dir = tempfile.mkdtemp()
        DEFAULT_LOCAL_ENVS_PATH.mkdir(parents=True, exist_ok=True)

        self.slug = "test-environment"
        self.env_path = DEFAULT_LOCAL_ENVS_PATH / self.slug
        self.kernels_path = self.env_path / "kernels"
        self.kernels_path.mkdir(parents=True, exist_ok=True)

        self.kernel_spec_file = self.kernels_path / "kernel.json"
        with self.kernel_spec_file.open("w") as f:
            json.dump({"argv": ["python"], "display_name": "Test Kernel"}, f)

    def tearDown(self):
        """Tear down test environment."""
        shutil.rmtree(self.temp_dir)
        super().tearDown()

    def test_uninstall_env_kernels(self):
        """Test UninstallEnvironmentHandler.uninstall_env_kernels method."""
        UninstallEnvironmentHandler.uninstall_env_kernels(self.slug)
        self.assertTrue(self.kernel_spec_file.exists())

    def test_remove_env_cycle(self):
        """Test UninstallEnvironmentHandler.remove_env_cycle method."""
        UninstallEnvironmentHandler.remove_env_cycle(self.slug)
        self.assertFalse(self.env_path.exists())

    def test_remove_env_cycle_with_existing_tmp_dirs(self):
        """Test UninstallEnvironmentHandler.remove_env_cycle method with existing tmp dirs."""
        for i in range(3):
            tmp_dir = DEFAULT_LOCAL_ENVS_PATH / f"tmp{i}"
            tmp_dir.mkdir(parents=True, exist_ok=True)
        UninstallEnvironmentHandler.remove_env_cycle(self.slug)
        for i in range(3):
            tmp_dir = DEFAULT_LOCAL_ENVS_PATH / f"tmp{i}"
            self.assertFalse(tmp_dir.exists())


@pytest.fixture
def file_manager():
    """Return a FileManager instance."""
    return FileManager()


@pytest.fixture
def default_local_envs_path():
    """Return the default local environments path."""
    return DEFAULT_LOCAL_ENVS_PATH
