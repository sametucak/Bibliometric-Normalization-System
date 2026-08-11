"""
Bibliometric Normalization System (BNS)

Module      : Similarity Engine
Version     : 1.0.0
Author      : Samet UÇAK
Created     : 2026

Description:
Similarity metrics for author matching.
"""
import pandas as pd
from rapidfuzz import fuzz

from .config import BNSConfig

config = BNSConfig()

def name_similarity(name1: str, name2: str) -> float:
    """
    Calculate similarity between two author names.
    """

    name1 = str(name1).lower()
    name2 = str(name2).lower()

    score1 = fuzz.token_sort_ratio(
        name1,
        name2
    )

    score2 = fuzz.WRatio(
        name1,
        name2
    )

    return max(score1, score2)    

def affiliation_similarity(aff1: str, aff2: str) -> float:
    """
    Calculate similarity between affiliations.
    """
    return fuzz.token_sort_ratio(str(aff1), str(aff2))
    
def keyword_similarity(key1: str, key2: str) -> float:
    """
    Calculate similarity between keywords.
    """
    return fuzz.token_sort_ratio(str(key1), str(key2))
    
def year_similarity(y1, y2) -> int:
    """
    Calculate publication year similarity.
    """

    if pd.isna(y1) or pd.isna(y2):
        return 50

    diff = abs(int(y1) - int(y2))

    if diff == 0:
        return 100

    elif diff <= 2:
        return 80

    elif diff <= 5:
        return 60

    return 20
    
def confidence_score(
    author1: str,
    author2: str,
    aff1: str,
    aff2: str,
    key1: str,
    key2: str,
    year1,
    year2,
) -> float:
    """
    Calculate final confidence score.
    """

    name = name_similarity(author1, author2)

    aff = affiliation_similarity(aff1, aff2)

    key = keyword_similarity(key1, key2)

    year = year_similarity(year1, year2)

    score = (
        name * 0.50 +
        aff * 0.25 +
        key * 0.15 +
        year * 0.10
    )

    return round(score, 2)

def merge_decision(score: float) -> str:
    """
    Decide whether two authors should be merged.
    """

    if score >= config.automatic_merge_threshold:
        return "Automatic Merge"

    elif score >= config.manual_review_threshold:
        return "Manual Review"

    else:
        return "Different Authors"

