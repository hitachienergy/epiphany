#!/usr/bin/env bash -eu

add_repo_from_script 'https://dl.2ndquadrant.com/default/release/get/10/rpm'
disable_repo '2ndquadrant-dl-default-release-pg10-debug'
