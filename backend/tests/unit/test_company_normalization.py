import pytest

from app.modules.companies.normalization import normalize_domain


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Example.COM", "example.com"),
        ("https://www.example.com/about", "example.com"),
        ("sub.example.com.", "sub.example.com"),
    ],
)
def test_normalize_domain(value: str, expected: str) -> None:
    assert normalize_domain(value) == expected


@pytest.mark.parametrize("value", ["", "localhost", "not a domain"])
def test_normalize_domain_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        normalize_domain(value)
