#!/usr/bin/env python
from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(
    name='django-pendulum-field',
    version='0.1.0',
    description='Django pendulum field',
    author='flokli',
    author_email='flokli@flokli.de',
    url='https://github.com/flokli/django-pendulum-field',
    packages=find_packages(),
    install_requires=['django', 'pendulum']
)
