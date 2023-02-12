# Shop API

## Table of contents

* [General info](#general-info)
* [Dependencies](#dependencies)
* [Setup](#setup)

## General info

This project is submodule for another project, which is an online food store.
This submodule is a RESTful HTTP API, which is an CRUD-interface for shop
database.

## Dependencies

Project is created with Python 3.11.
Main project dependencies:

* sqlalchemy
* fastapi
* alembic
* asyncpg
* uvicorn
* python-dotenv

## Setup

To run this project at localhost, install all dependencies locally using poetry
and run it via uvicorn (after alembic migrations):

```
$ cd ../shop-api
$ poetry install
$ alembic upgrade head && uvicorn src.api.app:app --port 8000 --host 127.0.0.1
```