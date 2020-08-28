# todo-list-api

FastAPI and MariaDB implementation of a simple todo list. Each todo list item can have one parent list item, while each item can have many children. Items can be created, edited, checked as complete, and deleted. Item parents (immediate only OR to the root) can also be queried.

## Requirements

* Windows 10 with Powershell
* Python 3.6+
* MariaDB installed with user and password as "root", else update the `!!! TODO` under Setup in `main.py`
* (optional) curl or Postman

## Setup

### Install sample database

Use `todo_list.sql` in this repo to import a sample database to your local MariaDB. This assumes user is "root", else use your different username and password at the prompt:

```mysql -u root -p todo_list < todo_list.sql```

The todo_list database represents this sample list: 

```
Venue
└-- Research potential venues
└-- Book venue  
└-- Pay for venue
    └-- Pay deposit 
    └-- Pay final invoice  
Food
└-- Appetizers
|   └-- Research catering companies
|   └-- Book catering company 
|   └-- Pay catering company
|       └-- Pay deposit 
|       └-- Pay final invoice 
└-- Cake
    └-- Research bakers 
    └-- Order from baker 
    └-- Pay final invoice
```

...represented in the todo_item table. Note that none of these items are "complete":

```
+---------+-----------------------------+----------+-----------+
| item_id | name                        | complete | parent_id |
+---------+-----------------------------+----------+-----------+
|       1 | Venue                       |        0 |      NULL |
|       2 | Research potential venues   |        0 |         1 |
|       3 | Book venue                  |        0 |         1 |
|       4 | Pay for venue               |        0 |         1 |
|       5 | Pay deposit                 |        0 |         4 |
|       6 | Pay final invoice           |        0 |         4 |
|       9 | Food                        |        0 |      NULL |
|      13 | Appetizers                  |        0 |         9 |
|      14 | Cake                        |        0 |         9 |
|      15 | Research bakers             |        0 |        14 |
|      16 | Order from baker            |        0 |        14 |
|      17 | Pay final invoice           |        0 |        14 |
|      18 | Research catering companies |        0 |        13 |
|      19 | Book catering company       |        0 |        13 |
|      20 | Pay catering company        |        0 |        13 |
|      21 | Pay deposit                 |        0 |        20 |
|      22 | Pay final invoice           |        0 |        20 |
+---------+-----------------------------+----------+-----------+
```


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

## Running locally

Ensure MariaDB is running on http://127.0.0.1:3306.

Run the FastAPI main.py on http://127.0.0.1:8000 from the project root:

```.\venv\Scripts\uvicorn.exe main:app --reload```

For documentation and sandbox for all available queries while the API is running, go to http://127.0.0.1:8000/docs.

Here are some example queries you can try on the sample database using curl or Postman:

| Action                          | Request                                     |
| ------------------------------- | ------------------------------------------- |
| Create new item with name "Test" and parent item whose id is 1 | curl -X POST "http://127.0.0.1:8000/items?name=Test&parent_id=1" -H  "accept: application/json" -d "" |
| Read all items | curl -X GET "http://127.0.0.1:8000/items" -H  "accept: application/json" |
| Read item with item_id 4         | curl -X GET "http://127.0.0.1:8000/items/4" -H  "accept: application/json" |
| Read only immediate parent of item_id 22 | curl -X GET "http://127.0.0.1:8000/items/22/parents?immediate_only=true" -H  "accept: application/json" |
| Read complete chain of parents of item_id 22 | curl -X GET "http://127.0.0.1:8000/items/22/parents?immediate_only=false" -H  "accept: application/json" |
| Update item with item_id 4 to be marked complete | curl -X PUT "http://127.0.0.1:8000/items/4?complete=true" -H  "accept: application/json" |
| Update item with item_id 4 to have name "Updated" and parent item whose id is 1 | curl -X PUT "http://127.0.0.1:8000/items/4?name=Updated&parent_id=1" -H  "accept: application/json" |
| Delete item with item_id 4 | curl -X DELETE "http://127.0.0.1:8000/items/4" -H  "accept: */*" |
