# Bug_Manager
Backend of a bug tracking application made with django and django rest framework.

## Setup instructions
- Clone this repository
- Create a virtual environment & activate it
- Install the required python packages with the following commands
    ```sh
    $ cd Bug_Manager
    $ pip install -r requirements.txt
    ```
- Install and run redis-server (preferably version 6.0.5)
- Make migrations with the following commands
    ```sh
    $ python manage.py makemigrations
    $ python manage.py migrate
    ```
- Run the server with the following command
    ```sh
    $ python manage.py runserver
    ```
- On line 42 in settings.py file change the **_DEFAULT_PERMISSION_CLASSES_** from _backend.permissions.NotDisabled_ to _rest_framework.permissions.AllowAny_ in order to use the api on your local machine without authentication.
- Now visit [http://localhost:8000/backend](http://localhost:8000/backend) for API root