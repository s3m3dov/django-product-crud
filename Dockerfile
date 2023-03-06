# Use the official Python image as a parent image
FROM python:3.10-slim-bullseye

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY pyproject.toml /app/

# Install poetry
RUN pip install poetry

# Install the app's dependencies
RUN poetry config virtualenvs.create false
RUN poetry lock
RUN poetry install --only main --no-interaction --no-ansi

# Copy the rest of the application code into the container
COPY . /app/

# Set the environment variable for Django
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

# Expose the port on which the Django app will run
EXPOSE 8000

# Start the Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
