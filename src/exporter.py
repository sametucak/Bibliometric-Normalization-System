"""
Bibliometric Normalization System (BNS)

Module      : Exporter
Version     : 1.0.0
Author      : Samet UÇAK
Created     : 2026

Description:
Export bibliometric results to Excel and CSV.
"""

from pathlib import Path

import pandas as pd

from .config import BNSConfig

config = BNSConfig()


def export_excel(
    df: pd.DataFrame,
    filepath: Path | str,
) -> None:
    """
    Export a DataFrame to an Excel file.
    """

    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_excel(
        filepath,
        index=False
    )

    print(f"Saved: {filepath}")

def export_csv(
    df: pd.DataFrame,
    filepath: Path | str,
) -> None:
    """
    Export a DataFrame to a CSV file.
    """

    filepath = Path(filepath)

    filepath.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        filepath,
        index=False,
        encoding=config.encoding
    )

    print(f"Saved: {filepath}")

def export_author_metrics(
    metrics: pd.DataFrame,
    output_dir: Path | str,
) -> None:
    """
    Export author metrics table.
    """

    export_excel(
        metrics,
        Path(output_dir) / "Author_Metrics.xlsx"
    )


def export_normalized_data(
    df: pd.DataFrame,
    output_dir: Path | str,
) -> None:
    """
    Export normalized WoS dataset.
    """

    export_excel(
        df,
        Path(output_dir) / "Normalized_WoS_Data.xlsx"
    )


def export_merge_report(
    merge_df: pd.DataFrame,
    output_dir: Path | str,
) -> None:
    """
    Export merge report.
    """

    export_excel(
        merge_df,
        Path(output_dir) / "Merge_Report.xlsx"
    )


def export_all_outputs(
    normalized_df: pd.DataFrame,
    metrics: pd.DataFrame,
    merge_df: pd.DataFrame,
    output_dir: Path | str,
) -> None:
    """
    Export all project outputs.
    """

    export_normalized_data(
        normalized_df,
        output_dir
    )

    export_author_metrics(
        metrics,
        output_dir
    )

    export_merge_report(
        merge_df,
        output_dir
    )

    print("\nAll outputs exported successfully.")

