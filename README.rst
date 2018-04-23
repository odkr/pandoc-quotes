=============
pandoc-quotes
=============

``pandoc-quotes`` is a filter for `pandoc <http://pandoc.org/>`_ that replaces
plain, that is, non-typographic, quotation marks with typographic ones.

You can define which typographic quotation marks to replace plain ones with
by setting either a document's ``quotation-marks``, ``quotation-language``,
or ``lang`` metadata field.

See the `manual page <man/pandoc-quotes.rst>`_ for more details.


Installing ``pandoc-quotes``
============================

You use ``pandoc-quotes`` **at your own risk**. You have been warned.

You need `Python 2.7 <https://www.python.org/>`_ or newer,
`panflute <https://github.com/sergiocorreia/panflute>`_, and
`PyYAML <https://github.com/yaml/pyyaml>`_.

Simply run::

    pip install pandoc_quotes

This will try to install ``pandoc-quotes`` manual page, but this
will only work on a limited number of systems.

Alternatively, you can also download the source for the `current version
<https://codeload.github.com/odkr/pandoc-quotes/tar.gz/v0.5.1>`_.

Simlpy run::

    curl https://codeload.github.com/odkr/pandoc-quotes/tar.gz/v0.5.1 | tar -xz
    cd pandoc-quotes-0.5.1
    python setup.py install


Documentation
=============

See the `manual page <man/pandoc-quotes.rst>`_ and the source for details.


Contact
=======

If there's something wrong with ``pandoc-quotes``, `open an issue
<https://github.com/odkr/pandoc-quotes/issues>`_.


License
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


Further Information
===================

GitHub:
<https://github.com/odkr/pandoc-quotes>

PyPI:
<https://pypi.org/project/pandoc-quotes>
