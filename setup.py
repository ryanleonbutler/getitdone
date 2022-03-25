#!/usr/bin/env python

from distutils.core import setup

# The text of the README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='getitdone',
    version='0.0.4',
    description='Command line to-do list application ',
    long_description=long_description,
    author='Ryan Butler',
    author_email='ryanleonbutler@gmail.com',
    license="GPLv3",
    url='https://github.com/ryanleonbutler/getitdone',
    packages=['getitdone'],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8.x",
    install_requires=[
        "SQLAlchemy=>1.4.32",
        "rich=>12.0.1",
        "textual=>0.1.17",
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business :: Scheduling',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    entry_points={
        "console_scripts": [
            "gid=getitdone:patched_main",
            "getitdone=blackd:patched_main [d]",
        ]
    },
)
