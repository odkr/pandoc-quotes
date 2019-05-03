#!/usr/bin/python
# Copyright 2016, 2019 Odin Kroeger
#
# This programme is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This programme is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Setup for the *pandoc-quotes* package."""

from shutil import copy
from os import path
from setuptools import setup


# Functions
# =========

def readme(readme_fname="README.rst"):
    """Returns the contents of README.rst.

    :param str readme_fname: Path to README.rst.
    :returns: Contents of *readme_fname*.
    :rtype: str
    """
    readme_path = path.join(path.dirname(__file__), readme_fname)
    with open(readme_path) as readme_handle:
        return readme_handle.read()


# Metadata
# ========

# Name of this package.
NAME = 'pandoc-refheadstyle'

# Version of this package.
VERSION = '0.6.1b0'


# All other metadata.
# pylint: disable=C0330
METADATA = {
    'name':             NAME,
    'version':          VERSION,
    'description':      'Pandoc filter that adapts quotation marks.',
    'long_description': readme(),
    'keywords':         'pandoc quotation marks',
    'url':              'https://github.com/odkr/pandoc-quotes/',
    'project_urls':     {
        'Source': 'https://github.com/odkr/pandoc-quotes/',
        'Tracker': 'https://github.com/odkr/pandoc-quotes/issues'
    },
    'author': 'Odin Kroeger',
    'author_email': 'epnzdp@maskr.me',
    'license': 'MIT',
    'python_requires': '>=2.7, <4',
    'packages': ['pandoc_quotes'],
    'install_requires': ['panflute', 'pyyaml'],
    'classifiers':      [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Filters'
        ],
    'scripts':          ['scripts/pandoc-quotes'],
    'include_package_data': True,
    # I have yet to test whether the manual page installs
    # if this is set to True.
    'zip_safe': False
}


# Boilerplate
# ===========

if __name__ == '__main__':
    setup(**METADATA)

    # This is a bit rude, but it should work on many systems.
    MANPAGE = path.join(path.dirname(__file__), 'man/pandoc-quotes.1')
    for i in ('/usr/local/share/man/man1', '/usr/share/man/man1'):
        if path.exists(i):
            try:
                copy(MANPAGE, i)
                break
            # pylint: disable=W0703
            except Exception:
                pass
