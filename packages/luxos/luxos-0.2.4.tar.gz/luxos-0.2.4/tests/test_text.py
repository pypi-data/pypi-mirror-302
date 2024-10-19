# ruff: noqa: W291, W293
from __future__ import annotations

import pytest

from luxos import text


def test_indent():
    txt = """

            Lorem Ipsum is simply dummy text of the printing and
          typesetting industry. Lorem Ipsum has been the industry's standard
         dummy text ever since the 1500s, when an unknown printer
           took a galley of type and scrambled it to make a type specimen book.
"""

    assert (
        text.indent(txt, "." * 2)
        == """\
..
..
..   Lorem Ipsum is simply dummy text of the printing and
.. typesetting industry. Lorem Ipsum has been the industry's standard
..dummy text ever since the 1500s, when an unknown printer
..  took a galley of type and scrambled it to make a type specimen book.
"""
    )


def test_indent2():
    txt = """\
     An unusually complicated text
    with un-even indented lines
   that make life harder
"""
    assert (
        text.indent(txt, pre="..")
        == """\
..  An unusually complicated text
.. with un-even indented lines
..that make life harder
"""
    )


def test_md():
    txt = """
    ### An example

    This is an example of help file, written in MD. The text.md(txt) function should
    format this nicely:
    
    - item 1
    - item 2
    
    | Tables   |      Are      |  Cool |
    |----------|:-------------:|------:|
    | col 1 is |  left-aligned | $1600 |
    | col 2 is |    centered   |   $12 |
    | col 3 is | right-aligned |    $1 |
"""

    assert (
        text.md(txt, md=False)
        == """
### An example

This is an example of help file, written in MD. The text.md(txt) function should
format this nicely:

- item 1
- item 2

| Tables   |      Are      |  Cool |
|----------|:-------------:|------:|
| col 1 is |  left-aligned | $1600 |
| col 2 is |    centered   |   $12 |
| col 3 is | right-aligned |    $1 |
"""
    )


def test_md_rich():
    pytest.importorskip("rich")

    txt = """
        ### An example

        This is an example of help file, written in MD. The text.md(txt) function should
        format this nicely:

        - item 1
        - item 2

        | Tables   |      Are      |  Cool |
        |----------|:-------------:|------:|
        | col 1 is |  left-aligned | $1600 |
        | col 2 is |    centered   |   $12 |
        | col 3 is | right-aligned |    $1 |
    """

    assert (
        text.md(txt, width=80)
        == """\
                                   An example                                   

This is an example of help file, written in MD. The text.md(txt) function should
format this nicely:                                                             

 • item 1                                                                       
 • item 2                                                                       

                                    
  Tables          Are         Cool  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
  col 1 is   left-aligned    $1600  
  col 2 is     centered        $12  
  col 3 is   right-aligned      $1  
                                    
"""
    )
    pass
