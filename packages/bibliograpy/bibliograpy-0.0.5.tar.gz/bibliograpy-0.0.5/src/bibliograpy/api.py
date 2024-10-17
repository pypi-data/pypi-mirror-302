"""Bibliograpy API module."""
from __future__ import annotations

import dataclasses
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, repr=False)
class Reference:
    """A bibliography reference."""

    cite_key: str

    address: str | None
    """address of the publisher or the institution
    
    not used in article, misc and unpublished
    optional everywhere else
    https://www.bibtex.com/f/address-field/"""

    annote: str | None
    """an annotation
    
    https://www.bibtex.com/f/annote-field/"""

    author: str | None
    """ist of authors of the work
    
    optional for booklet, manual and misc
    required everywhere else
    https://www.bibtex.com/f/author-field/"""

    booktitle: str | None
    """title of the book
    
    required for incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/booktitle-field/"""

    chapter: str | None
    """number of a chapter in a book
    
    required for inbook and incollection
    not used everywhere else
    https://www.bibtex.com/f/chapter-field/"""

    edition: str | None
    """edition number of a book
    
    optional for book, inbook, incollection and manual
    not used everywhere else
    https://www.bibtex.com/f/edition-field/"""

    editor: str | None
    """list of editors of a book
    
    required for book and inbook
    optional for incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/editor-field/"""

    howpublished: str | None
    """a publication notice for unusual publications
    
    optional for booklet and misc
    not used everywhere else
    https://www.bibtex.com/f/howpublished-field/"""

    institution: str | None
    """name of the institution that published and/or sponsored the report
    
    required for techreport
    not used everywhere else
    https://www.bibtex.com/f/institution-field/
    """

    journal: str | None
    """name of the journal or magazine the article was published in
    
    required for article
    not used everywhere else
    https://www.bibtex.com/f/journal-field/
    """

    month: str | None
    """the month during the work was published
    
    optional
    https://www.bibtex.com/f/month-field/"""

    note: str | None
    """
    notes about the reference
    
    required for unpublished
    optional everywhere else
    https://www.bibtex.com/f/note-field/"""

    number: str | int | None
    """number of the report or the issue number for a journal article
    
    optional for article, book, inbook, incollection, inproceedings and techreport
    not used everywhere else
    https://www.bibtex.com/f/number-field/"""

    organization: str | None
    """name of the institution that organized or sponsored the conference or that published the manual
    
    optional for inproceedings and manual
    not used everywhere else
    https://www.bibtex.com/f/organization-field/"""

    pages: str | int | None
    """page numbers or a page range
    
    required for inbook
    optional for article, incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/pages-field/"""

    publisher: str | None
    """name of the publisher
    
    required for book, inbook and incollection
    optional for inproceedings
    not used everywhere else
    https://www.bibtex.com/f/publisher-field/"""

    school: str | None
    """name of the university or degree awarding institution
    
    required for masterthesis and phdthesis
    not used everywhere else
    https://www.bibtex.com/f/school-field/"""

    series: str | None
    """name of the series or set of books
    
    optional for book, inbook, incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/series-field/"""

    title: str | None
    """title of the work
    
    optional for misc
    required everywhere else
    https://www.bibtex.com/f/title-field/"""

    type: str | None
    """type of the technical report or thesis
    
    optional for inbook, incollection, masterthesis and techreport
    not used everywhere else
    https://www.bibtex.com/f/type-field/"""

    volume: str | int | None
    """volume number
    
    optional for article, book, inbook, incollection and inproceedings
    not used everywhere else
    https://www.bibtex.com/f/volume-field/"""

    year: str | int | None
    """year the book was published
    
    required for article, book, inbook, incollection, inproceedings, masterthesis, phdthesis, techreport
    optional for booklet, misc and unpublished
    not used for manual
    https://www.bibtex.com/f/year-field/"""

    ### Non-standard

    doi: str | None
    """DOI number"""

    issn: str | None
    """ISSN number"""

    isbn: str | None
    """ISBN number"""

    url: str | None
    """URL of a web page"""


    def to_source_bib(self) -> str:
        """Serialization of the reference in processed python code."""

        base = f"{self.cite_key.upper()} = {type(self).__name__}.standard("

        fields = []
        for f in dataclasses.fields(type(self)):
            value = getattr(self, f.name)

            if isinstance(value, str):
                fields.append(f"{f.name}='{getattr(self, f.name)}'")
            elif isinstance(value, dict):
                fields.append(f"{f.name}='{getattr(self, f.name)['cite_key']}'")
            elif value is not None:
                fields.append(f'{f.name}={getattr(self, f.name)}')

        sep = ',\n'
        for _ in range(len(base)):
            sep += ' '
        return f"\n{base}{sep.join(fields)})"

    def to_pydoc(self) -> str:
        """Serialization of the reference in docstring."""
        return f"{self.title} [{self.cite_key}]"

    @classmethod
    def generic(cls,
                cite_key: str,
                address: str | None,
                annote: str | None,
                booktitle: str | None,
                author: str | None,
                chapter: str | None,
                edition: str | None,
                editor: str | None,
                howpublished: str | None,
                institution: str | None,
                journal: str | None,
                month: str | None,
                note: str | None,
                number: str | None,
                organization: str | None,
                pages: str | int | None,
                publisher: str | None,
                school: str | None,
                series: str | None,
                title: str | None,
                type: str | None,
                volume: str | int | None,
                year: str | int | None,
                doi: str | None,
                issn: str | None,
                isbn: str | None,
                url: str | None):
        """builds a generic reference, allowing to init each field"""
        return cls(cite_key=cite_key,
                   address=address,
                   annote=annote,
                   booktitle=booktitle,
                   author=author,
                   chapter=chapter,
                   edition=edition,
                   editor=editor,
                   howpublished=howpublished,
                   institution=institution,
                   journal=journal,
                   month=month,
                   note=note,
                   number=number,
                   organization=organization,
                   pages=pages,
                   publisher=publisher,
                   school=school,
                   series=series,
                   title=title,
                   type=type,
                   volume=volume,
                   year=year,
                   doi=doi,
                   issn=issn,
                   isbn=isbn,
                   url=url)

    @classmethod
    def optionals(cls,
                cite_key: str,
                address: str | None = None,
                annote: str | None = None,
                booktitle: str | None = None,
                author: str | None = None,
                chapter: str | None = None,
                edition: str | None = None,
                editor: str | None = None,
                howpublished: str | None = None,
                institution: str | None = None,
                journal: str | None = None,
                month: str | None = None,
                note: str | None = None,
                number: str | None = None,
                organization: str | None = None,
                pages: str | int | None = None,
                publisher: str | None = None,
                school: str | None = None,
                series: str | None = None,
                title: str | None = None,
                type: str | None = None,
                volume: str | int | None = None,
                year: str | int | None = None,
                doi: str | None = None,
                issn: str | None = None,
                isbn: str | None = None,
                url: str | None = None):
        """builds a reference, allowing to init each field or let it empty (only cite_key is mandatory)"""
        return cls(cite_key=cite_key,
                   address=address,
                   annote=annote,
                   booktitle=booktitle,
                   author=author,
                   chapter=chapter,
                   edition=edition,
                   editor=editor,
                   howpublished=howpublished,
                   institution=institution,
                   journal=journal,
                   month=month,
                   note=note,
                   number=number,
                   organization=organization,
                   pages=pages,
                   publisher=publisher,
                   school=school,
                   series=series,
                   title=title,
                   type=type,
                   volume=volume,
                   year=year,
                   doi=doi,
                   issn=issn,
                   isbn=isbn,
                   url=url)

    @classmethod
    def from_dict(cls, source: dict):
        """Builds a Configuration from a configuration dict."""
        return cls(
            cite_key=source['cite_key'],
            address=source['address'] if 'address' in source else None,
            annote=source['annote'] if 'annote' in source else None,
            author=source['author'] if 'author' in source else None,
            booktitle=source['booktitle'] if 'booktitle' in source else None,
            chapter=source['chapter'] if 'chapter' in source else None,
            edition=source['edition'] if 'edition' in source else None,
            editor=source['editor'] if 'editor' in source else None,
            howpublished=source['howpublished'] if 'howpublished' in source else None,
            institution=source['institution'] if 'institution' in source else None,
            journal=source['journal'] if 'journal' in source else None,
            month=source['month'] if 'month' in source else None,
            note=source['note'] if 'note' in source else None,
            number=source['number'] if 'number' in source else None,
            organization=source['organization'] if 'organization' in source else None,
            pages=source['pages'] if 'pages' in source else None,
            publisher=source['publisher'] if 'publisher' in source else None,
            school=source['school'] if 'school' in source else None,
            series=source['series'] if 'series' in source else None,
            title=source['title'] if 'title' in source else None,
            type=source['type'] if 'type' in source else None,
            volume=source['volume'] if 'volume' in source else None,
            year=source['year'] if 'year' in source else None,
            doi=source['doi'] if 'doi' in source else None,
            issn=source['issn'] if 'issn' in source else None,
            isbn=source['isbn'] if 'isbn' in source else None,
            url=source['url'] if 'url' in source else None)


@dataclass(frozen=True)
class ReferenceBuilder:
    """A builder of reference decorators."""

    reference_wrapper: Callable[[list[Reference]], str]

    @staticmethod
    def _default_lambda(refs: list[Reference]) -> str:

        if len(refs) == 1:
            return f"\n\nBibliography: {refs[0].to_pydoc()}\n"

        result = "\n\nBibliography:\n\n"
        for r in refs:
            result += f"* {r.to_pydoc()}\n"
        return result

    @staticmethod
    def default():
        """the default reference decorator"""
        return ReferenceBuilder(reference_wrapper=ReferenceBuilder._default_lambda)

    def __call__(self, *refs):
        """The reference decorator."""

        def internal(obj):
            if len(refs) == 1:
                ref0 = refs[0]
                if isinstance(ref0, Reference):
                    obj.__doc__ += self.reference_wrapper([ref0])
                elif isinstance(ref0, list):
                    obj.__doc__ += self.reference_wrapper(ref0)
            else:
                obj.__doc__ += self.reference_wrapper([*refs])
            return obj

        return internal

reference = ReferenceBuilder.default()

_bibtex_com = reference(Reference.optionals(cite_key='bibtex_com',
                                            title='www.bibtex.com'))

_bibtex_package = reference(
    Reference.optionals(cite_key='bibtex_package',
                        title='CTAN Bibtex package documentation',
                        url='https://distrib-coffee.ipsl.jussieu.fr/pub/mirrors/ctan/biblio/bibtex/base/btxdoc.pdf'))

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Article(Reference):
    """any article published in a periodical like a journal article or magazine article"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Book(Reference):
    """a book"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Booklet(Reference):
    """like a book but without a designated publisher"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Conference(Reference):
    """a conference paper"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Inbook(Reference):
    """a section or chapter in a book"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Incollection(Reference):
    """an article in a collection"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Inproceedings(Reference):
    """a conference paper (same as the conference entry type)"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Manual(Reference):
    """a technical manual"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Masterthesis(Reference):
    """a Masters thesis"""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Misc(Reference):
    """used if nothing else fits

    misc Use this type when nothing else fits.
    Required fields: none.
    Optional fields: author, title, howpublished, month, year, note."""

    @staticmethod
    def standard(cite_key: str,
                 annote: str | None = None,
                 author: str | None = None,
                 howpublished: str | None = None,
                 month: str | None = None,
                 note: str | None = None,
                 title: str | None = None,
                 year: str | int | None = None,
                 doi: str | None = None,
                 issn: str | None = None,
                 isbn: str | None = None,
                 url: str | None = None):
        """builds a standard misc reference"""

        return Misc(cite_key=cite_key,
                    address=None,
                    annote=annote,
                    booktitle=None,
                    author=author,
                    chapter=None,
                    edition=None,
                    editor=None,
                    howpublished=howpublished,
                    institution=None,
                    journal=None,
                    month=month,
                    note=note,
                    number=None,
                    organization=None,
                    pages=None,
                    publisher=None,
                    school=None,
                    series=None,
                    title=title,
                    type=None,
                    volume=None,
                    year=year,
                    doi=doi,
                    issn=issn,
                    isbn=isbn,
                    url=url)

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Phdthesis(Reference):
    """a PhD thesis

    phdthesis A PhD thesis.
    Required fields: author, title, school, year.
    Optional fields: type, address, month, note."""

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Proceedings(Reference):
    """the whole conference proceedings

    proceedings The proceedings of a conference.
    Required fields: title, year.
    Optional fields: editor, volume or number, series, address, month, organization, publisher, note."""

    @staticmethod
    def standard(cite_key: str,
                 title: str,
                 year: str | int,
                 annote: str | None = None,
                 editor: str | None = None,
                 number: str | None = None,
                 volume: str | int | None = None,
                 series: str | None = None,
                 address: str | None = None,
                 month: str | None = None,
                 organization: str | None = None,
                 publisher: str | None = None,
                 note: str | None = None,
                 doi: str | None = None,
                 issn: str | None = None,
                 isbn: str | None = None,
                 url: str | None = None):
        """builds a standard proceedings reference"""
        return Proceedings(cite_key=cite_key,
                           address=address,
                           annote=annote,
                           booktitle=None,
                           author=None,
                           chapter=None,
                           edition=None,
                           editor=editor,
                           howpublished=None,
                           institution=None,
                           journal=None,
                           month=month,
                           note=note,
                           number=number,
                           organization=organization,
                           pages=None,
                           publisher=publisher,
                           school=None,
                           series=series,
                           title=title,
                           type=None,
                           volume=volume,
                           year=year,
                           doi=doi,
                           issn=issn,
                           isbn=isbn,
                           url=url)

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class TechReport(Reference):
    """a technical report, government report or white paper

    techreport A report published by a school or other institution, usually numbered within a series.
    Required fields: author, title, institution, year.
    Optional fields: type, number, address, month, note."""

    @staticmethod
    def standard(cite_key: str,
                 author: str,
                 institution: str,
                 title: str,
                 year: str | int,
                 address: str | None = None,
                 annote: str | None = None,
                 month: str | None = None,
                 note: str | None = None,
                 number: str | None = None,
                 type: str | None = None,
                 doi: str | None = None,
                 issn: str | None = None,
                 isbn: str | None = None,
                 url: str | None = None):
        """builds a standard techreport reference"""
        return TechReport(cite_key=cite_key,
                   address=address,
                   annote=annote,
                   booktitle=None,
                   author=author,
                   chapter=None,
                   edition=None,
                   editor=None,
                   howpublished=None,
                   institution=institution,
                   journal=None,
                   month=month,
                   note=note,
                   number=number,
                   organization=None,
                   pages=None,
                   publisher=None,
                   school=None,
                   series=None,
                   title=title,
                   type=type,
                   volume=None,
                   year=year,
                   doi=doi,
                   issn=issn,
                   isbn=isbn,
                   url=url)

@_bibtex_package
@_bibtex_com
@dataclass(frozen=True, repr=False)
class Unpublished(Reference):
    """a work that has not yet been officially published

    unpublished A document having an author and title, but not formally published.
    Required fields: author, title, note.
    Optional fields: month, year."""

    @staticmethod
    def standard(cite_key: str,
                 author: str,
                 note: str,
                 title: str,
                 annote: str | None = None,
                 month: str | None = None,
                 year: str | int | None = None,
                 doi: str | None = None,
                 issn: str | None = None,
                 isbn: str | None = None,
                 url: str | None = None):
        """builds a standard unpublished reference"""
        return Unpublished(cite_key=cite_key,
                   address=None,
                   annote=annote,
                   booktitle=None,
                   author=author,
                   chapter=None,
                   edition=None,
                   editor=None,
                   howpublished=None,
                   institution=None,
                   journal=None,
                   month=month,
                   note=note,
                   number=None,
                   organization=None,
                   pages=None,
                   publisher=None,
                   school=None,
                   series=None,
                   title=title,
                   type=None,
                   volume=None,
                   year=year,
                   doi=doi,
                   issn=issn,
                   isbn=isbn,
                   url=url)
