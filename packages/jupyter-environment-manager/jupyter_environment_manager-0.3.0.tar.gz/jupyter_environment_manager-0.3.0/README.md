# jupyter-environment-manager

[![Documentation](https://img.shields.io/badge/Documentation-DF0982)](https://docs.qbraid.com/lab/user-guide/environments)
[![PyPI version](https://img.shields.io/pypi/v/jupyter-environment-manager.svg?color=blue)](https://pypi.org/project/jupyter-environment-manager/)
[![GitHub](https://img.shields.io/badge/issue_tracking-github-blue?logo=github)](https://github.com/qBraid/community/issues)
[![Stack Overflow](https://img.shields.io/badge/StackOverflow-qbraid-orange?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/qbraid)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?logo=discord&logoColor=white)](https://discord.gg/TPBU2sa8Et)

JupyterLab extension for managing execution environments, packages, and kernels.

This extension is composed of a Python package named `jupyter_environment_manager` for the server extension and
an NPM package named `@qbraid/jupyter-environment-manager` for the frontend extension.

[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/qBraid/community.git)

## Installation & Setup

For the best experience, use the Environment Manager on [lab.qbraid.com](https://lab.qbraid.com).
Login (or [create an account](https://account.qbraid.com)) and follow instructions in [user guide](https://docs.qbraid.com/lab/user-guide/environments) to get started.

The Environment manager requires **Python 3.9 or greater**, and is compatible with **JupyterLab 4.x**.

### Local Install

The Environment Manager can be installed using pip:

```shell
pip install jupyter-environment-manager
```

### Local Setup

To use the Environment Manager locally, you must configure your qBraid account credentials:

1. Create a qBraid account or log in to your existing account by visiting [account.qbraid.com](https://account.qbraid.com/)
2. Copy your API Key token from the left side of your account page (see [docs](https://docs.qbraid.com/home/account)).
3. Save your API key using the [qbraid-cli](https://docs.qbraid.com/cli/api-reference/qbraid_configure):

```bash
pip install qbraid-cli
qbraid configure
```

The command above stores your credentials locally in a configuration file `~/.qbraid/qbraidrc`,
where `~` corresponds to your home (`$HOME`) directory.

Alternatively, the Environment Manager can discover credentials from environment variables:

```bash
export QBRAID_API_KEY='QBRAID_API_KEY'
```

> See also: [qBraid API Keys](https://docs.qbraid.com/home/account#api-keys), [Local configuration](https://docs.qbraid.com/cli/user-guide/overview#local-configuration)

## Community

- For feature requests and bug reports: [Submit an issue](https://github.com/qBraid/community/issues)
- For discussions, and specific questions about the Environment Manager, qBraid Lab, or
  other topics, [join our discord community](https://discord.gg/TPBU2sa8Et)
- For questions that are more suited for a forum, post to [StackOverflow](https://stackoverflow.com/questions/tagged/qbraid) with the `qbraid` tag.

## Launch on qBraid

The "Launch on qBraid" button (top) can be added to any public GitHub
repository. Clicking on it automaically opens qBraid Lab, and performs a
`git clone` of the project repo into your account's home directory. Copy the
code below, and replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub
info.

Use the badge in your project's `README.md`:

```markdown
[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git)
```

Use the badge in your project's `README.rst`:

```rst
.. image:: https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png
    :target: https://account.qbraid.com?gitHubUrl=https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
    :width: 150px
```
