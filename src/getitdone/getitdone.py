#!/usr/bin/env python3

"""
`getitdone`, command line to-do list app... now let's make some lists!

Copyright (C) 2022  Ryan Butler
"""
import logging
import sqlite3
from os import mkdir
from pathlib import Path
from sqlite3 import Error
from sys import argv

from rich.logging import RichHandler


HOME_DIR = str(Path.home())
DB_NAME = "getitdone_db.sqlite"
DB_PATH = f"{HOME_DIR}/.getitdone/{DB_NAME}"


class List:
    def __init__(self):
        FORMAT = "%(message)s"
        logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
        self.log = logging.getLogger("rich")

    def create_db(self, home_dir: str, db_path: str):
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
        connection = self.connect_db(db_path)
        self.write_db(connection, createTable)

    def connect_db(self, path: str):
        """Create connection with db.

        Args:
            path (str): Path to the db.

        Returns:
            [type]: [description]
        """
        try:
            connection = sqlite3.connect(path)
            return connection
        except Error as e:
            self.log.error("Error: %s", e)
            print(f"The error '{e}' occurred")

    def write_db(self, connection, query: str):
        """Execute SQL write query with connection to db and commit the write.

        Args:
            connection: db connection.
            query (str): SQL query.
        """
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except Error as e:
            self.log.error("Error: %s", e)
            print(f"The error '{e}' occurred")

    def read_db(self, connection, query: str):
        """Execute SQL read query with connection to the db.

        Args:
            connection: db connection.
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
            self.log.error("Error: %s", e)
            print(f"The error '{e}' occurred")

    def new_task(self, connection, taskName: str):
        """Insert new task into db.

        Args:
            connection: db connection.
            taskName (str): Name of task.
        """
        query = f"""
            INSERT INTO
            tasks (name)
            VALUES
            ('{taskName}')
        """
        self.write_db(connection, query)
        print(f"'{taskName}' added to list")

    def update_task(self, connection, taskName: str, newName: str):
        """Update task in db.

        Args:
            connection: db connection.
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
            self.write_db(connection, query)
            print(f"'{taskName}' updated to `{newName}`")

    def delete_task(self, connection, taskName: str):
        """Delete task from db.

        Args:
            connection: db connection.
            taskName (str): Task name to be deleted.
        """
        userInput = input(f"Delete '{taskName}' from your list? Y/N ")
        if userInput.lower() == "y":
            query = f"DELETE FROM tasks WHERE name = '{taskName}'"
            self.write_db(connection, query)
            print(f"'{taskName}' deleted")

    def list_tasks(self, connection):
        """List all tasks in db."""
        query = "SELECT * FROM tasks"
        response = self.read_db(connection, query)
        print("\n### get-it-done ###\n\n" "-----------------")
        if len(response) < 1:
            print("...No tasks...")
        else:
            for task in response:
                print(f"{task[0]} - {task[1]}")
        print("-----------------\n")

    def command_help(self):
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


def main():
    list = List()
    list.create_db(HOME_DIR, DB_PATH)
    connection = list.connect_db(DB_PATH)
    try:
        action = ""
        if argv[1]:
            action = argv[1].lower()

        if action == "--new" or action == "-n":
            taskName = argv[2]
            list.new_task(connection, taskName)
        elif argv[1] == "--update" or argv[1] == "-u":
            taskName = argv[2]
            newName = argv[3]
            list.update_task(connection, taskName, newName)
        elif argv[1] == "--delete" or argv[1] == "-d":
            taskName = argv[2]
            list.delete_task(connection, taskName)
        elif argv[1] == "--list" or argv[1] == "-l":
            list.list_tasks(connection)
        elif argv[1] == "--help" or argv[1] == "-h":
            list.command_help()
        else:
            print("Please refer to help (`--help` or `-h`) for instructions\n")
    except IndexError:
        list.command_help()


if __name__ == "__main__":
    main()
