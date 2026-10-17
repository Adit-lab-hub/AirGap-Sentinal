# sentinel.py

> 18 nodes · cohesion 0.23

## Key Concepts

- **sentinel.py** (24 connections) — `sentinel.py`
- **diagnose_single_path()** (10 connections) — `sentinel.py`
- **run_cloud_diagnosis()** (8 connections) — `sentinel.py`
- **run_local_diagnosis()** (7 connections) — `sentinel.py`
- **os** (6 connections)
- **check_backend()** (6 connections) — `sentinel.py`
- **get_local_model()** (6 connections) — `sentinel.py`
- **main()** (6 connections) — `sentinel.py`
- **sys** (6 connections)
- **time** (5 connections)
- **argparse** (2 connections)
- **logging** (1 connections)
- **Resolves the local model to use, verifying it is pulled in Ollama. Why: Gives…** (1 connections) — `sentinel.py`
- **Executes local offline diagnosis using Ollama with automatic retry on JSON…** (1 connections) — `sentinel.py`
- **AirGap Sentinel: Offline Incident Responder & Log Diagnostician Pair-programmed…** (1 connections) — `sentinel.py`
- **Executes cloud diagnosis using Gemma 4 via Google Gemini API (Challenge C2).** (1 connections) — `sentinel.py`
- **Verifies backend connectivity and prints actionable troubleshooting steps.** (1 connections) — `sentinel.py`
- **Coordinates reading, AI diagnosis, and output formatting for one target file.** (1 connections) — `sentinel.py`

## Relationships

- [start_folder_watcher](start_folder_watcher.md) (6 shared connections)
- [parse_and_clean_json](parse_and_clean_json.md) (4 shared connections)
- [sanitize_command](sanitize_command.md) (4 shared connections)
- [test_sentinel.py](test_sentinel.py.md) (3 shared connections)
- [load_skill_prompt](load_skill_prompt.md) (3 shared connections)
- [TestAirGapSentinel](TestAirGapSentinel.md) (2 shared connections)
- [load_env_file](load_env_file.md) (1 shared connections)

## Source Files

- `sentinel.py`

## Audit Trail

- EXTRACTED: 58 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*