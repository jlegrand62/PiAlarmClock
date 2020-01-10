#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from os.path import dirname, abspath, join

# Set the ROOT folder
root_folder = abspath(dirname(__file__))
# Load the package information, see 'PiAlarmClock/src/PiAlarmClock/__about__.py'
about = {}
with open(join(root_folder, "src", "PiAlarmClock", "__about__.py")) as fp:
    exec(fp.read(), about)

# find packages
pkgs = find_packages('src')

setup_kwds = dict(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__uri__'],
    # license=about['__license__'],
    zip_safe=False,
    packages=pkgs,
    package_dir={'': 'src'},
    python_requires='>=3.6',
    setup_requires=[
    ],
    install_requires=[
        "kivy",
        "newspaper3k",
        "pyowm"
    ],
    tests_require=[
    ],
    entry_points={
    },
    scripts=[
        'PiAlarmClock/src/PiAlarmClock/main.py'
    ],
    keywords='',

    test_suite='nose.collector',
    project_urls={
        'Documentation': about['__uri__'],
        'Source': about['__uri__'],
    },
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ],
    platforms=[
        'Arm'
    ]
)

setup(**setup_kwds)
