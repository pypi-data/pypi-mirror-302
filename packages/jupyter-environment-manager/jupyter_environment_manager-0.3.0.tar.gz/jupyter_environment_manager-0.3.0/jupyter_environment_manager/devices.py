# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for checking device availability in current Lab image.

"""

import json
import subprocess

import tornado
from jupyter_server.base.handlers import APIHandler

from .config_logger import get_logger

logger = get_logger(__name__)


class GPUStatusHandler(APIHandler):
    """Handler for checking device availability in current Lab image."""

    @tornado.web.authenticated
    def get(self):
        """Checks if GPUs are available in current Lab image."""
        gpus_available = self.is_cuda_installed()
        data = {"gpusAvailable": gpus_available}
        self.finish(json.dumps(data))

    def is_cuda_installed(self) -> bool:
        """Return True if GPUs are enabled in this Lab image, False otherwise."""
        try:
            # Check nvidia-smi
            result = subprocess.run(
                ["nvidia-smi"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if result.returncode == 0:
                return True

            # Check nvcc version
            result = subprocess.run(
                ["nvcc", "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if result.returncode == 0 and "release" in result.stdout.decode("utf-8"):
                return True

        except (FileNotFoundError, OSError) as err:
            # This means that the command is not found, so CUDA is likely not installed.
            logger.error("Error checking nvidia-smi: %s", err)

        return False
