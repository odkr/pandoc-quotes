=============
pandoc-quotes
=============

----------------------------------------------------
Replaces plain quotation marks with typographic ones
----------------------------------------------------

:Author: Odin Kroeger
:Date: April 11, 2018
:Version: 0.4.0
:Manual section: 1


SYNOPSIS
========

pandoc-quotes [-h]


DESCRIPTION
===========

``pandoc-quotes`` is a filter for ``pandoc`` that replaces plain, that is,
non-typographic, quotes with typographic ones.

You can define with which typographic quotation marks to replace plain ones
by setting either the ``quotation-marks``, the ``quotation-language``, or
the ``lang`` metadata field.


``quotation-marks``
-------------------

The ``quotation-marks`` metadata field should be a list of four strings, where
the first item lists the primary left quotation mark, the second the primary
right quotation mark, the third the secondary left quotation mark, and the
fourth the secondary right quotation mark.

You always have to set all four quotation marks, even if you do not plan to
use secondary quotation marks.

If each quotation mark consists of precisely one character (it may span
multiple bytes though), you can write the list as a simple string.

If ``quotation-marks`` is set, the other fields are ignored.


``quotation-lang``
------------------

``quotation-lang`` should be an RFC 5646 code for the language the quotation
marks of which shall be used (e.g., "en-US", "pt-BR", "de", "es").

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


ADDING LANGUAGES
================

You can add quotation marks for unsupported languages or override
``pandoc-quotes`` default by placing a ``quot-marks.yaml`` file in
your pandoc data directory. ``quot-marks.yaml`` should be a valid
`YAML <http://yaml.org/>`_ file, which contains pairs of RFC 5646-ish
language codes (e.g., "en-US", "pt-BR", "de", "es") and lists of
quotation marks, in the following order: primary left, primary right,
secondary left, secondary right. If each quotation mark consists of
precisely one character (it may span multiple bytes though), you can
write the list as a simple string.


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
erroneous. See <https://github.com/okroeger/pandoc-quotes> if you'd like to
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
