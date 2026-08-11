from src.similarity import (
    affiliation_similarity,
    keyword_similarity,
    name_similarity,
    year_similarity,
)


def test_name_similarity_identical_names():
    assert name_similarity("Samet Ucak", "Samet Ucak") == 100.0


def test_name_similarity_similar_names():
    score = name_similarity("Samet Ucak", "Samet Ucakli")

    assert score > 90.0


def test_affiliation_similarity_identical_affiliations():
    assert (
        affiliation_similarity(
            "Istanbul Aydin University",
            "Istanbul Aydin University",
        )
        == 100.0
    )


def test_keyword_similarity_identical_keywords():
    assert (
        keyword_similarity(
            "bibliometrics; microbiology",
            "bibliometrics; microbiology",
        )
        == 100.0
    )


def test_year_similarity_same_year():
    assert year_similarity(2020, 2020) == 100


def test_year_similarity_different_years():
    assert year_similarity(2020, 2025) == 60