from src.author_normalization import normalize_author_name, extract_last_name


def test_normalize_author_name_lowercase():
    assert normalize_author_name("SAMET UCAK") == "samet ucak"


def test_normalize_author_name_whitespace():
    assert normalize_author_name("  SAMET   UCAK  ") == "samet ucak"


def test_normalize_author_name_preserves_order():
    assert normalize_author_name("UCAK, Samet") == "ucak, samet"


def test_extract_last_name_wos_surname_initial():
    assert extract_last_name("Smith J") == "smith"


def test_extract_last_name_wos_surname_full_name():
    assert extract_last_name("Smith John") == "smith"


def test_extract_last_name_wos_initial_surname():
    assert extract_last_name("J Smith") == "smith"


def test_extract_last_name_comma_format():
    assert extract_last_name("Smith, John") == "smith"
