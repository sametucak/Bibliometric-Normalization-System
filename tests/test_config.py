from src.config import BNSConfig


def test_default_config():
    config = BNSConfig()

    assert config.similarity_threshold == 0.90
    assert config.automatic_merge_threshold == 95.0
    assert config.manual_review_threshold == 85.0
    assert config.encoding == "utf-8-sig"