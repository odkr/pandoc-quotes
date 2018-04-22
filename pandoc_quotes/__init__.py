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

_PANDOC_DATA_DIRS = {'posix': ('~/.pandoc',),
                     'nt': (r'~\AppData\Roaming\pandoc',
                            r'~\Application Data\pandoc')}
"""Default Pandoc data directories by operating system type."""


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
        super().__init__()
        self.__dict__.update(**kwargs)

    def __str__(self):
        """Returns an error message."""
        return self.format.format(**vars(self))


class QuoMarkNotAStringError(Error):
    """Error raised if a given quotation mark is not of the type ``str``."""
    format = 'given quotation mark is not of type ``str``.'


class QuoMarkNotPrintableError(Error):
    """Error raised if a non-printable string is given as quotation mark."""
    format = 'non-printable string given as quotation mark.'


class QuoMarkUnknownLangError(Error):
    """Error raised if no quotes are defined for the given language."""
    format = '{lang}: unknown language.'


class QuoMarksWrongNumberError(Error):
    """Error raised if given a wrong number quotation."""
    format = 'quotation-marks: {num} given, 4 expected.'


# Classes
# =======

class _LangQuoMarkMap(dict):
    """A mapping of RFC 5646-ish language codes to quotation marks.

    Mappings are loaded from external `YAML <http://yaml.org/>`__ files.
    See ``quot-marks.yaml`` and ``LangQuoMarks.__init__`` below for details.
    """

    module_dir = os.path.dirname(__file__)
    """Directory of the current module."""

    data_dirs = [os.path.expanduser(i)
                 for i in _PANDOC_DATA_DIRS[os.name]]
    """Default pandoc data directories for the current operating."""

    map_files = [os.path.join(i, 'quot-marks.yaml')
                 for i in (module_dir, *data_dirs)]
    """Where to look for quotion maps."""

    def __init__(self):
        """Loads all maps."""
        super().__init__()
        for map_file in self.map_files:
            if os.path.exists(map_file):
                with open(map_file) as map_fh:
                    self.update(yaml.load(map_fh.read()))


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
                or ``rsquo`` is not a ``str``.
            ``QuoMarkNotPrintableError``:
                If ``ldquo``, ``rdquo``, ``lsquo``,
                or ``rsquo`` is not printable.
        """
        quo_marks = (ldquo, rdquo, lsquo, rsquo)
        for i in quo_marks:
            if not isinstance(i, str):
                raise QuoMarkNotAStringError()
            if not i.isprintable():
                raise QuoMarkNotPrintableError()
        return super().__new__(cls, quo_marks)

    ldquo = property(itemgetter(0))
    """Primary left quotation mark."""

    rdquo = property(itemgetter(1))
    """Primary right quotation mark."""

    lsquo = property(itemgetter(2))
    """Secondary left quotation mark."""

    rsquo = property(itemgetter(3))
    """Secondary right quotation mark."""


class LangQuoMarks(tuple):
    """Represents quotation marks of a given language.

    Items:
        0-4: As in ``QuoMarks``
        5: The language code for which quotation marks were found.
    """

    def __new__(cls, lang='en-US'):
        """Looks up quotation marks for a language.

        Arguments:
            ``lang`` (``str``):
                An RFC 5646-ish language code (e.g., "en-US", "pt-BR",
                "de", "es"). Defines the language the quotation marks
                of which to look up. Default: 'en-US'.

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

        Raises:
            ``QuoMarkUnknownLanguageError``:
                If no quotation marks have been defined for ``lang``.

            All exceptions ``QuoMarks`` raises.
        """
        map_ = _LangQuoMarkMap()
        for i in range(3):
            try:
                return super().__new__(cls, (*map_[lang], lang))
            except KeyError:
                if i == 0:
                    lang = lang.split('-')[0]
                elif i == 1:
                    for j in map_:
                        if j.startswith(lang):
                            lang = j
                            break
                    else:
                        break
        raise QuoMarkUnknownLangError(lang=lang)

    ldquo = property(itemgetter(0))
    """Primary left quotation mark."""

    rdquo = property(itemgetter(1))
    """Primary right quotation mark."""

    lsquo = property(itemgetter(2))
    """Secondary left quotation mark."""

    rsquo = property(itemgetter(3))
    """Secondary right quotation mark."""

    lang = property(itemgetter(4))
    """The laguage of the quotation marks."""


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

        Returns:
            If ``elem`` was not quoted, nothing.
            Otherwise, a list with an opening quote (as ``Str``), the children
                of ``elem``, and a closing quote (as ``Str``), in that order.

        Raises:
            All exceptions ``QuoMarks`` and ``LangQuoMarks`` raise.

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
                lang = 'en-US'
            self.marks = LangQuoMarks(lang=lang)
            return self(elem, doc)


# Functions
# =========

def replace_quo_marks(elem, marks): # pylint: disable=R1710
    """Replaces quote nodes with their children flanked by quotation marks.

    Arguments:
        ``elem`` (``panflute.Element``):
            An element in the AST.
        ``marks`` (``QuoMarks`` or ``LangQuoMarks``):
            The quotation marks to use.

    Returns:
        If ``elem`` was not quoted, nothing.
        Otherwise, a list with an opening quote (as ``Str``), the children
            of ``elem``, and a closing quote (as ``Str``), in that order.
    """
    if isinstance(elem, Quoted):
        unquoted = list(elem.content)
        if elem.quote_type == 'SingleQuote':
            return [Str(marks.lsquo), *unquoted, Str(marks.rsquo)]
        elif elem.quote_type == 'DoubleQuote':
            return [Str(marks.ldquo), *unquoted, Str(marks.rdquo)]
