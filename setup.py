#!/usr/bin/env python
from setuptools import setup

setup(
    name = 'TracDuplicates',
    version = '0.11-wordpress',
    packages = ['tracduplicates'],
    author = "Nils Maier",
    author_email = "testnutzer123@gmail.com",
    description = "Provides support for duplicates ticket references. Modified by Andrew Nacin for WordPress.",
    license = "BSD",
    keywords = "trac plugin ticket dependencies duplicates",
    url = "http://tn123.ath.cx/TracDuplicates",
    classifiers = [
        'Framework :: Trac',
    ],

    entry_points = {
        'trac.plugins': [
            'tracduplicates.web_ui = tracduplicates.web_ui',
        ]
    }
)
