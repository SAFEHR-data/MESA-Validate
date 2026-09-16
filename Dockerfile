FROM python:3.13-slim
SHELL ["/bin/bash", "-c"]

WORKDIR /app

ARG HTTP_PROXY
ENV HTTP_PROXY=$HTTP_PROXY
ENV HTTPS_PROXY=$HTTP_PROXY

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.11.28 /uv /uvx /usr/local/bin/

COPY requirements.txt pyproject.toml uv.lock README.md ./

RUN uv venv && source /app/.venv/bin/activate && uv sync && uv pip install -r requirements.txt

COPY Home.py schemas.yaml aic_logo.png auth.yaml .
COPY pages ./pages
COPY mesa_validate ./mesa_validate

CMD source /app/.venv/bin/activate && \
  python -m streamlit run Home.py --server.address=0.0.0.0 --server.port=8501 --server.headless=true
