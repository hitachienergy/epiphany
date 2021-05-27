# Installation guide

## Requirements

- Internet connection
- Molecule [dependencies](https://molecule.readthedocs.io/en/latest/installation.html)
- Docker
- ansible-lint

## Installation

```bash
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
