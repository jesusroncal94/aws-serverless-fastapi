FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS dependencies

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv export --frozen --no-dev --no-emit-project --format requirements-txt -o requirements.txt


FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS dev

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY src ./src
COPY tests ./tests
RUN uv sync --frozen

CMD ["uv", "run", "pytest", "-q"]


FROM public.ecr.aws/lambda/python:3.12 AS lambda

COPY --from=dependencies /app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt -t "${LAMBDA_TASK_ROOT}"

COPY src/shortener "${LAMBDA_TASK_ROOT}/shortener/"

CMD ["shortener.lambda_handler.handler"]
