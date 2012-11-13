# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import finch

requirements = open('requirements.txt').read().splitlines()
long_description = open('README.md').read()

setup(
    name='finch',
    version=finch.__version__,
    description='Asynchronous RESTful API consumer for Python',
    long_description=long_description,
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )
