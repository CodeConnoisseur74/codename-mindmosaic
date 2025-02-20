FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_NO_INDEX=1 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install `uv` directly using pip
RUN pip install --no-cache-dir uv

# Install dependencies globally (avoiding virtual env issues)
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on
EXPOSE 8000

# Copy the wait-for-it script into the container from the project root
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

CMD ["sh", "-c", "/app/wait-for-it.sh db:5432 -- uv run uvicorn api.main:app --host 0.0.0.0 --port 8000"]
