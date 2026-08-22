#!/usr/bin/env python3
"""
e36-wiring harness documentation audit.

Checks all .md / .wv / .csv files for known-wrong values and
cross-file inconsistencies.  Designed to run as a pre-commit hook
or manually as a full-repo scan.

Usage:
    python3 scripts/audit.py               # full repo scan
    python3 scripts/audit.py --staged      # staged files only (pre-commit)
    python3 scripts/audit.py --verbose     # show every file checked

Install hook:
    bash scripts/install-hooks.sh

Adding rules:
    Each DenyRule has:
      pattern   — regex that must NOT match any line in any audited file
      message   — human-readable explanation of why it's wrong
      source    — authoritative URL that confirms the correct value
      exclude   — optional regex; if it also matches the same line, the
                  violation is suppressed.  Use this when a line legitimately
                  mentions a wrong value *in order to warn against it*
                  (e.g. "NOT K43", "does not exist").
"""

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent
AUDIT_EXTENSIONS = {".md", ".wv", ".csv"}

# ---------------------------------------------------------------------------
# DENYLIST
# ---------------------------------------------------------------------------

@dataclass
class DenyRule:
    pattern: str
    message: str
    source: str = ""
    # If this regex also matches the same line, the violation is suppressed.
    # Use for lines that cite the wrong value *in order to warn against it*.
    exclude: str = ""
    _compiled: re.Pattern = field(init=False, repr=False)
    _compiled_exclude: Optional[re.Pattern] = field(init=False, repr=False)

    def __post_init__(self):
        self._compiled = re.compile(self.pattern)
        self._compiled_exclude = re.compile(self.exclude) if self.exclude else None

    def matches(self, line: str) -> bool:
        if not self._compiled.search(line):
            return False
        if self._compiled_exclude and self._compiled_exclude.search(line):
            return False
        return True


DENYLIST: list[DenyRule] = [

    # ── DEI Fire Sleeve ─────────────────────────────────────────────────────
    DenyRule(
        pattern=r"\b010461\b",
        message="DEI 010461 is not a Fire Sleeve (it's a Reflect-A-Cool sheet). "
                "Use 010470 (3/8\" ID × 36\" kit, $26.99).",
        source="https://www.designengineering.com/fire-sleeve-tape-kit-0-375-id-x-36/",
    ),
    DenyRule(
        pattern=r"\b010460\b",
        message="DEI 010460 does not exist as a Fire Sleeve. "
                "Use 010470 (3/8\" ID × 36\" kit, $26.99).",
        source="https://www.designengineering.com/fire-sleeve-tape-kit-0-375-id-x-36/",
    ),
    DenyRule(
        pattern=r'(?i)1/2["\']?\s*[Ii][Dd].{0,30}[Ff]ire\s*[Ss]leeve'
                r'|[Ff]ire\s*[Ss]leeve.{0,30}1/2["\']?\s*[Ii][Dd]',
        message="DEI makes no 1/2\" ID Fire Sleeve. Sizes are 3/8\", 5/8\", 3/4\", 1\". "
                "Use 3/8\" ID (p/n 010470) for WBO2 cable and CLT pigtail.",
        source="https://www.designengineering.com/fire-sleeve-tape-kit-0-375-id-x-36/",
    ),

    # ── DEI Reflect-A-Gold ──────────────────────────────────────────────────
    DenyRule(
        pattern=r"\b010417\b",
        message="DEI 010417 does not exist as Reflect-A-Gold. "
                "Correct PN is 010394 (1-1/2\" × 15' roll, $42.99).",
        source="https://www.designengineering.com/reflect-a-gold-heat-reflective-tape-1-5-x-15/",
    ),
    DenyRule(
        pattern=r'(?i)[Rr]eflect-[Aa]-[Gg]old.{0,40}\b1["\']?\s*wide'
                r'|\b1["\']?\s*wide.{0,40}[Rr]eflect-[Aa]-[Gg]old',
        message="Reflect-A-Gold minimum width is 1-1/2\" — it does not come in 1\" wide.",
        source="https://www.designengineering.com/reflect-a-gold-heat-reflective-tape-1-5-x-15/",
    ),
    DenyRule(
        pattern=r"(?i)90%\s*radiant.{0,60}[Rr]eflect-[Aa]-[Gg]old"
                r"|[Rr]eflect-[Aa]-[Gg]old.{0,60}90%\s*radiant",
        message="Reflect-A-Gold is NOT '90% radiant heat reflection' — that describes Reflect-A-Cool. "
                "Reflect-A-Gold is metalized polyimide laminated glass cloth, 800°F continuous.",
        source="https://www.designengineering.com/reflect-a-gold-heat-reflective-tape-1-5-x-15/",
    ),

    # ── AS79 contact size ────────────────────────────────────────────────────
    DenyRule(
        pattern=r"(?i)AS[-\s]?79.{0,30}size[-\s]?20|size[-\s]?20.{0,30}AS[-\s]?79",
        message="AS79 uses size-22 contacts, not size-20. "
                "Source: m-cal.com AS020-35SN (\"Primary Contacts Size: 22 AWG\").",
        source="https://m-cal.com/en-gb/883605120-mc03-as020-35sn-deutsch-autosport-as-connector-79-way-shell-size-20-pin-layout-20-35-style-0-flange-receptacle-red-n-keyway-sockets-standard",
        # Allow lines that are clarifying the *shell* size-20 vs contact size-22 distinction,
        # or that are explicitly warning against size-20 for AS79.
        exclude=r"(?i)(NOT|not for|does not|cannot|shell\s+size.?20|layout.?20.?35)",
    ),
    DenyRule(
        pattern=r"(?i)(firewall\s+bulkhead|AS\s*series).{0,60}size[-\s]?20\b",
        message="The AS-series firewall bulkhead uses size-22 contacts (5A, 22-26 AWG). "
                "Size-20 is for Maven HD30 / DT-series contacts.",
        source="https://www.ecuplus.de/en/deutsch-autosport-as620-35pn-79x-22-awg.html",
        # Allow lines explaining that size-20 is NOT for the AS bulkhead,
        # or referencing the HD30's size-20 contacts in contrast.
        exclude=r"(?i)(NOT|only|HD30|Maven|DT.?series|not for|cannot|does not)",
    ),

    # ── AS79 positioners ─────────────────────────────────────────────────────
    DenyRule(
        pattern=r"\bK43\b.{0,80}AS[-\s]?79|AS[-\s]?79.{0,80}\bK43\b",
        message="K43 (M22520/2-10) is the size-20 positioner. "
                "AS79 size-22 contacts need K42 (pin, M22520/2-09) and K40 (socket, M22520/2-07).",
        source="https://www.ecuplus.de/en/deutsch-autosport-as620-35pn-79x-22-awg.html",
        # Suppress when the same line explicitly disqualifies K43 (warning context).
        exclude=r"(?i)(NOT\s+K43|K43\s+is\s+(the\s+)?size|do not use.*K43|K43.*do not|wrong.*K43|K43.*wrong)",
    ),
    DenyRule(
        pattern=r"\bK43\b.{0,80}(firewall\s+bulkhead|AS\s+series)"
                r"|(firewall\s+bulkhead|AS\s+series).{0,80}\bK43\b",
        message="K43 (M22520/2-10) is the size-20 positioner. "
                "AS-series firewall bulkhead needs K42 (pin) + K40 (socket) for size-22 contacts.",
        source="https://dmctools.com/k40",
        exclude=r"(?i)(NOT\s+K43|K43\s+is\s+(the\s+)?size|do not use.*K43|K43.*do not|wrong.*K43)",
    ),
    DenyRule(
        pattern=r"M22520/2-10.{0,60}AS[-\s]?79|AS[-\s]?79.{0,60}M22520/2-10",
        message="M22520/2-10 is the K43 (size-20) positioner. "
                "AS79 needs K42 = M22520/2-09 (pin) and K40 = M22520/2-07 (socket).",
        source="https://deltaintl.com/products/k42",
        exclude=r"(?i)(NOT|wrong|do not|cannot|size.?20\s+positioner)",
    ),

    # ── HDT-48-00 scope ──────────────────────────────────────────────────────
    DenyRule(
        pattern=r"HDT-48-00.{0,80}AS[-\s]?79|AS[-\s]?79.{0,80}HDT-48-00",
        message="HDT-48-00 covers size 12/16/20 contacts only. "
                "It CANNOT crimp AS79 size-22 contacts. Use AFM8 + K42/K40.",
        source="https://www.deutschconnector.com/downloads/HDT-48-00%20Instructions.pdf",
        exclude=r"(?i)(NOT|cannot|does not|CANNOT|not for|not support|not.*size.?22)",
    ),
    DenyRule(
        pattern=r"(?i)HDT-48-00.{0,80}(firewall\s+bulkhead|AS\s+bulkhead)",
        message="HDT-48-00 is for Maven HD30 and DT-series (size 12/16/20) only. "
                "The AS-series firewall bulkhead requires AFM8 + K42 + K40.",
        source="https://www.deutschconnector.com/downloads/HDT-48-00%20Instructions.pdf",
        exclude=r"(?i)(NOT|cannot|does not|CANNOT|not for|not support)",
    ),

    # ── Non-existent part / tool numbers ────────────────────────────────────
    DenyRule(
        pattern=r"\bTL-10\b",
        message="Daniels DMC TL-10 does not exist on any DMC/Daniels product page. "
                "Likely intended: AFM8 (M22520/2-01).",
        source="https://dmctools.com/afm8",
        exclude=r"(?i)(does not exist|not exist|no such|previously listed|TL-10.*not)",
    ),
    DenyRule(
        pattern=r"Knipex\s+97\s+52\s+68",
        message="Knipex 97 52 68 does not exist in the Knipex catalog. "
                "Use Engineer PA-09 for VAG JMT/JPT pigtail contacts.",
        source="https://www.amazon.com/dp/B002AVVO7K",
        # Suppress when the line is citing it as an example of what NOT to use.
        exclude=r"(?i)(does not exist|not exist|previously listed|not in the|⚠️|WARNING|WARN)",
    ),
    DenyRule(
        pattern=r"(?i)HDT-48-00.{0,30}size[-\s]?22|size[-\s]?22.{0,30}HDT-48-00",
        message="HDT-48-00 cannot crimp size-22 contacts. Use AFM8 + K42 (pin) or K40 (socket).",
        source="https://dmctools.com/afm8",
        exclude=r"(?i)(NOT|cannot|does not|CANNOT|not support)",
    ),
]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_staged_files() -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True, cwd=ROOT,
    )
    return [
        ROOT / f
        for f in result.stdout.strip().splitlines()
        if f and (ROOT / f).suffix in AUDIT_EXTENSIONS
    ]


def get_all_files() -> list[Path]:
    files = []
    for ext in AUDIT_EXTENSIONS:
        files.extend(ROOT.rglob(f"*{ext}"))
    return [f for f in files if ".git" not in str(f)]


def audit_file(path: Path, verbose: bool) -> list[str]:
    errors = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return [f"  [read error] {path.relative_to(ROOT)}: {e}"]

    rel = path.relative_to(ROOT)
    if verbose:
        print(f"  checking {rel}", file=sys.stderr)

    for lineno, line in enumerate(lines, 1):
        for rule in DENYLIST:
            if rule.matches(line):
                errors.append(f"\n  {rel}:{lineno}")
                errors.append(f"  ERROR: {rule.message}")
                if rule.source:
                    errors.append(f"  SOURCE: {rule.source}")
                errors.append(f"  LINE:   {line.strip()[:140]}")

    return errors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    staged_only = "--staged" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    files = get_staged_files() if staged_only else get_all_files()
    files = [f for f in files if f.exists()]

    if not files:
        print("audit: no files to check.")
        sys.exit(0)

    mode = "staged files" if staged_only else "all files"
    print(f"audit: checking {len(files)} {mode} …", file=sys.stderr)

    all_errors: list[str] = []
    for f in sorted(files):
        all_errors.extend(audit_file(f, verbose))

    if all_errors:
        print("\n\033[31m✗ Harness doc audit FAILED\033[0m")
        for line in all_errors:
            print(line)
        # Each violation emits 4 lines; report count of violations
        print(
            f"\n{len(all_errors) // 4} violation(s) found. "
            "Fix the lines above before committing.\n"
            "To skip this check (use sparingly): git commit --no-verify"
        )
        sys.exit(1)
    else:
        print(f"\033[32m✓ Audit passed\033[0m — {len(files)} files, 0 violations.")
        sys.exit(0)


if __name__ == "__main__":
    main()
