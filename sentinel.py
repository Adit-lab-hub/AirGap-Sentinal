#!/usr/bin/env python3
"""
AirGap Sentinel: Offline Incident Responder & Log Diagnostician
Pair-programmed for MLH Hacktoberfest Hackathon (Prasang & Antigravity)

Phase 1 / Step 7: Real-time folder watching with watchdog and file stabilization.
"""

import sys
import os
import time
import json
import re
import logging
import argparse
from pathlib import Path

# Silence google-genai's noisy AFC advisory: it's a best-practice hint, not an error.
# The warning fires even when we don't use AFC; keep the log clean for operators.
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

# Enable line buffering so real-time events flush immediately in PowerShell/bash
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)

# Limits: Cap at the last 200 lines or 8000 characters because the crash
# almost invariably occurs at the very end of the file, preserving inference speed.
MAX_LINES = 200
MAX_CHARS = 8000

# Supported log extensions for real-time folder watching
SUPPORTED_EXTENSIONS = {".log", ".txt", ".dump"}

# Path to the diagnostics skill document that acts as our system prompt contract
SKILL_PATH = Path(__file__).parent / "diagnostics.SKILL.md"

# Dangerous commands blocklist: NEVER allow destructive or bricking commands
# to reach an operator even as a suggestion (Rule 6 & Rule 9).
DANGEROUS_PATTERNS = [
    r"\brm\b",           # Recursive or file deletion
    r"\bmkfs\b",         # Filesystem formatting
    r"\bdd\b",           # Raw disk overwrite
    r"\bshutdown\b",     # Power down
    r"\breboot\b",       # System restart
    r"chmod\s+-R",       # Bulk permission corruption
    r":\(\)\{",          # Fork bomb pattern :(){ :|:& };:
    r">\s*/dev/sd",      # Direct disk writing redirection
]


def load_skill_prompt() -> str:
    """
    Loads the system prompt from diagnostics.SKILL.md.
    Why: Keeps AI behavior version-controlled and inspectable as a skill contract.
    """
    if not SKILL_PATH.is_file():
        raise FileNotFoundError(f"Diagnostics skill file missing: {SKILL_PATH}")
    with open(SKILL_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()


def load_log_file(file_path: str) -> tuple[str, bool]:
    """
    Reads a target log file and truncates it to the most recent lines/characters.
    Returns:
        (log_text, was_truncated)
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty.
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Log file not found: {file_path}")

    # Read UTF-8 text; replace unreadable binary bytes so we never crash on corrupt dumps
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Clear error for empty file
    if not content.strip():
        raise ValueError(f"Log file is empty: {file_path}")

    was_truncated = False
    lines = content.splitlines()

    # Apply 200-line tail sliding window
    if len(lines) > MAX_LINES:
        lines = lines[-MAX_LINES:]
        content = "\n".join(lines)
        was_truncated = True

    # Apply 8000-character tail sliding window
    if len(content) > MAX_CHARS:
        content = content[-MAX_CHARS:]
        was_truncated = True

    return content, was_truncated


def get_local_model(client, requested_model: str | None = None) -> str:
    """
    Resolves the local model to use, verifying it is pulled in Ollama.
    Why: Gives helpful, copy-pasteable pull instructions rather than an opaque API error.
    """
    if requested_model:
        target = requested_model
    elif os.getenv("SENTINEL_MODEL"):
        target = os.getenv("SENTINEL_MODEL")
    else:
        target = "gemma3:4b"

    try:
        models_info = client.list()
        available_models = [m.model for m in models_info.models] if hasattr(models_info, "models") else []
        is_available = any(target in m for m in available_models)
        if not is_available:
            print(f"[ERROR] Model '{target}' is not pulled in Ollama.", file=sys.stderr)
            print(f"        To download it, run: ollama pull {target}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        print(f"[ERROR] Cannot connect to Ollama server at {host}: {e}", file=sys.stderr)
        print("        To start Ollama, run: wsl ollama serve", file=sys.stderr)
        sys.exit(1)

    return target


def parse_and_clean_json(raw_text: str) -> dict | None:
    """
    Extracts and parses a JSON object from raw LLM output.
    Why: LLMs occasionally wrap JSON in markdown codeblocks (```json ... ```);
    this normalizes and safely extracts the dictionary.
    """
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
    return None


def sanitize_command(command: str) -> str:
    """
    Checks the suggested command against known destructive patterns.
    Why: Never trust LLM output for system modifications; strictly enforce safe triage commands.
    """
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "BLOCKED: unsafe command suggested"
    return command


def run_local_diagnosis(log_text: str) -> tuple[dict | None, str, str]:
    """
    Executes local offline diagnosis using Ollama with automatic retry on JSON failure.
    Why: Pure air-gap; NEVER imports google-genai or touches the network.
    """
    import ollama

    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    client = ollama.Client(host=host)
    model_name = get_local_model(client)
    system_prompt = load_skill_prompt()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": log_text},
    ]

    response = client.chat(
        model=model_name,
        messages=messages,
        format="json",
        options={"temperature": 0},
    )
    raw_content = response["message"]["content"]
    parsed = parse_and_clean_json(raw_content)

    if parsed is None:
        retry_messages = messages + [
            {"role": "assistant", "content": raw_content},
            {"role": "user", "content": "Your previous response was not valid JSON. Reply ONLY with the requested JSON object."},
        ]
        retry_response = client.chat(
            model=model_name,
            messages=retry_messages,
            format="json",
            options={"temperature": 0},
        )
        raw_content = retry_response["message"]["content"]
        parsed = parse_and_clean_json(raw_content)

    return parsed, raw_content, model_name


def run_cloud_diagnosis(log_text: str) -> tuple[dict | None, str, str]:
    """
    Executes cloud diagnosis using Gemma 4 via Google Gemini API (Challenge C2).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("[ERROR] GEMINI_API_KEY environment variable is not set.", file=sys.stderr)
        print("        To use --cloud, set your API key in the environment:", file=sys.stderr)
        print('        PowerShell: $env:GEMINI_API_KEY="your_api_key_here"', file=sys.stderr)
        print('        Linux/WSL:  export GEMINI_API_KEY="your_api_key_here"', file=sys.stderr)
        sys.exit(1)

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("[ERROR] google-genai package not found. Run: pip install google-genai", file=sys.stderr)
        sys.exit(1)

    model_name = os.getenv("SENTINEL_CLOUD_MODEL", "gemma-4-31b-it")
    system_prompt = load_skill_prompt()

    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        print(f"[ERROR] Failed to initialize Gemini API client: {e}", file=sys.stderr)
        sys.exit(1)

    raw_content = ""
    try:
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.0,
        )
        response = client.models.generate_content(
            model=model_name,
            contents=log_text,
            config=config,
        )
        raw_content = response.text or ""
    except Exception as e:
        err_str = str(e).lower()
        if any(term in err_str for term in ["api_key", "401", "403", "unauthenticated", "permission"]):
            print(f"[ERROR] Gemini API authentication failed. Verify your GEMINI_API_KEY.", file=sys.stderr)
            print(f"        Details: {e}", file=sys.stderr)
            sys.exit(1)
        elif any(term in err_str for term in ["quota", "429", "resourceexhausted"]):
            print(f"[ERROR] Gemini API quota or rate limit exceeded: {e}", file=sys.stderr)
            sys.exit(1)
        elif any(term in err_str for term in ["connection", "unreachable", "dns", "timeout", "socket"]):
            print(f"[ERROR] Network error: Unable to reach Gemini API. Are you offline?", file=sys.stderr)
            print(f"        Details: {e}", file=sys.stderr)
            sys.exit(1)

        try:
            combined_message = f"{system_prompt}\n\nTARGET LOG TO DIAGNOSE:\n{log_text}"
            response = client.models.generate_content(
                model=model_name,
                contents=combined_message,
                config=types.GenerateContentConfig(temperature=0.0),
            )
            raw_content = response.text or ""
        except Exception as fallback_err:
            print(f"[ERROR] Cloud diagnosis failed on model '{model_name}': {fallback_err}", file=sys.stderr)
            sys.exit(1)

    parsed = parse_and_clean_json(raw_content)

    if parsed is None and raw_content:
        try:
            retry_prompt = (
                f"{system_prompt}\n\n"
                f"Your previous answer was not valid JSON:\n{raw_content}\n\n"
                f"Please reply ONLY with a valid JSON object diagnosing this log:\n{log_text}"
            )
            retry_res = client.models.generate_content(
                model=model_name,
                contents=retry_prompt,
                config=types.GenerateContentConfig(temperature=0.0),
            )
            raw_content = retry_res.text or ""
            parsed = parse_and_clean_json(raw_content)
        except Exception:
            pass

    return parsed, raw_content, model_name


def check_backend(use_cloud: bool = False):
    """
    Verifies backend connectivity and prints actionable troubleshooting steps.
    """
    if use_cloud:
        print("[CHECK] Testing CLOUD backend (Google Gemini API with Gemma 4)...")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("[FAIL] GEMINI_API_KEY environment variable is NOT set.")
            print('       Fix: $env:GEMINI_API_KEY="your-api-key" (PowerShell)')
            print('       Fix: export GEMINI_API_KEY="your-api-key" (Linux/WSL)')
            sys.exit(1)

        try:
            from google import genai
            from google.genai import types
        except ImportError:
            print("[FAIL] google-genai library is not installed.")
            print("       Fix: pip install google-genai")
            sys.exit(1)

        model_name = os.getenv("SENTINEL_CLOUD_MODEL", "gemma-4-31b-it")
        try:
            client = genai.Client(api_key=api_key)
            # 30-second timeout prevents --check from hanging on a slow cold-start.
            # http_options passes a per-request timeout through the underlying httpx transport.
            client.models.generate_content(
                model=model_name,
                contents="Reply with the single word: ready",
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    http_options=types.HttpOptions(timeout=30_000),  # milliseconds
                ),
            )
            print(f"[PASS] Successfully connected to Gemini API with Gemma 4 model '{model_name}'.")
        except Exception as e:
            print(f"[FAIL] Cloud backend check failed for model '{model_name}': {e}")
            sys.exit(1)

    else:
        print("[CHECK] Testing LOCAL backend (Ollama in WSL)...")
        import ollama
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        try:
            client = ollama.Client(host=host)
            models_info = client.list()
            available = [m.model for m in models_info.models] if hasattr(models_info, "models") else []
            model = get_local_model(client)
            print(f"[PASS] Ollama server is active at {host}.")
            print(f"[PASS] Target local model '{model}' is installed and ready.")
            print(f"       Installed models in Ollama: {', '.join(available)}")
        except Exception as e:
            print(f"[FAIL] Ollama server is unreachable at {host}: {e}")
            print("       Fix: Start Ollama in WSL by running 'wsl ollama serve' in a separate terminal.")
            sys.exit(1)


def format_and_print_diagnosis(
    parsed: dict | None,
    raw_content: str,
    raw_log: str,
    backend_label: str,
    duration: float,
):
    """
    Prints a clean, formatted incident report for the human operator.
    Enforces verbatim evidence verification and command safety labelling.
    """
    print("\n" + "=" * 65)
    print(f"  AIRGAP SENTINEL INCIDENT REPORT")
    print("=" * 65)
    print(f"{backend_label}")
    print(f"Diagnosis Time: {duration:.2f}s")
    print("-" * 65)

    if parsed is None:
        print("[WARNING] Could not parse structured JSON from model reply.")
        print("Raw model response:")
        print(raw_content)
        print("=" * 65 + "\n")
        return

    root_cause = parsed.get("root_cause", "N/A")
    evidence_line = parsed.get("evidence_line", "").strip()
    suggested_cmd = parsed.get("suggested_command", "N/A")
    confidence = str(parsed.get("confidence", "low")).upper()

    evidence_found = bool(evidence_line and evidence_line in raw_log)
    safe_cmd = sanitize_command(suggested_cmd)

    print(f"ROOT CAUSE:\n  {root_cause}\n")

    print(f"EVIDENCE LINE:")
    if evidence_line:
        print(f'  "{evidence_line}"')
        if not evidence_found:
            print("  [WARNING: evidence not found in log, treat diagnosis as unverified]")
        else:
            print("  [VERIFIED: Line matched character-for-character in original log]")
    else:
        print("  [No evidence line provided by model]")
    print()

    print(f"SUGGESTED, NOT RUN:")
    print(f"  $ {safe_cmd}")
    print()

    print(f"CONFIDENCE: {confidence}")
    print("=" * 65 + "\n")


def wait_for_file_stability(file_path: str, stable_duration: float = 1.0, check_interval: float = 0.25, timeout: float = 10.0) -> bool:
    """
    Waits until the target file's size stops changing for at least 1 second.
    Why: Crash dumps, logs, and network transfers write data in chunks. Reading
    immediately causes truncated reads or race conditions.
    """
    start_time = time.time()
    last_size = -1
    last_change_time = time.time()

    while time.time() - start_time < timeout:
        try:
            if not os.path.exists(file_path):
                time.sleep(check_interval)
                continue
            current_size = os.path.getsize(file_path)
            # Only consider non-empty files
            if current_size > 0:
                if current_size != last_size:
                    last_size = current_size
                    last_change_time = time.time()
                elif time.time() - last_change_time >= stable_duration:
                    return True
        except (OSError, PermissionError):
            pass
        time.sleep(check_interval)

    return os.path.exists(file_path) and os.path.getsize(file_path) > 0


def diagnose_single_path(file_path: str, use_cloud: bool = False):
    """
    Coordinates reading, AI diagnosis, and output formatting for one target file.
    """
    try:
        content, was_truncated = load_log_file(file_path)
        if was_truncated:
            print(f"[INFO] Log exceeded limit: kept only the LAST {MAX_LINES} lines / {MAX_CHARS} characters.")

        start_time = time.time()
        if use_cloud:
            parsed, raw_content, model_name = run_cloud_diagnosis(content)
            backend_label = f"Backend: CLOUD Gemma 4 via Gemini API ({model_name})"
        else:
            parsed, raw_content, model_name = run_local_diagnosis(content)
            backend_label = f"Backend: LOCAL Ollama ({model_name}) | Network calls: 0"
        duration = time.time() - start_time

        format_and_print_diagnosis(parsed, raw_content, content, backend_label, duration)

    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def start_folder_watcher(watch_dir: str, use_cloud: bool = False):
    """
    Watches a target directory for new .log/.txt/.dump files using watchdog.
    Why: Provides hands-free automated triage as incident files are dropped into the system.
    """
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    watch_path = Path(watch_dir).resolve()
    watch_path.mkdir(parents=True, exist_ok=True)

    class IncidentWatchHandler(FileSystemEventHandler):
        def __init__(self):
            super().__init__()
            self.processed = set()

        def _handle(self, src_path: str):
            p = Path(src_path)
            if p.is_dir():
                return
            if p.suffix.lower() not in SUPPORTED_EXTENSIONS:
                return

            abs_str = str(p.resolve())
            # Debounce by tracking recent file events
            now = time.time()
            if abs_str in self.processed:
                return

            print(f"\n[AirGap Sentinel] Detected incoming crash file: {p.name}")
            print("                  Waiting 1s for file write to complete...")

            # Wait until file write stops changing for 1 full second
            if not wait_for_file_stability(abs_str, stable_duration=1.0):
                print(f"[WARNING] File {p.name} did not stabilize in time; skipping.")
                return

            self.processed.add(abs_str)
            print(f"[AirGap Sentinel] File write complete. Initiating triage...")
            diagnose_single_path(abs_str, use_cloud=use_cloud)
            print(f"[AirGap Sentinel] Ready. Watching {watch_path.name}/ for new files...")

        def on_created(self, event):
            self._handle(event.src_path)

        def on_modified(self, event):
            self._handle(event.src_path)

    event_handler = IncidentWatchHandler()
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)
    observer.start()

    mode_str = "CLOUD Gemma 4 (Gemini API)" if use_cloud else "LOCAL Ollama (Air-gapped)"
    print("=" * 65)
    print("  AIRGAP SENTINEL REAL-TIME FOLDER WATCHER ACTIVE")
    print("=" * 65)
    print(f"Watched Directory:  {watch_path}")
    print(f"Supported Formats:  .log, .txt, .dump")
    print(f"Inference Backend:  {mode_str}")
    print("Awaiting incident drops... (Press Ctrl+C to stop)\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[AirGap Sentinel] Shutting down folder watcher...")
        observer.stop()
    observer.join()


def main():
    parser = argparse.ArgumentParser(
        description="AirGap Sentinel - Offline AI incident responder for air-gapped systems."
    )
    parser.add_argument(
        "--once",
        type=str,
        metavar="PATH",
        help="Diagnose a single log file and exit.",
    )
    parser.add_argument(
        "--watch",
        type=str,
        metavar="DIR",
        help="Watch a folder for incoming log files using watchdog.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify the AI backend connection and model availability.",
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        help="Use Gemma 4 via Google Gemini API instead of local Ollama.",
    )

    args = parser.parse_args()

    if not args.once and not args.watch and not args.check:
        parser.print_help()
        sys.exit(0)

    # 1. Health check mode
    if args.check:
        check_backend(use_cloud=args.cloud)
        sys.exit(0)

    # 2. Real-time folder watching mode
    if args.watch:
        start_folder_watcher(args.watch, use_cloud=args.cloud)
        sys.exit(0)

    # 3. Single-shot diagnosis mode
    if args.once:
        diagnose_single_path(args.once, use_cloud=args.cloud)


if __name__ == "__main__":
    main()
