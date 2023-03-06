# Django Product CRUD Viewpoints
This Django project provides views for managing products. It implements a Product model with fields for name, description, uuid, created, updated, logo, and rotate_duration.

The project uses Celery to handle the delayed task of loading the photo for the logo field and rotating the image 180 degrees. It also implements the ability to change a product only once and ensures adherence to PEP8 standards.

The app is deployed on AWS, and you can access it using this link: http://ec2-18-194-41-246.eu-central-1.compute.amazonaws.com/

## Requirements
- Git repository access for Max Alekseev (max@3dlook.me) and Denys Havryliv (denys.havryliv@3dlook.me)
- Project documentation in README.md
- Virtual environment (preferably pipenv -> used poetry)
- Migrations
- English language (comments and string constants)
- Proper logging of main processes

## Setup
- Clone the repository
- Create a virtual environment `using pipenv`
- Install dependencies with `poetry install`
- Run migrations with `python manage.py migrate`
- Start the development server with `python manage.py runserver`

## Used AWS Services:
- AWS EC2 - for deploying django app on linux instance (Used docker, nginx, gunicorn)
- AWS S3 BUCKET - for media files
- Amazon MQ - Used Rabbit MQ
- Amazon RDS - Used PostgreSQL

## API endpoints
- GET /products/ - list all products (with pagination)
- GET /products/[uuid]/ - retrieve a specific product by uuid
- POST /products/ - create a new product
- PUT /products/[uuid]/ - update an existing product
- DELETE /products/[uuid]/ - delete a product by uuid

## Testing
- Unit tests are implemented and can be run using python manage.py test.
