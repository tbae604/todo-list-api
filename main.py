"""
FastAPI and MariaDB implementation of a simple todo list. Each todo list item can have one parent list item, while each item can have many children. Items can be created, edited, checked as complete, and deleted. Item parents (immediate to root) can also be queried. See README for more information.
"""

import sys
from typing import Optional

from fastapi import FastAPI, HTTPException
import mariadb
from pydantic import BaseModel


# Setup ===============================================

try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        database="todo_list"
    )
    print(f"Connected to MariaDB on port 3306.")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

cur = conn.cursor()
app = FastAPI()


class TodoItem(BaseModel):
    """
    TODO: Not currently used
    """
    item_id: str
    name: str
    complete: Optional[bool] = None
    parent_id: Optional[str] = None


# Routes ==============================================

@app.get("/items")
def read_all_items():
    """
    Reads all Todo list items.

    \f
    :return: object containing list of items
    :rtype: dict
    """
    cur.execute("SELECT * from todo_item")
    items = []
    for (item_id, name, complete, parent_id) in cur:
        items.append(
            {
                "item_id": item_id,
                "name": name,
                "complete": complete,
                "parent_id": parent_id
            }
        )
    return {"items": items}


@app.get("/items/{item_id}")
def read_item(item_id: str):
    """
    Reads existing Todo list item by its item_id. Returns HTTPException if nothing with that item_id found. Assumes all item_id are unique.

    \f
    :param item_id: ID of existing item
    :type item_id: str
    :return: object representing the item
    :rtype: dict
    :raises: HTTPException
    """
    cur.execute("SELECT * from todo_item where item_id=?", (item_id,))
    values = cur.fetchone()
    if not values:
        raise HTTPException(
            status_code=404,
            detail="Could not fetch item with id {0}; "
                   "maybe it doesn't exist?".format(item_id)
            )
    return {
        "item_id": values[0],
        "name": values[1],
        "complete": values[2],
        "parent_id": values[3]
        }


@app.get("/items/{item_id}/parents")
def read_item_parents(item_id: str, immediate_only: Optional[bool] = True):
    """
    TODO

    Reads the immediate parent OR all parents, grandparents, etc of an item. Returns HTTPException if nothing with that item_id found. Assumes all item_id are unique.

    \f
    :param item_id: ID of existing item
    :type item_id: str
    :param immediate_only: If True, return only the immediate parent else all of them.
    :type item_id: bool
    :return: object containing nested items
    :rtype: dict
    :raises: HTTPException
    """
    return {"item_id": item_id, "name": "test", "complete": False}


@app.post("/items")
def create_item(name: str, complete: Optional[bool] = False, parent_id: Optional[str] = None):
    """
    TODO

    Create a new todo list item. Must have a name. Default for 'complete' status is False. Parent item ID optional.

    \f
    :param name: Name describing the item
    :type name: str
    :param complete: Has the item been completed or not
    :type complete: bool
    :param parent_id: ID of an existing item to be new item's immediate parent
    :type parent_id: str
    :return: object containing nested items
    :rtype: dict
    :raises: TODO
    """
    return {"item_id": item_id, "name": "test", "complete": False}


@app.put("/items/{item_id}")
def update_item(item_id: str, name: Optional[str] = None, complete: Optional[bool] = None, parent_id: Optional[str] = None):
    """
    TODO

    Update at least one of an existing item's name, completion, or parent. Returns HTTPException if nothing with that item_id found or if no values are provided. Assumes all item_id are unique.

    \f
    :param item_id: ID of an existing item to update
    :type item_id: str
    :param name: Name describing the item
    :type name: str
    :param complete: Has the item been completed or not
    :type complete: bool
    :param parent_id: ID of an existing item to be the item's immediate parent
    :type parent_id: str
    :return: object containing nested items
    :rtype: dict
    :raises: HTTPException
    """
    return {"item_id": item_id, "name": name, "parent_id": parent_id, "complete": complete}


@app.delete("/items/{item_id}")
def delete_item(item_id: str):
    """
    TODO

    Deletes existing Todo list item by its item_id. Returns HTTPException if nothing with that item_id found. Assumes all item_id are unique.

    \f
    :param item_id: ID of existing item
    :type item_id: str
    :return: TODO
    :rtype: TODO
    :raises: HTTPException
    """
    return {"item_id": item_id, "name": "test", "complete": False}
