FROM python:3.11.4-alpine3.18
WORKDIR /app
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
COPY scanner-cli.py /app
ENV SCAN_ENDPOINT="scanner-api-service"
ENV SCAN_PORT="8000"
ENV SCAN_FUNCTION="scan"
ENV SCAN_INTERVAL="300"
ENV SCAN_IP="127.0.0.1"
CMD ["python3", "/app/scanner-cli.py"]
