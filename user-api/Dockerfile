# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# create a env variable that can be used as a secret for the JWT token
RUN export JWT_SECRET_KEY=$(openssl rand -hex 32) && \
    echo $JWT_SECRET_KEY && \
    echo "JWT_SECRET_KEY=$JWT_SECRET_KEY" >> /etc/environment && \
    export $(cat /etc/environment | xargs)

# Expose port 8002 to communicate with the FastAPI app
EXPOSE 8002

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]