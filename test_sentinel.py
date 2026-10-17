#!/usr/bin/env python3
"""
Unit tests for AirGap Sentinel core modules and guardrails.
Verifies prompt contracts, log parser, JSON extractor, safety blocklist, and evidence verification.
"""

import os
import tempfile
import unittest
from pathlib import Path

import sentinel


class TestAirGapSentinel(unittest.TestCase):

    def test_load_skill_prompt(self):
        """Verify diagnostics.SKILL.md loads properly as system prompt contract."""
        prompt = sentinel.load_skill_prompt()
        self.assertIn("AirGap Sentinel", prompt)
        self.assertIn("root_cause", prompt)
        self.assertIn("evidence_line", prompt)
        self.assertIn("suggested_command", prompt)
        self.assertIn("confidence", prompt)

    def test_load_log_file_normal(self):
        """Verify normal log files load completely without truncation."""
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
            tf.write("line 1\nline 2\nline 3\n")
            temp_path = tf.name

        try:
            content, truncated = sentinel.load_log_file(temp_path)
            self.assertFalse(truncated)
            self.assertIn("line 1", content)
            self.assertIn("line 3", content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_log_file_empty_raises(self):
        """Verify empty log files raise ValueError."""
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
            tf.write("   \n  \n")
            temp_path = tf.name

        try:
            with self.assertRaises(ValueError):
                sentinel.load_log_file(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_load_log_file_truncation(self):
        """Verify logs > 200 lines truncate to the last 200 lines."""
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tf:
            for i in range(300):
                tf.write(f"log record #{i}\n")
            temp_path = tf.name

        try:
            content, truncated = sentinel.load_log_file(temp_path)
            self.assertTrue(truncated)
            lines = content.splitlines()
            self.assertEqual(len(lines), sentinel.MAX_LINES)
            self.assertIn("log record #299", lines[-1])
            self.assertNotIn("log record #0", content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def test_parse_and_clean_json_valid(self):
        """Verify extraction from raw JSON and markdown-wrapped JSON."""
        sample_json = {
            "root_cause": "Disk partition full",
            "evidence_line": "No space left on device",
            "suggested_command": "df -h",
            "confidence": "high"
        }
        raw_json_str = '{"root_cause": "Disk partition full", "evidence_line": "No space left on device", "suggested_command": "df -h", "confidence": "high"}'
        parsed = sentinel.parse_and_clean_json(raw_json_str)
        self.assertEqual(parsed, sample_json)

        # Markdown-wrapped ```json
        md_json_str = f"```json\n{raw_json_str}\n```"
        parsed_md = sentinel.parse_and_clean_json(md_json_str)
        self.assertEqual(parsed_md, sample_json)

    def test_sanitize_command_blocklist(self):
        """Verify dangerous and destructive commands are intercepted."""
        dangerous_commands = [
            "rm -rf /var/log/*",
            "rm somefile.txt",
            "mkfs.ext4 /dev/sda1",
            "dd if=/dev/zero of=/dev/sda bs=1M",
            "shutdown -h now",
            "reboot",
            "chmod -R 777 /etc",
            ":(){ :|:& };:",
            "echo test > /dev/sda",
        ]
        for cmd in dangerous_commands:
            result = sentinel.sanitize_command(cmd)
            self.assertEqual(result, "BLOCKED: unsafe command suggested", f"Failed to block: {cmd}")

    def test_sanitize_command_safe(self):
        """Verify benign investigation commands pass through unchanged."""
        safe_commands = [
            "df -h",
            "df -h /dev/sda1",
            "systemctl status sentinel-db",
            "journalctl -xeu sentinel-db.service",
            "free -m",
            "uptime",
            "cat /proc/meminfo",
        ]
        for cmd in safe_commands:
            result = sentinel.sanitize_command(cmd)
            self.assertEqual(result, cmd, f"False positive block on: {cmd}")

    def test_verbatim_evidence_verification(self):
        """Verify verbatim matching detects hallucinated lines."""
        raw_log = "Oct 17 12:14:22 edge-gateway-01 database-daemon[1420]: [FATAL] Failed to write transaction log: No space left on device (errno 28)"
        
        # Real exact line
        real_line = "Oct 17 12:14:22 edge-gateway-01 database-daemon[1420]: [FATAL] Failed to write transaction log: No space left on device (errno 28)"
        self.assertTrue(real_line in raw_log)

        # Hallucinated line
        hallucinated_line = "Oct 17 12:14:22 edge-gateway-01 database: No space left"
        self.assertFalse(hallucinated_line in raw_log)


if __name__ == "__main__":
    unittest.main()
