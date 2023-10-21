# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Create the directory for uploaded files
RUN mkdir /app/uploads

# Add a non-root user named 'upload-handler-user'
RUN groupadd -r upload-handler-group && useradd -r -g upload-handler-group upload-handler-user

# Change the owner of the uploads directory to a non-root user (e.g., appuser)
RUN chown -R upload-handler-user:upload-handler-user /app/uploads

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 8000 to communicate with the FastAPI app
EXPOSE 8000

# Run the application as a non-root user
USER upload-handler-user

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]