# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for checking and updating environment's state/status file(s).

"""
import json
import threading

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core.services.environments.paths import get_env_path
from qbraid_core.services.environments.state import install_status_codes

from .config_logger import get_logger
from .symlink import apply_symlinks

logger = get_logger(__name__)


class InstallStatusHandler(APIHandler):
    """Handler for checking environment's install status."""

    @tornado.web.authenticated
    def get(self):
        """Return codes describing environment's install status."""
        slug = self.get_query_argument("slug")
        data = install_status_codes(slug)
        self.finish(json.dumps(data))


class PostInstallSetupHandler(APIHandler):
    """Handler for environment configurations after successful install."""

    @tornado.web.authenticated
    def post(self):
        """Update environment's install success status."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")
        if not slug:
            status = 400
            message = "Missing 'slug' in request data."
            logger.error(message)
        else:
            status_data = install_status_codes(slug)
            complete = status_data.get("complete", 0)
            success = status_data.get("success", 0)
            if complete == 1 and success == 1:
                slug_path = get_env_path(slug)
                venv_path = str(slug_path / "pyenv")
                thread = threading.Thread(target=apply_symlinks, args=(venv_path,))
                thread.start()
                status = 202
                message = f"Applying symlinks to environment {slug} in background."
                logger.debug(message)
            else:
                status = 400
                message = (
                    "Invalid request: install status values complete and success must be 1 (True)."
                )
                logger.error(message)
        self.finish(json.dumps({"status": status, "message": message}))
