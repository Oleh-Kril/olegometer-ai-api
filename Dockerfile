# Use an official lightweight Python image.
FROM python:3.9-slim

# Prevent Python from writing .pyc files to disc and enable stdout/stderr logging.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory.
WORKDIR /app

# Install system dependencies if needed.
RUN apt-get update && apt-get install -y gcc

# Copy the requirements file and install Python dependencies.
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code.
COPY . /app/

# Expose port 8000 for the Django app.
EXPOSE 8000

# Run the Django API with gunicorn.
CMD ["gunicorn", "olegometer_ai_api.wsgi:application", "--bind", "0.0.0.0:8000"]
