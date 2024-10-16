# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Helper functions for managing system and conda environment Python executables.

"""
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from qbraid_core.system.executables import is_exe
from qbraid_core.system.versions import is_valid_semantic_version

from .config_logger import get_logger

logger = get_logger(__name__)


def get_python_version(executable: Optional[Path] = None) -> str:
    """
    Retrieves the semantic version of the Python executable or the default
    system Python if unspecified.

    Args:
        executable (Optional[Path]): Path to a Python executable or None for system Python.

    Returns:
        str: Semantic version of the Python executable.

    Raises:
        ValueError: If executable is invalid or version is not semantic.
        RuntimeError: If subprocess fails to retrieve the version.
    """
    if executable is None or str(executable) == sys.executable:
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    if shutil.which(executable) is None:
        raise ValueError(f"Python executable not found: {executable}")

    if sys.platform != "win32" and not is_exe(executable):
        raise ValueError(f"Invalid Python executable: {executable}")

    try:
        version_result = subprocess.run(
            [str(executable), "--version"], stdout=subprocess.PIPE, text=True, check=True
        )
    except subprocess.CalledProcessError as err:
        raise RuntimeError(f"Failed to get Python version for {executable}") from err

    output = version_result.stdout.strip()
    if not output.lower().startswith("python"):
        raise ValueError(f"Invalid Python executable: {executable}")

    version = output.split()[-1]

    if not is_valid_semantic_version(version):
        raise ValueError(f"Invalid Python version: {version}")

    return version


def is_notebook_environment(python_path: Path) -> bool:
    """
    Check if the specified Python environment has Jupyter Notebook and ipykernel installed.

    Args:
        python_path (Path): The path to the Python executable.

    Returns:
        bool: True if both packages are installed, False otherwise.
    """
    try:
        subprocess.run(
            [str(python_path), "-c", "import notebook; import ipykernel"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def check_python_env(env_path: Path) -> tuple[Optional[str], Optional[Path]]:
    """Check a single environment for the required Python executable and packages."""
    python_path = env_path / "bin" / "python"
    if not python_path.exists() or not is_notebook_environment(python_path):
        return None, None
    try:
        version = get_python_version(python_path)
        return version, python_path
    except (ValueError, RuntimeError):
        return None, None


def parallel_check_envs(env_paths: list[Path]) -> dict[str, Path]:
    """Check environments in parallel using multiple threads."""
    python_executables = {}
    with ThreadPoolExecutor() as executor:
        future_to_path = {executor.submit(check_python_env, path): path for path in env_paths}
        for future in as_completed(future_to_path):
            path = future_to_path[future]
            try:
                version, python_path = future.result()
                if version and python_path:
                    python_executables[version] = python_path
            except Exception as err:
                logger.error("%s generated an exception: %s", path, err)
    return python_executables


def get_python_executables(unique_versions: bool = True) -> dict[str, dict[str, Path]]:
    """
    Retrieves Python executables from system and Conda environments that
    have Jupyter Notebook and ipykernel installed. Optionally filters out
    duplicate Python versions across system and Conda environments.

    Args:
        unique_versions (bool): If True, duplicate Python versions are excluded.
            If False, includes all executables, regardless of duplicates.

    Returns:
        dict[str, dict[str, Path]]: Maps 'system' and 'conda' to dictionaries
            of Python versions and executable paths.
    """
    python_executables: dict[str, dict[str, Path]] = {"system": {}, "conda": {}}

    sys_python_path = Path(sys.executable)
    try:
        sys_python_version = get_python_version(sys_python_path)
        python_executables["system"][sys_python_version] = sys_python_path
    except (ValueError, RuntimeError) as err:
        logger.error("Error getting system Python version: %s", err)

    try:
        result = subprocess.run(
            ["conda", "env", "list"], stdout=subprocess.PIPE, text=True, check=True
        )
        lines = result.stdout.strip().split("\n") if result.stdout else []
    except subprocess.CalledProcessError:
        lines = []

    try:
        env_paths = [
            Path(line.split()[-1])
            for line in lines
            if line and not line.startswith("#") and len(line.split()) > 1
        ]

        conda_executables = parallel_check_envs(env_paths)
    except Exception as err:
        logger.error("Error getting Conda Python executables: %s", err)
        conda_executables = {}

    if unique_versions:
        try:
            seen_versions = set(python_executables["system"].keys())
            seen_versions = {".".join(version.split(".")[:2]) for version in seen_versions}
            for version, path in conda_executables.items():
                major_minor = ".".join(version.split(".")[:2])
                if major_minor not in seen_versions:
                    python_executables["conda"][version] = path
                    seen_versions.add(major_minor)
        except Exception as err:
            logger.error("Error filtering unique Python versions: %s", err)

    else:
        python_executables["conda"] = conda_executables

    return python_executables
