# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='fich',
    version='0.1',
    description='Asynchronous RESTful API consumer for Python',
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
