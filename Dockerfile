FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -e .
RUN mkdir -p /data/palace
RUN mempalace init /data/palace
CMD ["tail", "-f", "/dev/null"]
