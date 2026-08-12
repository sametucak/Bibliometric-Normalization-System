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

def test_build_author_groups_supports_wos_names_without_comma():
    import pandas as pd
    from src.merge_engine import build_author_groups
    df = pd.DataFrame({'normalized_author': ['smith j', 'smith john', 'garcia m', 'garcia maria']})
    groups = build_author_groups(df)
    assert groups['smith'] == ['smith j', 'smith john']
    assert groups['garcia'] == ['garcia m', 'garcia maria']


def test_build_merge_candidates_supports_wos_names_without_comma():
    import pandas as pd
    from src.merge_engine import build_author_groups, build_merge_candidates
    df = pd.DataFrame({'normalized_author': ['smith j', 'smith john', 'garcia m', 'garcia maria']})
    groups = build_author_groups(df)
    candidates = build_merge_candidates(groups)
    assert len(candidates) == 2
    assert set(zip(candidates['author1'], candidates['author2'])) == {('smith j', 'smith john'), ('garcia m', 'garcia maria')}


def test_apply_author_merges_supports_wos_names_without_comma():
    import pandas as pd
    from src.merge_engine import apply_author_merges
    df = pd.DataFrame({'normalized_author': ['smith john', 'smith jon']})
    merge_results = pd.DataFrame({'author1': ['smith john'], 'author2': ['smith jon'], 'decision': ['Automatic Merge']})
    result = apply_author_merges(df, merge_results)
    assert result.loc[result['normalized_author'] == 'smith jon', 'canonical_author'].iloc[0] == 'smith john'
