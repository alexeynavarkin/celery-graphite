#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io

from setuptools import find_packages, setup


with io.open('README.md', encoding='utf-8') as fp:
    DESCRIPTION = fp.read()


setup(
    name='celery-graphite',
    version='1.0.0',
    description='Simple Celery metrics exporter to graphite',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Alexey Navarkin',
    author_email='navarka.all@gmail.com',
    url='https://github.com/alexeynavarkin/celery-graphite',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "celery",
        "requests"
    ],
    entry_points={
            "console_scripts": [
                "celery-graphite=celery_graphite.__main__:main",
            ]
    }
)
