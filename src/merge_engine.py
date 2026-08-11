"""
Bibliometric Normalization System (BNS)

Module      : Merge Engine
Version     : 1.0.0
Author      : Samet UÇAK
Created     : 2026

Description:
Author merge and canonical author selection.
"""
import re
import pandas as pd

from .similarity import (
    confidence_score,
    merge_decision,
)

def get_first_initial(author_name: str) -> str:
    """
    Extract the first initial from an author name.
    Example:
        'Lugli, Gabriele Andrea' -> 'G'
        'Lugli, G. Andrea' -> 'G'
    """
    try:
        given = author_name.split(",")[1].strip()

        m = re.match(r"([A-Za-z])", given)

        if m:
            return m.group(1).upper()

    except Exception:
        pass

    return ""
    
def build_merge_candidates(author_groups: dict) -> pd.DataFrame:
    """
    Build candidate author pairs using:
      - same surname
      - same first initial
    """

    merge_table = []

    for lastname, authors in author_groups.items():

        if len(authors) < 2:
            continue

        initials = {}

        for author in authors:

            initial = get_first_initial(author)

            initials.setdefault(initial, []).append(author)

        for initial_authors in initials.values():

            if len(initial_authors) < 2:
                continue

            for i in range(len(initial_authors)):

                for j in range(i + 1, len(initial_authors)):

                    merge_table.append({

                        "lastname": lastname,
                        "author1": initial_authors[i],
                        "author2": initial_authors[j]

                    })

    return pd.DataFrame(merge_table)
    
def calculate_confidence(row: pd.Series,
                         author_lookup: pd.DataFrame) -> float:
    """
    Calculate confidence score for one author pair.
    """

    a = author_lookup.loc[row["author1"]]
    b = author_lookup.loc[row["author2"]]

    score = confidence_score(

        row["author1"],
        row["author2"],

        a["normalized_affiliation"],
        b["normalized_affiliation"],

        a["normalized_keywords"],
        b["normalized_keywords"],

        a["year"],
        b["year"]

    )

    return score
    
def score_merge_candidates(
    merge_df: pd.DataFrame,
    author_lookup: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate confidence score and decision
    for all merge candidates.
    """

    merge_df = merge_df.copy()

    scores = []

    for i, row in merge_df.iterrows():

        try:
            score = calculate_confidence(
                row,
                author_lookup
            )

        except Exception:
            score = 0

        scores.append(score)

    merge_df["confidence"] = scores
    merge_df["decision"] = merge_df["confidence"].apply(
        merge_decision
    )

    return merge_df
    
def select_canonical_author(
    author_a: str,
    author_b: str,
) -> str:
    """
    Select the canonical (preferred) author name
    between two equivalent author names.
    """

    score_a = 0
    score_b = 0

    if len(author_a) > len(author_b):
        score_a += 1
    elif len(author_b) > len(author_a):
        score_b += 1

    if "." not in author_a:
        score_a += 1

    if "." not in author_b:
        score_b += 1

    given_a = author_a.split(",")[1].strip()
    given_b = author_b.split(",")[1].strip()

    if len(given_a) > len(given_b):
        score_a += 1
    elif len(given_b) > len(given_a):
        score_b += 1

    if score_a >= score_b:
        return author_a

    return author_b
    
def build_author_lookup(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create one representative record for each normalized author.
    """

    df = df.copy()

    # Ensure citation counts are numeric
    df["times_cited"] = pd.to_numeric(
        df["times_cited"],
        errors="coerce"
    ).fillna(0)

    author_lookup = (
        df
        .sort_values("times_cited", ascending=False)
        .drop_duplicates(subset="normalized_author")
        .set_index("normalized_author")
    )

    return author_lookup


def build_author_groups(
    df: pd.DataFrame,
) -> dict:
    """
    Group normalized authors by surname.
    """

    groups = {}

    for author in df["normalized_author"].dropna().unique():

        lastname = author.split(",")[0].strip()

        groups.setdefault(lastname, []).append(author)

    return groups

def apply_author_merges(
    df: pd.DataFrame,
    merge_results: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply automatic author merges.

    Creates canonical_author column.
    """

    df = df.copy()

    df["canonical_author"] = df["normalized_author"]

    automatic = merge_results[
        merge_results["decision"] == "Automatic Merge"
    ]

    for _, row in automatic.iterrows():

        author1 = row["author1"]
        author2 = row["author2"]

        canonical = select_canonical_author(
            author1,
            author2
        )

        replace = (
            author2
            if canonical == author1
            else author1
        )

        df.loc[
            df["canonical_author"] == replace,
            "canonical_author"
        ] = canonical

    return df