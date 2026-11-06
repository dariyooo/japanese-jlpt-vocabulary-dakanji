import json
import re
import sys

from dalang_dict import GitHubFile, build_index, fetch, package_dictionary

GITHUB_REPO = "dariyooo/japanese-jlpt-vocabulary-dakanji"
ASSET = "japanese-jlpt-vocabulary-dakanji"
TITLE = "JLPT Vocabulary"

UPSTREAM_REPO = "stephenmk/yomitan-jlpt-vocab"
LEVELS = (5, 4, 3, 2, 1)

# Upstream's banks, one per level, each locked to a version in sources.lock.json and updated by the Update workflow
SOURCES = [
    GitHubFile(
        f"term_meta_bank_{level}.json",
        repo=UPSTREAM_REPO,
        path=f"yomitan-jlpt-vocab/term_meta_bank_{level}.json",
        used_for=f"N{level} words, the value of each entry is replaced by its level",
    )
    for level in LEVELS
]

DISPLAY_VALUE = re.compile(r"^N([1-5])$")

INDEX_FIELDS = {
    "sourceLanguage": "ja",
    # Higher values are easier levels, so sorting by it lists N5 first
    "frequencyMode": "occurrence-based",
    "author": "Jonathan Waller (JLPT lists), Stephen Kraus (yomitan-jlpt-vocab)",
    "url": f"https://github.com/{GITHUB_REPO}",
    "description": "JLPT level (N5-N1) of Japanese words. Unofficial: there are no official lists since 2010. "
    "The value of each entry is its level (N5 = 5 ... N1 = 1) so DaKanji can sort and filter by it, "
    "in Yomitan use the original yomitan-jlpt-vocab instead.",
    "attribution": "JLPT lists: Jonathan Waller, tanos.co.uk (CC BY). "
    "Matched to JMdict: Stephen Kraus, stephenmk/yomitan-jlpt-vocab (CC BY-SA 4.0).",
}


def get_level(display_value: str) -> int:
    """Returns the level of a display value like "N3", fails on anything else."""
    match = DISPLAY_VALUE.match(display_value)
    if match is None:
        sys.exit(f"Unexpected JLPT display value: {display_value!r}")
    return int(match.group(1))


def build_term_meta_bank(upstream_banks: list[list]) -> list:
    """Replaces the value of every upstream entry (-1) by its level, keeping everything else as it is.

    E.g. ["相","freq",{"reading":"あい","frequency":{"value":-1,"displayValue":"N1"}}] gets the value 1.
    """
    term_meta_bank = []
    for bank in upstream_banks:
        for term, mode, data in bank:
            if mode != "freq":
                sys.exit(f"Unexpected mode {mode!r} of {term}")
            frequency = data.get("frequency", data)
            frequency = {**frequency, "value": get_level(frequency["displayValue"])}
            data = {**data, "frequency": frequency} if "frequency" in data else frequency
            term_meta_bank.append([term, mode, data])
    return term_meta_bank


def verify_term_meta_bank(term_meta_bank: list) -> None:
    """Fails on words listed more than once and prints the per-level counts."""
    seen = set()
    counts = {f"N{level}": 0 for level in LEVELS}

    for term, _, data in term_meta_bank:
        key = (term, data.get("reading"))
        if key in seen:
            sys.exit(f"Duplicate word: {term} [{data.get('reading')}]")
        seen.add(key)
        counts[data.get("frequency", data)["displayValue"]] += 1

    print(f"Term meta bank verified: {len(seen)} words {counts}")


def main() -> None:
    upstream_banks = [json.loads(fetch(source).read_text(encoding="utf-8")) for source in SOURCES]

    term_meta_bank = build_term_meta_bank(upstream_banks)
    verify_term_meta_bank(term_meta_bank)
    index = build_index(TITLE, GITHUB_REPO, ASSET, **INDEX_FIELDS)
    package_dictionary(ASSET, index, {"term_meta_bank": term_meta_bank})
