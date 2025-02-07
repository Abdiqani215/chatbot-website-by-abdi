# Use an official Python image with necessary tools
FROM python:3.11

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential python3-dev

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the bot
CMD ["python", "your_bot_script.py"]
