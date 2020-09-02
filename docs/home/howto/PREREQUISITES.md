## Run Epicli from Docker image

There are 2 ways to get the image, build it locally yourself or pull it from the Epiphany docker registry.

### Build Epicli image locally

1. Install the following dependencies:

    - Docker

2. Open a terminal in the root directory of the Epiphany source code and run:

```bash
TAG=$(cat core/src/epicli/cli/version.txt.py)
docker build --file Dockerfile --tag epicli:${TAG} .
```

### Pull Epicli image from the registry

```bash
docker pull epiphanyplatform/epicli:TAG
```

Where `TAG` should be replaced with an existing tag.

*Check [here](https://cloud.docker.com/u/epiphanyplatform/repository/docker/epiphanyplatform/epicli) for the available tags.*

### Running the Epicli image

To run the image:

```bash
docker run -it -v LOCAL_DIR:/shared --rm epiphanyplatform/epicli:TAG
```

Where:
- `LOCAL_DIR` should be replaced with the local path to the directory for Epicli input (SSH keys, data yamls) and output (logs, build states),
- `TAG` should be replaced with an existing tag.

*Check [here](https://cloud.docker.com/u/epiphanyplatform/repository/docker/epiphanyplatform/epicli) for the available tags.*

## Epicli development

For setting up en Epicli development environment please refer to this dedicated document [here.](./../DEVELOPMENT.md)

## Important notes

### Note for Windows users

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

### Note about proxies

To run Epicli from behind a proxy, enviroment variables need to be set.

When running a development container (upper and lowercase are needed because of an issue with the Ansible dependency):

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

### Note about PostgreSQL preflight check

This reffers only to CentOS/Red Hat installations.

To prevent installation failure of PostgreSQL 10 server we are checking in preflight mode we are checking if previous 
installation has been installed from PostgreSQL official repository. If this has been installed from Software Collections
this will make Epiphany deployment fail in preflight mode. For more details please refer to [How to migrate from PostgreSQL installed from Software Collections to installed from PostgreSQL repository](./DATABASES.md#how-to-migrate-from-postgresql-installed-from-software-collections-to-installed-from-postgresql-repository)

### Note about custom CA certificates

In some cases it might be that a company uses custom CA certificates or CA bundles for providing secure connections. To use these with Epicli you can do the following:

#### Devcontainer

Note that for the comments below the filenames of the certificate(s)/bundle do not matter, only the extensions. The certificate(s)/bundle need to be placed here before building the devcontainer.

1. If you have one CA certificate you can add it here with the ```crt``` extension.
2. If you have multiple certificates in a chain/bundle you need to add them here individually with the ```crt``` extension and also add the single bundle with the ```pem``` extension containing the same certificates. This is needed unfortunally because not all tools inside the container accept the single bundle.

#### Epicli release container

If you are running Epicli from one of the prebuild release containers you can do the following to install the certificate(s):

  ```bash
  cp ./path/to/*.crt /usr/local/share/ca-certificates/
  chmod 644 /usr/local/share/ca-certificates/*.crt
  update-ca-certificates
  ```

If you plan to deploy on AWS you also need to add a seperate configuration for ```Boto3``` which can either be done by a ```config``` file or setting the ```AWS_CA_BUNDLE``` environment variable. More information about for ```Boto3``` can be found [here.](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
