from src.author_normalization import normalize_author_name


def test_normalize_author_name_lowercase():
    assert normalize_author_name("SAMET UCAK") == "samet ucak"


def test_normalize_author_name_whitespace():
    assert normalize_author_name("  SAMET   UCAK  ") == "samet ucak"


def test_normalize_author_name_preserves_order():
    assert normalize_author_name("UCAK, Samet") == "ucak, samet"