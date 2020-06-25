# Development

<!-- TOC -->

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Preparing the environment](#preparing-the-environment)
- [Supplying data to the devcontainer](#supplying-data-to-the-devcontainer)
- [Note for Windows users](#note-for-Windows-users)
- [Running and debugging](#running-and-debugging)  
- [Running unit tests](#running-unit-tests)
- [Running serverspec tests](#running-serverspec-tests)

<!-- /TOC -->

## Introduction

This document explains how to set up the preferred [VSCode](https://code.visualstudio.com/) development environment. While there are other options to develop Epiphany like [PyCharm](https://www.jetbrains.com/pycharm/), VSCode has the following advantages:

1. Epiphany is developed using many different technologies (Python, Ansible, Terraform, Docker, Jinja, YAML...) and VSCode has good tooling and extensions available to support everything in one IDE.

2. VSCode's [devcontainers](https://code.visualstudio.com/docs/remote/containers) allow us to quickly set up a dockerized development environment, which is the same for every developer regardless of development platform (Linux, MacOS, Windows).

*Note: More information when running the devcontainer environment on Windows or behind a proxy can be found [here](./howto/PREREQUISITES.md#important-notes).*

## Prerequisites

- [VSCode](https://code.visualstudio.com/)
- Docker-CE
  - [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows)
  - [MacOS](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
  - [Linux](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

*Note: VSCode devcontainers are not properly supported using Docker Toolbox on Windows. More info [here](https://github.com/microsoft/vscode-remote-release/issues/95).*

## Preparing the environment

1. Open the epicli project folder ```/epiphany/core/src/epicli/``` with VSCode.

2. VSCode will tell you that the workspace has recommended extensions:

    ![extensions](../assets/images/development/extensions.png)

    Press ```Install All``` and wait until they are all installed and then restart. During the extension installations the following popup might show up:

    ![devcontainer](../assets/images/development/devcontainer.png)

    Do **NOT** do that at this point. First you must restart VSCode to activate all extensions which were installed.

3. After restarting VSCode the popup to re-open the folder in a devcontainer will show again. Press ```Reopen in Container``` to start the build of the devcontainer. You should get the following message:

    ![building](../assets/images/development/building.png)

    You can click ```details``` to show the build process.

4. After the devcontainer is built and started, VSCode will show you the message again that this workspace has recommended extensions. This time it is for the devcontainer. Again, press ```Install All``` to install the available extensions inside the devcontainer.

Now you have a fully working Epiphany development environment!

## Supplying data to the devcontainer

The entire working directory (```/epiphany/core/src/epicli/```) is mounted inside the container. We recommend to create an additional directory called ```clusters``` there, in which you house your data YAMLs and SSH keys. This directory is already added to the .gitignore. When executing epicli commands from that directory this is also where any build output and logs are written to.

## Note for Windows users

- Watch out for line endings conversion. By default GIT for Windows sets `core.autocrlf=true`. Mounting such files with Docker results in `^M` end-of-line character in the config files.
Use: [Checkout as-is, commit Unix-style](https://stackoverflow.com/questions/10418975/how-to-change-line-ending-settings) (`core.autocrlf=input`) or Checkout as-is, commit as-is (`core.autocrlf=false`).

- Mounting NTFS disk folders in a Linux based image causes permission issues with SSH keys. You can copy them inside the container and set the proper permissions using:

    ```shell
    mkdir -p /home/vscode/.ssh
    cp ./clusters/ssh/id_rsa* /home/vscode/.ssh/
    chmod 700 /home/vscode/.ssh && chmod 644 /home/vscode/.ssh/id_rsa.pub && chmod 600 /home/vscode/.ssh/id_rsa
    ```

This needs to be executed from the devcontainer bash terminal:

![terminal](../assets/images/development/terminal.png)

## Running and debugging

For debugging, open the VSCode's Debug tab:

![debug](../assets/images/development/debug.png)

By default there is one launch configuration called ```epicli```. This launch configuration can be found in ```/epiphany/core/src/epicli/.vscode/``` and looks like this:

  ```json
    ...

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

    ...
  ```

You can copy this configuration and change values (like below) to create different ones to suite your needs:

  ```json
    ...

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

    ...
  ```

In the ```args``` field you can pass an array of the arguments that you want epicli to run with.

To run a configuration, select it and press the run button:

![rundebug](../assets/images/development/rundebug.png)

For more information about debugging in VSCode, go [here](https://code.visualstudio.com/docs/editor/debugging).

## Running Python unit tests

The standard Python test runner fails to discover the tests so we use the ```Python Test Explorer``` extension. To run the unit tests, open the VSCode's Test tab and press the run button:

![unittests](../assets/images/development/unittests.png)

See the [Python Test Explorer](https://marketplace.visualstudio.com/items?itemName=LittleFoxTeam.vscode-python-test-adapter) extension page on how to debug and run individual tests.

You can also run the Python unit tests from a launch configuration called ```unit tests```

![rununittests](../assets/images/development/rununittests.png)

## Running serverspec tests

We maintain a set of serverspec tests that can be run to verify if a cluster is functioning properly. While it might not cover all cases at this point it is a good place to start.

The serverspec tests are integrated in Epicli. To run them you can extend the launch configuration ```epicli``` with the following arguments:

  ```json
    ...

    {
        "name": "epicli",
        "type": "python",
        "request": "launch",
        "program": "${workspaceFolder}/cli/epicli.py",
        "cwd": "${workspaceFolder}",
        "pythonPath": "${config:python.pythonPath}",
        "env": { "PYTHONPATH": "${workspaceFolder}" },
        "console": "integratedTerminal",
        "args": ["test", "-b", "${workspaceFolder}/clusters/buildfolder/", "-g", "postgresql"]
    },

    ...
  ```

Where the ```-b``` argument points to the build folder of a cluster. The ```-g``` argument can be used to execute a subset of tests and is optional. Omitting ```-g``` will execute all tests.

## Epicli Python dependencies

Information about how to manage the Epicli Python dependencies can be found [here.](../../core/src/epicli/.devcontainer/requirements.md#python-requirement-management)
