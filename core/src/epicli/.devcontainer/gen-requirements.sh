#!/usr/bin/env bash
# Generate requirements.txt from poetry.lock.
poetry export --no-interaction --format=requirements.txt --without-hashes --output=./requirements.txt
