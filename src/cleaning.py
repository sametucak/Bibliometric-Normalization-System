"""
Bibliometric Normalization System (BNS)

Module      : Data Cleaning
Version     : 1.0.0
Author      : Samet UÇAK
Created     : 2026

Description:
Data cleaning and preprocessing functions.
"""

import pandas as pd

from .exceptions import ValidationError


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic data cleaning.
    """

    if df.empty:
        raise ValidationError("Input dataset is empty.")

    df = df.copy()

    df.columns = df.columns.str.strip()

    df = df.dropna(how="all")

    df = df.drop_duplicates()

    return df

