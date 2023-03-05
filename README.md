# Django Product CRUD Viewpoints
This is a Django project that provides views for managing products. The project implements a Product model with fields for name, description, uuid, created, updated, logo, and rotate_duration.

API endpoints include CRUD operations for the Product model, with pagination for the product list, and filtering to show which products have been modified.

The project uses Celery to handle the delayed task of loading the photo for the logo field and rotating the image 180 degrees. The project also implements the ability to change a product only once, and ensures adherence to PEP8 standards.

## Requirements
- Git repository access for Max Alekseev (max@3dlook.me) and Denys Havryliv (denys.havryliv@3dlook.me)
- Project documentation in README.md
- Virtual environment (preferably pipenv)
- Migrations
- English language (comments and string constants)
- Proper logging of main processes


## Setup
- Clone the repository
- Create a virtual environment using pipenv
- Install dependencies with pipenv install
- Run migrations with python manage.py migrate
- Start the development server with python manage.py runserver

## API endpoints
- GET /products/ - list all products (with pagination)
- GET /products/[uuid]/ - retrieve a specific product by uuid
- POST /products/ - create a new product
- PUT /products/[uuid]/ - update an existing product
- DELETE /products/[uuid]/ - delete a product by uuid

## Testing
- Unit tests are implemented and can be run using python manage.py test.
