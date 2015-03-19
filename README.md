# Chrome Webstore Ranking


## Python app

Ubuntu 14.10, initial setup:

```
sudo apt-get install python-dev python-virtualenv postgresql postgresql-server-dev-all redis
```

```
python setup.py develop
```

## Get latest migrations

You need to create a postgres user/db:

```
createuser cwr -P # password cwr
createdb cwr cwr
```

```
. bin/activate
cd cwr/
python manage.py db upgrade head
```

## Run http server

Once done with the inital setup, run the server with:

```
. bin/activate
python cwr/manage.py runserver
```

[http://localhost:5000/](http://localhost:5000/)


## Run redis and celery

Celery is needed to run the tasks that fetch the data from Chrome Web Store.

```
redis-server --port 6380 & # or in a separate terminal
. bin/activate
celery worker -B -A cwr.app.celery --loglevel=INFO
```

## CSS/JS dev:

```
cd cwr/static/
sudo npm install -g grunt-cli bower
npm install
bower install
grunt
```
