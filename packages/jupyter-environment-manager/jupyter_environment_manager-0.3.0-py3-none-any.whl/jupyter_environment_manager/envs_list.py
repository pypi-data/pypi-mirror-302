# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Handlers for aggregating environment and package list data.

"""
import asyncio
import configparser
import json
import os
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional

import tornado
from jupyter_server.base.handlers import APIHandler
from qbraid_core.services.environments.paths import (
    DEFAULT_LOCAL_ENVS_PATH,
    get_default_envs_paths,
    get_env_path,
    get_next_tmpn,
    get_tmp_dir_names,
    which_python,
)
from qbraid_core.services.environments.state import install_status_codes
from qbraid_core.services.environments.validate import is_valid_slug
from qbraid_core.system.executables import is_valid_python, python_paths_equivalent
from qbraid_core.system.packages import set_include_sys_site_pkgs_value

from .config_logger import get_logger
from .jobs import quantum_jobs_supported_enabled
from .kernels import get_kernels
from .symlink import apply_symlinks

logger = get_logger(__name__)


def _uri_to_filepath(uri: str) -> str:
    """Convert a file URI to a local file path."""
    if uri.startswith("file://"):
        return uri[len("file://") :]
    raise ValueError(f"Invalid URI: {uri}")


def extract_short_hash(pip_freeze_line: str) -> str:
    """
    Extracts the 7-character shortened hash from a pip freeze output line that includes a Git path.

    Args:
        pip_freeze_line (str): A line from pip freeze output containing a Git path.

    Returns:
        str: The 7-character shortened Git hash.

    Raises:
        ValueError: If no valid Git hash is found in the input.
    """
    # Regular expression to find the git hash in the provided string
    match = re.search(r"git\+https://.*@([a-fA-F0-9]{40})", pip_freeze_line)

    if match:
        # Extract the full 40-character hash and return the first 7 characters
        full_hash = match.group(1)
        return full_hash[:7]

    # If no hash is found, raise an error
    raise ValueError("No valid Git hash found in the input.")


def extract_package_version(pip_freeze_string: str) -> Optional[str]:
    """Extract the version of a package from a pip freeze string.
    Return None if the version cannot be extracted."""

    # semantic versioning pattern
    semver_pattern = r"(\d+\.\d+\.\d+)"
    match = re.search(semver_pattern, pip_freeze_string)
    if match:
        return match.group(1)

    # git repo editable mode install version pattern
    git_editable_pattern = (
        r"^-e\s+"
        r"git\+https:\/\/github\.com\/"
        r"[a-zA-Z0-9._-]+\/[a-zA-Z0-9._-]+\.git@"
        r"[a-fA-F0-9]{40}#"
        r"egg=[a-zA-Z0-9._-]+$"
    )
    if re.match(git_editable_pattern, pip_freeze_string):
        parts = pip_freeze_string.split("#egg=")
        git_url = parts[0].split(" ", 1)[-1]
        return extract_short_hash(git_url)

    try:
        return extract_short_hash(pip_freeze_string)
    except ValueError:
        pass

    try:
        # extract version from locally installed package setup file path
        maybe_uri = pip_freeze_string.split(" @ ")[1]
        filepath = _uri_to_filepath(maybe_uri).strip("\n")
        setup_cfg_path = os.path.join(filepath, "setup.cfg")
        config = configparser.ConfigParser()
        config.read(setup_cfg_path)
        return config.get("metadata", "version")
    except Exception as err:
        logger.error("Error extracting package version: %s", err)
    return None


def process_requirements_line(line: str) -> Optional[str]:
    """Process each line directly from pip freeze output."""
    requirement = line.strip()
    if not requirement:
        return None

    if len(requirement.split(" ")) == 3 and "@" in requirement:
        package, _, _ = requirement.partition(" @ ")
        if not package.strip():
            return None
        version = extract_package_version(requirement)
        if version is None:
            version = requirement.split(" ")[-1].strip("\n")
        requirement = f"{package}=={version}\n"
    elif requirement.startswith("-e"):
        _, _, package = requirement.partition("egg=")
        if not package.strip():
            return None
        version = extract_package_version(requirement)
        if version is None:
            return None
        requirement = f"{package.strip()}=={version.strip()}\n"

    if "==" in requirement:
        return requirement
    return None


def rewrite_requirements_file(reqs_txt: str, python: str) -> None:
    """Streamline pip freeze directly to requirements rewriting."""
    with open(reqs_txt, "w", encoding="utf-8") as file:
        with subprocess.Popen(
            [python, "-m", "pip", "freeze"], stdout=subprocess.PIPE, text=True
        ) as proc:
            if proc.stdout is not None:
                for line in proc.stdout:
                    processed_line = process_requirements_line(line)
                    if processed_line:
                        file.write(processed_line.rstrip("\n") + "\n")
            proc.wait()


def get_pip_list(reqs_txt: str) -> list[str]:
    """Read the final formatted list of packages."""
    try:
        with open(reqs_txt, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []


def put_pip_list(slug: str, system_site_packages: bool = True) -> list[str]:
    """Update/insert requirements.txt and return pip list."""
    python = which_python(slug)
    slug_path = str(get_env_path(slug))
    reqs_txt = os.path.join(slug_path, "requirements.txt")

    if is_valid_python(python) and not python_paths_equivalent(python, sys.executable):
        cfg = os.path.join(slug_path, "pyenv", "pyvenv.cfg")
        set_include_sys_site_pkgs_value(False, cfg)
        rewrite_requirements_file(reqs_txt, python)
        if system_site_packages:
            set_include_sys_site_pkgs_value(True, cfg)

    return get_pip_list(reqs_txt)


class PipListEnvironmentHandler(APIHandler):
    """Handler for managing environment package list data."""

    @tornado.web.authenticated
    def post(self):
        """Get pip list of environment."""
        input_data = self.get_json_body()
        slug = input_data.get("slug")
        system_site_packages = input_data.pop("systemSitePackages", None)
        system_site_packages_bool = (
            True if system_site_packages is None else bool(system_site_packages)
        )
        package_lst = put_pip_list(slug, system_site_packages=system_site_packages_bool)

        data = {}
        data["packages"] = package_lst

        self.finish(json.dumps(data))


class ListInstalledEnvironmentsHandler(APIHandler):
    """Handler for managing installed environment list data."""

    async def get_slug_data(
        self,
        slug_path: Path,
        uninstalling: Optional[set[str]] = None,
        kernels: Optional[set[str]] = None,
    ):
        """Get data for a single environment."""
        uninstalling = uninstalling or set()
        kernels = kernels or set()

        if not self.validate_slug_env(slug_path) or slug_path.name in uninstalling:
            return None

        slug = slug_path.name

        installed = [slug]
        active = []
        quantum_jobs = []
        quantum_jobs_enabled = []
        sys_python = []
        installing = self.check_install_status(slug)

        env_python = which_python(slug)
        if python_paths_equivalent(env_python, sys.executable):
            sys_python.append(slug)

        if self.is_active(slug_path, kernels):
            active.append(slug)

        try:
            supported, enabled = quantum_jobs_supported_enabled(slug)
            if supported:
                quantum_jobs.append(slug)
                if enabled:
                    quantum_jobs_enabled.append(slug)
        except Exception as err:
            logger.error("Error determining quantum jobs state for %s: %s", slug, err)

        if not installing:
            venv_path = str(slug_path / "pyenv")
            logger.debug("Checking / applying symlinks for %s", venv_path)
            thread = threading.Thread(target=apply_symlinks, args=(venv_path,))
            thread.start()

        env_data = {
            "installed": installed,
            "active": active,
            "quantumJobs": quantum_jobs,
            "quantumJobsEnabled": quantum_jobs_enabled,
            "sysPython": sys_python,
            "installing": installing,
        }

        return env_data

    async def get_environment_data(self, env_dir_path: Path, **kwargs):
        """Get data for all environments under a given environment path prefix."""
        if not env_dir_path.is_dir():
            return None

        tasks = [
            self.get_slug_data(slug_path, **kwargs)
            for slug_path in env_dir_path.iterdir()
            if slug_path.is_dir()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        installed: list[str] = []
        active: list[str] = []
        quantum_jobs: list[str] = []
        quantum_jobs_enabled: list[str] = []
        sys_python: list[str] = []
        installing: Optional[str] = None

        for result in filter(None, results):
            if isinstance(result, (Exception, BaseException)):
                logger.error("Error getting environment data: %s", result)
                continue
            installed.extend(result["installed"])
            environment_for_install = result["installing"]
            if environment_for_install and not installing:
                installing = environment_for_install
            active.extend(result["active"])
            quantum_jobs.extend(result["quantumJobs"])
            quantum_jobs_enabled.extend(result["quantumJobsEnabled"])
            sys_python.extend(result["sysPython"])

        environment_data = {
            "installed": installed,
            "active": active,
            "quantumJobs": quantum_jobs,
            "quantumJobsEnabled": quantum_jobs_enabled,
            "sysPython": sys_python,
            "installing": installing,
        }

        return environment_data

    @tornado.web.authenticated
    async def get(self):
        """Get data for all installed environments."""
        logger.debug("Getting installed environments data...")
        kernels = get_kernels()
        env_paths = get_default_envs_paths()
        uninstalling = self.uninstalling_envs()

        tasks = [
            self.get_environment_data(env_path, uninstalling=uninstalling, kernels=kernels)
            for env_path in env_paths
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        data = {
            "installed": [],
            "active": [],
            "installing": "",
            "quantumJobs": [],
            "quantumJobsEnabled": [],
            "sysPython": [],
        }

        for result in filter(None, results):
            if isinstance(result, Exception):
                logger.error("Error gathering environment data: %s", result)
                continue
            data["installed"].extend(result["installed"])
            if result["installing"] and not data["installing"]:
                data["installing"] = result["installing"]
            data["active"].extend(result["active"])
            data["quantumJobs"].extend(result["quantumJobs"])
            data["quantumJobsEnabled"].extend(result["quantumJobsEnabled"])
            data["sysPython"].extend(result["sysPython"])

        self.finish(json.dumps(data))

    @staticmethod
    def uninstalling_envs() -> set[str]:
        """Return set of environment slugs currently being uninstalled."""
        tmpd_names = get_tmp_dir_names(DEFAULT_LOCAL_ENVS_PATH)
        uninstalling: set[str] = set()

        for tmpd_name in tmpd_names:
            tmpdir = DEFAULT_LOCAL_ENVS_PATH / tmpd_name
            if tmpdir.is_dir():
                uninstalling.update(f.name for f in tmpdir.iterdir())

        return uninstalling

    @staticmethod
    def validate_slug_env(slug_path: Path) -> bool:
        """
        Return True if slug_path is a valid environment directory, False otherwise.
        If directory name is a valid slug, but does not contain a persistent state/status
        file, then it is moved to a tmp directory to be uninstalled. This is mainly a backstop
        for cancel install environment.

        """
        if not slug_path.is_dir():
            return False

        if not is_valid_slug(slug_path.name):
            return False

        persistent_files = [slug_path / "state.json", slug_path / "install_status.txt"]
        if any(file.exists() for file in persistent_files):
            return True

        if slug_path.parent == DEFAULT_LOCAL_ENVS_PATH:
            tmpd_names = get_tmp_dir_names(DEFAULT_LOCAL_ENVS_PATH)
            tmpn = get_next_tmpn(tmpd_names)
            rm_dir = DEFAULT_LOCAL_ENVS_PATH / tmpn
            rm_dir.mkdir(exist_ok=True)
            shutil.move(str(slug_path), str(rm_dir))

        return False

    @staticmethod
    def check_install_status(slug: str) -> Optional[str]:
        """Return slug if environment is installing, None otherwise."""
        try:
            install_data = install_status_codes(slug)
            return slug if install_data.get("complete") == 0 else None
        except KeyError as err:
            logger.error(
                "Missing 'complete' key in install data for slug: %s, Error: %s", slug, err
            )
            return None
        except Exception as err:
            logger.error("Error checking install status for slug: %s, Error: %s", slug, err)
            return None

    @staticmethod
    def is_active(slug_path: Path, kernels: set[str]) -> bool:
        """Return True if any env kernel is in the kernel set, False otherwise."""
        try:
            env_kernels_dir = slug_path / "kernels"
            if not env_kernels_dir.is_dir():
                return False

            for kernel in env_kernels_dir.iterdir():
                if kernel.name in kernels:
                    return True
            return False
        except Exception as err:
            logger.error("Error checking if environment kernel is active: %s", err)
            return False
