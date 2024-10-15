from setuptools import setup
from pg_mongodb import VERSION

DIST_NAME = "pg_mongodb"
__author__ = "baozilaji@gmail.com"

setup(
    name=DIST_NAME,
    version=VERSION,
    description="python game: mongodb",
    packages=[DIST_NAME],
    author=__author__,
    python_requires='>=3.9',
    install_requires=[
        'pg-environment>=0',
        'motor==3.4.0',
    ],
)
