# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint:disable=redefined-outer-name,too-many-arguments,unused-argument

"""
Tests for the jupyter_environment_manager envs_pkgs module.

"""

import json
import os
from unittest.mock import MagicMock, mock_open, patch

import pytest
import tornado.web
from qbraid_core.services.environments.paths import DEFAULT_LOCAL_ENVS_PATH

from jupyter_environment_manager.envs_pkgs import InstallPackagesHandler, UninstallPackageHandler


@pytest.fixture
def mock_app():
    """Return a tornado.web.Application instance."""
    return tornado.web.Application()


@pytest.fixture
def mock_request():
    """Return a MagicMock instance."""
    return MagicMock()


class TestInstallPackagesHandler:
    """Test InstallPackagesHandler class."""

    def test_post_with_no_packages_and_no_upgrade_pip(self, mock_app, mock_request):
        """Test post method with no packages and no upgradePip."""
        handler = InstallPackagesHandler(mock_app, mock_request)
        handler.get_json_body = MagicMock(
            return_value={
                "slug": "test_env",
                "packages": [],
                "upgradePip": 0,
                "systemSitePackages": 1,
            }
        )
        handler.finish = MagicMock()
        handler.current_user = "test_user"
        handler.post()
        res_data = {"status": 200, "message": "No package(s) provided."}
        handler.finish.assert_called_once_with(json.dumps(res_data))

    @pytest.mark.skip(reason="Need to fix this test")
    @patch("jupyter_environment_manager.envs_pkgs.threading.Thread")
    def test_post_with_packages(self, mock_thread, mock_app, mock_request):
        """Test InstallPackagesHandler.post method with packages."""
        handler = InstallPackagesHandler(mock_app, mock_request)
        handler.get_json_body = MagicMock(
            return_value={
                "slug": "test_env",
                "packages": ["package1", "package2"],
                "upgradePip": 0,
                "systemSitePackages": 1,
            }
        )
        handler.finish = MagicMock()
        handler.current_user = "test_user"
        handler.post()
        expected_data = {"status": 202, "message": "Started pip installs"}
        handler.finish.assert_called_once_with(json.dumps(expected_data))
        mock_thread.assert_called_once()

    @pytest.mark.skip(reason="Need to fix this test")
    @patch("jupyter_environment_manager.envs_pkgs.subprocess.run")
    @patch(
        "jupyter_environment_manager.envs_pkgs.which_python", return_value="/home/dev/.local/bin"
    )
    @patch("jupyter_environment_manager.envs_pkgs.set_include_sys_site_pkgs_value")
    @patch("jupyter_environment_manager.envs_pkgs.python_paths_equivalent", return_value=False)
    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"some": "data"}')
    def test_install_packages(
        self,
        mock_file_open,
        mock_exists,
        mock_python_paths_equivalent,
        mock_set_include_sys_site_pkgs_value,
        mock_which_python,
        mock_subprocess_run,
        mock_app,
        mock_request,
    ):
        """Test InstallPackagesHandler.install_packages method."""
        slug = "test_env"
        slug_path = os.path.join(str(DEFAULT_LOCAL_ENVS_PATH), slug)
        packages = ["package1", "package2"]
        upgrade_pip = False
        system_site_packages = True

        mock_subprocess_run.side_effect = [
            MagicMock(returncode=0, stdout=b"pip upgrade success", stderr=b""),
            MagicMock(returncode=0, stdout=b"install success", stderr=b""),
        ]

        InstallPackagesHandler.install_packages(
            slug, slug_path, packages, upgrade_pip, system_site_packages
        )

        mock_which_python.assert_called_once_with(slug)
        mock_python_paths_equivalent.assert_called_once_with(
            "/home/dev/.local/bin", "/home/dev/miniconda3/bin/python"
        )
        mock_set_include_sys_site_pkgs_value.assert_any_call(
            False, os.path.join(slug_path, "pyenv", "pyvenv.cfg")
        )
        mock_set_include_sys_site_pkgs_value.assert_any_call(
            True, os.path.join(slug_path, "pyenv", "pyvenv.cfg")
        )
        mock_subprocess_run.assert_any_call(
            [
                "/home/dev/.local/bin",
                "-m",
                "pip",
                "install",
                "-r",
                os.path.join(slug_path, "reqs_tmp.txt"),
            ],
            capture_output=True,
            check=False,
        )


class TestUninstallPackageHandler:
    """Test UninstallPackageHandler class."""

    def test_post_with_no_package(self, mock_app, mock_request):
        """Test UninstallPackageHandler.post method with no package."""
        handler = UninstallPackageHandler(mock_app, mock_request)
        handler.get_json_body = MagicMock(return_value={"slug": "test_env", "package": None})
        handler.finish = MagicMock()
        handler.current_user = "test_user"
        handler.post()
        expected_data = {"status": 400, "message": "No package provided."}
        handler.finish.assert_called_once_with(json.dumps(expected_data))

    @pytest.mark.skip(reason="Need to fix this test")
    @patch("jupyter_environment_manager.envs_pkgs.threading.Thread")
    def test_post_with_package(self, mock_thread, mock_app, mock_request):
        """Test UninstallPackageHandler.post method with package."""
        handler = UninstallPackageHandler(mock_app, mock_request)
        handler.get_json_body = MagicMock(return_value={"slug": "test_env", "package": "package1"})
        handler.finish = MagicMock()
        handler.current_user = "test_user"
        handler.post()
        expected_data = {"status": 202, "message": "Started pip uninstall"}
        handler.finish.assert_called_once_with(json.dumps(expected_data))
        mock_thread.assert_called_once()
