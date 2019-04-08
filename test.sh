#!/bin/sh
set -e

pip install -r requirements.txt -r requirements-dev.txt -r requirements-test.txt

flake8 --show-source --statistics

pytest
