# Graph Report - AirGap-Sentinal  (2026-10-17)

## Corpus Check
- 4 files · ~3,292 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: .log 3, (none) 2)

## Summary
- 60 nodes · 96 edges · 7 communities (4 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `45d206dd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_cloud_diagnosis
- start_folder_watcher
- AirGap Sentinel 🛡️
- diagnose_single_path
- sentinel.py
- AirGap Sentinel - Development Log (Graphify Integration)

## God Nodes (most connected - your core abstractions)
1. `diagnose_single_path()` - 10 edges
2. `AirGap Sentinel 🛡️` - 9 edges
3. `start_folder_watcher()` - 8 edges
4. `run_local_diagnosis()` - 7 edges
5. `run_cloud_diagnosis()` - 7 edges
6. `get_local_model()` - 6 edges
7. `parse_and_clean_json()` - 6 edges
8. `check_backend()` - 6 edges
9. `_handle()` - 6 edges
10. `main()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `sanitize_command()`  [INFERRED]
  DEVLOG.md → sentinel.py
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `wait_for_file_stability()`  [INFERRED]
  DEVLOG.md → sentinel.py
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `_handle()`  [INFERRED]
  DEVLOG.md → sentinel.py
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `format_and_print_diagnosis()`  [INFERRED]
  DEVLOG.md → sentinel.py

## Import Cycles
- None detected.

## Communities (7 total, 3 thin omitted)

### Community 0 - "run_cloud_diagnosis"
Cohesion: 0.21
Nodes (6): check_backend(), get_local_model(), load_skill_prompt(), main(), run_cloud_diagnosis(), run_local_diagnosis()

### Community 1 - "start_folder_watcher"
Cohesion: 0.31
Nodes (6): start_folder_watcher(), _handle(), __init__(), on_created(), on_modified(), wait_for_file_stability()

### Community 2 - "AirGap Sentinel 🛡️"
Cohesion: 0.13
Nodes (15): 1. Clone & Install Dependencies, 1. Verify Backend Connectivity (`--check`), 2. Diagnose a Single Incident Log (`--once PATH`), 2. Prepare Local Ollama (Offline Mode), 3. Real-Time Directory Watcher (`--watch DIR`), AirGap Sentinel 🛡️, Example Graph Queries Run During Development:, 🎬 Hackathon 2-Minute Demo Script for Judges (+7 more)

### Community 5 - "sentinel.py"
Cohesion: 0.21
Nodes (3): load_env_file(), parse_and_clean_json(), sanitize_command()

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AirGap Sentinel - Development Log (Graphify Integration)` connect `AirGap Sentinel - Development Log (Graphify Integration)` to `start_folder_watcher`, `sentinel.py`?**
  _High betweenness centrality (0.414) - this node is a cross-community bridge._
- **Should `AirGap Sentinel 🛡️` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `AirGap Sentinel 🛡️` connect `AirGap Sentinel 🛡️` to `AirGap Sentinel - Development Log (Graphify Integration)`?**
  _High betweenness centrality (0.407) - this node is a cross-community bridge._
- **Why does `format_and_print_diagnosis()` connect `AirGap Sentinel - Development Log (Graphify Integration)` to `diagnose_single_path`, `sentinel.py`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._