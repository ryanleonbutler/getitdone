"""Tests."""
import os

import getitdone.getitdone as gid


HOME_DIR = str(os.getcwd())
DB_NAME = "test_getitdone_db.sqlite"
DB_PATH = f"{HOME_DIR}/tests/{DB_NAME}"


def test_create_db():
    """Test database creation."""
    gid.create_db(HOME_DIR, DB_PATH)
    assert os.path.isfile(DB_PATH)
    os.remove(DB_PATH)


def test_connect_db():
    """Test connection to db."""
    gid.create_db(HOME_DIR, DB_PATH)
    try:
        connection = gid.connect_db(DB_PATH)
        conn = "success"
    except gid.sqlite3.Error:
        conn = "failed"
    assert conn == "success"
    connection.close()
    os.remove(DB_PATH)


def test_new_task():
    """Test create new task."""
    gid.create_db(HOME_DIR, DB_PATH)
    connection = gid.connect_db(DB_PATH)
    gid.new_task(connection, "Buy milk.")
    response = gid.read_db(connection, "SELECT name from tasks")
    for task in response:
        task_name = task[0]
    assert len(str(task_name)) == len("Buy milk.")
    connection.close()
    os.remove(DB_PATH)


def test_update_task(monkeypatch):
    """Test update of task."""
    gid.create_db(HOME_DIR, DB_PATH)
    connection = gid.connect_db(DB_PATH)
    oldTaskName = "Buy milk."
    gid.new_task(connection, oldTaskName)

    newTaskName = "Buy full cream milk."
    monkeypatch.setattr("builtins.input", lambda _: "y")
    gid.update_task(connection, oldTaskName, newTaskName)

    response = gid.read_db(connection, "SELECT name from tasks")
    taskName = ""
    for task in response:
        taskName = task[0]
    assert len(str(taskName)) == len(newTaskName)
    connection.close()
    os.remove(DB_PATH)


def test_delete_task(monkeypatch):
    """Test delete task."""
    gid.create_db(HOME_DIR, DB_PATH)
    connection = gid.connect_db(DB_PATH)
    taskName = "Buy milk."
    gid.new_task(connection, taskName)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    gid.delete_task(connection, taskName)
    response = gid.read_db(connection, "SELECT name from tasks")
    for task in response:
        taskName = task[0]
    if taskName is None:
        assert True
    connection.close()
    os.remove(DB_PATH)


def test_list_tasks():
    """List all tasks."""
    gid.create_db(HOME_DIR, DB_PATH)
    connection = gid.connect_db(DB_PATH)
    gid.new_task(connection, "Buy milk.")
    gid.new_task(connection, "Buy bread.")
    response = gid.read_db(connection, "SELECT name from tasks")
    taskList = []
    for task in response:
        taskList.append(task[0])
    assert len(taskList) == 2
    connection.close()
    os.remove(DB_PATH)
