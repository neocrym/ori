#!/bin/bash
set -Eeuxo pipefail
poetry run isort --atomic --apply --recursive ori tests
poetry run black .
poetry run pylint ori
