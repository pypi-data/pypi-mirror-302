# Bibliograpy

Bibliography management to decorate source code.

[![example workflow](https://github.com/SamuelAndresPascal/cosmoloj-py/actions/workflows/bibliograpy.yml/badge.svg)](https://github.com/SamuelAndresPascal/cosmoloj-py/actions)

[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/version.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/latest_release_date.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/latest_release_relative_date.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/platforms.svg)](https://anaconda.org/cosmoloj/bibliograpy)
[![Anaconda-Server Badge](https://anaconda.org/cosmoloj/bibliograpy/badges/license.svg)](https://anaconda.org/cosmoloj/bibliograpy)

[![PyPI repository Badge](https://badge.fury.io/py/bibliograpy.svg)](https://badge.fury.io/py/bibliograpy)


* [API](#api)
* [Preprocessing tool](#preprocessing-tool)
* [Documentation](#documentation)



## API

The Bibliograpy API allows to manage bibliographic centralized references using decorators.

Hence, is it possible to factorize all bibliographic sources as variables in a single module, using them as arguments of
decorators.

```py
"""The bibliography module."""

from bibliograpy.api import TechReport

IAU_2006_B1 = TechReport.standard(
    cite_key='iau_2006_b1',
    address=None,
    annote=None,
    author='',
    institution='iau',
    month=None,
    note=None,
    number=None,
    title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
    type=None,
    year=2006)
```

```py
"""The bibliography_client module using the bibliography.py module."""

from bibliograpy.api import reference

from bibliography import IAU_2006_B1

@reference(IAU_2006_B1)
def my_function():
    """My my_function documentation."""
    # some implementation here using the reference given as a parameter to the decorator

```

The usage of the decorator has two purposes.

First, to use a bibliographic reference defined once and for all, centralized and reusable.

Second, to implicitly add to the documentation of the decorated entity a bibliographical section.

```
import bibliography_client

>>> help(my_function)
Help on function my_function in module bibliography_client

my_function()
    My my_function documentation.

    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
```

## Preprocessing tool

Bibliograpy allows generating a source code bibliograpy from a resource bibliography file.

Bibliograpy process supports bibliography files in yaml format. Each bibliographic entry contains three fields. 
The `type` field only supports the `misc` value. The `key` fields represents the bibliographic entry unique key (id).
The `title` field represents the readable form or the entry. For instance:

```yml
- entry_type: misc
  cite_key: nasa
  title: NASA
- entry_type: misc
  cite_key: iau
  title: International Astronomical Union
```

This bibliography file can be preprocessend by the `bibliograpy process` tool.

```
bibliograpy process
```

This preprocessing produces the corresponding bibliographic references that can be used as
bibliograpy decorator arguments.

```py
from bibliograpy.api import Misc


NASA = Misc(cite_key='nasa',
            address=None,
            annote=None,
            author=None,
            booktitle=None,
            chapter=None,
            edition=None,
            editor=None,
            howpublished=None,
            institution=None,
            journal=None,
            month=None,
            note=None,
            number=None,
            organization=None,
            pages=None,
            publisher=None,
            school=None,
            series=None,
            title='NASA',
            type=None,
            volume=None,
            year=None,
            doi=None,
            issn=None,
            isbn=None,
            url=None)

IAU = Misc(cite_key='iau',
           address=None,
           annote=None,
           author=None,
           booktitle=None,
           chapter=None,
           edition=None,
           editor=None,
           howpublished=None,
           institution=None,
           journal=None,
           month=None,
           note=None,
           number=None,
           organization=None,
           pages=None,
           publisher=None,
           school=None,
           series=None,
           title='International Astronomical Union',
           type=None,
           volume=None,
           year=None,
           doi=None,
           issn=None,
           isbn=None,
           url=None)
```

## Documentation

[Latest release](https://cosmoloj.com/mkdocs/bibliograpy/latest/)

[Trunk](https://cosmoloj.com/mkdocs/bibliograpy/master/)