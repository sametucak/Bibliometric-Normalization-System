import pandas as pd

from src.author_id import assign_author_ids


def test_assign_author_ids():
    df = pd.DataFrame(
        {
            "normalized_author": [
                "samet ucak",
                "ali veli",
                "samet ucak",
            ]
        }
    )

    result = assign_author_ids(df)

    assert result.loc[0, "author_id"] == "A000001"
    assert result.loc[1, "author_id"] == "A000002"
    assert result.loc[2, "author_id"] == "A000001"


def test_author_id_column_is_created():
    df = pd.DataFrame(
        {
            "normalized_author": [
                "samet ucak",
                "ali veli",
            ]
        }
    )

    result = assign_author_ids(df)

    assert "author_id" in result.columns