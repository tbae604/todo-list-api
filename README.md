# todo-list-api

FastAPI and MariaDB implementation of a simple todo list. Each todo list item can have one parent list item, while each item can have many children. Items can be created, edited, checked as complete, and deleted. Item parents (immediate to root) can also be queried.

## Requirements

* Windows 10 with Powershell
* Python 3.6+
* MariaDB
* Postman

## Setup

### Sample database

TODO

### API checkout

Check out this repo then create a Python virtual environment at the project root, i.e.:

```py -m venv .\venv```

Activate the venv, also at the project root:
```.\venv\Scripts\activate.bat```

Install FastAPI and uvicorn into the venv:
```
.\venv\Scripts\pip.exe install fastapi
.\venv\Scripts\pip.exe install uvicorn
```


## To run locally

Run the FastAPI main.py on http://127.0.0.1:8000 from the project root:
```.\venv\Scripts\uvicorn.exe main:app --reload```

Try the following queries in Postman:
* http://127.0.0.1:8000
* http://127.0.0.1:8000/items/5?q=somequery