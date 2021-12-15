# Casting Agency API Backend

The Casting Agency API was built as a proof of concept to showcase knowledge learned through the Udacity Full Stock Nanodegree.  The API is fully functional and has tests to showcase the different endpoints, errors and roles within the application.  The application has two primary functions: to keep track of actors and to keep track of movies.  Authentication to the application is handled by Auth0.

## API endpoints, associated Roles and Users

## API endpoints
`get:actors` - Get list of actors \
`get:movies` - Get list of movies \
`add:actor` - Add actor  \
`delete:actor` - Delete actor \
`add:movie` - Add movie \
`delete:movie` - Delete movie \
`update:actor` - Update actor information \
`update:movie` - Update movie information 

## Roles
Casting Assistant - Can `get:actors` and `get:movies`\
Casting Directory - Can `get:actors`, `get:movies`, `add:actor`, `delete:actor`, `update:actor`, and `update:movie` \
Executive Producer - Can `get:actors`, `get:movies`, `add:actor`, `delete:actor`, `add:movie`, `delete:movie`, `update:actor`, and `update:movie`

## Users
For production use, users would sign up at [https://auth0.com/](Auth0) \

As this is a Proof of Concept and has no sensitive data, 3 users have been created to test the application as the provided tokens may run out.  Use the following to authenticate to auth0 for the API.\
Credentials - User:Pass
```
casting.assistant.ank@gmail.com:ILove2Assist!  - Casting Assistant role
casting.director.ank@gmail.com:I<32Direct4U! - Casting Director role
executive.producer.ank@gmail.com:ElJefe4ever! - Executive Producer role
```

## Important things to know for installation

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

### Running on Heroku
The `setup.sh` config file specifies the database name among other things.  `Procfile` and `setup.sh` will need to be configured to run on Heroku.

API is currently hosted at: `https://casting-agency-ank.herokuapp.com`

### Database setup
The database utilizes Postgresql.  The database will need to be created before the server can be used.  In testing and development it is recommended to drop the previous table and re-create.

To drop database:
`dropdb agency`

To create database:
`createdb agency`

### Note about running locally
The server is setup to run on Heroku.  if you are running locally, you will need to edit the `env.sh` file and update the DATABASE_URL to be a local server.  

### Server setup
```bash
source env.sh
source /path/to/pyenv/bin/activate
```

To run the server, execute:

```bash
flask run
```

## Testing the server
The file "source.sh" has tokens to test the application.  If the tokens are expired, refresh them and update the file then run `source source.sh`.

To test the API:
```bash
dropdb agency_test
createdb agency_test
python test_api.py
```