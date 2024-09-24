# Use the official Python 3.7 Alpine image
FROM python:3.7-alpine

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Upgrade pip and install the requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

# Command to run the application
CMD ["python3", "app.py"]