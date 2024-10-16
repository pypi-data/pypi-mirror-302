# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for managing user configurations and other local data.

"""
import configparser
import json
import os
import threading
import time
from pathlib import Path
from typing import Any

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core.config import USER_CONFIG_PATH
from qbraid_core.system.generic import get_current_utc_datetime_as_string

from .config_logger import get_logger
from .executables import get_python_executables

logger = get_logger(__name__)


class UserConfigHandler(APIHandler):
    """Handler for managing user configurations and other local data."""

    @tornado.web.authenticated
    def get(self):
        """Get user's qBraid credentials and available Python executables."""
        credentials = self.read_qbraidrc()
        executables = get_python_executables()
        executables_data = self.summarize_python_executables(executables)

        config = {**credentials, **executables_data}
        self.finish(json.dumps(config))

    def read_qbraidrc(self):
        """Read the qbraidrc file and return the contents as a dictionary."""
        config = configparser.ConfigParser()

        # Dictionary to store the results
        result = {
            "email": os.getenv("JUPYTERHUB_USER"),
            "apiKey": os.getenv("QBRAID_API_KEY"),
            "refreshToken": os.getenv("REFRESH"),
            "url": "https://api.qbraid.com/api",
        }

        # Check if the file exists
        if not os.path.exists(USER_CONFIG_PATH):
            return result

        # Read the configuration file
        config.read(USER_CONFIG_PATH)

        # Extract email and refresh-token
        if "default" in config:
            result["url"] = config["default"].get("url", result["url"])
            result["email"] = config["default"].get("email", result["email"])
            result["apiKey"] = config["default"].get("api-key", result["apiKey"])
            result["refreshToken"] = config["default"].get("refresh-token", result["refreshToken"])

        return result

    @staticmethod
    def summarize_python_executables(executables: dict[str, dict[str, Path]]) -> dict[str, Any]:
        """
        Summarizes Python executables by creating a structured dictionary containing versions
        and paths from both system and conda sources.

        Args:
            executables (dict[str, dict[str, Path]]): A dictionary containing 'system' and 'conda'
                keys with nested dictionaries mapping Python versions to their executables.

        Returns:
            dict[str, any]: A dictionary with the following keys:
                - 'pythonVersions': List of all unique Python versions.
                - 'pythonVersionMap': Dict mapping each unique Python version to its str exec path.
                - 'systemPythonVersion': The version of Python from 'system' or None if not present.

        """
        python_versions = set()
        python_version_map = {}

        # Process system versions
        system_versions = executables.get("system", {})
        system_version = next(iter(system_versions), None)

        # Aggregate versions and map them to their paths
        for category in ["system", "conda"]:
            for version, path in executables.get(category, {}).items():
                python_versions.add(version)
                python_version_map[version] = str(path)

        return {
            "pythonVersions": sorted(python_versions),
            "pythonVersionMap": python_version_map,
            "systemPythonVersion": f"Python {system_version}",
        }

    @tornado.web.authenticated
    def post(self):
        """Save timestamp certificate file for isMount check."""
        home = Path(os.getenv("HOME") or Path.home())
        directory = home / ".qbraid" / "certs"
        directory.mkdir(parents=True, exist_ok=True)

        formatted_time = get_current_utc_datetime_as_string()
        filepath = directory / formatted_time

        # Create an empty file
        with filepath.open("w", encoding="utf-8"):
            pass  # The file is created and closed immediately

        thread = threading.Thread(target=self.delayed_file_delete, args=(str(filepath),))
        thread.start()

        self.finish(json.dumps({"filename": formatted_time}))

    def delayed_file_delete(self, filepath):
        """Delete a file."""
        time.sleep(5)
        try:
            Path(filepath).unlink()
        except (FileNotFoundError, OSError) as err:
            logger.error("Error deleting file: %s", err)
