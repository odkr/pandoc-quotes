from shutil import copy
from os import path
from setuptools import setup

setup(name='pandoc-quotes',
      version='0.5.1',
      description='Pandoc filter that adapts quotation marks.',
      long_description='``pandoc-quotes`` is a filter for '
                       '`pandoc <http://pandoc.org/>`_ that replaces plain, '
                       'that is, non-typographic, quotation marks with '
                       'typographic ones.',
      keywords='pandoc quotation marks',
      url='https://github.com/odkr/pandoc-quotes/',
      project_urls={'Source': 'https://github.com/odkr/pandoc-quotes/',
                    'Tracker': 'https://github.com/odkr/pandoc-quotes/issues'},
      author='Odin Kroeger',
      author_email='epnzdp@maskr.me',
      license='MIT',
      python_requires='>=2.7,<4',
      packages=['pandoc_quotes'],
      zip_safe=False,
      install_requires=['panflute', 'pyyaml'],
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 2.7',
                   'Environment :: Console',
                   'Operating System :: OS Independent',
                   'Topic :: Text Processing :: Filters'],
      scripts=['scripts/pandoc-quotes'],
      include_package_data=True)

# This is a bit rude, but it should work on many systems.
for i in ('/usr/local/share/man/man1', '/usr/share/man/man1'):
    if path.exists(i):
        try:
            copy(path.join(path.dirname(__file__), 'man/pandoc-quotes.1'), i)
            break
        except Exception:
            pass
