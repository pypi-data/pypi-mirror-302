from setuptools import setup
from pg_httpserver import VERSION

DIST_NAME = "pg_httpserver"
__author__ = "baozilaji@gmail.com"

setup(
	name=DIST_NAME,
	version=VERSION,
	description="python game: httpserver",
	packages=['pg_httpserver'],
	author=__author__,
	python_requires='>=3.5',
	install_requires=[
		'pg-redis>=0',
		'fastapi==0.65.3',
		'uvicorn==0.14.0'
	],
)
