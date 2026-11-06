import pytest

from japanese_jlpt_vocabulary.build import build_term_meta_bank, get_level, verify_term_meta_bank


def entry(term: str, reading: str, value: int, display_value: str) -> list:
    return [term, "freq", {"reading": reading, "frequency": {"value": value, "displayValue": display_value}}]


def test_replaces_value_by_level_and_keeps_display_value():
    bank = build_term_meta_bank([[entry("相", "あい", -1, "N1")]])
    assert bank == [entry("相", "あい", 1, "N1")]


def test_handles_entries_without_reading():
    bank = build_term_meta_bank([[["ああ", "freq", {"value": -1, "displayValue": "N3"}]]])
    assert bank == [["ああ", "freq", {"value": 3, "displayValue": "N3"}]]


def test_keeps_upstream_order():
    bank = build_term_meta_bank([[entry("会う", "あう", -1, "N5")], [entry("相", "あい", -1, "N1")]])
    assert [e[0] for e in bank] == ["会う", "相"]


@pytest.mark.parametrize("display_value", ["N6", "N0", "N1 (JMdict)", ""])
def test_fails_on_unexpected_display_value(display_value):
    with pytest.raises(SystemExit):
        get_level(display_value)


def test_fails_on_duplicate_word():
    with pytest.raises(SystemExit):
        verify_term_meta_bank([entry("相", "あい", 1, "N1"), entry("相", "あい", 2, "N2")])
