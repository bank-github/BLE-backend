# Use Python base image
FROM python:3.12.4-slim

# Set the working directory inside the container
WORKDIR /usr/src/app/FastAPI

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose port 8000 (default for uvicorn)
EXPOSE 8000

# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--reload"]
