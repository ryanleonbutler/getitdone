from setuptools import setup

# The text of the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

# This call to setup() does all the work
setup(
    name="getitdone",
    version="0.0.2",
    description="Manage your to-do lists from the command line",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://ryanbutler.online",
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
    scripts=["getitdone/getitdone"],
)
