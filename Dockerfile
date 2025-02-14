# Use Python 3.12 slim image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install `uv` directly using pip
RUN pip install --no-cache-dir uv

# Copy the pyproject.toml and uv.lock files into the container
COPY pyproject.toml uv.lock ./

# Create a virtual environment and synchronise dependencies
RUN uv venv && uv sync

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Copy the startup script into the container
COPY start.sh /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Use the script as the command to run
CMD ["/app/start.sh"]
