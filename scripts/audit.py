#!/usr/bin/env python3
"""
e36-wiring harness documentation audit.

Checks all .md / .wv / .csv files for known-wrong values and
cross-file inconsistencies.  Designed to run as a pre-commit hook
or manually as a full-repo scan.

═══════════════════════════════════════════════════════════════════════════════
ARCHITECTURE CONTEXT (H2O engine-bay-mount + phase model)
═══════════════════════════════════════════════════════════════════════════════

As of the race-h20-investigation branch, the wiring architecture is:

  - MaxxECU RACE H2O is engine-bay-mounted (OEM DME E-box cavity, intake side
    of RHD car — driver-opposite side). All engine sensor / IGN / INJ / GPO
    signals direct-terminate at the ECU's C1/C2 Molex CMC connectors. There
    is NO firewall bulkhead in the engine-sensor path.

  - Cabin↔engine signals cross via the Maven HD30 Dual 16+16 Bulkhead kit:
      * Connector A (16-pin): CAN + DCT shifter — populated Phase 2/3.
      * Connector B (16-pin): APS throttle input — SAFETY-CRITICAL by design,
        populated Phase 3.
    Product page: mavenspeed.com/collections/b2t-engineering/products/
                  dual-connector-bulkhead

  - PMU16 is a Phase 3 install. NOT present in Phase 1 or Phase 2. Phase 1
    fuel pump uses a discrete high-current relay (JDT Racing rewire kit) driven
    by MaxxECU GPO 2 via M50 pre-terminated harness 12-pin extra pin 3.

  - The Deutsch AS79 79-way firewall bulkhead is DEPRECATED. Files
    harnesses/firewall-bulkhead.wv and harnesses/firewall-bulkhead-dual.wv
    have been deleted. Use harnesses/firewall-crossing-maven.wv.

Phase-split .wv files (created when a component's wiring changes across
phases due to the PMU16 or ECU-harness transition):
  - harnesses/8hp-body-integrations-phase{1,3}.wv (reverse light circuit)
  - harnesses/fuel-pump-hanger-phase{1,3}.wv (Walbro F90000267 drive)
  - harnesses/flex-fuel-sensor-phase{1,3}.wv (GM 13577379 sensor)

Vendor citations in this audit:
  - MaxxECU H2O: maxxecu.com/products/race/, maxxecu.com/webhelp/wirings-maxxecu_pinout.html
  - Ecumaster PMU16: docs/vendor/ecumaster/PMU16_Manual_v101.pdf
  - Walbro F90000267: walbrofuelpumps.com/450lph-walbro-e85-racing-fuel-pump-f90000267.html
  - JDT Racing rewire kit: jdtracing.com/products/walbro-ti-f90000267-450lph-fuel-pump-w-install-kit-rewire-kit-e85-compatible
  - Deutsch HDT-48-00: deutschconnector.com selection guide


Usage:
    python3 scripts/audit.py               # full repo scan
    python3 scripts/audit.py --staged      # staged files only (pre-commit)
    python3 scripts/audit.py --verbose     # show every file checked

Install hook:
    bash scripts/install-hooks.sh

═══════════════════════════════════════════════════════════════════════════════
METHODOLOGY — HOW TO MAINTAIN THIS AUDIT
═══════════════════════════════════════════════════════════════════════════════

This audit is intentionally self-reinforcing: every inconsistency found in a
manual review becomes a DenyRule or a structural check so it can never silently
re-appear.

Workflow after finding an issue:
  1. Fix the affected file(s).
  2. Identify the "wrong value" pattern and add a DenyRule below — or, if the
     check requires comparing two values across a file, add a structural check
     in the structural_audit_file() section at the bottom.
  3. Optionally add the correct value to KNOWN_CMC_PINS / KNOWN_AS79_PINS if
     it is a signal→pin mapping that should be enforced everywhere.
  4. Run the audit to confirm it now catches the old value and passes on the
     corrected file.

There are three layers of protection:

  Layer 1 — DENYLIST (regex, per-line)
    Catches explicit wrong values: wrong part numbers, wrong AWG specs,
    deprecated architecture references, wrong connector family names, etc.
    Rule of thumb: add one rule per issue class found, not per file.

  Layer 2 — KNOWN_CMC_PINS / check_signal_pin_references (structural, cross-file)
    A ground-truth dict maps signal keywords to their correct CMC pin numbers.
    The checker scans every "CMC pin NN" reference near a signal keyword and
    flags mismatches.  Add an entry whenever a signal→pin mapping is confirmed
    by an authoritative source (MaxxECU wiring diagram or maxxecu-07k.wv).

  Layer 3 — check_wire_color_convention / check_duplicate_pins (structural)
    Validates .wv cable definitions: color↔function convention and no duplicate
    pin indices in the same connections entry.

Adding a DenyRule:
    Each DenyRule has:
      pattern   — regex that must NOT match any line in any audited file
      message   — human-readable explanation of why it's wrong
      source    — authoritative file or URL confirming the correct value
      exclude   — optional regex; if it also matches the same line, the
                  violation is suppressed.  Use this when a line legitimately
                  mentions a wrong value *in order to warn against it*
                  (e.g. "NOT K43", "does not exist", "20 AWG will not seat").

Tips:
  • Use the exclude= field liberally — it is better to have a rule that
    suppresses one legitimate warning-context line than to have no rule at all.
  • Prefer narrow patterns over broad ones: "CLT.*CMC pin 13" is better than
    "CMC pin 13" (which could legitimately appear in WBO2 heater context).
  • After each manual audit round, grep for the old-wrong patterns in the
    repo to confirm there are no survivors.
"""

import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).parent.parent
# Also scan the sibling e36-docs repo if present. All DenyRules apply there too — the
# walkthrough .md and .csv files in e36-docs are just as likely to carry stale values.
EXTRA_ROOTS: list[Path] = [
    p for p in [ROOT.parent / "e36-docs"] if p.is_dir()
]
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

    # ── H2O engine-bay-mount architecture — deprecated AS79 references ──────
    # As of the race-h20-investigation branch, the MaxxECU RACE H2O is engine-bay-
    # mounted and the Deutsch AS79 79-way firewall bulkhead is REMOVED entirely.
    # Signals cross via the Maven HD30 dual 16+16 bulkhead (Connector A = CAN + DCT
    # cabin signals, Connector B = safety-critical APS throttle input) — see
    # harnesses/firewall-crossing-maven.wv and docs/vendor/maxxecu/MaxxECU_RACE_H2O.md.
    # Any active AS79 statement (not a deprecation-context reference) is now stale.
    DenyRule(
        pattern=r"(?i)\bAS[-\s]?79\b",
        message="AS79 firewall bulkhead has been deprecated. Under the H2O engine-bay-mount "
                "architecture the MaxxECU is engine-bay-mounted and there is no AS79 in the "
                "build. Cabin↔engine signals cross via the Maven HD30 dual 16+16 bulkhead. "
                "See harnesses/firewall-crossing-maven.wv and docs/vendor/maxxecu/MaxxECU_RACE_H2O.md. "
                "If this line is a deprecation reference (comparing to old arch), add 'deprecated' "
                "or 'no longer used' or 'was AS79' or 'switch to Maven' to the same line.",
        source="harnesses/firewall-crossing-maven.wv",
        exclude=r"(?i)(deprecated|no longer|no.?longer|was\s+AS79|previously|removed|abandoned"
                r"|superseded|obsolete|instead of|replaces|replaced|migration|migrated"
                r"|switch to|switching to|H2O|switch from|not\s+AS79|AS.?series\s+(bulkhead\s+)?from\s+a\s+previous"
                r"|old\s+arch|old\s+architecture|previous\s+architecture|Phase\s+1\s+used"
                r"|dropping|dropped|scrap|scrapped|no\s+separate\s+AS|no\s+separate\s+AS-series"
                r"|not\s+used|not\s+active|N/A|does\s+not\s+exist)",
    ),
    DenyRule(
        pattern=r"harnesses/firewall-bulkhead(-dual)?\.wv",
        message="harnesses/firewall-bulkhead.wv and harnesses/firewall-bulkhead-dual.wv have "
                "been DELETED. Use harnesses/firewall-crossing-maven.wv instead. "
                "(git history preserves the old files for archival access.)",
        source="harnesses/firewall-crossing-maven.wv",
        exclude=r"(?i)(deleted|removed|deprecated|superseded|replaced|no longer|obsolete"
                r"|was\s+in|old\s+plan|old\s+file|previous\s+arch|history|archival)",
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
    # (HDT-48-00 vs size-22 rule removed — no more size-22 contacts in this build.)

    # (Size-22D 20 AWG rule removed — no AS79 size-22 contacts in this build.
    #  Maven HD30 size-16 contacts accept 14-20 AWG. See docs/wiring-bom.md System 8.)

    # (AIN 2 / pin 51 cross-file consistency rule removed — bulkhead pin numbers
    #  no longer applicable under direct-terminate architecture.)

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

    # (PST-F1 bulkhead pin numbers rule removed — PST-F1 no longer crosses a bulkhead.
    #  Under H2O arch, sensor and ECU are both engine-bay-side. Phase 1: PST-F1 pigtail
    #  → M50 harness 16-pin aux breakout pins 1/2/12/14. Phase 3: PST-F1 → CMC C1
    #  pins 25/29/37/33 direct-terminate. See harnesses/pst-f1-sensor.wv.)

    # ── TB motor output — GPO3/4 is wrong ────────────────────────────────────
    DenyRule(
        pattern=r"(?i)(Motor\+|Motor-|ETh.*Motor|DBW.*Motor).{0,60}(GPO\s*[34]|GPO3|GPO4)",
        message="The 07K DBW throttle body motor connects to MaxxECU C2 H4 (MOTOR 1+) and C2 H2 (MOTOR 1−), "
                "NOT GPO 3 or GPO 4. GPO 3 = VVT solenoid; GPO 4 = spare. Using GPO for H-bridge motor "
                "drive would damage the output. Source: harnesses/maxxecu-07k.wv.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(NOT\s+GPO|do\s+not\s+use\s+GPO|GPO.*wrong|not\s+Motor)",
    ),

    # ── APS routing under H2O arch — Maven Connector B, NOT Connector A ──────
    # Under the new arch, Connector B is designated safety-critical and reserved
    # for APS (throttle command input). Connector A carries CAN + DCT shifter.
    # See docs/dbw-pinouts.md § Firewall Crossing Allocation.
    DenyRule(
        pattern=r"(?i)APS.{0,60}Maven.{0,10}(HD30\s+)?[Cc]onnector\s+A"
                r"|Maven.{0,10}(HD30\s+)?[Cc]onnector\s+A.{0,60}APS",
        message="APS crosses via Maven HD30 Connector B (safety-critical, populated Phase 3), "
                "NOT Connector A. Connector A carries CAN + DCT shifter cabin signals. "
                "Source: harnesses/firewall-crossing-maven.wv; docs/dbw-pinouts.md § Firewall Crossing Allocation.",
        source="harnesses/firewall-crossing-maven.wv",
        exclude=r"(?i)(NOT\s+Connector\s+A|Connector\s+A.{0,20}not|CAN.{0,10}DCT|Connector\s+B\s+for\s+APS"
                r"|B\s*=\s*APS|not\s+A|instead\s+of\s+A|was\s+A|old\s+plan)",
    ),
    DenyRule(
        pattern=r"(?i)(APS|e.?pedal).{0,60}cabin.to.cabin|cabin.to.cabin.{0,60}(APS|e.?pedal)",
        message="APS is NOT cabin-to-cabin under the H2O engine-bay-mount arch — MaxxECU is "
                "engine-bay-mounted, so APS crosses the firewall via Maven Connector B (6 wires). "
                "Source: harnesses/epedal-bmw-e46.wv; docs/dbw-pinouts.md.",
        source="harnesses/epedal-bmw-e46.wv",
        exclude=r"(?i)(NOT\s+cabin.to.cabin|was\s+cabin|previously|old\s+plan|deprecated"
                r"|cabin.to.cabin.{0,10}was|now\s+cross|does\s+cross)",
    ),

    # ── Maven bulkhead — dual 16+16, NOT single 35-pin ───────────────────────
    # Earlier plan was a single 35-pin HD30 24-35 connector. Superseded by
    # dual 16+16 kit which gives cleaner pin allocation and dedicated safety-
    # critical Connector B for APS.
    # NOTE: The shell-size-24 designation is Deutsch's shell nomenclature — it
    # applies to BOTH the old single 35-pin insert AND the new individual 16-way
    # inserts in the dual kit. Only flag when the DEPRECATED "24-35" arrangement
    # or the "35-pin" wording appears.
    DenyRule(
        pattern=r"(?i)Maven.{0,20}(35.pin|HD30\s+24.?35|shell.?size.?24[-\s]?35|24.?35\s+arrangement)",
        message="The Maven single 35-pin HD30 (shell-size-24, 24-35 arrangement) was superseded "
                "by the Maven Dual Connector Bulkhead 16+16 kit. See docs/wiring-bom.md System 8. "
                "Product page: mavenspeed.com/collections/b2t-engineering/products/dual-connector-bulkhead",
        source="https://mavenspeed.com/collections/b2t-engineering/products/dual-connector-bulkhead",
        exclude=r"(?i)(superseded|deprecated|was|previously|abandoned|old\s+plan|instead\s+of"
                r"|not\s+35|dual\s+16|16.{0,3}16|16.way|16.pin)",
    ),
    # Deprecated pigtail-stub tail with 20 AWG (old method, never valid in this build)
    DenyRule(
        pattern=r"(?i)pigtail.{0,20}stub.{0,40}20\s*AWG|20\s*AWG.{0,40}pigtail.{0,20}stub",
        message="The pigtail-stub / 20 AWG engine-side tail approach is deprecated. "
                "All harness wires are 22 AWG TXL end-to-end, direct termination. "
                "Source: wiring-bom.md § Pigtail tail wire removed; harness-build.md § Direct Termination.",
        source="docs/harness-build.md",
        exclude=r"(?i)(removed|replaced|no longer|deprecated|previous|NOT|old method|was.*20)",
    ),

    # ── EWP supply wire gauge ─────────────────────────────────────────────────
    # Audit round 3: wiring-bom.md line 43 (bulk wire table) said 10 AWG.
    # 10 AWG is marginal at 35.5A / 1.5m; 8 AWG is spec.
    DenyRule(
        pattern=r"(?i)(EWP|CWA400|electric\s+water\s+pump).{0,50}10\s*AWG",
        message="EWP supply wire must be 8 AWG. 10 AWG is marginal at 35.5A / 1.5m "
                "(voltage drop exceeds CWA400 spec). "
                "Source: wiring-bom.md CABLE_PWR_OUT definition.",
        source="docs/wiring-bom.md",
        # GND return cable (CABLE_GND) at 10 AWG is fine — lower impedance path, shorter.
        # Dual-leg architecture (10 AWG per leg × 2 in parallel) is fine — parallel = lower resistance.
        # "Insufficient" / "marginal" lines are warning context, not an error.
        exclude=r"(?i)(marginal|NOT|8.AWG.{0,20}not.{0,20}10|10.*marginal|insufficient|undersized"
                r"|CABLE_GND|chassis\s+GND|GND.*10\s*AWG|10\s*AWG.*GND"
                r"|per\s+leg|per.leg|parallel\s+leg|O5.*O14|dual.*AWG)",
    ),

    # ── CLT CMC pin number ────────────────────────────────────────────────────
    # Audit round 3: 26-07k-harness.md line 127 said "CMC pin 13" for CLT.
    # CMC pin 13 = D1 = WBO2 Heater−.  CLT = CMC F1 = pin 21.
    DenyRule(
        pattern=r"(?i)(CLT|coolant.{0,10}temp).{0,40}CMC.{0,10}pin\s*13"
                r"|CMC.{0,10}pin\s*13.{0,40}(CLT|coolant.{0,10}temp)",
        message="CLT is at CMC F1 = pin 21. CMC pin 13 = D1 = WBO2 Heater−. "
                "Wiring CLT to pin 13 connects coolant temp to the WBO2 heater output. "
                "Source: harnesses/maxxecu-07k.wv ECU_CMC pinlabels.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(NOT|wrong|was.*13|13.*was|correct.*21|21.*correct)",
    ),

    # ── Knock sensor 1J0973712 contact family ────────────────────────────────
    # Audit round 3: 26-07k-harness.md line 120 said "JMT 1.5mm" for 1J0973712.
    # 1J0973712 uses flat-blade (push-on spade) contacts, not round-pin JMT.
    DenyRule(
        pattern=r"(?i)1J0973712.{0,40}JMT|JMT.{0,40}1J0973712",
        message="1J0973712 (knock sensor connector) uses flat-blade (push-on spade) contacts — "
                "NOT JMT 1.5mm round-pin. JMT contacts will not seat in 1J0973712 cavities. "
                "Source: E36_CSVs/E36_Phase3_FinalSwap.csv; 26-07k-harness.md parts table.",
        source="docs/wiring-bom.md",
        exclude=r"(?i)(NOT|will not seat|JMT.{0,10}not|not.{0,10}JMT|flat.blade.*not|not.*flat.blade)",
    ),

    # (AS79 pin 34 / IGN 7 rule removed — AS79 no longer applicable. The underlying
    #  IGN 7 unused claim is preserved via the KNOWN_CMC_PINS map for CMC D2.)

    # ── TPS1 mislabeled as AIN 5 ─────────────────────────────────────────────
    # Audit round 3: dbw-pinouts.md line 171 parenthetical "(AIN 5 / was M52 TPS)".
    # TPS1 is at CMC G2 (C1 TPS input). AIN 5 = CMC C2 G3 = clutch position sensor.
    DenyRule(
        pattern=r"(?i)TPS\s*1?.{0,30}AIN\s*5|AIN\s*5.{0,30}TPS\s*1?",
        message="TPS1 is at CMC G2 (C1 TPS input). AIN 5 = CMC C2 G3 (clutch position sensor). "
                "These are different pins on different ECU connectors. "
                "Source: harnesses/maxxecu-07k.wv ECU_CMC and ECU_C2 pinlabels.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(NOT|wrong|AIN\s*5.{0,20}is.{0,20}clutch|clutch.{0,20}AIN\s*5|≠)",
    ),

    # ── INJ signal wire splice ────────────────────────────────────────────────
    # Audit round 3: harness-build.md line 373 said INJ signal wire uses a
    # "separate Raychem splice at the same pigtail, going to pin 2".
    # INJ signal wires run end-to-end; only the +12V bus (pin 1) gets a Raychem tap.
    DenyRule(
        pattern=r"(?i)(INJ.{0,20}signal|signal.{0,20}INJ).{0,60}(Raychem\s*splice|pigtail\s*splice|splice.{0,20}pin\s*2)",
        message="INJ signal wires (EV14 pin 2) run end-to-end from AS79 to EV14 terminal — no splice. "
                "Only the shared +12V bus (EV14 pin 1) uses a Raychem tap splice. "
                "Source: harness-build.md § Direct Termination; wiring-bom.md line 45.",
        source="docs/harness-build.md",
        exclude=r"(?i)(NOT|no\s+splice|no\s+intermediate|end.to.end|directly from)",
    ),

    # (0411-240-2005 vs AS79 extraction rule removed — AS79 no longer used.
    #  Maven HD30 size-16 extraction uses standard Deutsch round-shoulder tool.)

    # ── DBW TPS cable sensor GND color ───────────────────────────────────────
    # Audit round 3: wiring-bom.md line 348 listed BK (chassis GND) and GN (GPO)
    # for the DBW TPS 4-wire cable.  Correct: BN (sensor GND), WH (TPS2 signal).
    DenyRule(
        pattern=r"(?i)(DBW.{0,10}TPS|TPS.{0,10}4.wire).{0,60}\bBK\b.{0,30}(sensor\s*GND|SGND|GND\s*signal)",
        message="DBW TB TPS 4-wire sensor GND wire must be BN (Brown), not BK (Black). "
                "BK = chassis GND only. BN = sensor GND / VR Signal−. "
                "Source: harnesses/maxxecu-07k.wv W_DBW_TPS cable colors.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(NOT|wrong|BN.{0,20}not.{0,20}BK|use.{0,10}BN)",
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

    # ── Fuel pump SSR — replaced (Phase 1: discrete relay; Phase 3: PMU16 O4) ─
    DenyRule(
        pattern=r"(?i)(fuel\s+pump|F90000267).{0,80}(Crydom|D1D40|SSR\s+Load|SSR\s+Ctrl)",
        message="The Crydom D1D40 SSR has been removed from the fuel pump circuit. "
                "Phase 1 (M52): discrete high-current relay (JDT Racing rewire kit or Bosch 0332-002-156), "
                "MaxxECU GPO 2 → relay coil. Phase 3 (07K swap): PMU16 O4 (25A, PWM-capable) direct-drive "
                "replaces the discrete relay. NEITHER phase uses an SSR. "
                "Source: harnesses/fuel-pump-hanger-phase1.wv, harnesses/fuel-pump-hanger-phase3.wv.",
        source="harnesses/fuel-pump-hanger-phase3.wv",
        exclude=r"(?i)(removed|replaced|replaces|no\s+longer|NOT|obsolete|superseded)",
    ),

    # ── PMU16 is Phase 3 install ONLY ─────────────────────────────────────────
    # PMU16 is not in the car during Phase 1 or Phase 2. Any active statement
    # claiming a PMU16 output drives a load in Phase 1 is stale.
    DenyRule(
        pattern=r"(?i)Phase\s*1.{0,60}PMU16|PMU16.{0,60}Phase\s*1\s*(install|arrives|drives|present|is\s+installed|installation)",
        message="PMU16 is NOT installed in Phase 1 or Phase 2 — it arrives at Phase 3 (07K swap moment) "
                "along with the Maven bulkhead, custom 07K harness, EWP, APS pedal, and electric AC. "
                "Under Phase 1, loads that PMU16 will eventually drive use OEM relays or aftermarket "
                "discrete relays driven by MaxxECU GPO outputs. See harnesses/power-distribution.wv "
                "'PHASE 3 INSTALL FILE' header + OEM E36 RELAY REPLACEMENT MAP.",
        source="harnesses/power-distribution.wv",
        exclude=r"(?i)(NOT\s+installed|not\s+in|no\s+PMU\s+in\s+Phase\s+1|arrives\s+at\s+Phase\s+3"
                r"|Phase\s+3\s+install|no\s+longer|previously|deprecated|old\s+plan|was\s+Phase\s+1"
                r"|corrected|Phase\s+3\s+arrival|Phase\s+3\s+file)",
    ),

    # ── MaxxECU is engine-bay-mounted (H2O), NOT cabin-mounted ────────────────
    # Under the H2O architecture the MaxxECU RACE H2O sits in the engine bay
    # (OEM DME E-box cavity, intake side of RHD car). Any active statement
    # saying "MaxxECU is cabin-mounted" is stale.
    DenyRule(
        pattern=r"(?i)MaxxECU\s+is\s+cabin.?mounted|cabin.?mounted\s+MaxxECU",
        message="Under the H2O engine-bay-mount architecture, the MaxxECU RACE H2O is engine-bay-"
                "mounted (OEM DME E-box cavity, intake side of RHD car). NOT cabin-mounted. "
                "Source: docs/vendor/maxxecu/MaxxECU_RACE_H2O.md; harnesses/firewall-crossing-maven.wv.",
        source="docs/vendor/maxxecu/MaxxECU_RACE_H2O.md",
        exclude=r"(?i)(NOT\s+cabin|no\s+longer\s+cabin|was\s+cabin|previously\s+cabin|old\s+arch"
                r"|deprecated|now\s+engine.?bay|engine.?bay\s+mount|H2O|corrected)",
    ),

    # ── Deleted / renamed .wv file references ─────────────────────────────────
    DenyRule(
        pattern=r"harnesses/8hp-body-integrations\.wv",
        message="harnesses/8hp-body-integrations.wv has been SPLIT into "
                "harnesses/8hp-body-integrations-phase1.wv (M50 harness + discrete relay) and "
                "harnesses/8hp-body-integrations-phase3.wv (PMU16 direct-drive). "
                "Update the reference to the phase-appropriate file.",
        source="harnesses/8hp-body-integrations-phase1.wv",
        exclude=r"(?i)(split|deleted|renamed|superseded|-phase1|-phase3|old\s+file|was\s+split)",
    ),
    DenyRule(
        pattern=r"harnesses/fuel-pump-hanger\.wv",
        message="harnesses/fuel-pump-hanger.wv has been SPLIT into "
                "harnesses/fuel-pump-hanger-phase1.wv (discrete relay + JDT rewire kit) and "
                "harnesses/fuel-pump-hanger-phase3.wv (PMU16 O4 direct-drive). "
                "Update the reference to the phase-appropriate file.",
        source="harnesses/fuel-pump-hanger-phase1.wv",
        exclude=r"(?i)(split|deleted|renamed|superseded|-phase1|-phase3|old\s+file|was\s+split)",
    ),
    DenyRule(
        pattern=r"harnesses/flex-fuel-sensor\.wv",
        message="harnesses/flex-fuel-sensor.wv (if referenced) does not exist as a single file — "
                "flex fuel is split into harnesses/flex-fuel-sensor-phase1.wv (M50 harness 16-pin "
                "aux breakout DIN 3) and harnesses/flex-fuel-sensor-phase3.wv (CMC C1 direct DIN 3). "
                "Update the reference to the phase-appropriate file.",
        source="harnesses/flex-fuel-sensor-phase1.wv",
        exclude=r"(?i)(does not exist|deleted|-phase1|-phase3|split)",
    ),

    # ── 07K crank sensor type — Hall, NOT VR ─────────────────────────────────
    # Audit round 4 (2025-07): OE# 07K906433B confirmed Hall (Valeo 366675 datasheet
    # "Sensor Type: Hall Sensor"; the07k.wiki "The 07K engine uses a Hall Effect crank
    # position sensor").  BGP wiring diagram labels it "VR" — that diagram is wrong.
    DenyRule(
        pattern=r"(?i)(07K|07k).{0,40}(passive\s*VR|VR\s*sensor|VR\+|VR-|Trigger\s*GND\s*/\s*VR)",
        message="The VW 07K crank sensor is Hall effect (OE# 07K906433B), NOT passive VR. "
                "BGP wiring diagram labels 'VR+/VR-/Shield' but the07k.wiki confirms this is wrong. "
                "Confirmed: Valeo PN 366675 datasheet 'Sensor Type: Hall Sensor'. "
                "Correct connector: CRANK_HALL, pinout +5V/Signal/SensorGND. "
                "MTune trigger = Digital (Hall, opto), NOT VR sensor Zero-crossing.",
        source="https://www.amcarparts.co.uk/valeo/657870-crankshaft-sensor-valeo-366675-for-audi-vw-oe-07k906433b-3276423666759",
        exclude=r"(?i)(NOT\s+VR|Hall.{0,10}not.{0,10}VR|confirmed.{0,10}Hall|BGP.{0,30}wrong"
                r"|was.*VR|VR.*was|M52.*VR|VR.*M52|re-terminate|→G1|VR.*→|VR-→)",
    ),
    # CRANK_VR is valid in maxxecu-m52.wv (M52 IS a VR sensor). Only flag in 07K context.
    DenyRule(
        pattern=r"07K.{0,60}CRANK_VR|CRANK_VR.{0,60}07K",
        message="CRANK_VR connector was renamed CRANK_HALL in the 07K harness — the 07K crank sensor "
                "is Hall effect, not VR. Update any 07K-context reference to CRANK_HALL. "
                "Source: harnesses/maxxecu-07k.wv.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(renamed|was\s+CRANK_VR|OLD|replaced|M52)",
    ),
    # Crank VR- (CMC H2, pin 30) must NOT be wired as a new 07K connection.
    # Allow lines that are documenting the M52 routing in order to contrast with 07K.
    DenyRule(
        pattern=r"(?i)(07K|[Cc]rank).{0,30}CMC\s*H2|CMC\s*H2.{0,30}(07K|[Cc]rank)\b",
        message="CMC H2 (Trigger GND / VR−, pin 30) is unused for the 07K Hall crank sensor. "
                "H2 was for M52 VR−. 07K crank wires: "
                "pin16→H3(TRIGGER), pin17→G1(+5V), pin18→H1(SensorGND). "
                "Source: harnesses/maxxecu-07k.wv connections block.",
        source="harnesses/maxxecu-07k.wv",
        exclude=r"(?i)(M52\s+only|UNUSED|not\s+used|M52.*VR|VR.*M52|was.*H2|H2.*was|NOT|only.*M52"
                r"|re-terminate|G1.*\+5V|\+5V.*G1|→G1|M52:)",
    ),

    # ── PST-F1 connector pincount — 5-pin, NOT 4-pin ────────────────────────
    # Audit round 4 (2025-07): Bosch Motorsport PST-F1 datasheet confirmed 5-pin
    # Bosch Trapezoid connector (F02U.B00.751-01). Pin 1 = NC. Active pins 2-5.
    # All previous docs said 4-pin — wrong; ordering a 4-pin body mismatches sensor.
    DenyRule(
        pattern=r"(?i)PST.{0,5}F.?1.{0,20}4.pin|4.pin.{0,20}PST.{0,5}F.?1",
        message="Bosch PST-F1 uses a 5-pin Bosch Trapezoid connector (F02U.B00.751-01). "
                "Pin 1 = NC; active pins: 2=Pressure, 3=+5V, 4=GND, 5=Temp. "
                "Ordering a 4-pin body will not match the sensor physically. "
                "Source: Bosch Motorsport PST-F1 datasheet (bosch-motorsport.com); xtramotorsport.com.",
        source="https://xtramotorsport.com/product/bosch-motorsport-combined-10-bar-pressure-temp-sensor-for-oil-and-fuel/",
        exclude=r"(?i)(NOT\s+4|5.pin|5\s+pin|was.*4.pin|4.pin.*was|NOT\s+a\s+4)",
    ),

    # ── WBO2 LSU 4.9 ≠ M52 harness / Phase 1 ────────────────────────────────
    # Audit round 5 (2026-08): Phase 1 pre-terminated MaxxECU M50 harness uses
    # LSU 4.2 (verified live: maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html).
    # Phase 3 (07K) custom harness uses LSU 4.9 — a new purchase with a different pinout.
    # The two sensors and connectors are NOT interchangeable.
    DenyRule(
        pattern=r"(?i)(LSU\s*4\.9|4\.9\s*connector).{0,60}(same\s+as\s+M52|M52\s+harness|from\s+M52|carry.over)",
        message="LSU 4.9 (Phase 3 / 07K) is NOT the same as the M52 harness WBO2 connector. "
                "Phase 1 (M52) pre-terminated harness uses LSU 4.2 (verified live 2026-08-26: "
                "maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html). "
                "Phase 3 (07K) uses LSU 4.9 — different pinout, separate new purchase, new bung required. "
                "Do NOT reuse the Phase 1 connector or sensor for Phase 3.",
        source="https://www.maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html",
        exclude=r"(?i)(NOT\s+the\s+same|different\s+from|new\s+purchase|4\.2\s+not\s+4\.9|≠)",
    ),

    # ── Phase 1 pre-terminated harness — do NOT use the old 'does not use' note ──
    # Audit round 5 (2026-08): Phase 1 DOES use the pre-terminated harness.
    # The old note in MaxxECU_M50_Terminated_Harness.md has been corrected.
    # Catch any reversion to the old text.
    DenyRule(
        pattern=r"(?i)(build\s+does\s+NOT\s+use\s+the\s+pre.terminated|does\s+not\s+use\s+the\s+pre.terminated\s+harness)",
        message="Phase 1 DOES use the MaxxECU M50 pre-terminated engine harness. "
                "The old note 'This build does NOT use the pre-terminated harness' was incorrect and has been removed. "
                "Source: docs/vendor/maxxecu/MaxxECU_M50_Terminated_Harness.md (corrected 2026-08-26); "
                "E36_CSVs/E36_Phase1_Combined.csv Phase 1B ECU Wiring row.",
        source="docs/vendor/maxxecu/MaxxECU_M50_Terminated_Harness.md",
        exclude=r"(?i)(Phase\s+1\s+DOES\s+use|old\s+note|has\s+been\s+removed|corrected|was\s+incorrect)",
    ),
]

# ---------------------------------------------------------------------------
# Ground-truth signal → CMC pin mapping  (Layer 2)
# ---------------------------------------------------------------------------
# Source of truth: harnesses/maxxecu-07k.wv ECU_CMC / ECU_C2 pinlabels block.
# Each entry: signal_keyword → (row_col_label, cmc_pin_number)
# The checker below scans every "CMC pin NN" reference near the keyword and
# flags if NN does not match cmc_pin_number.
#
# How to add entries:
#   1. Confirm the pin number from maxxecu-07k.wv ECU_CMC pinlabels comments.
#   2. Add ("SIGNAL_KEYWORD", "row_col", pin_number) — keyword is case-insensitive.
#   3. Run the audit to confirm no false positives (adjust keyword if needed).
KNOWN_CMC_PINS: list[tuple[str, str, int]] = [
    # (signal_keyword, cmc_row_col, correct_cmc_pin_number)
    ("CLT",             "F1",  21),   # Coolant Temp → C1 F1
    ("IAT",             "F2",  22),   # Intake Air Temp → C1 F2
    ("WBO2 Heater",     "D1",  13),   # WBO2 Heater- → C1 D1
    ("GND Shield",      "E3",  19),   # Shield drain GND → C1 E3
    ("Sensor GND",      "H1",  29),   # Sensor GND rail → C1 H1
    ("+5V sensor",      "G1",  25),   # Shared +5V sensor supply → C1 G1
    ("MAP",             "J3",  37),   # MAP sensor AIN → C1 J3 (AIN 4)
    ("PST-F1 pressure", "J3",  37),   # PST-F1 pressure output → AIN 3 (same J3)
    ("PST-F1 temp",     "J1",  33),   # PST-F1 temp output → AIN 1 (C1 J1)
    ("AIN 1",           "J1",  33),   # AIN 1 → C1 J1
    ("AIN 2",           "J2",  34),   # AIN 2 → C1 J2
    ("AIN 3",           "J3",  37),   # AIN 3 → C1 J3
    ("AIN 4",           "J4",  38),   # AIN 4 → C1 J4
    ("TPS1",            "G2",  26),   # TPS1 / DBW TB TPS1 → C1 G2 (was M52 TPS wire)
    ("TPS2",            "J2",  34),   # TPS2 / DBW TB TPS2 → C1 J2 (AIN 2)
    ("HOME",            "H4",  32),   # Cam Hall HOME input → C1 H4
    ("Cam Hall",        "H4",  32),   # Cam Hall signal → C1 H4 (HOME)
    ("Knock 1",         "K3",  39),   # Knock sensor 1 → C1 K3 (DIN/VR1)
    ("Knock 2",         "K4",  40),   # Knock sensor 2 → C1 K4 (DIN/VR2)
    ("Flex fuel",       "C1",   9),   # Flex fuel signal → C1 row-C column-1 (DIN 3, pin 9)
    ("DIN 3",           "C1",   9),   # DIN 3 → C1 (pin 9) — flex fuel input
    ("IGN 1",           "A2",   2),   # Ignition output 1 → C1 A2
    ("IGN 2",           "A3",   3),   # Ignition output 2 → C1 A3
    ("IGN 3",           "B2",   6),   # Ignition output 3 → C1 B2
    ("IGN 4",           "B3",   7),   # Ignition output 4 → C1 B3
    ("IGN 5",           "C2",  10),   # Ignition output 5 → C1 C2
    ("INJ 1",           "K1",  45),   # Injector output 1 → C1 K1
    ("INJ 2",           "K2",  46),   # Injector output 2 → C1 K2
    ("INJ 3",           "M1",  49),   # Injector output 3 → C1 M1
    ("INJ 4",           "M2",  50),   # Injector output 4 → C1 M2
    ("INJ 5",           "M3",  51),   # Injector output 5 → C1 M3
    ("VVT solenoid",    "D4",  16),   # GPO 3 / VVT solenoid (07K) → C1 D4
    # Crank Hall signal → TRIGGER (H3, pin 31). Confirmed Audit round 4.
    # Note: M52 VR+ uses the same pin (H3/31) — same ECU destination, different sensor type.
    ("TRIGGER",         "H3",  31),   # Crank trigger signal → C1 H3 (both M52 VR+ and 07K Hall)
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
    for root in [ROOT] + EXTRA_ROOTS:
        for ext in AUDIT_EXTENSIONS:
            files.extend(root.rglob(f"*{ext}"))
    return [f for f in files if ".git" not in str(f)]


def _rel(path: Path) -> str:
    """Return path relative to the nearest known root, prefixed with repo name."""
    for root in [ROOT] + EXTRA_ROOTS:
        try:
            return f"{root.name}/{path.relative_to(root)}"
        except ValueError:
            pass
    return str(path)


def audit_file(path: Path, verbose: bool) -> list[str]:
    errors = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return [f"  [read error] {_rel(path)}: {e}"]

    rel = _rel(path)
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

    rel = _rel(path)
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


def check_wire_color_convention(path: Path) -> list[str]:
    """
    For each cable definition in a .wv file, correlate the colors: list with
    the wirelabels: list and flag wires whose color violates the build convention.

    Convention source: docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf
    (aligned build doc: docs/harness-build.md § Wire Color Convention)

      BU  — Ignition coil drive signals (IGN N)
      GY  — Injector drive signals (INJ N)
      GN  — GPO outputs (GPO N / actuator drives)
      BN  — Sensor GND; VR trigger return (Signal-); switch/paddle GND
      YE  — Shield GND drain wire
      WH  — Analog sensor signals; CAN H in WH/BU pair
      BK  — Power/chassis GND only (never sensor GND)
      RD  — +12V, +5V sensor supply

    Only checks labels that are unambiguous enough to enforce by regex.
    Excludes cables whose name contains OEM / BODY / X20 (body harness interface
    wires intentionally follow OEM colors) and PMU16_CAN (GY is CAN H there).
    """
    if path.suffix != ".wv":
        return []
    errors = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []

    rel = _rel(path)

    # Patterns for wirelabels that identify specific signal types
    _IGN_LABEL   = re.compile(r"IGN\s*\d", re.IGNORECASE)
    _INJ_LABEL   = re.compile(r"INJ\s*\d", re.IGNORECASE)
    _GPO_LABEL   = re.compile(r"GPO\s*\d", re.IGNORECASE)
    _SGND_LABEL  = re.compile(
        r"(Sensor\s*GND|SGND|Signal-|Signal\s*-|Trigger\s*GND)", re.IGNORECASE
    )
    _SHIELD_LABEL = re.compile(r"\bShield\b", re.IGNORECASE)

    # OEM-interface and PMU CAN cables are exempt from convention enforcement
    _EXEMPT_CABLE = re.compile(r"(?i)(OEM|BODY|X20|PMU.*CAN|CAN.*PMU)")

    colors_re    = re.compile(r"^\s+colors:\s*\[([^\]]+)\]")
    wirelabels_re = re.compile(r"^\s+wirelabels:\s*\[(.+)\]")
    cable_name_re = re.compile(r"^\s{2}(\w+):\s*$")  # top-level cable name

    current_cable = ""
    cable_lineno  = 0
    pending_colors: list[str] = []
    colors_lineno = 0

    def _check(cable: str, c_lineno: int, colors: list[str],
                labels: list[str], lbl_lineno: int) -> list[str]:
        if _EXEMPT_CABLE.search(cable):
            return []
        errs = []
        for i, (color, label) in enumerate(zip(colors, labels)):
            color = color.strip()
            label = label.strip().strip('"').strip("'")
            w_pos = f"wire {i+1} ({label!r})"
            loc = f"\n  {rel}:{lbl_lineno}  cable={cable}"

            if _IGN_LABEL.search(label) and color != "BU":
                errs += [loc,
                    f"  ERROR: {w_pos} — IGN drive must be BU (Blue). Got {color!r}.",
                    f"  SOURCE: docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf",
                    f"  LINE:   colors: {colors}"]
            elif _INJ_LABEL.search(label) and color != "GY":
                errs += [loc,
                    f"  ERROR: {w_pos} — INJ drive must be GY (Grey). Got {color!r}.",
                    f"  SOURCE: docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf",
                    f"  LINE:   colors: {colors}"]
            elif _GPO_LABEL.search(label) and color != "GN":
                errs += [loc,
                    f"  ERROR: {w_pos} — GPO output must be GN (Green). Got {color!r}.",
                    f"  SOURCE: docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf",
                    f"  LINE:   colors: {colors}"]
            elif _SGND_LABEL.search(label) and color != "BN":
                errs += [loc,
                    f"  ERROR: {w_pos} — Sensor GND / trigger return must be BN (Brown). Got {color!r}.",
                    f"  SOURCE: docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf",
                    f"  LINE:   colors: {colors}"]
            elif _SHIELD_LABEL.search(label) and color != "YE":
                errs += [loc,
                    f"  ERROR: {w_pos} — Shield drain wire must be YE (Yellow). Got {color!r}.",
                    f"  SOURCE: docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf",
                    f"  LINE:   colors: {colors}"]
        return errs

    for lineno, line in enumerate(lines, 1):
        # Track current top-level cable name
        m = cable_name_re.match(line)
        if m:
            current_cable = m.group(1)
            cable_lineno = lineno
            pending_colors = []
            continue

        # Capture colors list
        m = colors_re.match(line)
        if m:
            raw = m.group(1)
            pending_colors = [c.strip() for c in raw.split(",")]
            colors_lineno = lineno
            continue

        # When we hit wirelabels, run the check
        m = wirelabels_re.match(line)
        if m and pending_colors:
            raw = m.group(1)
            # Simple split on commas (labels may be quoted; strip quotes after)
            labels = [lbl.strip() for lbl in raw.split(",")]
            errors.extend(_check(
                current_cable, cable_lineno,
                pending_colors, labels, lineno
            ))
            pending_colors = []

    return errors


def check_signal_pin_references(path: Path) -> list[str]:
    """
    Layer 2 structural check: scan every line for patterns like
    "SIGNAL ... CMC pin NN" and verify NN matches KNOWN_CMC_PINS.

    This catches the class of error where a doc correctly names the signal
    but then quotes the wrong CMC pin number — the kind of error that is easy
    to introduce when copying rows from one table to another.

    Only triggers when BOTH the signal keyword AND a CMC-pin reference appear
    within 120 characters on the same line.  Pure signal mentions (no pin
    number) are ignored.  Lines that also contain NOT / wrong / correct /
    was / fix are suppressed (warning-context lines).
    """
    if path.suffix not in {".md", ".csv"}:
        return []
    errors = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []

    rel = _rel(path)
    _SUPPRESS = re.compile(r"(?i)\b(NOT|wrong|was|correct|fix|error|should be|incorrect)\b")
    _CMC_PIN  = re.compile(r"\bCMC\s+pin\s+(\d+)\b", re.IGNORECASE)

    for keyword, row_col, correct_pin in KNOWN_CMC_PINS:
        kw_re = re.compile(re.escape(keyword), re.IGNORECASE)
        for lineno, line in enumerate(lines, 1):
            if not kw_re.search(line):
                continue
            if _SUPPRESS.search(line):
                continue
            for m in _CMC_PIN.finditer(line):
                found_pin = int(m.group(1))
                if found_pin != correct_pin:
                    errors.append(f"\n  {rel}:{lineno}")
                    errors.append(
                        f"  ERROR: Signal '{keyword}' referenced with CMC pin {found_pin}, "
                        f"but KNOWN_CMC_PINS says it should be CMC {row_col} = pin {correct_pin}. "
                        f"Source: harnesses/maxxecu-07k.wv ECU_CMC pinlabels."
                    )
                    errors.append(f"  SOURCE: harnesses/maxxecu-07k.wv")
                    errors.append(f"  LINE:   {line.strip()[:140]}")
    return errors


def structural_audit_file(path: Path) -> list[str]:
    errors = []
    errors.extend(check_duplicate_pins_in_connections(path))
    errors.extend(check_wire_color_convention(path))
    errors.extend(check_signal_pin_references(path))
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
