#!/bin/sh

pip install -r requirements.txt -r requirements-test.txt

pytest
