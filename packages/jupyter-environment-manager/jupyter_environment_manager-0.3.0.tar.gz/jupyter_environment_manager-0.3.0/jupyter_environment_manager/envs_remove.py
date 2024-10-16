# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for uninstalling/removing environments.

"""

import json
import shutil
import threading
import time

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core.services.environments.kernels import remove_kernels
from qbraid_core.services.environments.paths import (
    DEFAULT_LOCAL_ENVS_PATH,
    get_next_tmpn,
    get_tmp_dir_names,
)
from qbraid_core.services.environments.state import install_status_codes
from qbraid_core.system.filemanager import FileManager

from .config_logger import get_logger
from .kernels import get_kernels

logger = get_logger(__name__)


class UninstallEnvironmentHandler(APIHandler):
    """Handler for uninstalling environments."""

    @tornado.web.authenticated
    def post(self):
        """Remove environment's kernels and change slug directory
        to tmp so it can be deleted in the background."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")

        try:
            self.uninstall_env_kernels(slug)
        except Exception as err:
            logger.error("Failed to remove kernel specs for %s: %s", slug, err)

        try:
            thread = threading.Thread(target=self.remove_env_cycle, args=(slug,))
            thread.start()

            status = 202
            message = f"Uninstalling environment {slug}."
            logger.info(message)
        except Exception as err:
            status = 500
            message = f"Error uninstalling environment {slug}: {err}."
            logger.error(message)

        data = {"status": status, "message": message}
        self.finish(json.dumps(data))

    @staticmethod
    def uninstall_env_kernels(slug: str) -> None:
        """Remove environment's kernels from JupyterKernelSpecManager, if they exist."""
        kernelspec_path = DEFAULT_LOCAL_ENVS_PATH / slug / "kernels"

        if kernelspec_path.is_dir():
            kernels: set = get_kernels()
            for item in kernelspec_path.iterdir():
                if item.name in kernels:
                    remove_kernels(slug)

    @staticmethod
    def remove_env_cycle(slug: str) -> None:
        """Remove tmp directories in the background."""
        start = time.time()
        threader = FileManager()
        slug_path = DEFAULT_LOCAL_ENVS_PATH / slug
        status_codes = install_status_codes(slug)
        installing = status_codes.get("complete") == 0
        tmpd_names = get_tmp_dir_names(DEFAULT_LOCAL_ENVS_PATH)
        init_tmp_dirs = len(tmpd_names)
        num_cylces = 0
        sec_elapsed = 0

        while (
            num_cylces == 0
            or len(tmpd_names) > 0
            or installing
            and slug_path.is_dir()
            and sec_elapsed < 60
        ):
            if slug_path.is_dir() and (installing or num_cylces == 0):
                tmpn = get_next_tmpn(tmpd_names)
                rm_dir = DEFAULT_LOCAL_ENVS_PATH / tmpn
                if installing:
                    rm_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(slug_path, rm_dir)
                tmpd_names.append(tmpn)
                if num_cylces == 0:
                    init_tmp_dirs += 1

            for tmpd_name in tmpd_names:
                tmpdir = DEFAULT_LOCAL_ENVS_PATH / tmpd_name
                try:
                    threader.remove_tree(tmpdir)
                except Exception as err:
                    logger.error("Error removing directory %s: %s", tmpdir, err)

            # wait 5 seconds for each tmp rm to finish
            time.sleep(5)

            tmpd_names = get_tmp_dir_names(DEFAULT_LOCAL_ENVS_PATH)
            sec_elapsed = int(time.time() - start)
            num_cylces += 1

        num_threads = threader.counter()
        threader.join_threads()
        threader.reset_counter()

        logger.info(
            "Successfully uninstalled %d env(s) in %ds using %d threads "
            "over %d threaded remove cycles.",
            init_tmp_dirs,
            sec_elapsed,
            num_threads,
            num_cylces,
        )
