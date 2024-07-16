# Dockerizing Chat App that includes technologies such as Django with Daphne(To work with websockets), Postgres, Redis, and Nginx

<!-- ## Want to learn how to build this?

Check out the [tutorial](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx). -->

## An general overview

We use daphne that works with websockets in the channel layer using ASGI (Asyncronous server gateway interface )

nginx and daphne  explanation with diagram

### General Dependencies:

1. Install conda(Only If you want to work without containers locally)
1. Docker and Docker compose for development and production

### Development

Uses the default Django development server.

1. Create *.env.dev* with this format and update the environment variables.
    ```sh
    DEBUG=1
    SECRET_KEY=foo
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    DJANGO_SETTINGS_MODULE=app.settings
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=hello_django_dev
    SQL_USER=hello_django
    SQL_PASSWORD=hello_django
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres
    
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@email.com
    DJANGO_SUPERUSER_PASSWORD=admin
    ```
1. Update the environment variables in the *docker-compose.yml* and *.env.dev* files.
1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

    ```sh
    $ docker-compose exec web python manage.py createsuperuser --noinput
    ```

    Run if you want to test more data, entering data in the dataentry.py file

    ```sh
    $ docker-compose exec  -T web ./manage.py shell <  dataentry.py

### Production

Uses daphne + nginx.

1. Create *.env.prod* with this format and update the environment variables.
    ```sh
    DEBUG=0
    SECRET_KEY=change_me
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 0.0.0.0 [::1]
    DJANGO_SETTINGS_MODULE=app.settingsdir.production
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=hello_django_prod
    SQL_USER=hello_django
    SQL_PASSWORD=hello_django
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@email.com
    DJANGO_SUPERUSER_PASSWORD=admin
    ```
2. Create *.env.prod.db* with this format and update the environment variables.
    ```sh
    POSTGRES_USER=hello_django
    POSTGRES_PASSWORD=hello_django
    POSTGRES_DB=hello_django_prod
    ```
3. Dockerfile description 
    In production

4. Build the images and run the containers:

    ```sh
    $ docker compose -f docker-compose.prod.yml up --build 
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.


### CI/CD


1. Quality Assurance

    ```sh
    $ Make Lint # -> pre-commit run --all-files
    ```
    This command execute this file
    ```sh
    repos:
    - repo: https://github.com/ambv/black
      rev: stable
      hooks:
        - id: black
          language_vesion: python3.11
          stages: [commit]
    - repo: https://github.com/PyCQA/flake8
    rev: 4.0.1
    hooks:
        - id: flake8
        args: ['--ignore=E203, E226, E501, E503, F403, F401, F405, C101, Q000, E2, E129, E402, B950, E302, E303']
        additional_dependencies:
            - flake8-bugbear
            - flake8-builtins
            - flake8-coding
            - flake8-import-order
            - flake8-polyfill
            - flake8-quotes
        stages: [commit]
    ```