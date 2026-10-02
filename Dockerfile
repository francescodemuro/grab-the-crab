FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml README.md ./
COPY src ./src
RUN python -m pip install --no-cache-dir build && python -m build --wheel

FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /opt/grab-the-crab
COPY requirements/demo-py312.txt /tmp/demo-requirements.txt
COPY --from=builder /build/dist/*.whl /tmp/
RUN python -m pip install --no-cache-dir -r /tmp/demo-requirements.txt \
    && python -m pip install --no-cache-dir --no-deps /tmp/*.whl \
    && rm -rf /tmp/*.whl /tmp/demo-requirements.txt \
    && useradd --create-home --uid 10001 crab
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/readyz', timeout=3)"
CMD ["python", "-m", "uvicorn", "adaptive_response.web_app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
