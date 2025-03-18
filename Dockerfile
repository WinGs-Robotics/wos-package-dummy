FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir betterproto websocket-client requests

COPY . .

ENTRYPOINT ["python3"]