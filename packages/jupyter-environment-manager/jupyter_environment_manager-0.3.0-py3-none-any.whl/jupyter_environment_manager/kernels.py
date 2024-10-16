# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for managing IPython kernels.

"""

import json
from pathlib import Path
from typing import Any

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core.services.environments.kernels import add_kernels, get_all_kernels, remove_kernels
from qbraid_core.services.environments.paths import get_env_path

from .config_logger import get_logger

logger = get_logger(__name__)


def get_kernels() -> set[str]:
    """Get list of all installed kernels with valid executables."""
    kernelspec_dict: dict = get_all_kernels(exclude_invalid=True)
    return {k for k, _ in kernelspec_dict.items()}


class ToggleEnvKernelHandler(APIHandler):
    """Handler for activating/deactivating environment by adding/removing kernel."""

    @tornado.web.authenticated
    def post(self):
        """Activate/deactivate environment by adding/removing kernel"""
        input_data = self.get_json_body()
        slug = input_data.get("slug")
        if slug is None:
            status = 400
            message = "Missing 'slug' in request data."
            resp_data = {"status": status, "message": message}
            logger.error(message)
        else:
            slug_path = get_env_path(slug)
            resp_data = self.toggle_env_kernels(slug_path)

        self.finish(json.dumps(resp_data))

    @staticmethod
    def toggle_env_kernels(slug_path: Path | str) -> dict[str, Any]:
        """
        Toggle the state of kernels associated with an environment
        by either adding or removing them.

        """
        slug_path = Path(slug_path)
        kernels_path = slug_path / "kernels"
        if not kernels_path.is_dir():
            return {"status": 404, "message": "Kernels directory not found."}

        num_added, num_removed, num_failed = 0, 0, 0
        known_kernels = get_kernels()

        for kernel_file in kernels_path.iterdir():
            action = remove_kernels if kernel_file.name in known_kernels else add_kernels
            try:
                action(slug_path.name)
                if action == remove_kernels:
                    num_removed += 1
                else:
                    num_added += 1
            except Exception as err:
                logger.error(
                    "Failed to %s kernel %s: %s",
                    "remove" if action == remove_kernels else "add",
                    kernel_file.name,
                    err,
                )
                num_failed += 1

        parts = []
        if num_added > 0:
            parts.append(f"Added {num_added}")
        if num_removed > 0:
            parts.append(f"Removed {num_removed}")
        if num_failed > 0:
            parts.append(f"Failed to toggle {num_failed}")

        message = ", ".join(parts) + " kernel(s)."
        status = 200 if num_failed == 0 else 500
        logger.debug(message)
        return {"status": status, "message": message}
