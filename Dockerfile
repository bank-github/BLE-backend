# Use Python base image
FROM python:3.12.4

# Set the working directory inside the container
WORKDIR /usr/src/app/FastAPI

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose port 8000 (default for uvicorn)
EXPOSE 7777

# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "7777"]
