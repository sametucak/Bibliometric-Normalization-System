"""
Bibliometric Normalization System (BNS)

Main application entry point.

Author : Samet UÇAK
Version: 1.0.0
"""

from pathlib import Path
from typing import Callable, Optional

import pandas as pd

from src.config import BNSConfig
from src.logger import get_logger
from src.cleaning import clean_data
from src.column_mapping import map_wos_columns
from src.author_normalization import normalize_dataset
from src.merge_engine import (
    build_author_groups,
    build_author_lookup,
    build_merge_candidates,
    score_merge_candidates,
    apply_author_merges,
)
from src.indicator import build_author_metrics
from src.exporter import export_all_outputs
from src.author_id import assign_author_ids


config = BNSConfig()
logger = get_logger()


def run_pipeline(
    input_file: Path,
    output_dir: Path,
    progress_callback: Optional[Callable[[int, str], None]] = None,
) -> None:
    """
    Run the complete BNS workflow.

    Parameters
    ----------
    input_file : Path
        Path to the input Web of Science Excel file.
    output_dir : Path
        Directory where BNS output files will be created.
    """
    if progress_callback:
        progress_callback(0, "Starting analysis...")

    logger.info("=== Bibliometric Normalization System (BNS) ===")
    logger.info("Starting analysis...")

    input_file = Path(input_file)
    output_dir = Path(output_dir)

    if progress_callback:
        progress_callback(10, "Loading data...")

    df = pd.read_excel(input_file)

    logger.info(f"Loaded records: {len(df)}")

    if progress_callback:
        progress_callback(20, "Cleaning data...")

    df = clean_data(df)

    logger.info(f"After cleaning: {len(df)}")

    if progress_callback:
        progress_callback(30, "Mapping WoS columns...")

    df = map_wos_columns(df)

    logger.info("Column mapping completed.")

    if progress_callback:
        progress_callback(40, "Normalizing authors...")

    df = normalize_dataset(df)

    logger.info("Author normalization completed.")

    if progress_callback:
        progress_callback(50, "Building author groups...")

    author_groups = build_author_groups(df)

    logger.info(
        f"Author groups created: {len(author_groups)}"
    )

    author_lookup = build_author_lookup(df)

    if progress_callback:
        progress_callback(60, "Generating merge candidates...")

    merge_candidates = build_merge_candidates(
        author_groups
    )

    logger.info(
        f"Merge candidates found: {len(merge_candidates)}"
    )

    if progress_callback:
        progress_callback(70, "Scoring merge candidates...")

    merge_results = score_merge_candidates(
        merge_candidates,
        author_lookup
    )

    logger.info("Merge scoring completed.")

    print(
        merge_results["decision"]
        .value_counts()
    )

    print(
        merge_results[
            merge_results["decision"] == "Manual Review"
        ]
    )

    df = apply_author_merges(
        df,
        merge_results
    )

    if progress_callback:
        progress_callback(80, "Assigning Author IDs...")

    df = assign_author_ids(df)

    logger.info("Author IDs assigned.")

    logger.info("Author merge application completed.")

    if progress_callback:
        progress_callback(90, "Calculating indicators...")

    metrics = build_author_metrics(df)

    logger.info("Indicator calculation completed.")

    if progress_callback:
        progress_callback(95, "Exporting results...")

    export_all_outputs(
        df,
        metrics,
        merge_results,
        output_dir
    )

    logger.info("Export completed.")


def main() -> None:
    """
    Run the complete BNS workflow using the default
    v1.0.0 input and output locations.
    """

    input_file = (
        config.input_dir
        / "combining yazar listesi.xlsx"
    )

    run_pipeline(
        input_file,
        config.output_dir
    )


if __name__ == "__main__":
    main()
