# Irancell Microservice Tasks
#### This README file mostly focused on api service.

Project Info:
- **Language:** Python 3.10 or higher
- **Framework:** Django and Django Rest Framework
- **Virtualization:** Docker
- **Testing Framework:** Pytest


## Table of Contents

- [Project Setup](#project-setup)
- [Docker and Makefile Commands](#docker-and-makefile-commands)
- [Managing the Django Application](#managing-the-django-application)
- [Running Tests](#running-tests)
- [API Testing with Postman](#api-testing-with-postman)
- [Summary of commands](#summary-of-commands)
- [Contact Info](#contact-info)

## Project Setup

Before starting, ensure you have Docker and Docker Compose installed. With Docker, all dependencies and services (like PostgreSQL, Nginx) are containerized, simplifying the setup.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Python installed locally (for running isolated commands, optional)
- Make (optional, for using `Makefile` commands)

### Setup

1. Extract the project files or clone it from the repo:

    ```bash
    git clone https://github.com/f4rih/irancell-tasks
    ```
2. Create an `.env` file contains database settings for each service:

    ```bash
    POSTGRES_HOST=db
    POSTGRES_USER=user
    POSTGRES_PORT=5432
    POSTGRES_PASSWORD=password
    POSTGRES_DB=irancell
 
    ```

3. Build and run the Docker containers:
    ```bash
    make up
    ```

4. Apply database migrations:
    ```bash
    make migrate
    ```

Now, project should be accessible via `http://localhost`. Nginx serves as a reverse proxy to the Django application running with Gunicorn.

---

## Docker and Makefile Commands

I've used `Makefile` to simplify common Docker and Django commands.

- **Starting and Stopping Containers:**
  - `make up`: Builds and starts the Docker containers in detached mode.
  - `make down`: Stops and removes all containers and associated networks.
  - `make restart`: Stops, rebuilds, and starts containers.

- **Building and Logging:**
  - `make build`: Builds the Docker images without starting containers.
  - `make logs`: Follows and displays logs from all services.


---

## Managing the Django Application

The following commands help manage Django-related tasks:

- **Migrate Database**:
    ```bash
    make migrate
    ```

- **Create a Superuser**:
    ```bash
    make createsuperuser
    ```

- **Django Shell**:
    ```bash
    make shell
    ```

## Running Tests

To run tests with `pytest`, use:

```bash
make test
```
**I've used sqlite for testing database for simplicity, Feel free to change it inside the `test_settings.py`**

This command runs pytest inside the web container.

## API Testing with Postman

You can test the API endpoints using a provided Postman collection.


### Summary of Commands

| Command                | Description                           |
|------------------------|---------------------------------------|
| `make up`              | Start and build the Docker containers |
| `make down`            | Stop and remove the containers        |
| `make restart`         | Restart the Docker containers         |
| `make migrate`         | Apply Django migrations               |
| `make createsuperuser` | Create a Django superuser             |
| `make loaddata`        | Load initial data from fixtures       |
| `make test`            | Run the test suite with pytest        |
| `make logs`            | View logs for all services            |

## Contact info

If you have any further questions, please feel free to reach out to me at [farih@pm.me](mailto:farih@pm.me)

