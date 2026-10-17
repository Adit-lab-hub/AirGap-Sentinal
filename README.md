# AirGap Sentinel 🛡️

> **Zero-Trust, Air-Gapped Incident Responder & Root-Cause Diagnostician for Critical Infrastructure**  
> *Built by Prasang for MLH Hacktoberfest Hackathon.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Ollama](https://img.shields.io/badge/Ollama-Offline%20AI-orange.svg)](https://ollama.com/)
[![Gemini API](https://img.shields.io/badge/Gemma%204-Gemini%20API-4285F4.svg)](https://ai.google.dev/)
[![Graphify](https://img.shields.io/badge/Graphify-Knowledge%20Graph-8A2BE2.svg)](https://github.com/Graphify-Labs/graphify)

---

## 📌 Project Overview

Operators running factory PLCs, secure data center server rooms, SCADA networks, and offshore rigs frequently work in **air-gapped environments** with strict zero-trust network policies or zero internet access. When a mission-critical daemon crashes or an edge gateway throws an I/O exception, operators cannot paste proprietary logs into cloud LLMs.

**AirGap Sentinel** solves this:
1. **Automated Incident Watcher:** Monitors an incoming directory using `watchdog`. When a `.log`, `.txt`, or `.dump` file lands, it waits 1 second for write completion before triaging.
2. **Deterministic Root-Cause Analysis:** Uses a version-controlled operational prompt contract (`diagnostics.SKILL.md`) at `temperature: 0` to produce structured JSON root-cause diagnoses.
3. **Verbatim Evidence Verification (Zero Hallucination):** Every citation is checked character-for-character against the original log. If the AI hallucinates, it is immediately flagged as unverified.
4. **Safety Guardrails:** All suggested remediation commands pass through an active blocklist (`rm`, `mkfs`, `dd`, `shutdown`, `reboot`, `chmod -R`, etc.) and are labelled `SUGGESTED, NOT RUN`. Commands are **never** executed automatically.

---

## 🏆 Hackathon Challenges Satisfied

| Challenge | Feature & Architectural Proof |
| :--- | :--- |
| **C1. Best Open-Source AI Project** | **100% Offline Local Inference:** Runs open-weight models (`gemma3:4b` / `gemma4:e4b`) entirely on local GPU/CPU hardware via Ollama. Operates with Wi-Fi and ethernet physically disconnected (`Network calls: 0`). |
| **C2. Best Use of Gemma 4** | **Official Google GenAI Integration:** When internet uplink is available, the `--cloud` flag invokes Google's cutting-edge **Gemma 4** (`gemma-4-26b-a4b-it` / `gemma-4-31b-it`) via the official `google-genai` SDK and Gemini API. |
| **C3. Graphify OSS Integration** | **Codebase Knowledge Graph:** Developed using the Graphify CLI (`graphifyy`). Visual interactive architecture and dependency maps are committed directly in [`graphify-out/`](./graphify-out/) and tracked in [`DEVLOG.md`](./DEVLOG.md). |
| **C4. Public Open Source Submission** | Public repository licensed under the open-source [MIT License](./LICENSE). |

---

## 🚀 Quick Start & Installation

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/Prasang/airgap-sentinel.git
cd airgap-sentinel
pip install -r requirements.txt
```

### 2. Prepare Local Ollama (Offline Mode)

Ensure Ollama is installed and running (native Windows or inside WSL):

```bash
# Verify Ollama is running and pull the local Gemma model
ollama pull gemma3:4b
```

---

## 💻 Running AirGap Sentinel

AirGap Sentinel supports both native Windows PowerShell and Linux/WSL environments.

### 1. Verify Backend Connectivity (`--check`)

```powershell
# Windows PowerShell (Local Ollama)
python sentinel.py --check

# Windows PowerShell (Cloud Gemma 4 via Gemini API)
$env:GEMINI_API_KEY="your-api-key"
python sentinel.py --check --cloud
```

```bash
# Linux / WSL (Local Ollama)
python3 sentinel.py --check

# Linux / WSL (Cloud Gemma 4 via Gemini API)
export GEMINI_API_KEY="your-api-key"
python3 sentinel.py --check --cloud
```

### 2. Diagnose a Single Incident Log (`--once PATH`)

```powershell
# Windows PowerShell - Local Offline Run (Zero Network Calls)
python sentinel.py --once samples/disk_full.log

# Windows PowerShell - Cloud Gemma 4 Run
python sentinel.py --once samples/disk_full.log --cloud
```

```bash
# Linux / WSL - Local Offline Run
python3 sentinel.py --once samples/disk_full.log

# Linux / WSL - Cloud Gemma 4 Run
python3 sentinel.py --once samples/disk_full.log --cloud
```

### 3. Real-Time Directory Watcher (`--watch DIR`)

```powershell
# Windows PowerShell
python sentinel.py --watch ./watched
```

```bash
# Linux / WSL
python3 sentinel.py --watch ./watched
```

---

## 📊 Sample Output

```text
=================================================================
  AIRGAP SENTINEL INCIDENT REPORT
=================================================================
Backend: LOCAL Ollama (gemma3:4b) | Network calls: 0
Diagnosis Time: 14.48s
-----------------------------------------------------------------
ROOT CAUSE:
  The database daemon encountered a critical error due to a full disk 
  on the sda1 partition, preventing it from writing transaction logs 
  and persisting data. This led to a cascade of failures including 
  the telemetry agent and plc-collector.

EVIDENCE LINE:
  "Oct 17 12:14:22 edge-gateway-01 database-daemon[1420]: [FATAL] Failed to write transaction log: No space left on device (errno 28)"
  [VERIFIED: Line matched character-for-character in original log]

SUGGESTED, NOT RUN:
  $ df -h

CONFIDENCE: HIGH
=================================================================
```

---

## 🧠 How We Used Graphify (Challenge C3)

During development, we used **Graphify** (`graphifyy`) to parse, index, and query our Python AST architecture.

* **Committed Graph Artifacts:**
  * [`graphify-out/graph.json`](./graphify-out/graph.json): 81 semantic nodes and 127 structural edges representing the complete call hierarchy and dataflow.
  * [`graphify-out/graph.html`](./graphify-out/graph.html): Interactive D3 visual network representation of the Sentinel architecture.
  * [`graphify-out/GRAPH_TREE.html`](./graphify-out/GRAPH_TREE.html): Interactive D3 collapsible tree hierarchy representation.
  * [`graphify-out/AirGap-Sentinal-callflow.html`](./graphify-out/AirGap-Sentinal-callflow.html): Interactive Mermaid architecture diagrams and execution call-flow tables.
  * [`graphify-out/wiki/`](./graphify-out/wiki/): 20 architectural wiki markdown articles indexed at `index.md`.
  * [`graphify-out/GRAPH_REPORT.md`](./graphify-out/GRAPH_REPORT.md): Community clustering report detailing symbol cohesion and modular boundaries.
* **Audit Trail:**
  * All Graphify execution milestones and semantic queries are logged in [`DEVLOG.md`](./DEVLOG.md).

### Example Graph Queries Run During Development:
```bash
# 1. Trace folder watcher debouncing and file stability coordination
graphify query "wait_for_file_stability"

# 2. Verify command blocklist enforcement callpath
graphify query "sanitize_command"
```

---

## 🎬 Hackathon 2-Minute Demo Script for Judges

1. **Test Offline Backend Health:**
   ```powershell
   python sentinel.py --check
   ```
   *Expected:* Confirms Ollama is reachable and `gemma3:4b` is ready.

2. **Diagnose Sample Incident (Wi-Fi can be disabled!):**
   ```powershell
   python sentinel.py --once samples/disk_full.log
   ```
   *Expected:* Instant diagnosis showing `No space left on device`, verified evidence line, and suggested command `$ df -h` labelled `SUGGESTED, NOT RUN`.

3. **Verify Safe Command Blocklist Guardrail:**
   ```powershell
   python -c "import sentinel; print(sentinel.sanitize_command('rm -rf /var/log'))"
   ```
   *Expected:* Outputs `BLOCKED: unsafe command suggested`.

4. **Test Real-Time Automated Folder Watcher:**
   * Open Terminal 1:
     ```powershell
     python sentinel.py --watch ./watched
     ```
   * In Terminal 2, drop a new log file:
     ```powershell
     Copy-Item "samples/disk_full.log" "watched/factory_alert.log"
     ```
   * Watch Terminal 1 detect the file, wait 1s for file size stabilization, and output the incident diagnosis autonomously.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE) - Created by Prasang (2026).
