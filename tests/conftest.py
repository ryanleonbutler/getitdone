import os
from pathlib import Path
from getitdone.getitdone import Gid

HOME_DIR = str(Path.home())
DB_NAME = "getitdone_db_tests.sqlite"
DB_DIR_PATH = f"{HOME_DIR}/.getitdone_tests"
DB_FULL_PATH = f"{HOME_DIR}/.getitdone_tests/{DB_NAME}"


def pytest_sessionstart(session):
    gid = Gid()
    if not os.path.isdir(DB_DIR_PATH):
        os.mkdir(DB_DIR_PATH)
        gid.create_db(DB_FULL_PATH)


def pytest_sessionfinish(session, exitstatus):
    os.remove(DB_FULL_PATH)
    os.rmdir(DB_DIR_PATH)
