#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import (
    setup,
    find_packages,
)

PACKAGE_VERSION = '1.0.4'

EXTRAS_REQUIRE = {
    'lint': [
        'black>=18.6b4,<19',
        'flake8>=3.5.0,<4.0.0',
        'mypy<0.600',
        'pytest>=3.4.1,<4.0.0',
    ],
    'test': [
        'hypothesis>=3.4.2,<4.0.0',
        'pytest>=3.4.1,<4.0.0',
        'pytest-pythonpath>=0.3,<1.0',
    ],
    'deploy': [
        'bumpversion>=0.5.3,<1.0.0',
        'tox>=2.9.1,<3.0.0',
        'wheel>=0.30.0,<1.0.0',
    ],
    'dev': [
        "twine",
    ]
}

EXTRAS_REQUIRE['dev'] = (
        EXTRAS_REQUIRE['dev'] +
        EXTRAS_REQUIRE['lint'] +
        EXTRAS_REQUIRE['test'] +
        EXTRAS_REQUIRE['deploy']
)

this_dir = os.path.dirname(__file__)
readme_filename = os.path.join(this_dir, 'README.rst')

with open(readme_filename) as f:
    PACKAGE_LONG_DESCRIPTION = f.read()

setup(
    name='trx-utils',
    version=PACKAGE_VERSION,
    description="""Common utility functions for tron codebases.""",
    long_description=PACKAGE_LONG_DESCRIPTION,
    author='Shamsudin Serderov',
    author_email='iexbase@protonmail.com',
    url='https://github.com/iexbase/trx-utils',
    include_package_data=True,
    install_requires=[
        "base58",
        "eth-hash",
        "eth-typing",
        "toolz>0.8.2,<1;implementation_name=='pypy'",
        "cytoolz>=0.8.2,<1.0.0;implementation_name=='cpython'",
    ],
    python_requires='>=3.5,!=3.5.2,<4',
    py_modules=['trx_utils'],
    license="MIT",
    zip_safe=False,
    packages=find_packages(exclude=["tests"]),
    package_data={'trx_utils': ['py.typed']},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
