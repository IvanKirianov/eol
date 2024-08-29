# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5002 for k8s_scanner
EXPOSE 5002

# Command to run k8s_scanner
CMD ["python3", "k8s_scanner/k8s_scanner.py"]
