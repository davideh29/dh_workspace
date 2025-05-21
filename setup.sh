#!/usr/bin/env bash
set -e
pip install -r requirements.txt
export PYTHONPATH="$(pwd)/src:${PYTHONPATH}"
echo "Environment configured. Run tests with: pytest"
