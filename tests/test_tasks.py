"""Tests."""
import os

import pytest

from getitdone.getitdone import List


HOME_DIR = str(os.getcwd())
DB_NAME = "test_getitdone_db.sqlite"
DB_PATH = f"{HOME_DIR}/tests/{DB_NAME}"


@pytest.fixture
def list():
    _list = List()
    yield _list


def test_create_db(list):
    """Test database creation."""
    list.create_db(HOME_DIR, DB_PATH)
    assert os.path.isfile(DB_PATH)
    os.remove(DB_PATH)


def test_connect_db(list):
    """Test connection to db."""
    list.create_db(HOME_DIR, DB_PATH)
    try:
        connection = list.connect_db(DB_PATH)
        conn = "success"
        connection.close()
    except list.sqlite3.Error:
        conn = "failed"
    assert conn == "success"
    os.remove(DB_PATH)


def test_new_task(list):
    """Test create new task."""
    list.create_db(HOME_DIR, DB_PATH)
    connection = list.connect_db(DB_PATH)
    list.new_task(connection, "Buy milk.")
    response = list.read_db(connection, "SELECT name from tasks")
    task_name = ""
    for task in response:
        task_name = task[0]
    assert len(str(task_name)) == len("Buy milk.")
    connection.close()
    os.remove(DB_PATH)


def test_update_task(list, monkeypatch):
    """Test update of task."""
    list.create_db(HOME_DIR, DB_PATH)
    connection = list.connect_db(DB_PATH)
    oldTaskName = "Buy milk."
    list.new_task(connection, oldTaskName)

    newTaskName = "Buy full cream milk."
    monkeypatch.setattr("builtins.input", lambda _: "y")
    list.update_task(connection, oldTaskName, newTaskName)

    response = list.read_db(connection, "SELECT name from tasks")
    taskName = ""
    for task in response:
        taskName = task[0]
    assert len(str(taskName)) == len(newTaskName)
    connection.close()
    os.remove(DB_PATH)


def test_delete_task(list, monkeypatch):
    """Test delete task."""
    list.create_db(HOME_DIR, DB_PATH)
    connection = list.connect_db(DB_PATH)
    taskName = "Buy milk."
    list.new_task(connection, taskName)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    list.delete_task(connection, taskName)
    response = list.read_db(connection, "SELECT name from tasks")
    for task in response:
        taskName = task[0]
    if taskName is None:
        assert True
    connection.close()
    os.remove(DB_PATH)


def test_list_tasks(list):
    """List all tasks."""
    list.create_db(HOME_DIR, DB_PATH)
    connection = list.connect_db(DB_PATH)
    list.new_task(connection, "Buy milk.")
    list.new_task(connection, "Buy bread.")
    response = list.read_db(connection, "SELECT name from tasks")
    taskList = []
    for task in response:
        taskList.append(task[0])
    assert len(taskList) == 2
    connection.close()
    os.remove(DB_PATH)
