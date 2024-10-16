"""Tests for the stringstyler module."""

from io import StringIO

import pytest

from stringstyler import print_color_text, color_text


@pytest.mark.parametrize(
    "color, style, expected",
    [
        ("red", None, "\x1b[31mHello, World!\x1b[0m\n"),
        ("green", "bold", "\x1b[01;32mHello, World!\x1b[0m\n"),
    ],
)
def test_print_color_text(color, style, expected):
    """Test the print_color_text function."""
    with StringIO() as out:
        text = "Hello, World!"
        print_color_text(text, color=color, style=style, file=out)
        assert out.getvalue() == expected


@pytest.mark.parametrize(
    "color, style, expected",
    [
        ("red", None, "\x1b[31mHello, World!\x1b[0m"),
        ("green", "bold", "\x1b[01;32mHello, World!\x1b[0m"),
    ],
)
def test_color_text(color, style, expected):
    """Test the color_text decorator."""

    @color_text(color=color, style=style)
    def get_text():
        return "Hello, World!"

    assert get_text() == expected
