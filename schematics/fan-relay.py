"""
Fan circuit schematic — PMU16 O3 direct PWM output from power-distribution.wv

This script generates a circuit schematic using schemdraw.
Run it to produce fan-relay.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic).
The WireViz file (power-distribution.wv) shows WHERE each wire terminates.
You need both to build and troubleshoot the circuit.

NOTE: The mechanical relay (RELAY_FAN) has been removed from this build.
The Ecumaster PMU16 output O3 drives the SPAL fan directly with a
high-side MOSFET switch. PWM speed control is available on O3 for use
with a PWM-capable SPAL fan (future upgrade -- no rewiring needed).

Ecumaster PMU16 Output O3 (PHYS pin 26):
  High-side MOSFET switch, 25A rated, PWM-capable
  Activated by MaxxECU CAN fan control command
  Phase 2 upgrade: wire SPAL PWM-capable fan to O3 -- enable variable
    speed control in PMU software (no hardware change needed)

Condenser fan (O6) is a separate PMU16 output -- activated by
MaxxECU CAN AC-on signal, not hardwired to the AC switch output.

How this circuit works:
  1. Key on -> PMU16 sees IGN +12V on +12V SW pin -> PMU16 activates
  2. MaxxECU monitors CLT and sends fan enable/duty CAN command to PMU16
  3. PMU16 O3 MOSFET closes -> BATT+ flows through O3 to fan motor
  4. Fan runs. When MaxxECU deactivates, O3 opens, fan stops.
  5. Phase 2: MaxxECU sends PWM duty command over CAN -> O3 PWMs fan speed

PMU16 O3 replaces: RELAY_FAN (Bosch ISO mini) + F3 coil fuse +
  F6 load fuse + GPO6 trigger wire (Bosch relay + 4 wires -> 1 output)

Usage:
  pip install schemdraw matplotlib
  python3 schematics/fan-relay.py
  open schematics/fan-relay.svg
"""

import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')  # non-interactive backend -- no display window needed
import os

OUT = os.path.join(os.path.dirname(__file__), "fan-relay.svg")

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=10.5)

    # ── PMU16 O3 MOSFET switch (center) ─────────────────────────────────────
    # Model as a switch: left = load in (from BATT+), right = load out (to fan)
    pmu = d.add(elm.Switch().right().at((4, 0)).label(
        "PMU16 O3\n(MOSFET, 25A, PWM-capable)\nPHYS pin 26", loc="top"))

    # ── CAN control signal (below) ──────────────────────────────────────────
    d.add(elm.Line().down().at(pmu.start).length(1.2))
    d.add(elm.Label().label(
        "MaxxECU CAN → PMU16\nfan enable / PWM duty command\n(replaces GPO6 + relay coil wires)",
        loc="right"))

    # ── Load circuit: BATT+ → ANL fuse → PMU16 M6 stud → O3 → fan ──────────
    d.add(elm.Line().left().at(pmu.start).length(0.6))
    d.add(elm.Fuse().left().label("ANL main fuse\n(within 18\" batt)", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT+\n(PMU16 M6 stud)\n12 AWG", loc="right"))

    # Battery negative → GND
    d.add(elm.Line().down().at(batt_node.end).length(3.6))
    d.add(elm.Ground())

    # ── Output (right): O3 → fan motor → GND ────────────────────────────────
    d.add(elm.Line().right().at(pmu.end).length(0.8))
    d.add(elm.Motor().right().label("SPAL Fan Motor\n(Phase 2: PWM-capable model)", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    # ── Explanation note at bottom ───────────────────────────────────────────
    d.add(elm.Label().at((4.5, -3.4)).label(
        "PMU16 O3 logs actual fan current -- stall detection built in\n"
        "Replaces: RELAY_FAN (Bosch ISO) + F3 coil fuse + F6 load fuse + GPO6 trigger wire\n"
        "Condenser fan: separate PMU16 O6 output, CAN-commanded when AC on",
        loc="center"
    ))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/fan-relay.svg")
