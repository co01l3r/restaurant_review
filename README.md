# restaurant_review

a diary, store ratings and spending values at the restaurant, count total spending at the restaurant, calculate ratings, and set proper pricing tags from a summary of ratings from all users. Just backend.

#### how to use:
```virtualenv```
```python
$ virtualenv <env_name>
$ source <env_name>/bin/activate
(<env_name>) $ pip install -r path/to/requirements.txt

from project folder:

(<env_name>) $ python3 manage.py runserver
```

or via ```Docker```:

```shell
$ docker-compose up --build
```
alternatively, if you have a container already build-up:

```shell
$ docker-compose up
```
project will then be available at these hosts under port ```0.0.0.0:8000```:


to test app in docker, run tests like this while db container is up
```shell
$ docker-compose exec web python manage.py test
```

available API endpoints:
```shell
[
    "/api/token",
    "/api/token/refresh",
    "/api/customers",
    "/api/customers/<str:username>",
    "/api/restaurants",
    "/api/restaurants/<int:restaurant_id>",
    "/api/restaurants/create",
    "/api/restaurants/edit/<int:restaurant_id>",
    "/api/restaurants/delete/<int:restaurant_id>",
    "/api/restaurants/<int:restaurant_id>/reviews",
    "/api/restaurants/<int:restaurant_id>/reviews/create",
    "/api/restaurants/<int:restaurant_id>/reviews/edit/api/restaurants/<int:restaurant_id>/reviews",
    "/api/restaurants/<int:restaurant_id>/average-rating",
    "/api/restaurants/<int:restaurant_id>/pricing-category",
    "/api/reviews",
    "/api/reviews/<int:review_id>",
    "/api/visits",
    "/api/visits/<int:visit_id>",
    "/api/visits/<int:visit_id>/delete"
]
```
