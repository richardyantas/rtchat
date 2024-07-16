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
    $ docker compose -f docker-compose.yml up --build --force-recreate
    ```

    Data for testing is created using the dataentry.py file:
    ```python
    from django.contrib.auth.models import User
    from chat.models import * 
    from users.models import *

    u1 = User.objects.create_user(
        "robert", 
        email="robert@email.com", 
        password="bareco3t@wer"
    )
    u2 = User.objects.create_user(
        "camilo", 
        email="camilo@email.com",
        password="bareco3t@wer"
    )

    pc = ChatGroup(group_name="public-chat")
    pc.save()

    g1 = GroupMessage(group=pc, 
                    author=u1, 
                    body="hello there?")
    g1.save()

    g2 = GroupMessage(group=pc, 
                    author=u2, 
                    body="whatsapp bro ..")
    g2.save()
    p1 = Profile.objects.get(pk=2)
    p1.image = "avatars/ape1.jpg" 
    p1.displayname = "roboto"

    p2 = Profile.objects.get(pk=3)
    p2.image = "avatars/ape2.jpg"
    p2.displayname = "dino"

    p1.save()
    p2.save()
    ```
    This file (dataentry.py) is executed from entrypoint.sh in  Dockerfile:

    ```sh
    #!/bin/sh
    if [ "$DATABASE" = "postgres" ]
    then
        echo "Waiting for postgres..."

        while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
        done

        echo "PostgreSQL started"
    fi
    python manage.py flush --no-input
    python manage.py migrate
    python manage.py createsuperuser --noinput
    python manage.py shell < dataentry.py
    exec "$@"

    ```


    Test it out at [http://localhost:8000](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.


    The following command help us to stop and remove containers and also remove network and volumes created before.

    ```sh
    $ docker compose -f docker-compose.yml down -v
    ```

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
    Test it out at [http://0.0.0.0:1337](http://0.0.0.0:1337). No mounted folders. To apply changes, the image must be re-built.

    The following command help us to stop and remove containers and also remove network and volumes created before.

    ```sh
    $ docker compose -f docker-compose.prod.yml down -v
    ```


### CI/CD


1. Quality Assurance
    
    Github actions help us to run CI on github environments.

    ```sh
    name: Quality Assurance
    on: [pull_request, workflow_call]

    jobs:
    quality-assurance:
        name: Quality Assurance
        runs-on: ubuntu-latest
        container: python:3.11.4-slim-buster

        services:
        db:
            image: postgres:15
            env:
            POSTGRES_DB: hello_django
            POSTGRES_USER: hello_django
            POSTGRES_PASSWORD: hello_django_dev

        steps:
        - name: Install Git
            run: apt-get update && apt-get install -y git
        
        - name: Verify Git installation
            run: git --version

        - uses: actions/checkout@v2
        
        - name: Give ownership
            run: git config --global --add safe.directory /__w/rtchat/rtchat
            
        - name: Debug repository contents
            run: |
            ls -la
            pwd
            git status

        - name: Install make
            run: apt-get update && apt-get install -y make            

        - name: Install Dependencies
            run: make install && make install-pre-commit

        - name: Lint
            run: make lint

        - name: Test
            run: make test
    ```
    
    Make Lint, help us to apply formatters(Black) and linters(Flake8) to our code.
    
    ```sh
    $ Make Lint # -> pre-commit run --all-files
    ```
    This above command execute the file `.pre-commit-config.yaml`

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
