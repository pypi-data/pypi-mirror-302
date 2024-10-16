# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Configure the pytest plugin for the jupyter_environment_manager extension.

"""

import pytest

pytest_plugins = ("pytest_jupyter.jupyter_server",)


@pytest.fixture
def jp_server_config(jp_server_config):
    return {"ServerApp": {"jpserver_extensions": {"jupyter_environment_manager": True}}}
