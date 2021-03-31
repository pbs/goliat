#!/usr/bin/env python
from setuptools import setup, find_packages

dependencies = [
    'django==1.11.29',
    'django-extraconfig',
]

setup(
    name='goliat',
    version='0.1',
    description='The PBS RESTful API Explorer.',
    author='TPG CORE Services Team',
    author_email='tpg-pbs-coreservices@threepillarglobal.com',
    url='https://github.com/pbs/goliat',
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
    setup_requires=['s3sourceuploader'],
)
