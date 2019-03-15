# Contributing

<!-- TOC -->

- [Contributing](#contributing)
  - [Welcome](#welcome)
  - [Workflow](#workflow)
  - [Security](#security)
  - [Group/Project Layouts](#group-project-layouts)

<!-- /TOC -->

## Welcome

All contributions are welcomed! Contributions can be anything including adding a bug issue. Anything that contributes in any way to Epiphany is considered a contribution and is welcomed.

## Workflow - TBD

## Security

Security *must* be built-in from day one on any merge request. Meaning, all changes must be able to pass security checks and that you have made sure not to include any hardcoded values such as keys, IDs, passwords, etc. By default it establishes perimeter security via firewall rules, IPTables, etc. but it also incorporates cross platform Kubernetes Secrets. Security enhancements will always be addressed. Epiphany will always comply with MCSR.

## Group/Project Layouts

Epiphany is broken into a hierarchy with `epiphany-platform` as a group in GitHub that contains folders such as `core`, `docs`, etc. Of course, you can use whatever IDE/editor you like but a good one for this is `Visual Studio Code`. It's based on the same foundation as `Atom` but seems to have more options and when dealing with Azure, it's actually easier.

```text

# Create a folder called epiphany
mkdir epiphany
cd epiphany

# Git clone each project in the epiphany group
git clone git@github.com/epiphany-platform/epiphany.git

# Folders inside epiphany-platform repository:
# core - Base core of Epiphany.
# data - Data.yaml files that define Epiphany clusters.
# docs - Epiphany platform documentation.
# examples - Examples of how to configure an Epiphany environment, add an application to the Epiphany platform, etc.

```
