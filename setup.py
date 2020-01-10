#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from os.path import dirname, abspath, join

# Set the ROOT folder
root_folder = abspath(dirname(__file__))
# Load the package information, see 'PiAlarmClock/src/PiAlarmClock/__about__.py'
about = {}
with open(join(root_folder, 'src', 'PiAlarmClock', "__about__.py")) as fp:
    exec(fp.read(), about)

setup_kwds = dict(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__uri__'],
    # license=about['__license__'],
    package_dir={'':'src'},   # tell distutils packages are under src
    packages=find_packages(),
    zip_safe=False,
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
        'src/PiAlarmClock/main.py'
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
    platform_system=[
        'Linux'
    ],
    platform_machine=[
        'armv6l',
        'armv7l'
    ]
)

setup(**setup_kwds)
