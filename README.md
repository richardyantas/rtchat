# Dockerizing Django with Postgres, Gunicorn, and Nginx

## Want to learn how to build this?

Check out the [tutorial](https://testdriven.io/dockerizing-django-with-postgres-gunicorn-and-nginx).

## An general overview

We use daphne that works with websockets in the channel layer using ASGI (Asyncronous server gateway interface )

nginx and gunicorn  explanation with diagram



### Development

Uses the default Django development server.

1. Rename *.env.dev-sample* to *.env.dev*.
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
    ```

    Git hooks such as pre-commit is added in this project, that executes flake8(linter) and black(formatter)
    
    ```sh
    ```

    Git hub actions description

    ```sh
    ```

### Production

Uses gunicorn + nginx.

1. Rename *.env.prod-sample* to *.env.prod* and *.env.prod.db-sample* to *.env.prod.db*. Update the environment variables.
1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.
