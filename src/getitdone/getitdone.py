#!/usr/bin/env python3

"""
'getitdone', command line to-do list app... now let's make some lists!

Copyright (C) 2022  Ryan Butler
"""
import logging
import os
import sqlite3
from pathlib import Path
from sqlite3 import Error
from sys import argv

from rich import print as print
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table


HOME_DIR = str(Path.home())
DB_NAME = "getitdone_db.sqlite"
DB_DIR_PATH = f"{HOME_DIR}/.getitdone"
DB_FULL_PATH = f"{HOME_DIR}/.getitdone/{DB_NAME}"


class Gid:
    def __init__(self):
        FORMAT = "%(message)s"
        logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
        self.log = logging.getLogger("rich")

    def create_db(self, db_path: str):
        """Create db in HOME_DIR."""
        createTable = """
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        status TEXT NOT NULL
        );
        """
        try:
            connection = self.connect_db(db_path)
            self.write_db(connection, createTable)
        except FileExistsError as error:
            self.log.warn("%s", error)

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
        except Error as error:
            self.log.error("%s", error)

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
        except Exception as error:
            self.log.error("Error: %s", error)

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
        except Exception as error:
            self.log.error("Error: %s", error)

    def new_task(self, connection, taskName: str, status: str = "not started"):
        """Insert new task into db.

        Args:
            connection: db connection.
            taskName (str): Name of task.
        """
        query = f"""
            INSERT INTO
            tasks (name, status)
            VALUES
            ('{taskName}', '{status}')
        """
        self.write_db(connection, query)
        print(f"\n'{taskName}' added to list...\n")

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
            print(f"\n'{taskName}' updated to '{newName}'...\n")

    def delete_task(self, connection, taskName: str):
        """Delete task from db.

        Args:
            connection: db connection.
            taskName (str): Task name to be deleted.
        """
        userInput = input(f"\nDelete '{taskName}' from your list?(Y/N) ")
        if userInput.lower() == "y":
            query = f"DELETE FROM tasks WHERE name = '{taskName}'"
            self.write_db(connection, query)
            print(f"\n'{taskName}' deleted...\n")

    def list_tasks(self, connection):
        """List all tasks in db."""
        query = "SELECT * FROM tasks"
        response = ""
        try:
            response = self.read_db(connection, query)
        except Exception as error:
            self.log.error("Error: %s", error)

        table = Table(title="GID - Tasks", caption_justify="left", style="blue")
        table.add_column("No.", justify="right", style="white", no_wrap=True)
        table.add_column("Name", justify="left", style="magenta", no_wrap=True)
        table.add_column("Status", justify="center", style="cyan", no_wrap=True)

        if not response:
            print("\nGID - no tasks, go have some fun!\n")
        else:
            for task in response:
                table.add_row(str(task[0]), task[1], task[2])
            console = Console()
            console.print("\n", table, "\n")

    def command_help(self):
        """Print help with available list of commands and arguments."""
        print("\nGID - Help\n")
        print(
            "OPTIONS\n"
            "'--new' or '-n' '<task-name>'\n"
            "\tCreate a new task with name in first argument\n\n"
            "'--update' or '-u' '<task-name>' '<new-name>'\n"
            "\tUpdate task in first argument with value of second argument\n\n"
            "'--delete' or '-d' '<task-name>'\n"
            "\tDelete task in first argument with value of second argument\n\n"
            "'--list' or '-l'\n"
            "\tList all tasks\n\n"
            "'--help' or '-h'\n"
            "\tShows man page for todolist\n"
        )


def main():
    gid = Gid()
    if not os.path.isdir(DB_DIR_PATH):
        os.mkdir(DB_DIR_PATH)
        gid.create_db(DB_FULL_PATH)
    connection = gid.connect_db(DB_FULL_PATH)
    try:
        action = ""
        if argv[1]:
            action = argv[1].lower()

        if action == "--new" or action == "-n":
            taskName = argv[2]
            gid.new_task(connection, taskName)
        elif argv[1] == "--update" or argv[1] == "-u":
            taskName = argv[2]
            newName = argv[3]
            gid.update_task(connection, taskName, newName)
        elif argv[1] == "--delete" or argv[1] == "-d":
            taskName = argv[2]
            gid.delete_task(connection, taskName)
        elif argv[1] == "--list" or argv[1] == "-l":
            gid.list_tasks(connection)
        elif argv[1] == "--help" or argv[1] == "-h":
            gid.command_help()
        else:
            print("Please refer to help ('--help' or '-h') for instructions\n")
    except IndexError:
        gid.command_help()


if __name__ == "__main__":
    main()
