# Python requirement management

## Current setup

For package version and requirment management we currently use 2 different tools:

1. [Pipenv](https://github.com/pypa/pipenv) is used to version/manage/lockdown the direct dependencies for Epicli and to generate a ```requirements.txt``` used by [PIP](https://pypi.org/project/pip/).
2. [PIP](https://pypi.org/project/pip/) and the ```requirements.txt``` is used to provision the devcontainer and build release wheels.

The main reasons for this 2-way approach:

- Pipenv had a 2 year gap in development leaving lots of issues unresolved:
  - Very slow environment instalation speeds
  - Connection and proxy issues while installing
  - Virtual environment management
- Pipenv currently does not support an easy way for building deployment wheels.
- Managing dependencies with PIP and a ```requirements.txt``` is a nightmare.

## How to manage packages

1. Open a shell in your devcontainer in the ```.devcontainer``` folder.
2. Then run the following to initialize the Pipenv environment:

    ```shell
    pipenv install --pre
    ```

    We use the ```--pre``` flag here because some dependency packages of ```azure-cli``` are marked as
    pre-release and Pipenv will otherwise complain.

3. Now use the following Pipenv commands to manage your packages:

    - ```pipenv update ...```
    - ```pipenv install ...```
    - ```pip uninstall ...```
  
    More info [here.](https://pipenv.pypa.io/en/latest/)

4. After that run the following to generate a new ```requirments.txt```:

    ```shell
    ./gen-requirements.sh
    ```

5. Now you can rebuild your devcontainer to use the new ```requirements.txt```

## How to update package license info and documentation

1. Update the ```license.py``` by running the following from the project root in your devcontainer:

    ```shell
    python gen-licenses.py YOUR-GITHUB-PAT
    ```

    For obtaining a GitHub Personal Access Token, check [here.](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).
    Only `public_repo` scope is required.

    This will also generate a ```DEPENDENCIES.md``` file with a table containing all packages and licensing information.

2. Copy the table content from the generated ```DEPENDENCIES.md``` to ```epiphany\docs\home\COMPONENTS.md``` replacing the content under the ```Epicli Python dependencies``` section.
