# Use lightweight official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first (for efficient caching)
COPY requirements.txt .

# Install dependencies without cache to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend code into container
COPY . .

# Expose port 9000
EXPOSE 9000

# Run the Flask app
CMD ["python", "app.py"]