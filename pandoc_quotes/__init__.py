# encoding=utf-8
"""Sets the right quotes in a Pandoc Abstract Syntax Tree.

Copyright (c) 2018 Odin Kroeger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Modules
# =======

import os
from operator import itemgetter

import yaml
from panflute import Quoted, Str


# Constants
# =========

_DATA_DIRS_BY_OS = {'posix': ('~/.pandoc',),
                    'nt': (r'~\AppData\Roaming\pandoc',
                           r'~\Application Data\pandoc')}
"""Default Pandoc data directories by operating system type."""

_DATA_DIRS = map(os.path.expanduser, _DATA_DIRS_BY_OS[os.name])
"""Default pandoc data directories for the current operating system."""

_MODULE_DIR = os.path.dirname(__file__)
"""Directory of the current module."""

MAP_FILES = [os.path.join(i, 'quot-marks.yaml')
             for i in [_MODULE_DIR] + _DATA_DIRS]
"""Where to look for quotion maps."""

ENCODING = 'utf-8'
"""The encoding of map files."""

DEFAULT_LANGUAGE = 'en-US'
"""The laguage to use by default, , as RFC 5646-like language code."""


# Exceptions
# ==========

class Error(Exception):
    """Base class for exceptions of this module."""
    format = 'Unspecified error.'
    """Format for error messages, should be overriden by subclasses."""

    def __init__(self, **kwargs):
        """Creates a new exception.

        Arguments:
            ``kwargs`` (mapping):
                A dictionary that is used to fill in values
                in the error message.
        """
        super(Error, self).__init__()
        self.__dict__.update(**kwargs)

    def __str__(self):
        """Returns an error message."""
        return self.format.format(**vars(self))


class QuoMarkNotAStringError(Error):
    """Error raised if a given quotation mark is not of the type ``str``."""
    format = 'given quotation mark is not of type ``str``.'


class QuoMarkNotPrintableError(Error):
    """Error raised if a non-printable string is given as quotation mark."""
    format = '{file} contains non-printable characters.'


class QuoMarkUnknownLangError(Error):
    """Error raised if no quotes are defined for the given language."""
    format = '{lang}: unknown language.'


class QuoMarksWrongNumberError(Error):
    """Error raised if given a wrong number quotation."""
    format = 'quotation-marks: {num} given, 4 expected.'


# Classes
# =======

class QuoMarks(tuple):
    """A tuple that represents quotation marks.

    Items:
        0:  Primary left quotation mark.
        1:  Primary right quotation mark.
        2:  Secondary left quotation mark.
        3:  Secondary right quotation mark.

    All quotation marks must be defined and printable strings.
    """

    def __new__(cls, ldquo, rdquo, lsquo, rsquo):
        """Creates a new tuple to store quotation marks.

        Arguments:
            ``ldquo`` (``str``):
                The left primary quotation mark.
            ``rdquo`` (``str``):
                The right primary quotation mark.
            ``lsquo`` (``str``):
                The left secondary quotation mark.
            ``rsquo`` (``str``):
                The right secondary quotation mark.

        Returns (``QuoMarks``):
            A tuple that represents quotation marks.

        Raises:
            ``QuoMarkNotAStringError``:
                If ``ldquo``, ``rdquo``, ``lsquo``,
                or ``rsquo`` is not a ``basestring``.
        """
        quo_marks = (ldquo, rdquo, lsquo, rsquo)
        for i in quo_marks:
            if not isinstance(i, basestring): # pylint: disable=E0602
                raise QuoMarkNotAStringError()
        return tuple.__new__(cls, quo_marks)

    ldquo = property(itemgetter(0))
    """Primary left quotation mark."""

    rdquo = property(itemgetter(1))
    """Primary right quotation mark."""

    lsquo = property(itemgetter(2))
    """Secondary left quotation mark."""

    rsquo = property(itemgetter(3))
    """Secondary right quotation mark."""


class QuoMarkReplacer: # pylint: disable=R0903
    """Replaces plain quotation marks in a document with typographic ones."""

    def __init__(self, marks=None):
        if not marks is None:
            self.marks = marks

    def __call__(self, elem, doc):
        """Replaces plain quotation marks in a document with typographic ones.

        Which typographic quotation marks will be used depends on the
        metadata fields ``quotation-marks``, ``quotation-lang``, ``lang``
        of ``doc`` (see ``QuoMarks.__init__`` and ``LangQuoMarks.__init__``
        for the format of those fields), with ``quotation-marks`` taking
        precedence over ``quotation-lang`` and ``quotation-lang`` taking
        precedence over ``lang``.

        Arguments:
            ``elem`` (``panflute.Element``):
                An element in the AST.
            ``doc`` (``panflute.Doc``):
                The document.

        Constants:
            ``MAP_FILES`` (sequence of ``str`` instances):
                Where to look for quotion maps.

            ``ENCODING`` (``str``):
                The encoding of map files.

            ``DEFAULT_LANGUAGE`` (``str``)
                The laguage to use by default,
                as RFC 5646-like language code.

        Returns:
            If ``elem`` was not quoted, nothing.
            Otherwise, a list with an opening quote (as ``Str``), the children
                of ``elem``, and a closing quote (as ``Str``), in that order.

        Raises:
            All exceptions ``QuoMarks.__init__`` and
            ``lookup_quotation_marks`` raise.

            ``QuoMarksWrongNumberError``:
                If a wrong number of quotation marks has been given.
        """
        try:
            return replace_quo_marks(elem, self.marks)
        except AttributeError:
            strings = doc.get_metadata('quotation-marks')
            if strings:
                try:
                    self.marks = QuoMarks(*strings)
                except TypeError:
                    raise QuoMarksWrongNumberError(num=len(strings))
                return self(elem, doc)
            lang = doc.get_metadata('quotation-lang')
            if not lang:
                lang = doc.get_metadata('lang')
            if not lang:
                lang = DEFAULT_LANGUAGE
            map_files = doc.get_metadata('quotation-lang-mapping')
            if map_files:
                map_files = MAP_FILES + [os.path.expanduser(map_files)]
            else:
                map_files = MAP_FILES
            self.marks = lookup_quo_marks(lang=lang, map_files=map_files,
                                          encoding=ENCODING)
            return self(elem, doc)


# Functions
# =========

def load_maps(map_files, encoding='utf-8'):
    """Loads maps of RFC 5646-like language codes to quotation marks.

    Arguments:
        ``map_files`` (sequence of ``str`` instances):
            A sequence of possible location of `YAML <http://yaml.org/>`_
            files that contain mappings of RFC 5646-like language codes to
            quotation marks.
        ``encoding`` (``str``):
            The encoding of those files. Defaults to 'utf-8'.

    Returns (``dict``):
        A mapping of RFC 5646-like language codes to quotation marks.
        Quotation marks are represented as ``unicode`` instances,
        *not* as ``QuoMarks`` instances.

    Raises:
        ``QuoMarkNotPrintableError``:
            If a map file contains non-printable characters.

    See ``quot-marks.yaml`` and ``lookup_quotation_marks`` for details.
    """
    maps = {}
    for map_file in map_files:
        if os.path.exists(map_file):
            with open(map_file) as map_fh:
                try:
                    maps.update(yaml.load(map_fh.read().decode(encoding)))
                except UnicodeDecodeError:
                    raise QuoMarkNotPrintableError(file=map_file)
    return maps


def lookup_quo_marks(lang='en-US', map_files=MAP_FILES, encoding='utf-8'):
    """Looks up quotation marks for a language.

    Arguments:
        ``lang`` (``str``):
            An RFC 5646-ish language code (e.g., "en-US", "pt-BR",
            "de", "es"). Defines the language the quotation marks
            of which to look up. Default: 'en-US'.
        ``maps`` (sequence of ``str`` instances):
            A List of possible locations of mappsings of RFC 5646-like
            language codes to lists of quotation marks.
            Default: ``MAP_FILES`` (module constant).
        ``encoding`` (``str``):
            The encoding of those files. Defaults to 'utf-8'.

    If ``lang`` contains a country code, but no quotation marks have
    been defined for that country, the country code is discarded and
    the quotation marks for the language simpliciter are looked up.
    For example, 'de-DE' will find 'de'.

    If ``lang`` does not contain a country code or if that code has been
    discarded and no quotation marks have been defined for that language
    simpliciter, but quotation marks have been defined for variants of that
    language as they are spoken in a particular country, the quotation
    marks of the variant that has been defined first are used. For example,
    'en' will find 'en-US'.

    Returns (``QuoMarks``):
        The quotation marks of that language.

    Raises:
        ``QuoMarkUnknownLanguageError``:
            If no quotation marks have been defined for ``lang``.

        All exceptions ``load_quotation_maps`` and
        ``QuoMarks.__init__`` raise.
    """
    map_ = load_maps(map_files, encoding=encoding)
    for i in range(3):
        try:
            return QuoMarks(*map_[lang])
        except KeyError:
            if i == 0:
                lang = lang.split('-')[0]
            elif i == 1:
                for j in map_:
                    if not isinstance(j, basestring): # pylint: disable=E0602
                        continue
                    if j.startswith(lang):
                        lang = j
                        break
                else:
                    break
    raise QuoMarkUnknownLangError(lang=lang)


def replace_quo_marks(elem, marks): # pylint: disable=R1710
    """Replaces quote nodes with their children flanked by quotation marks.

    Arguments:
        ``elem`` (``panflute.Element``):
            An element in the AST.
        ``marks`` (``QuoMarks``):
            The quotation marks to use.

    Returns:
        If ``elem`` was not quoted, nothing.
        Otherwise, a list with an opening quote (as ``Str``), the children
            of ``elem``, and a closing quote (as ``Str``), in that order.
    """
    if isinstance(elem, Quoted):
        unquoted = list(elem.content)
        if elem.quote_type == 'SingleQuote':
            return [Str(marks.lsquo)] + unquoted + [Str(marks.rsquo)]
        elif elem.quote_type == 'DoubleQuote':
            return [Str(marks.ldquo)] + unquoted + [Str(marks.rdquo)]
