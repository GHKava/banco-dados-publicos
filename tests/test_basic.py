"""
Test básico para validar CI pipeline.
"""

import pytest


def test_basic_import():
    """Testa import do package principal."""
    import src

    assert src.__version__ == "0.1.0"


def test_basic_math():
    """Teste trivial para validar pytest."""
    assert 1 + 1 == 2


def test_string_operations():
    """Teste de operações de string."""
    text = "banco-dados-publicos"
    assert text.replace("-", "_") == "banco_dados_publicos"
    assert len(text) > 0


@pytest.mark.parametrize(
    "input,expected",
    [
        (1, 1),
        (2, 4),
        (3, 9),
        (4, 16),
    ],
)
def test_square(input, expected):
    """Testa operação de quadrado."""
    assert input**2 == expected
