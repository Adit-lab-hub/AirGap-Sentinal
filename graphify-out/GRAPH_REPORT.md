# Graph Report - Aircap_sentinal  (2026-10-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 38 nodes · 72 edges · 8 communities (2 shown, 6 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- run_cloud_diagnosis
- start_folder_watcher
- check_backend
- diagnose_single_path
- parse_and_clean_json
- sanitize_command
- format_and_print_diagnosis

## God Nodes (most connected - your core abstractions)
1. `diagnose_single_path()` - 10 edges
2. `start_folder_watcher()` - 8 edges
3. `run_cloud_diagnosis()` - 7 edges
4. `run_local_diagnosis()` - 7 edges
5. `get_local_model()` - 6 edges
6. `check_backend()` - 6 edges
7. `main()` - 6 edges
8. `parse_and_clean_json()` - 6 edges
9. `_handle()` - 5 edges
10. `load_skill_prompt()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `check_backend()` --calls--> `get_local_model()`  [EXTRACTED]
  sentinel.py → sentinel.py  _Bridges community 0 → community 2_
- `diagnose_single_path()` --calls--> `run_cloud_diagnosis()`  [EXTRACTED]
  sentinel.py → sentinel.py  _Bridges community 0 → community 3_
- `run_cloud_diagnosis()` --calls--> `parse_and_clean_json()`  [EXTRACTED]
  sentinel.py → sentinel.py  _Bridges community 0 → community 4_
- `main()` --calls--> `start_folder_watcher()`  [EXTRACTED]
  sentinel.py → sentinel.py  _Bridges community 1 → community 2_
- `_handle()` --calls--> `diagnose_single_path()`  [EXTRACTED]
  sentinel.py → sentinel.py  _Bridges community 1 → community 3_

## Import Cycles
- None detected.

## Communities (8 total, 6 thin omitted)

### Community 0 - "run_cloud_diagnosis"
Cohesion: 0.28
Nodes (4): get_local_model(), load_skill_prompt(), run_cloud_diagnosis(), run_local_diagnosis()

### Community 1 - "start_folder_watcher"
Cohesion: 0.31
Nodes (6): start_folder_watcher(), _handle(), __init__(), on_created(), on_modified(), wait_for_file_stability()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `start_folder_watcher()` connect `start_folder_watcher` to `check_backend`, `sentinel.py`?**
  _High betweenness centrality (0.187) - this node is a cross-community bridge._
- **Why does `diagnose_single_path()` connect `diagnose_single_path` to `run_cloud_diagnosis`, `start_folder_watcher`, `check_backend`, `sentinel.py`, `format_and_print_diagnosis`?**
  _High betweenness centrality (0.127) - this node is a cross-community bridge._
- **Why does `run_local_diagnosis()` connect `run_cloud_diagnosis` to `diagnose_single_path`, `parse_and_clean_json`, `sentinel.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._