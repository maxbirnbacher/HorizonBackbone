# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install netcat
RUN apt-get update && apt-get install -y netcat

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 to communicate with the FastAPI app
EXPOSE 8000
EXPOSE 4000-5000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]