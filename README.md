# todo-list-api

FastAPI and MariaDB implementation of a simple todo list. Each todo list item can have one parent list item, while each item can have many children. Items can be created, edited, checked as complete, and deleted. Item parents (immediate to root) can also be queried.

## Requirements

* Windows 10 with Powershell
* Python 3.6+
* MariaDB installed with user and password as "root", else see `main.py` TODOs
* Postman

## Setup

### Install sample database

TODO

### API checkout

Check out this repo then create a Python virtual environment at the project root, i.e.:

```py -m venv .\venv```

Activate the venv, also at the project root:

```.\venv\Scripts\activate.bat```

Install these libraries into the venv:
```
.\venv\Scripts\pip.exe install fastapi
.\venv\Scripts\pip.exe install uvicorn
.\venv\Scripts\pip.exe install mariadb
```

## To run locally

Ensure MariaDB is running on http://127.0.0.1:3306.

Run the FastAPI main.py on http://127.0.0.1:8000 from the project root:

```.\venv\Scripts\uvicorn.exe main:app --reload```

For documentation and sandbox for all available queries while the API is running, go to http://127.0.0.1:8000/docs.

Here are some example queries you can try on the sample database using curl or Postman:

| Action                          | Use                                         |
| ------------------------------- | ------------------------------------------- |
| Read all items | curl -X GET "http://127.0.0.1:8000/items" -H  "accept: application/json" |
| Read item with item_id 4         | curl -X GET "http://127.0.0.1:8000/items/4" -H  "accept: application/json" |