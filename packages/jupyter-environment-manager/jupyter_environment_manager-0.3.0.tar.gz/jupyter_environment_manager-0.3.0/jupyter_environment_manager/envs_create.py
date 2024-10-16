# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for creating custom environments.

"""
import json
import sys
import threading
from pathlib import Path

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core.services.environments.create import create_local_venv, create_qbraid_env_assets
from qbraid_core.services.environments.paths import DEFAULT_LOCAL_ENVS_PATH
from qbraid_core.services.environments.state import update_state_json
from qbraid_core.system.executables import is_valid_python

from .config_logger import get_logger

logger = get_logger(__name__)


class CreateCustomEnvironmentHandler(APIHandler):
    """Handler for creating custom environments."""

    @tornado.web.authenticated
    def post(self):
        """Create a new qBraid environment."""
        try:
            input_data = self.get_json_body() or {}

            slug: str = input_data["slug"]
            prompt: str = input_data["prompt"]
            display_name: str = input_data["kernelName"]
            env_name: str = input_data.get("name", prompt)
            image_data_url: str | None = input_data.get("image")
            python_exe: str | None = input_data.get("pythonExecPath")

            if python_exe is None or not is_valid_python(python_exe):
                python_exe = sys.executable

            slug_path: Path = DEFAULT_LOCAL_ENVS_PATH / slug
            local_resource_dir = slug_path / "kernels" / f"python3_{slug}"
            local_resource_dir.mkdir(parents=True, exist_ok=True)

            # create state.json
            update_state_json(slug_path, 0, 0)

            # create python venv
            thread = threading.Thread(
                target=create_local_venv, args=(str(slug_path), prompt, python_exe)
            )
            thread.start()

            # create kernel.json
            create_qbraid_env_assets(slug, env_name, display_name, str(slug_path), image_data_url)

            res_data = {"status": 202, "message": "Custom env setup underway"}
        except KeyError as err:
            logger.error("Missing required data: %s", err)
            res_data = {"status": 400, "message": str(err)}
        except Exception as err:
            logger.error("Error creating custom environment: %s", err)
            res_data = {"status": 500, "message": str(err)}

        self.finish(json.dumps(res_data))
