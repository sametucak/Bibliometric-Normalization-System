from src.merge_engine import merge_decision


def test_automatic_merge_at_threshold():
    assert merge_decision(95) == "Automatic Merge"


def test_automatic_merge_above_threshold():
    assert merge_decision(100) == "Automatic Merge"


def test_manual_review_at_threshold():
    assert merge_decision(85) == "Manual Review"


def test_manual_review_between_thresholds():
    assert merge_decision(90) == "Manual Review"


def test_different_authors_below_threshold():
    assert merge_decision(84.9) == "Different Authors"


def test_different_authors_zero_score():
    assert merge_decision(0) == "Different Authors"