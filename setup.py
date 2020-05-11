import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="getitdone",
    version="0.1.0",
    description="Manage your to-do lists from the command line",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://ryanleonbutler.com",
    author="Ryan Butler",
    author_email="ryanleonbutler@gmail.com",
    license="AGPL",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business :: Scheduling',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=["getitdone"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "getitdone=getitdone.main:main",
        ]
    },
)