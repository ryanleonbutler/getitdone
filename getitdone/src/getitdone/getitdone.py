#!/usr/bin/env python3

"""
`getitdone` to-do list application
"""

import sys

import sqlite3
from sqlite3 import Error


class Todolist:
    def __init__(self):
        self.task_list = []

    def new(self, task_name):
        # TODO: add feedback to terminal after new task is created
        self.task_list.append(task_name)

        query = f"""
        INSERT INTO
          tasks (name)
        VALUES
          ('{task_name}')
        """
        execute_query(connection, query)

    def update(self, task_name, new_name):
        # TODO: integrate updates with db
        task_index = self.task_list.index(task_name)
        self.task_list[task_index] = new_name

    def delete(self, task_name):
        # TODO: integrate deletes with db
        user_input = input(
            f"Are you sure you wish to delete `{task_name}` from your todolist? Y/N "
        )
        if user_input.lower() == "y":
            self.task_list.remove(task_name)
        else:
            pass

    def show(self):
        query = """
                SELECT * FROM tasks
                """
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
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query executed successfully")
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
    todo_list = Todolist()

    # TODO: path of db needs to be dynamic to user folder
    connection = create_connection("getitdonedb.sqlite")
    execute_query(connection, create_table)

    try:
        if sys.argv[1] == "-new" or sys.argv[1] == "-n":
            action = sys.argv[1].lower()
            task_name = sys.argv[2].title()

            todo_list.new(task_name)

        elif sys.argv[1] == "-update" or sys.argv[1] == "-u":
            action = sys.argv[1].lower()
            task_name = sys.argv[2].title()
            new_name = sys.argv[3].title()

            todo_list.update(task_name, new_name)

        elif sys.argv[1] == "-delete" or sys.argv[1] == "-d":
            action = sys.argv[1].lower()
            task_name = sys.argv[2].title()

            todo_list.delete(task_name)

        elif sys.argv[1] == "-show" or sys.argv[1] == "-s":
            todo_list.show()

        elif sys.argv[1] == "-help" or sys.argv[1] == "-h":
            command_help()

        else:
            print(
                "Please refer to the man page (`-help` or `-h`) for list of options and arguments\n"
            )

    except IndexError as err:
        print(
            "Please refer to the man page (`-help` or `-h`) for list of options and arguments\n"
        )
