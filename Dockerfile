### Dockerfile to build a scanner-as-a-service image
FROM ubuntu:22.04

# Install the required packages
RUN apt update && \
    apt -y upgrade && \
    apt -y --no-install-recommends install python3 python3-pip nmap && \
    apt -y autoremove && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Install the required Python packages
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the scanner API
COPY ./scanner* /app

# Create a non-root user
RUN useradd -m scanner && chown -R scanner:scanner /app
USER scanner

# Run the scanner API
EXPOSE 8000
ENTRYPOINT [ "python3", "/app/scanner-api.py" ]
