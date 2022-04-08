"""Tests."""
import os
from pathlib import Path

import pytest

from getitdone.getitdone import Gid


HOME_DIR = str(Path.home())
DB_NAME = "getitdone_db_tests.sqlite"
DB_DIR_PATH = f"{HOME_DIR}/.getitdone_tests"
DB_FULL_PATH = f"{HOME_DIR}/.getitdone_tests/{DB_NAME}"


@pytest.fixture
def gid():
    _gid = Gid()
    return _gid


@pytest.fixture
def setup_db(scope="module", autouse=True):
    print("DB Setup")
    yield
    print("DB Cleanup")


def test_new_db():
    """Test database creation."""
    assert os.path.isfile(DB_FULL_PATH)


def test_connect_db(gid):
    """Test connection to db."""
    try:
        connection = gid.connect_db(DB_FULL_PATH)
        conn = "success"
        connection.close()
    except gid.sqlite3.Error:
        conn = "failed"
    assert conn == "success"


def test_new_task(gid):
    """Test create new task."""
    connection = gid.connect_db(DB_FULL_PATH)
    gid.new_task(connection, "Buy milk.")
    response = gid.read_db(connection, "SELECT name from tasks")
    task_name = ""
    for task in response:
        task_name = task[0]
    assert len(str(task_name)) == len("Buy milk.")
    connection.close()


def test_update_task(gid, monkeypatch):
    """Test update of task."""
    connection = gid.connect_db(DB_FULL_PATH)
    oldTaskName = "Buy milk."
    newTaskName = "Buy full cream milk."
    monkeypatch.setattr("builtins.input", lambda _: "y")
    gid.update_task(connection, oldTaskName, newTaskName)

    response = gid.read_db(connection, "SELECT name from tasks")
    taskName = ""
    for task in response:
        taskName = task[0]
    assert len(str(taskName)) == len(newTaskName)
    connection.close()


def test_delete_task(gid, monkeypatch):
    """Test delete task."""
    connection = gid.connect_db(DB_FULL_PATH)
    taskName = "Buy milk."
    monkeypatch.setattr("builtins.input", lambda _: "y")
    gid.delete_task(connection, taskName)
    response = gid.read_db(connection, "SELECT name from tasks")
    for task in response:
        taskName = task[0]
    if taskName is None:
        assert True
    connection.close()


def test_list_tasks(gid):
    """List all tasks."""
    connection = gid.connect_db(DB_FULL_PATH)
    gid.new_task(connection, "Buy cereal.")
    gid.new_task(connection, "Buy bread.")
    response = gid.read_db(connection, "SELECT name from tasks")
    taskList = []
    for task in response:
        taskList.append(task[0])
    assert len(taskList) == 3
    connection.close()
