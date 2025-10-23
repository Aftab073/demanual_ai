# Step 1: Use an official Python 3.11 image as the base
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
# This is done separately to leverage Docker's layer caching
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Step 4: Copy the rest of your backend code into the container
COPY backend/ .

# Step 5: Tell Docker what command to run when the container starts
# This starts the Uvicorn server, listening on all network interfaces
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
