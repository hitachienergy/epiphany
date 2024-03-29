# Python requirement management

## Setup

For package version and requirment management we currently use 2 different tools:

1. [Poetry](https://github.com/python-poetry/poetry) is used to version/manage/lockdown the direct dependencies for Epicli and to generate a `requirements.txt` used by [PIP](https://pypi.org/project/pip/).
2. [PIP](https://pypi.org/project/pip/) and the `requirements.txt` is used to provision the devcontainer and release containers.

The main reasons for this 2-way approach:

- Managing dependencies with PIP and a `requirements.txt` is a nightmare.
- We need `requirements.txt` to generate license information and documentation
- `requirements.txt` is used by BlackDuck scan to scan our license usage in the project from the package perspective.

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

1. Open a shell in your devcontainer in the `.devcontainer` folder.

2. Run the following to update the `license.py` and generate the `DEPENDENCIES.md` file:

    ```shell
    python gen-dependency-info.py YOUR-GITHUB-PAT
    ```

    For obtaining a GitHub Personal Access Token, check [here](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).
    Only `public\_repo` scope is required.

3. Copy the table content from the generated `DEPENDENCIES.md` to `epiphany\docs\home\COMPONENTS.md` replacing the content under the `Epicli Python dependencies` section. 
   Always check if the `DEPENDENCIES.md` entries have empty or `UNKNOWN` values in the table that might need manual additions.
