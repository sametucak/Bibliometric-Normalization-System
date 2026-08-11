"""
Configuration settings for the Bibliometric Normalization System (BNS).
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BNSConfig:
    input_dir: Path = Path("input")
    output_dir: Path = Path("output")

    similarity_threshold: float = 0.90

    automatic_merge_threshold: float = 95.0
    manual_review_threshold: float = 85.0

    encoding: str = "utf-8-sig"

