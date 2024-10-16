# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Tests for the jupyter_environment_manager devices module.

"""

from unittest.mock import MagicMock, patch

import pytest  # type: ignore
from tornado.web import Application  # type: ignore

from jupyter_environment_manager.devices import GPUStatusHandler


class TestGPUStatusHandler:
    """Test GPUStatusHandler class."""

    @patch("subprocess.run")
    def test_is_cuda_installed_with_nvidia_smi_success(self, mock_subprocess_run):
        """Test is_cuda_installed method with nvidia-smi success."""
        mock_subprocess_run.return_value.returncode = 0

        application = Application()
        request = MagicMock()

        handler = GPUStatusHandler(application, request)
        assert handler.is_cuda_installed() is True

    @patch("subprocess.run")
    def test_is_cuda_installed_with_nvidia_smi_failure(self, mock_subprocess_run):
        """Test is_cuda_installed method with nvidia-smi failure."""
        mock_subprocess_run.return_value.returncode = 1

        application = Application()
        request = MagicMock()

        handler = GPUStatusHandler(application, request)
        assert handler.is_cuda_installed() is False

    @patch("subprocess.run")
    def test_is_cuda_installed_with_nvcc_version_success(self, mock_subprocess_run):
        """Test is_cuda_installed method with nvcc --version success."""
        mock_subprocess_run.side_effect = [
            MagicMock(return_value=MagicMock(returncode=1)),  # Mock failure for nvidia-smi
            MagicMock(
                return_value=MagicMock(returncode=0, stdout=b"nvcc: NVIDIA (R) Cuda compiler")
            ),  # Mock success for nvcc --version
        ]

        application = Application()
        request = MagicMock()

        handler = GPUStatusHandler(application, request)
        assert handler.is_cuda_installed() is False

    @patch("subprocess.run")
    def test_is_cuda_installed_with_nvcc_version_failure(self, mock_subprocess_run):
        """Test is_cuda_installed method with nvcc --version failure."""
        mock_subprocess_run.side_effect = [
            MagicMock(return_value=MagicMock(returncode=1)),
            MagicMock(return_value=MagicMock(returncode=1)),
        ]

        application = Application()
        request = MagicMock()

        handler = GPUStatusHandler(application, request)
        assert handler.is_cuda_installed() is False

    @patch("subprocess.run")
    def test_get_method_raises_runtime_error(self, mock_subprocess_run):
        """Test get method raises RuntimeError with invalid data."""
        mock_subprocess_run.return_value.returncode = 0

        application = Application()
        request = MagicMock()

        handler = GPUStatusHandler(application, request)
        with pytest.raises(RuntimeError):
            handler.get()
