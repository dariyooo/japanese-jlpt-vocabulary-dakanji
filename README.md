# japanese-jlpt-vocabulary-dakanji

JLPT level (N5-N1) of Japanese words for DaKanji.

The dictionary only contains the JLPT level and is meant to be installed alongside a word dictionary like JMdict.
Each word is stored as a `term_meta_bank` frequency entry whose value is its level,
e.g. `["相","freq",{"reading":"あい","frequency":{"value":1,"displayValue":"N1"}}]`,
and the index declares `"frequencyMode": "occurrence-based"`, so DaKanji can sort and filter by level (N5 = 5 ... N1 = 1).

This is why the dictionary is for DaKanji only: Yomitan would include the levels in its frequency average.
In Yomitan use the original [yomitan-jlpt-vocab](https://github.com/stephenmk/yomitan-jlpt-vocab), which stores every level as `-1` for this reason.

## Sources

There are no official vocabulary lists for the JLPT since 2010, so all levels are unofficial.

* **Words and levels**: Jonathan Waller's [JLPT resources](http://www.tanos.co.uk/jlpt/), the de facto standard.
* **Matched to JMdict**: Stephen Kraus' [yomitan-jlpt-vocab](https://github.com/stephenmk/yomitan-jlpt-vocab),
  which converts Waller's lists to Yomitan banks with the headwords and readings of JMdict.
  Its five `term_meta_bank_{n}.json` files are used as they are, only the value of each entry (`-1`) is replaced by the level of its display value.

The sources are locked to a version in `sources.lock.json`.
The *Update* workflow checks them weekly, commits newer versions and releases the dictionary if it changed.

## Installation

Make sure [uv](https://github.com/astral-sh/uv) is installed on your system and run

``` bash
uv sync
```

## Usage

``` bash
uv run build.py
```

This creates the dictionary in `out/` (`japanese-jlpt-vocabulary-dakanji.zip`, `japanese-jlpt-vocabulary-dakanji.index.json` and `japanese-jlpt-vocabulary-dakanji.manifest.json`).
Downloaded sources are cached in `tmp/sources/`, the uncompressed dictionary is kept in `tmp/japanese-jlpt-vocabulary-dakanji/` for inspection.

## Development

``` bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pyright               # type check
uv run pytest                # tests
```

The repo follows the [DaLang dictionary repo standard](https://github.com/dariyooo/dalang-dict-utils/blob/main/docs/repo-standard.md),
update the shared setup with `uvx copier update --trust`.

## Release

Push a tag with today's date:

``` bash
git tag 2026-11-01 && git push origin 2026-11-01
```

The *Release* workflow runs the checks, builds the dictionary with the tag as revision and publishes it as the GitHub release of the tag.
To redo a release, push the tag again with `git tag -f 2026-11-01 && git push -f origin 2026-11-01`.
Installed dictionaries pick up new releases through "Check for updates".

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), as required by yomitan-jlpt-vocab (CC BY-SA 4.0, Stephen Kraus).
JLPT lists by Jonathan Waller (CC BY).
