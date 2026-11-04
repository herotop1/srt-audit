"""Validate SRT files without third-party runtime dependencies."""
import argparse
import json
import re
import sys
from pathlib import Path

STAMP = re.compile(r"^(\d{2,}):(\d{2}):(\d{2}),(\d{3})$")
TIMING = re.compile(r"^(.+?)\s+-->\s+(.+?)$")


def parse_timestamp(value):
    match = STAMP.fullmatch(value)
    if not match:
        return None
    h, m, s, ms = map(int, match.groups())
    if m > 59 or s > 59:
        return None
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def validate(content):
    """Return validation issues; each issue has cue, code, and message."""
    content = content.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not content:
        return [{"cue": 0, "code": "empty", "message": "File has no subtitle cues"}]
    issues = []
    previous_end = -1
    for position, block in enumerate(re.split(r"\n[ \t]*\n", content), 1):
        lines = [line.strip() for line in block.splitlines()]
        if len(lines) < 3:
            issues.append({"cue": position, "code": "incomplete", "message": "Expected index, timing line and subtitle text"})
            continue
        if lines[0] != str(position):
            issues.append({"cue": position, "code": "index", "message": f"Expected sequence number {position}"})
        times = TIMING.fullmatch(lines[1])
        if not times:
            issues.append({"cue": position, "code": "timing", "message": "Invalid timing line"})
            continue
        start, end = (parse_timestamp(piece) for piece in times.groups())
        if start is None or end is None:
            issues.append({"cue": position, "code": "timestamp", "message": "Invalid timestamp"})
            continue
        if start >= end:
            issues.append({"cue": position, "code": "duration", "message": "Start must precede end"})
        if start < previous_end:
            issues.append({"cue": position, "code": "overlap", "message": "Cue overlaps or begins before previous cue ends"})
        previous_end = end
        if not any(lines[2:]):
            issues.append({"cue": position, "code": "text", "message": "Cue contains no subtitle text"})
    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate .srt subtitle timing and structure")
    parser.add_argument("files", nargs="+", type=Path, help="SRT file paths")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of human-readable text")
    args = parser.parse_args(argv)
    reports = []
    for path in args.files:
        try:
            issues = validate(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeError) as exc:
            issues = [{"cue": 0, "code": "read", "message": str(exc)}]
        reports.append({"file": str(path), "ok": not issues, "issues": issues})
    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
    else:
        for report in reports:
            print(f"{report['file']}: {'PASS' if report['ok'] else 'FAIL'}")
            for issue in report["issues"]:
                print(f"  cue {issue['cue']}: {issue['code']} — {issue['message']}")
    return 1 if any(not report["ok"] for report in reports) else 0


if __name__ == "__main__":
    sys.exit(main())
