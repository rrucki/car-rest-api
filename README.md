# Simple Car Rest API

## Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/rrucki/car-rest-api.git
```
And change your directory to:
```sh
cd car-rest-api
```

In `car-rest-api/` create `.env` file with a secret key, for example:

```sh
SECRET_KEY = 3!jkj%z)dj4*=pr3#5&#o+ub)nn(%i!j5by(npteq@r_690@zk
```

Migrate:

```sh
docker-compose run web python3 manage.py migrate
```
Build, create, start, and attach to containers for a service:

```sh
sudo docker-compose up
```
And navigate to `http://0.0.0.0:8000/cars/`.
