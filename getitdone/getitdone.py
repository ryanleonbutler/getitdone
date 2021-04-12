#!/usr/bin/env python3

"""
`getitdone` is a terminal to-do list tool.

Copyright (C) 2021  Ryan Butler
"""
import sqlite3
from os import mkdir
from pathlib import Path
from sqlite3 import Error
from sys import argv


HOME_DIR = str(Path.home())
DB_NAME = "getitdone_db.sqlite"
DB_PATH = f"{HOME_DIR}/.getitdone/{DB_NAME}"


def create_db(home_dir, db_path):
    """Create db in HOME_DIR."""
    createTable = """
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    );
    """
    try:
        mkdir(f"{home_dir}/.getitdone")
    except FileExistsError:
        pass
    connection = connect_db(db_path)
    write_db(connection, createTable)


def connect_db(path: str) -> object:
    """Create connection with db.

    Args:
        path (str): Path to the db.

    Returns:
        [type]: [description]
    """
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        connection = f"The error '{e}' occurred"
        print(f"The error '{e}' occurred")
    return connection


def write_db(connection: object, query: str):
    """Execute SQL write query with connection to db and commit the write.

    Args:
        connection (object): db connection.
        query (str): SQL query.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def read_db(connection: object, query: str) -> object:
    """Execute SQL read query with connection to the db.

    Args:
        connection (object): db connection.
        query (str): SQL query.

    Returns:
        object: Result object from db.
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def new_task(connection: object, taskName: str):
    """Insert new task into db.

    Args:
        connection (object): db connection.
        taskName (str): Name of task.
    """
    query = f"""
        INSERT INTO
        tasks (name)
        VALUES
        ('{taskName}')
    """
    write_db(connection, query)
    print(f"'{taskName}' added to list")


def update_task(connection: object, taskName: str, newName: str):
    """Update task in db.

    Args:
        connection (object): db connection.
        taskName (str): Current name of task.
        newName (str): New name of task.
    """
    userInput = input(f"Update '{taskName}' with '{newName}'? Y/N ")
    if userInput.lower() == "y":
        query = f"""
            UPDATE tasks
            SET name = '{newName}'
            WHERE name = '{taskName}'
        """
        write_db(connection, query)
        print(f"'{taskName}' updated to `{newName}`")


def delete_task(connection: object, taskName: str):
    """Delete task from db.

    Args:
        connection (object): db connection.
        taskName (str): Task name to be deleted.
    """
    userInput = input(f"Delete '{taskName}' from your list? Y/N ")
    if userInput.lower() == "y":
        query = f"DELETE FROM tasks WHERE name = '{taskName}'"
        write_db(connection, query)
        print(f"'{taskName}' deleted")


def list_tasks(connection):
    """List all tasks in db."""
    query = "SELECT * FROM tasks"
    response = read_db(connection, query)
    print("\n### get-it-done ###\n\n" "-----------------")
    if len(response) < 1:
        print("...No tasks...")
    else:
        for task in response:
            print(f"{task[0]} - {task[1]}")
    print("-----------------\n")


def command_help():
    """Print help with available list of commands and arguments."""
    print("\n### get-it-done ###\n")
    print(
        "OPTIONS\n"
        "\t`--new` or `-n` '<task-name>'\n"
        "\t\tCreate a new task with name in first argument\n\n"
        "\t`--update` or `-u` '<task-name>' '<new-name>'\n"
        "\t\tUpdate task in first argument with value of second argument\n\n"
        "\t`--delete` or `-d` '<task-name>'\n"
        "\t\tDelete task in first argument with value of second argument\n\n"
        "\t`--list` or `-l`\n"
        "\t\tList all tasks\n\n"
        "\t`--help` or `-h`\n"
        "\t\tShows man page for todolist\n"
    )


if __name__ == "__main__":
    create_db(HOME_DIR, DB_PATH)
    connection = connect_db(DB_PATH)
    action = argv[1].lower()
    try:
        if action == "--new" or action == "-n":
            taskName = argv[2]
            new_task(connection, taskName)
        elif argv[1] == "--update" or argv[1] == "-u":
            taskName = argv[2]
            newName = argv[3]
            update_task(connection, taskName, newName)
        elif argv[1] == "--delete" or argv[1] == "-d":
            taskName = argv[2]
            delete_task(connection, taskName)
        elif argv[1] == "--list" or argv[1] == "-l":
            list_tasks(connection)
        elif argv[1] == "--help" or argv[1] == "-h":
            command_help()
        else:
            print("Please refer to help (`--help` or `-h`) for instructions\n")
    except IndexError:
        print("Please refer to help (`--help` or `-h`) for instructions\n")
