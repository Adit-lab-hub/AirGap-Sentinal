# TestAirGapSentinel

> 11 nodes · cohesion 0.22

## Key Concepts

- **TestAirGapSentinel** (9 connections) — `test_sentinel.py`
- **load_log_file()** (6 connections) — `sentinel.py`
- **.test_load_log_file_empty_raises()** (3 connections) — `test_sentinel.py`
- **.test_load_log_file_normal()** (3 connections) — `test_sentinel.py`
- **.test_load_log_file_truncation()** (3 connections) — `test_sentinel.py`
- **.test_verbatim_evidence_verification()** (2 connections) — `test_sentinel.py`
- **Reads a target log file and truncates it to the most recent lines/characters.…** (1 connections) — `sentinel.py`
- **Verify verbatim matching detects hallucinated lines.** (1 connections) — `test_sentinel.py`
- **Verify normal log files load completely without truncation.** (1 connections) — `test_sentinel.py`
- **Verify empty log files raise ValueError.** (1 connections) — `test_sentinel.py`
- **Verify logs > 200 lines truncate to the last 200 lines.** (1 connections) — `test_sentinel.py`

## Relationships

- [sentinel.py](sentinel.py.md) (2 shared connections)
- [sanitize_command](sanitize_command.md) (2 shared connections)
- [test_sentinel.py](test_sentinel.py.md) (1 shared connections)
- [load_skill_prompt](load_skill_prompt.md) (1 shared connections)
- [parse_and_clean_json](parse_and_clean_json.md) (1 shared connections)

## Source Files

- `sentinel.py`
- `test_sentinel.py`

## Audit Trail

- EXTRACTED: 19 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*