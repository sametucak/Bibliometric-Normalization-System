"""
Bibliometric Normalization System (BNS)

Module: Author ID Generator
"""

import pandas as pd


def assign_author_ids(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Assign unique IDs to normalized authors.
    """

    df = df.copy()

    authors = (
        df["normalized_author"]
        .dropna()
        .unique()
    )

    author_map = {
        author: f"A{index:06d}"
        for index, author in enumerate(authors, start=1)
    }

    df["author_id"] = (
        df["normalized_author"]
        .map(author_map)
    )

    return df