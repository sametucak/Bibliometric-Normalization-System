"""
Bibliometric Normalization System (BNS)

Main application entry point.

Author : Samet UÇAK
Version: 1.0.0
"""

from pathlib import Path

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

def main() -> None:
    """
    Run the complete BNS workflow.
    """

    logger.info("=== Bibliometric Normalization System (BNS) ===")
    logger.info("Starting analysis...")

    input_file = config.input_dir / "combining yazar listesi.xlsx"

    df = pd.read_excel(input_file)
    
    logger.info(f"Loaded records: {len(df)}")
    
    df = clean_data(df)
    
    logger.info(f"After cleaning: {len(df)}")
    
    df = map_wos_columns(df)
    
    logger.info("Column mapping completed.")
    
    df = normalize_dataset(df)
    
    logger.info("Author normalization completed.")
        
    author_groups = build_author_groups(df)

    logger.info(
        f"Author groups created: {len(author_groups)}"
    )


    author_lookup = build_author_lookup(df)

    merge_candidates = build_merge_candidates(
        author_groups
    )

    logger.info(
        f"Merge candidates found: {len(merge_candidates)}"
    )

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
    df = assign_author_ids(df)

    logger.info("Author IDs assigned.")

    logger.info("Author merge application completed.")
   
    metrics = build_author_metrics(df)
    
    logger.info("Indicator calculation completed.")
   
    export_all_outputs(
        df,
        metrics,
        merge_results,
        config.output_dir
    )

    logger.info("Export completed.")
    
if __name__ == "__main__":
    main()