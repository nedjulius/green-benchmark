# Web app

Currently it is using _Flask_ and _SQLite_.

## Getting started

1. Create virtual environment by running `python3 -m venv venv`
2. Activate venv by running `source venv/bin/activate`
3. Install dependencies with `pip install -r requirements.txt`

## Seeding the database

Before starting the application, seed the _SQLite_ database by running `python3 seed.py` while in virtual environment. **Warning**: seeding the database drops existing tables, so please make sure you don't have existing database before you run `seed` script.

## Starting the server

Once setup, run `python3 app.py` which will start the server.

If you add new dependencies, update requirements.txt with pip freeze > requirements.txt
