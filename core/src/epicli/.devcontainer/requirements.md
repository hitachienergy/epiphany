# Python requirement management

## Previous setup

For package version and requirment management we currently use 2 different tools:

1. [Pipenv](https://github.com/pypa/pipenv) is used to version/manage/lockdown the direct dependencies for Epicli and to generate a `requirements.txt` used by [PIP](https://pypi.org/project/pip/).
2. [PIP](https://pypi.org/project/pip/) and the `requirements.txt` is used to provision the devcontainer and build release wheels.

The main reasons for this 2-way approach:

- Pipenv had a 2 year gap in development leaving lots of issues unresolved:
  - Very slow environment instalation speeds
  - Connection and proxy issues while installing
  - Virtual environment management
- Pipenv currently does not support an easy way for building deployment wheels.
- Managing dependencies with PIP and a `requirements.txt` is a nightmare.

## Current setup (>= 0.10.0)

1. Pipenv has been replaced with [Poetry](https://github.com/python-poetry/poetry).
2. Everything else should work as before.

## How to manage packages

1. Open a shell in your devcontainer in the `.devcontainer` folder.

2. Then run the following command to install packages defined in `poetry.lock`:

    ```shell
    poetry install
    ```

3. Now use the following commands to manage your packages:

    - `poetry update ...`
    - `poetry install ...`
    - `pip uninstall ...`

    More info [here](https://python-poetry.org/docs/).

4. After that run the following to generate a new `requirements.txt`:

    ```shell
    ./gen-requirements.sh
    ```

5. Now you can rebuild your devcontainer to use the new `requirements.txt`.

## How to update package license info and documentation

1. Update the `license.py` by running the following from the project root in your devcontainer:

    ```shell
    python gen-dependency-info.py YOUR-GITHUB-PAT
    ```

    For obtaining a GitHub Personal Access Token, check [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).
    Only `public\_repo` scope is required.

    This will also generate a `DEPENDENCIES.md` file with a table containing all packages and licensing information.

2. Copy the table content from the generated `DEPENDENCIES.md` to `epiphany\docs\home\COMPONENTS.md` replacing the content under the `Epicli Python dependencies` section.
