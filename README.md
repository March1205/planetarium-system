# Planetarium Service API

This project provides an API to browse and book planetarium tickets. The API is built with Django and Django REST framework, and it includes features for user authentication, booking reservations, and managing planetarium shows.

## Features

- User registration and authentication
- Browse and book planetarium shows
- Manage reservations
- API documentation using drf-spectacular
- Protected data: Only staff can see other people's reservations

## Prerequisites

- Docker
- Docker Compose

## Environment Variables

Create a `.env` file in the root directory of the project. You can use the `.env.example` file as a template:

1. Copy the `.env.example` file to a new file named `.env`:

    ```sh
    cp .env.example .env
    ```

2. Update the `.env` file with your own values:

    ```env
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_USER=your_postgres_user
    POSTGRES_DB=your_postgres_db
    POSTGRES_HOST=db
    POSTGRES_PORT=5432
    PGDATA=/var/lib/postgresql/data
    SECRET_KEY=your_secret_key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost
    ```


## Setting Up the Project
1. Clone the Repository

```sh
git clone https://github.com/yourusername/planetarium_system.git
cd planetarium_system
```
2. Build and Run the Docker Containers
```sh
docker-compose build
docker-compose up
```
3. Run Database Migrations
```sh
docker-compose exec planetarium python manage.py migrate 
```
4. Load Initial Data (if any)
```sh
docker-compose exec planetarium python manage.py loaddata planetarium_db_data.json 
```
5. Access the Application

Your application should be running on `http://localhost:8001`.

Access the API documentation at `http://localhost:8001/api/doc/swagger/`.


## Running Tests
To run the tests, use the following command:

```sh
docker-compose exec planetarium python manage.py test
```

## Project Structure
- planetarium/ - Contains the planetarium app with models, views, serializers, and URLs.
- user/ - Contains the user app with custom user model, views, serializers, and URLs. 

## Additional Information
- Static Files: Static files are served from the static/ directory.
- Media Files: Media files are served from the media/ directory.
- Database: The project uses PostgreSQL as the database.
