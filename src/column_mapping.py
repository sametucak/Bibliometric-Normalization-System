"""
Bibliometric Normalization System (BNS)

Module      : Column Mapping
Version     : 1.0.0

Description:
Maps raw bibliometric database columns
to internal BNS standard columns.
"""

import pandas as pd

from .exceptions import ValidationError


def map_wos_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert Web of Science column names
    into BNS standard column names.
    """

    df = df.copy()

    mapping = {
        "Author Full Name": "author",
        "Author Address / Affiliation": "affiliation",
        "Author Keywords": "keywords",
        "Publication Year": "year",
        "Times Cited": "times_cited",
}

    df = df.rename(columns=mapping)

    required = [
        "author",
        "affiliation",
        "keywords",
        "year",
        "times_cited",
]
    
    missing = set(required) - set(df.columns)

    if missing:
        raise ValidationError(
            f"Missing columns after mapping: {', '.join(sorted(missing))}"
        )

    return df