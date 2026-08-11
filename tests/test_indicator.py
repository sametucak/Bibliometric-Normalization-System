import pandas as pd

from src.indicator import publication_count


def test_publication_count():
    df = pd.DataFrame(
        {
            "normalized_author": [
                "samet ucak",
                "samet ucak",
                "ali veli",
            ]
        }
    )

    result = publication_count(df)

    samet = result.loc[
        result["normalized_author"] == "samet ucak",
        "publication_count",
    ].iloc[0]

    ali = result.loc[
        result["normalized_author"] == "ali veli",
        "publication_count",
    ].iloc[0]

    assert samet == 2
    assert ali == 1

from src.indicator import citation_count


def test_citation_count():
    df = pd.DataFrame(
        {
            "normalized_author": [
                "samet ucak",
                "samet ucak",
                "ali veli",
            ],
            "times_cited": [10, 5, 20],
        }
    )

    result = citation_count(df)

    assert result.loc[
        result["normalized_author"] == "samet ucak",
        "citation_count",
    ].iloc[0] == 15

    assert result.loc[
        result["normalized_author"] == "ali veli",
        "citation_count",
    ].iloc[0] == 20

from src.indicator import average_citations


def test_average_citations():
    df = pd.DataFrame(
        {
            "normalized_author": [
                "samet ucak",
                "samet ucak",
                "ali veli",
            ],
            "times_cited": [10, 5, 20],
        }
    )

    result = average_citations(df)

    assert result.loc[
        result["normalized_author"] == "samet ucak",
        "average_citations",
    ].iloc[0] == 7.5

    assert result.loc[
        result["normalized_author"] == "ali veli",
        "average_citations",
    ].iloc[0] == 20.0

from src.indicator import h_index


def test_h_index():
    df = pd.DataFrame(
        {
            "normalized_author": [
                "samet ucak",
                "samet ucak",
                "samet ucak",
                "ali veli",
                "ali veli",
            ],
            "times_cited": [10, 8, 5, 20, 3],
        }
    )

    result = h_index(df)

    assert result.loc[
        result["normalized_author"] == "samet ucak",
        "h_index",
    ].iloc[0] == 3

    assert result.loc[
        result["normalized_author"] == "ali veli",
        "h_index",
    ].iloc[0] == 2

from src.indicator import i10_index

def test_i10_index():
    df = pd.DataFrame({
        "normalized_author": [
            "samet ucak", "samet ucak", "samet ucak", "samet ucak",
            "ali veli", "ali veli", "ali veli"
        ],
        "times_cited": [15, 12, 10, 8, 20, 10, 3]
    })

    result = i10_index(df)

    samet = result.loc[
        result["normalized_author"] == "samet ucak", "i10_index"
    ].iloc[0]

    ali = result.loc[
        result["normalized_author"] == "ali veli", "i10_index"
    ].iloc[0]

    assert samet == 3
    assert ali == 2

from src.indicator import first_publication_year


def test_first_publication_year():
    df = pd.DataFrame({
        "normalized_author": [
            "samet ucak",
            "samet ucak",
            "samet ucak",
            "ali veli",
            "ali veli",
        ],
        "year": [2020, 2018, 2022, 2019, 2021],
    })

    result = first_publication_year(df)

    assert result.loc[
        result["normalized_author"] == "samet ucak",
        "first_publication_year",
    ].iloc[0] == 2018

    assert result.loc[
        result["normalized_author"] == "ali veli",
        "first_publication_year",
    ].iloc[0] == 2019

from src.indicator import last_publication_year


def test_last_publication_year():
    df = pd.DataFrame({
        "normalized_author": [
            "samet ucak",
            "samet ucak",
            "samet ucak",
            "ali veli",
            "ali veli",
        ],
        "year": [2020, 2018, 2022, 2019, 2021],
    })

    result = last_publication_year(df)

    assert result.loc[
        result["normalized_author"] == "samet ucak",
        "last_publication_year",
    ].iloc[0] == 2022

    assert result.loc[
        result["normalized_author"] == "ali veli",
        "last_publication_year",
    ].iloc[0] == 2021

from src.indicator import academic_age


def test_academic_age():
    df = pd.DataFrame({
        "normalized_author": [
            "samet ucak",
            "samet ucak",
            "ali veli",
            "ali veli",
        ],
        "year": [2018, 2022, 2019, 2021],
    })

    result = academic_age(df)

    assert result.loc[
        result["normalized_author"] == "samet ucak",
        "academic_age",
    ].iloc[0] == 5

    assert result.loc[
        result["normalized_author"] == "ali veli",
        "academic_age",
    ].iloc[0] == 3

from src.indicator import build_author_metrics


def test_build_author_metrics():
    df = pd.DataFrame({
        "normalized_author": [
            "samet ucak",
            "samet ucak",
            "samet ucak",
            "ali veli",
            "ali veli",
        ],
        "times_cited": [15, 12, 10, 20, 10],
        "year": [2018, 2020, 2022, 2019, 2021],
    })

    result = build_author_metrics(df)

    expected_columns = [
        "normalized_author",
        "publication_count",
        "citation_count",
        "average_citations",
        "h_index",
        "i10_index",
        "first_publication_year",
        "last_publication_year",
        "academic_age",
    ]

    assert result.columns.tolist() == expected_columns

    samet = result.loc[
        result["normalized_author"] == "samet ucak"
    ].iloc[0]

    assert samet["publication_count"] == 3
    assert samet["citation_count"] == 37
    assert samet["average_citations"] == 12.33
    assert samet["h_index"] == 3
    assert samet["i10_index"] == 3
    assert samet["first_publication_year"] == 2018
    assert samet["last_publication_year"] == 2022
    assert samet["academic_age"] == 5

    ali = result.loc[
        result["normalized_author"] == "ali veli"
    ].iloc[0]

    assert ali["publication_count"] == 2
    assert ali["citation_count"] == 30
    assert ali["average_citations"] == 15.0
    assert ali["h_index"] == 2
    assert ali["i10_index"] == 2
    assert ali["first_publication_year"] == 2019
    assert ali["last_publication_year"] == 2021
    assert ali["academic_age"] == 3