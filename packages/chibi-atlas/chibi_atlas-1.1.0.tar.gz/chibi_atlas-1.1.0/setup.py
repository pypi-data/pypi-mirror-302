#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ 'pyyaml>=5.1.2' ]

setup(
    author="dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: Utilities',
    ],
    description="small lib to proccess the keys of the dict like attributes",
    install_requires=requirements,
    license="WTFPL",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chibi_atlas',
    name='chibi_atlas',
    packages=find_packages(include=['chibi_atlas', 'chibi_atlas.*']),
    url='https://github.com/dem4ply/chibi_atlas',
    version='1.1.0',
    zip_safe=False,
)
