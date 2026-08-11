"""
Bibliometric Normalization System (BNS)

Module      : Author Normalization
Version     : 1.0.0
Author      : Samet UÇAK
Created     : 2026

Description:
Author, affiliation and keyword normalization.
"""

import re

import pandas as pd

from .exceptions import ValidationError

def normalize_author_name(author: str) -> str:
    """
    Normalize author names.
    """

    if pd.isna(author):
        return ""
  
    author = str(author).strip()
    
    # Remove punctuation differences

    author = author.replace(".", "")
    
    author = author.replace("-", " ")

    # Standardize case
    
    author = author.lower()

    # Remove extra spaces
    
    author = re.sub(r"\s+", " ", author)

    return author
    
def extract_last_name(author):
    """
    Extract surname from author name.
    """

    if "," in author:
        return author.split(",")[0].strip()

    return author.strip()

def normalize_affiliation(text):
    """
    Normalize affiliation names.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def normalize_keywords(text):
    """
    Normalize keyword list.
    """

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def normalize_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize the complete dataset.
    """

    required_columns = [
        "author",
        "affiliation",
        "keywords",
    ]

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValidationError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    df = df.copy()

    # Normalize author names
    df["normalized_author"] = (
        df["author"]
        .apply(normalize_author_name)
    )

    # Extract surname
    df["last_name"] = (
        df["normalized_author"]
        .apply(extract_last_name)
    )

    # Normalize affiliations
    df["normalized_affiliation"] = (
        df["affiliation"]
        .apply(normalize_affiliation)
    )

    # Normalize keywords
    df["normalized_keywords"] = (
        df["keywords"]
        .apply(normalize_keywords)
    )

    return df


