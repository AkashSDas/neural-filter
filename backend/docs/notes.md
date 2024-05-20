# Notes

## Setup

Install `fastapi` and `uvicorn`. FastAPI is a modern web framework for building APIs with Python 3.6+ based on standard Python type hints. Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools.

```bash
pipenv install fastapi uvicorn
```

Get `pipenv` environment and venv paths:

```bash
pipenv --where # /neural-filter/backend
pipenv --venv # /.local/share/virtualenvs/backend-F9Iaey3e
```

## Basic Usage

Starting the app:

```bash
cd ./src
fastapi dev main.py
```
