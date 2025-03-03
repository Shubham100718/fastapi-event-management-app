# Use a slim Python image for production
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the application port
EXPOSE 5000

# Run Gunicorn with Uvicorn workers
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

