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

    # ── Wire gauge / contact compatibility ───────────────────────────────────
    DenyRule(
        pattern=r"Size\s+22D\s+20\s+AWG",
        message="Size-22D solid barrel contacts accept 22–26 AWG only. "
                "20 AWG will not seat correctly in the barrel and will produce a cold crimp. "
                "Use 22 AWG for the main harness wire through the contact; pigtail stubs "
                "on the engine side (after the splice) may be heavier gauge.",
        source="https://www.ecuplus.de/en/deutsch-autosport-as620-35pn-79x-22-awg.html",
        exclude=r"(?i)(NOT|cannot|does not|incompatible|too large|will not fit)",
    ),

    # ── Cross-file pin number consistency ────────────────────────────────────
    DenyRule(
        pattern=r"(?i)(AIN\s*2|pin\s*J2).{0,40}pin\s+51\b|pin\s+51\b.{0,40}(AIN\s*2|pin\s*J2)",
        message="AIN 2 (CMC J2) crosses the AS79 firewall bulkhead at pin 56, not pin 51. "
                "Pin 51 = PST-F1 temp (AIN 1 / CMC J1). "
                "Source: firewall-bulkhead.wv — pin 51 = PST-F1 temp (AIN 1); pin 56 = AIN 2.",
        source="harnesses/firewall-bulkhead.wv",
        exclude=r"(?i)(NOT|wrong|error|was.*51|previously|51.*was|correct.*56|56.*correct)",
    ),

    # ── EPS controller capability ─────────────────────────────────────────────
    DenyRule(
        pattern=r"(?i)(EPS|electric\s+power\s+steering).{0,80}(VSS\s+input|GPO\s*→\s*EPS|wire.*MaxxECU.*EPS|EPS.*VSS)",
        message="The EPowerSteering.com KIT-33 Basic EPS Controller has no VSS or external "
                "signal input. Assist is fixed via dashboard potentiometer only — there is no "
                "port to wire MaxxECU into. Speed-sensitive assist is not supported by this product. "
                "Source: harnesses/eps-column.wv; E36_9000RPM_Project_Plan_Verified.md (recommendation struck).",
        source="harnesses/eps-column.wv",
        exclude=r"(?i)(no\s+VSS|not\s+supported|has\s+no|does\s+not\s+have|no\s+external|no\s+port|cannot|removed|struck)",
    ),

    # ── PST-F1 bulkhead pin numbers ───────────────────────────────────────────
    DenyRule(
        pattern=r"(?i)PST.{0,20}(pin\s+27|pin\s+30|pin\s+33|pin\s+34)",
        message="PST-F1 crosses the AS79 bulkhead at pins 79 (SensorGND), 47 (+5V), 50 (pressure/AIN3), "
                "51 (temp/AIN1). Pins 27/30/33/34 are flex fuel +12V, coil/inj +12V, IGN6, and IGN7 — "
                "completely wrong. Source: harnesses/firewall-bulkhead.wv pins 47/50/51/79.",
        source="harnesses/firewall-bulkhead.wv",
        exclude=r"(?i)(NOT|wrong|error|correct|was\s+pin)",
    ),

    # ── TB motor output — GPO3/4 is wrong ────────────────────────────────────
    DenyRule(
        pattern=r"(?i)(Motor\+|Motor-|ETh.*Motor|DBW.*Motor).{0,60}(GPO\s*[34]|GPO3|GPO4)",
        message="The 07K DBW throttle body motor connects to MaxxECU C2 H4 (MOTOR 1+) and C2 H2 (MOTOR 1−), "
                "NOT GPO 3 or GPO 4. GPO 3 = VVT solenoid; GPO 4 = spare. Using GPO for H-bridge motor "
                "drive would damage the output. Source: harnesses/maxxecu-07k.wv.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(NOT\s+GPO|do\s+not\s+use\s+GPO|GPO.*wrong|not\s+Motor)",
    ),

    # ── APS through AS79 pins 72-77 ───────────────────────────────────────────
    # Only flag when a line specifically routes APS *through the bulkhead* on pins 72-77.
    # ME7.1.1 OEM connector reference tables (e.g. "APS 1 GND | pin 72 | A14") are fine.
    DenyRule(
        pattern=r"(?i)(APS.{0,40}(bulkhead|AS79).{0,40}pin\s+7[2-7]|bulkhead.{0,40}APS.{0,40}pin\s+7[2-7]|APS.{0,20}pins?\s+72.{0,10}77.{0,40}(bulkhead|reserved|crossing|firewall))",
        message="APS (e-pedal) does not use AS79 pins 72–77. APS is cabin-to-cabin via Maven HD30 "
                "Connector A cabin face pins A14–A19. AS79 pins 72–77 remain spare. "
                "Source: harnesses/firewall-bulkhead-dual.wv, harnesses/epedal-bmw-e46.wv.",
        source="harnesses/firewall-bulkhead-dual.wv",
        exclude=r"(?i)(NOT|spare|not\s+used|remain\s+spare|AS79.*not|no.*bulkhead|cabin-to-cabin)",
    ),

    # ── TB wiring stays engine side — wrong claim ─────────────────────────────
    DenyRule(
        pattern=r"(?i)(Motor\+.*Motor.{0,30}|TB\s+wiring.{0,50})(stay|stays|remain|engine\s+side).{0,60}(bulkhead|firewall|not\s+cross)",
        message="TB wiring (Motor+/−, TPS1, TPS2, +5V, GND) crosses the AS79 firewall bulkhead — "
                "MaxxECU is cabin-mounted. Motor+/− via pins 22/23; TPS1/TPS2 via pins 48/56; "
                "+5V/GND via pins 47/79. Source: harnesses/maxxecu-07k.wv.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(NOT|wrong|does\s+not\s+stay|incorrect)",
    ),

    # ── EWP SSR / relay — replaced by PMU16 ──────────────────────────────────
    DenyRule(
        pattern=r"(?i)(CWA400|EWP|electric\s+water\s+pump).{0,80}(Crydom|D1D40|40A\s+relay|power\s+hold\s+relay)",
        message="The Crydom D1D40 SSR and separate 40A relay have been removed from the EWP circuit. "
                "PMU16 O5+O14 (parallel, 50A combined) drives the CWA400 directly. PMU16 handles "
                "post-shutdown cooling — no MaxxECU power hold relay needed. "
                "Source: harnesses/ewp-controller.wv, harnesses/power-distribution.wv.",
        source="harnesses/ewp-controller.wv",
        exclude=r"(?i)(removed|replaced|no\s+longer|NOT|obsolete|superseded)",
    ),

    # ── Fuel pump SSR — replaced by PMU16 O4 ─────────────────────────────────
    DenyRule(
        pattern=r"(?i)(fuel\s+pump|F90000267).{0,80}(Crydom|D1D40|SSR\s+Load|SSR\s+Ctrl)",
        message="The Crydom D1D40 SSR has been removed from the fuel pump circuit. "
                "Phase 3: PMU16 O4 (25A, PWM-capable) drives the pump directly via CAN command from MaxxECU. "
                "Phase 1 (M52): standard relay, MaxxECU GPO 2 → relay coil — no SSR. "
                "Source: harnesses/power-distribution.wv, harnesses/fuel-pump-hanger.wv.",
        source="harnesses/power-distribution.wv",
        exclude=r"(?i)(removed|replaced|replaces|no\s+longer|NOT|obsolete|superseded)",
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
# Structural checks (require parsing, not just regex)
# ---------------------------------------------------------------------------

def check_duplicate_pins_in_connections(path: Path) -> list[str]:
    """
    In .wv connections blocks, each entry is a YAML list of connector:pin-list pairs.
    A duplicate pin index within the SAME connector reference in one entry means
    two different signals are mapped to the same physical pin — e.g. [2, 1, 6, 5, 6]
    has pin 6 twice.  This check catches that class of error.

    Exemption: connectors whose name contains BUS/SUPPLY/RAIL/GND/PWR/BATT are
    intentional fan-in points (e.g. VCC1 + VCC2 both → same +5V bus pin).
    Duplicate pins on those connectors are valid and are not flagged.
    """
    if path.suffix != ".wv":
        return []
    errors = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []

    rel = str(path.relative_to(ROOT))
    # Match lines like:   - - CONNECTOR: [1, 2, 3, 4, 5]
    #                     - - CONNECTOR: [2, 1, 6, 5, 6]   ← pin 6 twice
    # Connector name is the word before the colon.
    _BUS_NAMES = re.compile(r"(?i)(SUPPLY|BUS|RAIL|GND|PWR|BATT)")
    pin_list_re = re.compile(r"-\s*-?\s*(\w+):\s*\[([^\]]+)\]")
    for lineno, line in enumerate(text.splitlines(), 1):
        m = pin_list_re.search(line)
        if not m:
            continue
        connector_name, raw = m.group(1), m.group(2)
        # Skip bus/supply connectors — intentional many-to-one termination.
        if _BUS_NAMES.search(connector_name):
            continue
        try:
            pins = [int(p.strip()) for p in raw.split(",") if p.strip().lstrip("-").isdigit()]
        except ValueError:
            continue
        if len(pins) != len(set(pins)):
            seen, dupes = set(), set()
            for p in pins:
                if p in seen:
                    dupes.add(p)
                seen.add(p)
            errors.append(f"\n  {rel}:{lineno}")
            errors.append(
                f"  ERROR: Duplicate pin index(es) {sorted(dupes)} in connections entry "
                f"for {connector_name} — two signals mapped to the same physical pin. "
                f"Check connector wiring against its pincount. "
                f"(If this is an intentional bus fan-in, add SUPPLY/BUS/RAIL to the connector name.)"
            )
            errors.append(f"  LINE:   {line.strip()[:140]}")
    return errors


def structural_audit_file(path: Path) -> list[str]:
    errors = []
    errors.extend(check_duplicate_pins_in_connections(path))
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
        all_errors.extend(structural_audit_file(f))

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
