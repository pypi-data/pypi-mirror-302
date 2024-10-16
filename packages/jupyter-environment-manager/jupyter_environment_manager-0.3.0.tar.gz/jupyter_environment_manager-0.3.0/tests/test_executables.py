# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Tests for the jupyter_environment_manager exectuables module.

"""

import unittest
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import patch

from jupyter_environment_manager.executables import (
    check_python_env,
    get_python_executables,
    get_python_version,
    is_notebook_environment,
    parallel_check_envs,
)


class TestPythonEnvironmentHelpers(unittest.TestCase):
    """Tests for helper functions that interface with python executables."""

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_get_python_version_valid(self, mock_which, mock_run):
        """Test that the get_python_version function returns the correct version."""
        mock_which.return_value = True
        mock_run.return_value.stdout = "Python 3.8.5"
        mock_run.return_value.returncode = 0

        version = get_python_version(Path("/usr/bin/python3"))
        self.assertEqual(version, "3.8.5")

    @patch("subprocess.run")
    @patch("shutil.which")
    def test_get_python_version_invalid_executable(
        self, mock_which, mock_run
    ):  # pylint: disable=unused-argument
        """Test that the get_python_version function raises an error for an invalid executable."""
        mock_which.return_value = None

        with self.assertRaises(ValueError) as context:
            get_python_version(Path("/invalid/path/python"))
        self.assertEqual(
            str(context.exception), "Python executable not found: /invalid/path/python"
        )

    @patch("subprocess.run")
    def test_get_python_version_invalid_output(self, mock_run):
        """Test that the get_python_version function raises an error for invalid output."""
        mock_run.return_value.stdout = "Not a Python version"
        mock_run.return_value.returncode = 0

        with self.assertRaises(ValueError):
            get_python_version(Path("/usr/bin/python3"))

    @patch("subprocess.run")
    def test_is_notebook_environment_installed(self, mock_run):
        """
        Test that the is_notebook_environment function returns True
        for a notebook environment.

        """
        mock_run.return_value.returncode = 0

        result = is_notebook_environment(Path("/usr/bin/python3"))
        self.assertTrue(result)

    @patch("subprocess.run")
    def test_is_notebook_environment_not_installed(self, mock_run):
        """
        Test that the is_notebook_environment function returns False for
        a non-notebook environment.

        """
        mock_run.side_effect = CalledProcessError(1, "python")

        result = is_notebook_environment(Path("/usr/bin/python3"))
        self.assertFalse(result)

    @patch("jupyter_environment_manager.executables.is_notebook_environment")
    def test_check_python_env_invalid(self, mock_is_notebook):
        """Test that the check_python_env function returns None for an invalid environment."""
        mock_is_notebook.return_value = False

        version, path = check_python_env(Path("/invalid/env"))
        self.assertIsNone(version)
        self.assertIsNone(path)

    @patch("subprocess.run")
    @patch("jupyter_environment_manager.executables.parallel_check_envs")
    def test_get_python_executables(self, mock_parallel_check, mock_run):
        """
        Test that the get_python_executables function returns the correct
        conda and system executables.

        """
        mock_run.return_value.stdout = "base /opt/conda\n"
        mock_parallel_check.return_value = {"3.8.5": Path("/env1/bin/python")}

        result = get_python_executables()
        self.assertIn("system", result)
        self.assertIn("conda", result)

    @patch("jupyter_environment_manager.executables.check_python_env")
    def test_parallel_check_envs(self, mock_check_python_env):
        """
        Test that the parallel_check_envs function returns the correct
        version to path mappings.

        """
        mock_check_python_env.side_effect = [
            ("3.8.5", Path("/env1/bin/python")),
            ("3.9.0", Path("/env2/bin/python")),
        ]

        env_paths = [Path("/env1"), Path("/env2")]
        result = parallel_check_envs(env_paths)
        expected_result = {
            "3.8.5": Path("/env1/bin/python"),
            "3.9.0": Path("/env2/bin/python"),
        }
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
