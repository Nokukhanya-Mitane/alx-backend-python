# Use Python 3.10 as base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app code
COPY . .

# Expose Django default port
EXPOSE 8000

# Default command to run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
