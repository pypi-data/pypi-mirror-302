"""Test module for bibliograpy"""
import sys
import pydoc

from bibliograpy.api import reference, Misc, TechReport, Reference, ReferenceBuilder

IAU = Misc.standard(cite_key='iau',
                    title='International Astronomical Union')

IAU_2006_B1 = TechReport.standard(
    cite_key='iau_2006_b1',
    author='',
    institution='iau',
    title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
    year=2006)

def test_to_source_bib():
    """test to python source bib serialization"""
    assert (IAU_2006_B1.to_source_bib() ==
"""
IAU_2006_B1 = TechReport.standard(cite_key='iau_2006_b1',
                                  author='',
                                  institution='iau',
                                  title='Adoption of the P03 Precession Theory and Definition of the Ecliptic',
                                  year=2006)""")

def test_dependencies_args_default():
    """test deps command without supplying file"""

    @reference(IAU_2006_B1)
    def bib_ref():
        """ma doc"""

    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(bib_ref) ==
"""Python Library Documentation: function bib_ref in module test_api

b\bbi\bib\bb_\b_r\bre\bef\bf()
    ma doc

    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
""")
    else:
        assert (pydoc.render_doc(bib_ref) ==
"""Python Library Documentation: function bib_ref in module test_api

b\bbi\bib\bb_\b_r\bre\bef\bf()
    ma doc
    
    Bibliography: Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
""")

    @reference([IAU_2006_B1, IAU])
    def bib_ref_foo():
        """ma doc avec plusieurs références"""


    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_api

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références

    Bibliography:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(bib_ref_foo) ==
"""Python Library Documentation: function bib_ref_foo in module test_api

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_f\bfo\boo\bo()
    ma doc avec plusieurs références
    
    Bibliography:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")

    @reference(IAU_2006_B1, IAU)
    def bib_ref_bar():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(bib_ref_bar) ==
"""Python Library Documentation: function bib_ref_bar in module test_api

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_b\bba\bar\br()
    ma doc avec plusieurs références en varargs

    Bibliography:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(bib_ref_bar) ==
"""Python Library Documentation: function bib_ref_bar in module test_api

b\bbi\bib\bb_\b_r\bre\bef\bf_\b_b\bba\bar\br()
    ma doc avec plusieurs références en varargs
    
    Bibliography:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")

def test_custom_reference_builder():
    """test custom reference builder"""

    def custom_wrapper(refs: list[Reference]) -> str:
        if len(refs) == 1:
            return f"\n\nBibliographie: {refs[0].to_pydoc()}\n"

        result = "\n\nBibliographie:\n\n"
        for r in refs:
            result += f"* {r.to_pydoc()}\n"
        return result

    ref = ReferenceBuilder(reference_wrapper=custom_wrapper)

    @ref(IAU_2006_B1, IAU)
    def tatafr():
        """ma doc avec plusieurs références en varargs"""


    if sys.version_info.minor == 12:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs

    Bibliographie:

    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
    else:
        assert (pydoc.render_doc(tatafr) ==
"""Python Library Documentation: function tatafr in module test_api

t\bta\bat\bta\baf\bfr\br()
    ma doc avec plusieurs références en varargs
    
    Bibliographie:
    
    * Adoption of the P03 Precession Theory and Definition of the Ecliptic [iau_2006_b1]
    * International Astronomical Union [iau]
""")
