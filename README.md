# Holiday planner backend

A server built with Django and the Django REST framework and a postgres database, both served in containers with docker compose.

My strategy was to build it as minimal as possible but still prepare it for production and maintain a good structure. I added endpoints and serializers for creating and getting but not for updating. The server is served with production environment in mind, with gunicorn and uvicorn and env variables form a `.env` file. There is however no logging, tracing, rate limiting or caching added.

The tests are not comprehensive but just to prove that I thought of different types of tests, of both unit tests and E2E. I would have tested the serializers more if I spent more time on the project. Making sure all edge cases are accounted for, in terms of validation and creation when it fails in different ways. For example creating a schedule with an invalid destination ID will probably cause issues. The tests would be run in docker before a deploy but has to be run manually in this project.

For the country I made latitude and longitude Decimalfields but I send them as strings to avoid inaccurate floating-point representations. I added order as a field in the background but it's being set automatically and is not exposed to the user, it would need some more handling and possibly reworking to work with editing. I used the AbstractUser to be able to support login in the future. I tried to think of having a good model separation in the backend. I probably would have separated the create schedule if I had some more time. It's doing too much and the input is too large and difficult to validate. I would have built one endpoint for just creating the schedule, where I send in the name only and create the id and created_at. And then you add destinations to the schedule through a POST at `schedules/destinations/`. The naming isn't very good, `routes` is better and `sights` maybe. That would follow REST better as well and would be easier to maintain.

I also added docs served at http://localhost:8000/api/schema/swagger-ui/ so that you can easily see what I have built. And simple smoke tests that can be run against the container.

I spent some time last Thursday thinking about what I wanted to build and how, and setting up the empty framework for a python/django project. Then I spent half a day (3-4h) today implementing the solution. And some time afterwards looking through it and writing this summary.

## Commands

### Run local tests

```sh
make test
```

### Start server

```sh
make serve
```

### Load server with dummy data for destinations and users

```sh
make load-dummy-data
```

### Run smoke tests

Terminal 1:

```sh
make serve
```

Terminal 2:

```sh
make smoke-tests
```

### Curl the server

```sh
curl -X GET 'http://localhost:8000/api/schedules/'
```

## Docs

Run `make serve` and go to:

- http://localhost:8000/api/schema/swagger-ui/

If you loaded the server with dummy data you query the server with user id 1-5 and destination id 1-8
