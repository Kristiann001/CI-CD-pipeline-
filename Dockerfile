# Use the official slim Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source
COPY app/ ./app/

# Expose the service port
EXPOSE 8000

# Run the Flask app
CMD ["python", "-m", "app.counter"]
