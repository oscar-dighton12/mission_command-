# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code, assets, and data files into the container
COPY . /app

# Expose the port that Dash runs on
EXPOSE 8050

# Command to run your application
CMD ["python", "app.py"]