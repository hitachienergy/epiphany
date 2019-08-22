# Development

<!-- TOC -->

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Preparing the environment](#preparing-the-environment)
- [Supplying data to the devcontainer](#supplying-data-to-the-devcontainer)
- [Note for Windows users](note-for-Windows-users)
- [Running and debugging](#running-and-debugging)  
- [Running unit tests](#running-unit-testsugging)

<!-- /TOC -->

## Introduction

This document will explain how to setup the prefered [VSCode](https://code.visualstudio.com/) development environment. While there are other options to develop Epiphany like [PyCharm](https://www.jetbrains.com/pycharm/) VSCode has the following advantages:

1. Epiphany is developed using many different technologies (Python, Ansible, Terraform, Docker, Jinja, YAML...) and VSCode has good tooling and extensions available to support everything in one IDE.

2. VSCode`s [devcontainers](https://code.visualstudio.com/docs/remote/containers) allow us to quickly setup a dockerized development environment which is the same  for every developer regardless of development platform (Linux, MacOS, Windows).

## Prerequisites

- [VSCode](https://code.visualstudio.com/)
- Docker-CE
  - [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
  - [MacOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
  - [Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

Note: VSCode devcontainers are not properly supported using Docker Toolbox on Windows. More info [here](https://github.com/microsoft/vscode-remote-release/issues/95).

## Preparing the environment

1. Open the epicli project folder ```/epiphany/core/src/epicli/``` with VSCode.

2. VSCode will tell you that the workspace has recommanded extensions:

    ![Logical view architecture diagram](../assets/images/development/extensions.png)

    Press ```Install all``` and wait until they are all installed and then restart. During the extension installations the following popup might show up:

    ![Logical view architecture diagram](../assets/images/development/devcontainer.png)

    Do **NOT** do that at this point. First you must restart VSCode to activate all extensions which where installed.

3. After restarting VSCode the popup to re-open the folder in a devcontainer will show again. Press ```Reopen in Container``` to start the build of the devcontainer. You should get the following message:

    ![Logical view architecture diagram](../assets/images/development/building.png)

    You can click ```detail``` to show the build process.

4. After the devcontainer is done building and started VSCode will give you the message again that this workspace has recommanded extensions. This time it is for the devcontainer. Again press ```Install all``` to install the available extensions inside the devcontainer.

Now you have a fully working Epiphany development environment!

## Supplying data to the devcontainer

The entire working directory (```/epiphany/core/src/epicli/```)is mounted inside the container. We recommand to create an aditional directory called ```cluster``` there in which you house your data YAMLs and SSH keys. This directory is already added to the .gitignore. When executing epicli commands from that directory this is also where any build output and logs will be written to.

## Note for Windows users

- Watch out for line endings conversion. By default GIT for Windows sets `core.autocrlf=true`. Mounting such files with Docker results in `^M` end-of-line character in the config files.
Use: [Checkout as-is, commit Unix-style](https://stackoverflow.com/questions/10418975/how-to-change-line-ending-settings) (`core.autocrlf=input`) or Checkout as-is, commit as-is (`core.autocrlf=false`).

- Mounting NTFS disk folders in a linux based image causes permission issues with SSH keys. You can copy them inside the container and set the propper permissions using:

    ```shell
    mkdir -p /home/vscode/.ssh/
    cp ./cluster/ssh/id_rsa* /home/vscode/.ssh/
    chmod 400 /home/vscode/ssh/id_rsa*
    ```

This needs to be executed from the devcontainer bash terminal:

![Logical view architecture diagram](../assets/images/development/terminal.png)

## Running and debugging

For debugging open the VSCode debug tab:

![Logical view architecture diagram](../assets/images/development/debug.png)

Per default there is one launch configuration present called ```epicli```. This launch configuration can be found in ```/epiphany/core/src/epicli/.vscode/``` and looks like this:

  ```json
    "configurations": [
        {
            "name": "epicli",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/cli/epicli.py",
            "cwd": "${workspaceFolder}",
            "pythonPath": "${config:python.pythonPath}",
            "env": { "PYTHONPATH": "${workspaceFolder}" },
            "console": "integratedTerminal",
            "args": ["apply",  "-f",  "${workspaceFolder}/PATH_TO_YOUR_DATA_YAML"]
        }
    ]
  ```

You can copy this configuration and change the names like to create different ones to suite your needs:

  ```json
    "configurations": [
        {
            "name": "epicli",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/cli/epicli.py",
            "cwd": "${workspaceFolder}",
            "pythonPath": "${config:python.pythonPath}",
            "env": { "PYTHONPATH": "${workspaceFolder}" },
            "console": "integratedTerminal",
            "args": ["apply",  "-f",  "${workspaceFolder}/PATH_TO_YOUR_DATA_YAML"]
        },
        {
            "name": "epicli show version",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/cli/epicli.py",
            "cwd": "${workspaceFolder}",
            "pythonPath": "${config:python.pythonPath}",
            "env": { "PYTHONPATH": "${workspaceFolder}" },
            "console": "integratedTerminal",
            "args": ["--version"]
        }
    ]
  ```

In the ```args``` field you can pass an array of the arguments that you want epicli to run with.

To run a configuration select it and press the run button:

![Logical view architecture diagram](../assets/images/development/reundebug.png)

For more information about debugging in VSCode go [here](https://code.visualstudio.com/docs/editor/debugging).

## Running unit tests

To run the unit test open the test tab in VSCode:



The [Python Test Explorer](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter) extension will detect the tests properly and let you run and debug them.