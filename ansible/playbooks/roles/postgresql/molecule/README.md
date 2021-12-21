# Installation guide

## Requirements

- Internet connection
- Molecule [dependencies](https://molecule.readthedocs.io/en/latest/installation.html)
- Docker
- ansible-lint
- ansible with resolved systemd related [bug](https://github.com/ansible/ansible/issues/71528#issuecomment-729778048)

## Local Installation

```bash
pip install ansible
pip install 'molecule[docker]'
pip install ansible-lint
```

## Execution

### General

```bash
molecule test -s <scenario-name>
```

### Separate steps

```bash
molecule lint -s <scenario-name>
molecule converge -s <scenario-name>
molecule idempotence -s <scenario-name>
molecule verify -s <scenario-name>
```
