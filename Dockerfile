FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
RUN mkdir -p /data/palace
CMD ["sh", "-c", "mempalace init /data/palace --yes 2>/dev/null || true && tail -f /dev/null"]
