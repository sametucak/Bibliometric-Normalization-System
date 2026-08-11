import pandas as pd

from src.exporter import (
    export_excel,
    export_csv,
    export_author_metrics,
    export_normalized_data,
    export_merge_report,
    export_all_outputs,
)


def test_export_excel(tmp_path):
    df = pd.DataFrame({
        "author": ["samet ucak", "ali veli"],
        "value": [1, 2],
    })

    filepath = tmp_path / "test.xlsx"

    export_excel(df, filepath)

    assert filepath.exists()

    result = pd.read_excel(filepath)

    assert result.equals(df)


def test_export_csv(tmp_path):
    df = pd.DataFrame({
        "author": ["samet ucak", "ali veli"],
        "value": [1, 2],
    })

    filepath = tmp_path / "test.csv"

    export_csv(df, filepath)

    assert filepath.exists()

    result = pd.read_csv(filepath)

    assert result.equals(df)


def test_export_author_metrics(tmp_path):
    df = pd.DataFrame({
        "normalized_author": ["samet ucak"],
        "publication_count": [5],
    })

    export_author_metrics(df, tmp_path)

    assert (tmp_path / "Author_Metrics.xlsx").exists()


def test_export_normalized_data(tmp_path):
    df = pd.DataFrame({
        "normalized_author": ["samet ucak"],
    })

    export_normalized_data(df, tmp_path)

    assert (tmp_path / "Normalized_WoS_Data.xlsx").exists()


def test_export_merge_report(tmp_path):
    df = pd.DataFrame({
        "author1": ["samet ucak"],
        "author2": ["samet uçak"],
    })

    export_merge_report(df, tmp_path)

    assert (tmp_path / "Merge_Report.xlsx").exists()


def test_export_all_outputs(tmp_path):
    normalized_df = pd.DataFrame({
        "normalized_author": ["samet ucak"],
    })

    metrics = pd.DataFrame({
        "normalized_author": ["samet ucak"],
        "publication_count": [1],
    })

    merge_df = pd.DataFrame({
        "author1": ["samet ucak"],
        "author2": ["samet uçak"],
    })

    export_all_outputs(
        normalized_df,
        metrics,
        merge_df,
        tmp_path,
    )

    assert (tmp_path / "Normalized_WoS_Data.xlsx").exists()
    assert (tmp_path / "Author_Metrics.xlsx").exists()
    assert (tmp_path / "Merge_Report.xlsx").exists()