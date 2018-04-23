=============
pandoc-quotes
=============

----------------------------------------------------
Replaces plain quotation marks with typographic ones
----------------------------------------------------

:Author: Odin Kroeger
:Date: April 22, 2018
:Version: 0.6.0
:Manual section: 1


SYNOPSIS
========

pandoc-quotes [-h]


DESCRIPTION
===========

``pandoc-quotes`` is a filter for ``pandoc`` that replaces plain, that is,
non-typographic, quotes with typographic ones.

You can define which typographic quotation marks to replace plain ones with
by setting either a document's ``quotation-marks``, ``quotation-language``,
or ``lang`` metadata field.


``quotation-marks``
-------------------

A list of four strings, where the first item lists the primary left quotation
mark, the second the primary right quotation mark, the third the secondary
left quotation mark, and the fourth the secondary right quotation mark.

For example::

    ---
    quotation-marks:
        - ''
        - ´´
        - '
        - ´
    ...

You always have to set all four quotation marks.

If each quotation mark consists of precisely one character,
you can write the list as a simple string.

For example::

    ---
    quotation-marks: ""''
    ...

If ``quotation-marks`` is set, the other fields are ignored.


``quotation-lang``
------------------

An `RFC 5646`_-like code for the language the quotation marks of
which shall be used (e.g., "en-US", "pt-BR", "de", "es").

For example::

    ---
    quotation-lang: de-AT
    ...

**Note:** Only the language and the country tags of RFC 5646 are supported.
So, "it-CH" (i.e., Italian as spoken in Switzerland) is fine, but "it-756"
(also Italian as spoken in Switzerland) will just return the quotation
marks for "it" (i.e., Italian as spoken in general).

If ``quotation-marks`` is set, ``lang`` is ignored.


``lang``
--------

The format of ``lang`` is the same as for ``quotation-lang``.

``lang`` is the metadata field that ``pandoc-citeproc`` uses to define
what language your reference list should be in. If ``pandoc-citeproc``
and ``pandoc-quotes`` both support your language, you need not set
``quotation-lang``, ``pandoc-quotes`` will use ``lang``, too.

For example::

    ---
    lang: de-AT
    ...


ADDING LANGUAGES
================

You can add quotation marks for unsupported languages, or override the
defaults of ``pandoc-quotes``, by placing a file named ``quot-marks.yaml``
in your pandoc data directory.

``quot-marks.yaml`` should be a, UTF-8 encoded, YAML_ file. It should
contain mappings of `RFC 5646`_-like language codes (e.g., "en-US", "pt-BR",
"de", "es") to lists of quotation marks, which are given in the same
format as for ``quotation-marks``.

See the ``quot-marks.yaml`` file that comes with ``pandoc-quotes``
for an example.

You can tell ``pandoc-quotes`` to look for such a mapping elsewhere, too, by
setting the ``quotation-lang-mapping`` metadata field to the path of such a
file. '~' will be replaced with your home directory. You can name that file
as you like.

For example::

    ---
    quotation-lang-mapping: ~/.panzer/my-quot-marks.yaml
    ...


CAVEATS
=======

``pandoc`` represents documents as abstract syntax trees, and quotations are
nodes in that tree. However, ``pandoc-quotes`` replaces those nodes with the
content of the quotation, adding proper quotation marks. Put another way,
``pandoc-quotes`` pushes quotations from the syntax of a document's
representation into its semantics. As a consequence, ``pandoc`` will no longer
recognise quotes. Also, filters running after ``pandoc-quotes`` won't either.
Therefore, you should *not* use ``pandoc-quotes`` with output formats that
represent quotes syntactically (e.g., HTML, LaTeX, ConTexT). Also, it should
be the last or one of the last filters you apply.

Support for quotation styles of different languages is incomplete and likely
erroneous. See <https://github.com/odkr/pandoc-quotes> if you'd like to
help fix this.


LICENSE
=======

Copyright 2018 Odin Kroeger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


FURTHER INFORMATION
===================

* <https://github.com/odkr/pandoc-quotes>
* <https://pypi.org/project/pandoc-quotes>


SEE ALSO
========

pandoc(1), pandoc-citeproc(1)


.. _`RFC 5646`: https://tools.ietf.org/html/rfc5646
.. _YAML: http://yaml.org/
