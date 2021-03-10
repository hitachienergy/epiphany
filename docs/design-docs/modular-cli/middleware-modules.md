# Ansible based module

## Purpose

To provide separation of concern on middleware level code we need to have consistent way to produce ansible based modules.

## Requirements

There are following requirements for modules:
 * Allow two-ways communication with other modules via Statefile
 * Allow a reuse of ansible roles between modules

## Design

### Components
1. Docker – infrastructure modules are created as Docker containers so far so this approach should continue
2. Ansible – we do have tons of ansible code which could be potentially reused. Ansible is also a _de facto_ industry standard for software provisioning, configuration management, and application deployment.
3. Ansible-runner – do to need of automation we should use ansible-runner application which is a wrapper for ansible commands (i.e.: ansible-playbook) and provides good code level integration features (i.e.: passing of variables to playbook, extracting logs, RC and facts cache). It is originally used in AWX.
4. E-structures – we started to use e-structures library to simplify interoperability between modules.
5. Ansible Roles – we need to introduce more loosely coupled ansible code while extracting it from main epiphany code repository. To achieve it we need to utilize ansible roles in “ansible galaxy” way, which means each role should be separately developed, tested and versioned. To coordinate multiple roles between they should be connected in a modules single playbook. 
      
### Commands

Current state of understanding of modules is that we should have at least two commands:
1. Init – would be responsible to build configuration file for the module. In design, it would be exactly the same as “init” command in infrastructure modules.
2. Apply – that command would start ansible logic using following order:
   1. Template inventory file – command would get configuration file and using its values, would generate ansible inventory file with all required by playbook variables.
   2. Provide ssh key file – command would copy provided in “shared” directory key into expected location in container

There is possibility also to introduce additional “plan” command with usage of “—diff” and “—check” flags for ansible playbook but:
 * It doesn't look like required step like in terraform-based modules
 * It requires additional investigation for each role how to implement it. 
   
### Structure
Module repository should have structure similar to following:
 * Directory “cmd” – Golang entrypoint binary files should be located here.
 * Directory “resources” – would be root for [ansible-runner “main” directory](https://ansible-runner.readthedocs.io/en/latest/intro.html#runner-input-directory-hierarchy)
   * Subdirectory “project” – this directory should contain entrypoint.yml file being main module playbook. 
     * Subdirectory “roles” – this optional directory should contain local (not shared) roles. Having this directory would be considered “bad habit”, but it's possible.
 * Files in “root” directory – Makefile, Dockerfile, go.mod, README.md, etc.
