# Use the official Python 3.7 Alpine image
FROM python:3.12.5-alpine

# Step 2: Set environment variables to prevent .pyc files and enable buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/
# COPY discord_leaderboards/ /app/discord_leaderboards

# Upgrade pip and install the requirements
RUN pip install --upgrade pip && pip install -r requirements.txt

# Command to run the application
CMD python3 -u /app/discord_leaderboards/app.py
