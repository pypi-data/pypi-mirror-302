FROM python:3.10-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


ADD . /app
WORKDIR /app
RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"
RUN uv build
CMD ["uv", "run", "whiteduck"]