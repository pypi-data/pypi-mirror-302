# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

# pylint:disable=protected-access,unnecessary-lambda,too-many-arguments

"""
Tests for the jupyter_environment_manager configure module.

"""

import unittest
from unittest.mock import MagicMock, patch

from tornado.httputil import HTTPServerRequest
from tornado.web import Application

from jupyter_environment_manager.configure import UserConfigHandler


def get_handler(handler_class, *args, **kwargs):
    """Return handler instance."""
    app = Application()

    request = MagicMock(spec=HTTPServerRequest)
    request.connection = MagicMock()
    request.method = "GET"
    request.uri = "/"
    request.headers = {"Content-Type": "application/json"}
    request.arguments = {}
    request._transforms = []

    return handler_class(app, request, *args, **kwargs)


class TestUserConfigHandler(unittest.TestCase):
    """Tests for the UserConfigHandler class."""

    def setUp(self):
        """Set up test environment."""
        self.handler = get_handler(UserConfigHandler)

    @patch("os.path.exists")
    def test_read_qbraidrc_file_not_exists(self, mock_exists):
        """Test read_qbraidrc method when the file does not exist."""
        mock_exists.return_value = False
        result = self.handler.read_qbraidrc()
        self.assertIsNotNone(result)

    @patch("os.path.exists")
    @patch("builtins.open", read_data="[default]\n")
    def test_read_qbraidrc_file_without_keys(
        self, mock_file, mock_exists
    ):  # pylint: disable=unused-argument
        """Test read_qbraidrc method when the file exists but does not contain keys."""
        mock_exists.return_value = True
        result = self.handler.read_qbraidrc()
        self.assertIsNotNone(result)

    def test_summarize_python_executables(self):
        """Test summarize_python_executables method."""
        executables = {
            "system": {"3.8": "/usr/bin/python3.8"},
            "conda": {"3.9": "/home/user/miniconda3/bin/python3.9"},
        }
        result = self.handler.summarize_python_executables(executables)
        self.assertEqual(result["pythonVersions"], ["3.8", "3.9"])
        self.assertEqual(
            result["pythonVersionMap"],
            {"3.8": "/usr/bin/python3.8", "3.9": "/home/user/miniconda3/bin/python3.9"},
        )
        self.assertEqual(result["systemPythonVersion"], "Python 3.8")

    @patch("pathlib.Path.unlink")
    def test_delayed_file_delete_error(self, mock_unlink):
        """Test delayed_file_delete method with an error"""
        mock_unlink.side_effect = OSError
        self.handler.delayed_file_delete("/existing/file")
        mock_unlink.assert_called_once()

    def test_summarize_python_executables_system_only(self):
        """Test summarize_python_executables method with system Python only."""
        executables = {"system": {"3.8": "/usr/bin/python3.8"}}
        result = self.handler.summarize_python_executables(executables)
        self.assertEqual(result["pythonVersions"], ["3.8"])
        self.assertEqual(result["pythonVersionMap"], {"3.8": "/usr/bin/python3.8"})
        self.assertEqual(result["systemPythonVersion"], "Python 3.8")

    @patch("pathlib.Path.unlink")
    def test_delayed_file_delete_file_not_exists(self, mock_unlink):
        """Test delayed_file_delete method with a non-existent file."""
        mock_unlink.side_effect = FileNotFoundError
        self.handler.delayed_file_delete("/non/existent/file")
        mock_unlink.assert_called_once()


if __name__ == "__main__":
    unittest.main()
