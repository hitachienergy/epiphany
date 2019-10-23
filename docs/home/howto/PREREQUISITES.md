## Run Epicli from Docker image

There are 2 ways to get the image, build it locally yourself or pull it from the Epiphany docker registry.

### Build Epicli image locally

1. Install the following dependencies:

    - Python 3.7
    - PIP
    - Pipenv
    - Docker

2. Open a terminal in `/core/src/epicli` and run:

    On Linux:

    ```bash
    ./build-docker.sh
    ```

    On windows:

    ```bash
    ./build-docker.bat
    ```
  
### Pull Epicli image from the registry

```bash
docker pull epiphanyplatform/epicli:TAG
```

*Check [here](https://cloud.docker.com/u/epiphanyplatform/repository/docker/epiphanyplatform/epicli) for the available tags.*

### Running the Epicli image

To run the image:

Locally build:

```bash
docker run -it -v LOCAL_DIR:/shared --rm epicli
```

Pulled:

```bash
docker run -it -v LOCAL_DIR:/shared --rm epiphanyplatform/epicli:TAG
```

*Check [here](https://cloud.docker.com/u/epiphanyplatform/repository/docker/epiphanyplatform/epicli) for the available tags.*

Where `LOCAL_DIR` should be replaced with the local path to the directory for Epicli input (SSH keys, data yamls) and output (logs, build states).

## Run Epicli directly from OS

*Note: Epicli will only run on Lixux or MacOS and not on Windows. This is because Ansible at this point in time does not work on Windows.*

1. To be able to run the Epicli from your local OS you have to install:

    - Python 3.7
    - PIP
    - Pipenv

2. Open a terminal in `/core/src/epicli` and run:

    ```bash
    pipenv install
    ```

    This will create a virtual Python 3.7 environment and install all needed dependencies.

3. Build the Epicli wheel:

    ```bash
    ./build-wheel.sh
    ```

4. Enter the virtual Python enviroment:

    ```bash
    pipenv shell
    ```

5. Install the Epicli wheel inside the virtual enviroment:

    ```bash
    pip install dist/epicli-VERSION-py3-none-any.whl
    ```

6. Verify the Epicli installation:

    ```bash
    epicli --version
    ```

    This should return the version of the CLI deployed.

Now you can use Epicli inside the created virtual environment.

## Epicli development

For setting up en Epicli development environment please refer to this dedicated document [here.](./../DEVELOPMENT.md)

## Note for Windows users

- Watch out for the line endings conversion. By default Git for Windows sets `core.autocrlf=true`. Mounting such files with Docker results in `^M` end-of-line character in the config files.
Use: [Checkout as-is, commit Unix-style](https://stackoverflow.com/questions/10418975/how-to-change-line-ending-settings) (`core.autocrlf=input`) or Checkout as-is, commit as-is (`core.autocrlf=false`). Be sure to use a text editor that can work with Unix line endings (e.g. Notepad++).

- Remember to allow Docker Desktop to mount drives in Settings -> Shared Drives

- Escape your paths properly:

  - Powershell example:
  ```bash
  docker run -it -v C:\Users\USERNAME\git\epiphany:/epiphany --rm epiphany-dev:
  ```
  - Git-Bash example:
  ```bash
  winpty docker run -it -v C:\\Users\\USERNAME\\git\\epiphany:/epiphany --rm epiphany-dev
  ```

- Mounting NTFS disk folders in a linux based image causes permission issues with SSH keys. When running either the development or deploy image:

1. Copy the certs on the image:

    ```bash
    mkdir -p ~/.ssh/epiphany-operations/
    cp /epiphany/core/ssh/id_rsa* ~/.ssh/epiphany-operations/
    ```
2. Set the propper permission on the certs:

    ```bash
    chmod 400 ~/.ssh/epiphany-operations/id_rsa*
    ```

## Note about proxies

To run Epicli from behind a proxy, enviroment variables need to be set.

When running directly from OS (upper and lowercase are needed because of an issue with the Ansible dependency):

  ```bash
  export http_proxy="http://PROXY_SERVER:PORT"
  export https_proxy="https://PROXY_SERVER:PORT"
  export HTTP_PROXY="http://PROXY_SERVER:PORT"
  export HTTPS_PROXY="https://PROXY_SERVER:PORT"
  ```

Or when running from a Docker image (upper and lowercase are needed because of an issue with the Ansible dependency):

  ```bash
  docker run -it -v POSSIBLE_MOUNTS... -e HTTP_PROXY=http://PROXY_SERVER:PORT -e HTTPS_PROXY=http://PROXY_SERVER:PORT http_proxy=http://PROXY_SERVER:PORT -e https_proxy=http://PROXY_SERVER:PORT --rm IMAGE_NAME
  ```
