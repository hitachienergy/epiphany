#!/usr/bin/env py
import subprocess

def main():
    return subprocess.call('mkdir -p tests/cli/results/ && python -m pytest ./tests/ --junit-xml=tests/cli/results/result.xml | tee tests/cli/results/result.txt', shell=True)

if __name__ == '__main__':
    exit(main())
