"""
FastAPI and MariaDB implementation of a simple todo list. Each todo list item can have one parent list item, while each item can have many children. Items can be created, edited, checked as complete, and deleted. Item parents (immediate only OR to the root) can also be queried. See README for more information.
"""

import sys
from typing import Optional

from fastapi import FastAPI, HTTPException, status
import mariadb


# Setup ===============================================

try:
    conn = mariadb.connect(
        user="root",         # !!! TODO: Change if user is not "root"
        password="root",     # !!! TODO: Change if password is not "root"
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
    Reads existing Todo list item by its item_id. Returns HTTPException if nothing with that item_id found.

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
    Reads the immediate parent OR all parents, grandparents, etc of an item. Returns HTTPException if nothing with that item_id found. If no parent(s), an empty list is returned.

    \f
    :param item_id: ID of existing item
    :type item_id: str
    :param immediate_only: If True, return only the immediate parent else all of them.
    :type item_id: bool
    :return: object representing parent(s) requested
    :rtype: dict
    :raises: HTTPException
    """
    item = read_item(item_id)
    parents = []
    current_parent_id = item["parent_id"]

    if immediate_only:
        if current_parent_id:
            parent = read_item(current_parent_id)
            parents.append(parent)
        return {"parents": parents}   

    while current_parent_id:
        parent = read_item(current_parent_id)
        parents.append(parent)
        current_parent_id = parent["parent_id"]
    return {"parents": parents}


@app.post("/items")
def create_item(name: str, complete: Optional[bool] = False, parent_id: Optional[str] = None):
    """
    Create a new todo list item. Must have a name. Default for 'complete' status is False. Parent item ID optional. Returns HTTPException if parent_id provided but parent does not exist.

    \f
    :param name: Name describing the item
    :type name: str
    :param complete: Has the item been completed or not
    :type complete: bool
    :param parent_id: ID of an existing item to be new item's immediate parent
    :type parent_id: str
    :return: object representing the new item
    :rtype: dict
    :raises: HTTPException
    """
    if parent_id:
        try:
            read_item(parent_id)
        except HTTPException:
            raise HTTPException(
                status_code=404,
                detail="Could not fetch parent item with id {0}; "
                    "maybe it doesn't exist?".format(parent_id)
            )
    
    cur.execute("INSERT INTO todo_item (name, complete, parent_id) VALUES (?, ?, ?)",
        (name, complete, parent_id,)
    )
    item_id = cur.lastrowid
    conn.commit()
    return read_item(item_id)


@app.put("/items/{item_id}")
def update_item(item_id: str, name: Optional[str] = None, complete: Optional[bool] = None, parent_id: Optional[str] = None):
    """
    Update at least one of an existing item's name, completion, or parent. Returns HTTPException if no values are provided, if item with given item_id does not exist, or if parent_id provided but parent does not exist.

    \f
    :param item_id: ID of an existing item to update
    :type item_id: str
    :param name: Name describing the item
    :type name: str
    :param complete: Has the item been completed or not
    :type complete: bool
    :param parent_id: ID of an existing item to be the item's immediate parent
    :type parent_id: str
    :return: object representing the updated item
    :rtype: dict
    :raises: HTTPException
    """
    if name == None and parent_id == None and complete == None:
        raise HTTPException(
            status_code=400,
            detail="Please provide at least one of name, complete, parent_id values to update."
        )

    try:
        read_item(item_id)
    except HTTPException:
        raise HTTPException(
            status_code=404,
            detail="Could not fetch item with id {0}; "
                "maybe it doesn't exist?".format(parent_id)
        )

    if parent_id:
        try:
            read_item(parent_id)
        except HTTPException:
            raise HTTPException(
                status_code=404,
                detail="Could not fetch parent item with id {0}; "
                    "maybe it doesn't exist?".format(parent_id)
            )

    # Build query with new values
    new_values = {}
    for v in ('name', 'parent_id', 'complete'):
        value = locals()[v]
        if value != None:
            new_values[v] = value

    update_query = "UPDATE todo_item set {0} where item_id={1}".format(
        ', '.join('%s=%r' % x for x in new_values.items()),
        item_id,
    )
    cur.execute(update_query)
    conn.commit()
    return read_item(item_id)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str):
    """
    Deletes existing Todo list item by its item_id. Returns HTTPException if nothing with that item_id found.

    \f
    :param item_id: ID of existing item
    :type item_id: str
    :raises: HTTPException
    """
    try:
        read_item(item_id)
    except HTTPException:
        raise HTTPException(
            status_code=404,
            detail="Could not find item with id {0}; "
                "maybe it doesn't exist?".format(item_id)
        )
    cur.execute("DELETE FROM todo_item WHERE item_id = ?", (item_id,))
    conn.commit()
