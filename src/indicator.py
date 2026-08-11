"""
Bibliometric Normalization System (BNS)

Module      : Bibliometric Indicators
Version     : 1.0.0
Author      : Samet UÇAK
Created     : 2026

Description:
Publication, Citation and Local H-index calculations.
"""

import pandas as pd
from .exceptions import ValidationError

def publication_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate publication count for each normalized author.
    """

    publications = (
        df
        .groupby("normalized_author")
        .size()
        .reset_index(name="publication_count")
    )

    return publications

def citation_count(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total citations for each normalized author.
    """

    df = df.copy()

    df["times_cited"] = pd.to_numeric(
        df["times_cited"],
        errors="coerce"
    ).fillna(0)

    citations = (
        df
        .groupby("normalized_author")["times_cited"]
        .sum()
        .reset_index(name="citation_count")
    )

    return citations
    
def average_citations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate average citations per publication.
    """

    publication = publication_count(df)

    citation = citation_count(df)

    metrics = publication.merge(
        citation,
        on="normalized_author"
    )

    metrics["average_citations"] = (
        metrics["citation_count"] /
        metrics["publication_count"]
    ).round(2)

    return metrics[
        ["normalized_author", "average_citations"]
    ]

def h_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Hirsch h-index for each normalized author.
    """

    results = []

    for author, group in df.groupby("normalized_author"):

        citations = (
            pd.to_numeric(
                group["times_cited"],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
            .sort_values(ascending=False)
            .tolist()
        )
        
        h = 0

        for i, c in enumerate(citations, start=1):

            if c >= i:
                h = i
            else:
                break

        results.append({

            "normalized_author": author,
            "h_index": h

        })

    return pd.DataFrame(results)

def i10_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate i10-index for each normalized author.
    """

    results = []

    for author, group in df.groupby("normalized_author"):

        i10 = (
            pd.to_numeric(
                group["times_cited"],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
            .ge(10)
            .sum()
        )
        
        results.append({

            "normalized_author": author,
            "i10_index": int(i10)

        })

    return pd.DataFrame(results)

def first_publication_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the first publication year for each author.
    """

    return (
        df.groupby("normalized_author")["year"]
        .min()
        .reset_index(name="first_publication_year")
    )

def last_publication_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the most recent publication year for each author.
    """

    return (
        df.groupby("normalized_author")["year"]
        .max()
        .reset_index(name="last_publication_year")
    )

def academic_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate academic age for each author.
    """

    first = first_publication_year(df)

    last = last_publication_year(df)

    age = first.merge(
        last,
        on="normalized_author"
    )

    age["academic_age"] = (
        age["last_publication_year"]
        - age["first_publication_year"]
        + 1
    )

    return age[
        [
            "normalized_author",
            "academic_age"
        ]
    ]

def build_author_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a complete author-level bibliometric indicators table.
    """

    required_columns = [
        "normalized_author",
        "times_cited",
        "year",
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValidationError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    df = df.copy()

    df["times_cited"] = pd.to_numeric(
        df["times_cited"],
        errors="coerce"
    ).fillna(0)

    df["year"] = pd.to_numeric(
        df["year"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["year"]
    )

    publication = publication_count(df)

    citation = citation_count(df)

    average = average_citations(df)

    h = h_index(df)

    i10 = i10_index(df)

    first = first_publication_year(df)

    last = last_publication_year(df)

    age = academic_age(df)

    metrics = (
       
        publication
        .merge(citation, on="normalized_author")
        .merge(average, on="normalized_author")
        .merge(h, on="normalized_author")
        .merge(i10, on="normalized_author")
        .merge(first, on="normalized_author")
        .merge(last, on="normalized_author")
        .merge(age, on="normalized_author")
    )

    return metrics

