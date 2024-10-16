# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    git \
    libpq-dev \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the SDK source code
COPY kubiya_sdk ./kubiya_sdk
COPY setup.py .
COPY README.md .

# Install the SDK
RUN pip install --no-cache-dir -e .

# Create a symlink to the CLI script
RUN ln -s /app/kubiya_sdk/cli.py /usr/local/bin/cli.py

# Make the CLI script executable
RUN chmod +x /usr/local/bin/cli.py
RUN chmod +x /app/kubiya_sdk/cli.py

# Set the entrypoint to the CLI script
ENTRYPOINT ["python", "/usr/local/bin/cli.py"]

# Use CMD to provide default arguments to the entrypoint
CMD ["--help"]
