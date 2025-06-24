# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000 
EXPOSE 8001

# Command to run the application
CMD ["gunicorn", "capstone.wsgi:application", "--bind", "0.0.0.0:8000"]