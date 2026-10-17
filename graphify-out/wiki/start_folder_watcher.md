# start_folder_watcher

> 8 nodes · cohesion 0.32

## Key Concepts

- **start_folder_watcher()** (8 connections) — `sentinel.py`
- **_handle()** (6 connections) — `sentinel.py`
- **wait_for_file_stability()** (5 connections) — `sentinel.py`
- **__init__()** (3 connections) — `sentinel.py`
- **on_created()** (2 connections) — `sentinel.py`
- **on_modified()** (2 connections) — `sentinel.py`
- **Waits until the target file's size stops changing for at least 1 second. Why:…** (1 connections) — `sentinel.py`
- **Watches a target directory for new .log/.txt/.dump files using watchdog. Why:…** (1 connections) — `sentinel.py`

## Relationships

- [sentinel.py](sentinel.py.md) (6 shared connections)
- [sanitize_command](sanitize_command.md) (2 shared connections)

## Source Files

- `sentinel.py`

## Audit Trail

- EXTRACTED: 16 (89%)
- INFERRED: 2 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*