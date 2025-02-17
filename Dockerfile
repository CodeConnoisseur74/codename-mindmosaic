# Use Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install `uv` directly using pip
RUN pip install --no-cache-dir uv

# Copy the pyproject.toml and uv.lock files into the container
COPY pyproject.toml uv.lock ./

# Create a virtual environment and synchronise dependencies
RUN uv sync

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Copy the wait-for-it script into the container from the project root
COPY wait-for-it.sh /app/wait-for-it.sh

# Make the script executable
RUN chmod +x /app/wait-for-it.sh

CMD ["sh", "-c", "wait-for-it db:5432 -- uv run uvicorn api.main:app --host 0.0.0.0 --port 8000"]
