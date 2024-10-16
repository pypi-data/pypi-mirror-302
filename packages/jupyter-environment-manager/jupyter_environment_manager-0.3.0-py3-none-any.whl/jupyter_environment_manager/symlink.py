# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Helper functions for managing symbolic links to Python executables.

"""
import os
import sys
from pathlib import Path

from qbraid_core.system.executables import get_python_version_from_cfg, get_python_version_from_exe
from qbraid_core.system.versions import is_valid_semantic_version

from .config_logger import get_logger
from .executables import get_python_executables

logger = get_logger(__name__)


def extract_version_from_dir_name(directory_name: str, prefix: str) -> str:
    """
    Extracts the Python version number from a directory name.

    Args:
        directory_name (str): The name of the directory containing the Python version.
        prefix (str): The expected prefix of the directory name, usually 'python'.

    Returns:
        str: The extracted Python version number.

    Raises:
        ValueError: If the extracted version is not a valid semantic version.
    """
    version = directory_name[len(prefix) :]
    if not is_valid_semantic_version(version):
        raise ValueError(f"Invalid Python version: {version}")
    return version


def get_site_packages_python_version(venv_path: Path) -> str:
    """
    Get the version of the Python directory in the virtual environment. Assumes the directory
    structure of a Python virtual environment with the libraries stored in 'lib/python*'.

    Args:
        venv_path (Path): The path to the virtual environment.

    Returns:
        str: The semantic version of Python found in the virtual environment.

    Raises:
        FileNotFoundError: If no Python directories are found.
        ValueError: If no matching Python directory is found or multiple directories do not
                    match the expected Python version from configuration.
    """
    match_prefix = "python"
    python_dirs = sorted(p for p in venv_path.glob(f"lib/{match_prefix}*") if not p.is_symlink())
    if not python_dirs:
        raise FileNotFoundError("No Python directories found in the specified virtual environment.")

    if len(python_dirs) == 1:
        directory_name = python_dirs[0].name
        return extract_version_from_dir_name(directory_name, match_prefix)

    python_cfg_version = get_python_version_from_cfg(venv_path)
    if not python_cfg_version:
        raise ValueError("Python version not found in the configuration file.")

    expected_dir_name = match_prefix + python_cfg_version

    matching_dir = next((p.name for p in python_dirs if p.name == expected_dir_name), None)
    if matching_dir is not None:
        return extract_version_from_dir_name(matching_dir, match_prefix)

    raise ValueError(
        "Multiple Python directories found; none match the Python version "
        "specified in the configuration file."
    )


def remove_symlink(target_path: Path) -> None:
    """
    Remove a symlink or file at the target path. If the target path exists and
    is either a symlink or a regular file, it will be removed. If the target path
    is a directory or an unsupported file type, the function will raise an error.

    Args:
        target_path (Path): The path to the symlink or file to be removed.

    Raises:
        ValueError: If the target path is a directory or an unsupported file type.
    """
    if target_path.exists() or target_path.is_symlink():
        if target_path.is_dir():
            raise ValueError("Operation not supported for directories.")
        if not (target_path.is_symlink() or target_path.is_file()):
            raise ValueError(f"Unsupported file type at {target_path}")

        target_path.unlink()


def update_symlink(target_path: Path, new_target: Path | str, **kwargs) -> None:
    """
    Update a symlink to point to a new target.

    Args:
        target_path (Path): The path to the existing symlink or file.
        new_target (Path or str): The new path the symlink should point to.
        **kwargs: Additional keyword arguments for the symlink creation.
    """
    try:
        target_path.symlink_to(new_target, **kwargs)
    except OSError as err:
        logger.error("Error updating symlink from %s to %s: %s", target_path, new_target, err)


def update_pyvenv_cfg(pyvenv_cfg_path: Path, conda_exec_path: Path, conda_py_version: str) -> None:
    """
    Updates the 'home' and 'version' in a pyvenv.cfg file based on the given
    conda executable path and Python version.

    Args:
        pyvenv_cfg_path (Path): The pathlib.Path object pointing to the pyvenv.cfg file.
        conda_exec_path (Path): The pathlib.Path object pointing to the conda Python executable.
        conda_py_version (str): The Python version associated with the conda environment.
    """
    if pyvenv_cfg_path.exists():
        lines = pyvenv_cfg_path.read_text().splitlines()

        new_home = str(conda_exec_path.parent)

        updated_lines = []
        for line in lines:
            if line.startswith("home ="):
                updated_lines.append(f"home = {new_home}")
            elif line.startswith("version ="):
                updated_lines.append(f"version = {conda_py_version}")
            else:
                updated_lines.append(line)

        pyvenv_cfg_path.write_text("\n".join(updated_lines) + "\n")
    else:
        logger.error("pyvenv.cfg file not found: %s", pyvenv_cfg_path)


def create_python_version_symlink(venv_path: Path) -> None:
    """
    Create a symlink for the Python directory that matches the system's Python version
    if it differs from the version used in the virtual environment.
    """
    if not venv_path.exists():
        raise FileNotFoundError(f"Virtual environment directory does not exist: {venv_path}")

    python_exe_version = get_python_version_from_exe(venv_path)
    sys_py_version_parts = (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    sys_py_version_full = ".".join(map(str, sys_py_version_parts))

    # if the executables don't match, then this venv was created
    # from a different base python than what is currently active
    if python_exe_version is not None and sys_py_version_full != python_exe_version:
        return

    existing_py_version = get_site_packages_python_version(venv_path)
    existing_py_version_parts = tuple(int(part) for part in existing_py_version.split("."))
    num_parts = len(existing_py_version_parts)

    if num_parts < 2 or num_parts > 3:
        raise ValueError(f"Invalid Python version: {existing_py_version}")

    # If the directory already matches the system's
    # major and minor version, then no symlink is needed
    if existing_py_version_parts[:2] == sys_py_version_parts[:2]:
        return

    executables = get_python_executables()
    conda_exe = executables.get("conda")
    if not conda_exe:
        logger.error(
            "No conda executables found; cannot create symlink for %s", existing_py_version
        )
        return

    bin_path = venv_path / "bin"
    python_path = bin_path / "python"
    pyvenv_cfg_path = venv_path / "pyvenv.cfg"

    major, minor = existing_py_version_parts[:2]
    python_major_path = bin_path / f"python{major}"
    python_minor_path = bin_path / f"python{major}.{minor}"

    for conda_py_version, conda_exec_path in conda_exe.items():
        conda_version_parts = tuple(int(part) for part in conda_py_version.split("."))
        if existing_py_version_parts[:2] == conda_version_parts[:2]:
            remove_symlink(python_path)
            remove_symlink(python_major_path)
            remove_symlink(python_minor_path)
            update_symlink(python_path, conda_exec_path)
            update_symlink(python_major_path, "python")
            update_symlink(python_minor_path, "python")

            update_pyvenv_cfg(pyvenv_cfg_path, conda_exec_path, conda_py_version)
            return

    logger.error("No matching Python executable found for %s", existing_py_version)

    return


def create_lib64_symlink(venv_path: Path) -> None:
    """Create symlink from lib64 to lib in virtual environment."""
    pyenv_lib = venv_path / "lib"
    pyenv_lib64 = venv_path / "lib64"

    if pyenv_lib.exists() and not pyenv_lib64.exists():
        remove_symlink(pyenv_lib64)
        update_symlink(pyenv_lib64, "lib", target_is_directory=True)


def supports_symlink() -> bool:
    """Check if the current OS supports symlinks."""
    # POSIX compliant systems (Unix-like systems) support symlinks
    # Windows supports symlinks from Vista onwards, but creating them might require
    # administrator privileges unless Developer Mode is enabled on Windows 10 and later
    return os.name == "posix" or (sys.version_info >= (3, 2) and os.name == "nt")


def apply_symlinks(venv_path: Path | str) -> None:
    """Apply necessary symlinks to the virtual environment."""
    venv_path = Path(venv_path)
    can_symlink = supports_symlink()

    if can_symlink:
        try:
            create_python_version_symlink(venv_path)
        except Exception as err:
            logger.error("Error creating Python version symlink: %s", err)

        try:
            create_lib64_symlink(venv_path)
        except Exception as err:
            logger.error("Error creating lib64 symlink: %s", err)
