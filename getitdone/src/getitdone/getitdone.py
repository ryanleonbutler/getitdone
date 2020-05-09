#!/usr/bin/env python3

"""
`getitdone` to-do list application
"""

import sys

import sqlite3
from sqlite3 import Error


class Todolist:
    def __init__(self):
        self.list = []


class Task:
    def __init__(self, task_name):
        self.task_name = task_name


def new(task_name):
    query = f"""
        INSERT INTO
        tasks (name)
        VALUES
        ('{task_name}')
    """
    execute_query(connection, query)
    print(f"'{task_name}' added to list")


def update(task_name, new_name):
    # TODO: integrate updates with db
    user_input = input(
        f"Update '{task_name}' with '{new_name}'? Y/N "
    )
    query = f"""
        UPDATE tasks
        SET name = '{new_name}'
        WHERE name = '{task_name}'
    """
    execute_query(connection, query)
    print(f"'{task_name}' updated to `{new_name}`")


def delete(task_name):
    # TODO: integrate deletes with db
    user_input = input(f"Delete '{task_name}' from your list? Y/N ")
    if user_input.lower() == "y":
        query = f"DELETE FROM tasks WHERE name = '{task_name}'"
        execute_query(connection, query)
        print(f"'{task_name}' deleted")
    else:
        pass


def show():
    query = "SELECT * FROM tasks"
    response = execute_read_query(connection, query)
    print("\n### get-it-done ###\n\n"
          "-----------------")
    if len(response) < 1:
        print(f"...No tasks...")
    else:
        for task in response:
            print(f"{task[0]} - {task[1]}")
    print("-----------------\n")


def command_help():
    print("\n### get-it-done ###\n")
    print(
        "OPTIONS\n"
        "\t`-new` or `-n` '<task-name>'\n"
        "\t\tCreate a new task with name in first argument\n\n"
        "\t`-update` or `-u` '<task-name>' '<new-name>'\n"
        "\t\tUpdate task in first argument with value second argument\n\n"
        "\t`-delete` or `-d` '<task-name>'\n"
        "\t\tDelete task in first argument with value second argument\n\n"
        "\t`-show` or `-s` '<task-name>'\n"
        "\t\tDelete task in first argument with value second argument\n\n"
        "\t`-help` or `-h`\n"
        "\t\tShows man page for todolist\n"
    )


def create_connection(path):
    # TODO: path of db needs to be dynamic to user folder
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


create_table = """
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
    );
"""


if __name__ == "__main__":
    tasks = Todolist()

    # TODO: path of db needs to be dynamic to user folder
    connection = create_connection("getitdonedb.sqlite")
    execute_query(connection, create_table)
    action = sys.argv[1].lower()

    try:
        if action == "-new" or action == "-n":
            task_name = sys.argv[2]
            task = Task(task_name)
            new(task_name)
        elif sys.argv[1] == "-update" or sys.argv[1] == "-u":
            task_name = sys.argv[2]
            new_name = sys.argv[3]
            update(task_name, new_name)
        elif sys.argv[1] == "-delete" or sys.argv[1] == "-d":
            task_name = sys.argv[2]
            delete(task_name)
        elif sys.argv[1] == "-show" or sys.argv[1] == "-s":
            show()
        elif sys.argv[1] == "-help" or sys.argv[1] == "-h":
            command_help()
        else:
            print("Please refer to help (`-help` or `-h`) for instructions\n")
    except IndexError as err:
        print("Please refer to help (`-help` or `-h`) for instructions\n")
