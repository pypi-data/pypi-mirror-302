# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Initialize the backend server extension

"""
try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode:
    # https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs
    import warnings

    warnings.warn("Importing 'jupyter_environment_manager' outside a proper installation.")
    __version__ = "dev"

from .handlers import setup_handlers


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "@qbraid/jupyter-environment-manager"}]


# only required for labexes that provision a server extension as well
def _jupyter_server_extension_points():
    return [{"module": "jupyter_environment_manager"}]


def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    url_path = "jupyter-environment-manager"
    setup_handlers(server_app.web_app, url_path)
    server_app.log.info(f"Registered jupyter_environment_manager extension at URL path /{url_path}")


# For backward compatibility
load_jupyter_server_extension = _load_jupyter_server_extension
