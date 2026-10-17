# Graph Report - AirGap-Sentinal  (2026-10-17)

## Corpus Check
- 5 files · ~3,801 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 7 file(s) not represented in the graph (top: .log 5, (none) 2)

## Summary
- 81 nodes · 127 edges · 10 communities (4 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `45d206dd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- run_cloud_diagnosis
- start_folder_watcher
- AirGap Sentinel 🛡️
- TestAirGapSentinel
- parse_and_clean_json
- sanitize_command
- load_skill_prompt
- load_env_file

## God Nodes (most connected - your core abstractions)
1. `diagnose_single_path()` - 10 edges
2. `TestAirGapSentinel` - 9 edges
3. `AirGap Sentinel 🛡️` - 9 edges
4. `run_cloud_diagnosis()` - 8 edges
5. `start_folder_watcher()` - 8 edges
6. `parse_and_clean_json()` - 7 edges
7. `sanitize_command()` - 7 edges
8. `run_local_diagnosis()` - 7 edges
9. `load_log_file()` - 6 edges
10. `get_local_model()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `wait_for_file_stability()`  [INFERRED]
  DEVLOG.md → sentinel.py
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `_handle()`  [INFERRED]
  DEVLOG.md → sentinel.py
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `sanitize_command()`  [INFERRED]
  DEVLOG.md → sentinel.py
- `AirGap Sentinel - Development Log (Graphify Integration)` --references--> `format_and_print_diagnosis()`  [INFERRED]
  DEVLOG.md → sentinel.py

## Import Cycles
- None detected.

## Communities (10 total, 6 thin omitted)

### Community 0 - "run_cloud_diagnosis"
Cohesion: 0.23
Nodes (6): check_backend(), diagnose_single_path(), get_local_model(), main(), run_cloud_diagnosis(), run_local_diagnosis()

### Community 1 - "start_folder_watcher"
Cohesion: 0.32
Nodes (6): start_folder_watcher(), _handle(), __init__(), on_created(), on_modified(), wait_for_file_stability()

### Community 2 - "AirGap Sentinel 🛡️"
Cohesion: 0.13
Nodes (15): 1. Clone & Install Dependencies, 1. Verify Backend Connectivity (`--check`), 2. Diagnose a Single Incident Log (`--once PATH`), 2. Prepare Local Ollama (Offline Mode), 3. Real-Time Directory Watcher (`--watch DIR`), AirGap Sentinel 🛡️, Example Graph Queries Run During Development:, 🎬 Hackathon 2-Minute Demo Script for Judges (+7 more)

### Community 7 - "sanitize_command"
Cohesion: 0.18
Nodes (3): AirGap Sentinel - Development Log (Graphify Integration), format_and_print_diagnosis(), sanitize_command()

## Knowledge Gaps
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `AirGap Sentinel - Development Log (Graphify Integration)` connect `sanitize_command` to `start_folder_watcher`?**
  _High betweenness centrality (0.341) - this node is a cross-community bridge._
- **Should `AirGap Sentinel 🛡️` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._
- **Why does `AirGap Sentinel 🛡️` connect `AirGap Sentinel 🛡️` to `sanitize_command`?**
  _High betweenness centrality (0.314) - this node is a cross-community bridge._
- **Why does `sanitize_command()` connect `sanitize_command` to `run_cloud_diagnosis`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._