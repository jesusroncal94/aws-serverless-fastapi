#!/usr/bin/env bash
# The one check agents and CI run before calling a change done.
set -euo pipefail
cd "$(dirname "$0")/.."

image=aws-serverless-fastapi-check
docker build --quiet --target dev -t "$image" .
docker run --rm --network none "$image" uv run ruff check src tests
docker run --rm --network none "$image" uv run pytest -q
