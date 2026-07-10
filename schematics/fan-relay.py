"""
Fan relay circuit schematic — RELAY_FAN from power-distribution.wv

This script generates a circuit schematic using schemdraw.
Run it to produce fan-relay.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic).
The WireViz file (power-distribution.wv) shows WHERE each wire terminates.
You need both to build and troubleshoot the circuit.

Standard Bosch ISO mini relay pin numbers (printed on the relay body):
  85  coil negative  — MaxxECU GPO 6 pulls this to GND to activate relay
  86  coil positive  — IGN +12V (key-on), fused at 5A
  30  common         — BATT+ (always-on), fused at 20A
  87  normally open  — output to fan motor when relay is ON
  87a normally closed — output when relay is OFF (not used here)

How this relay works:
  1. Turn the key on → IGN +12V flows through F3 fuse → reaches coil pin 86
  2. When coolant temp threshold is hit, MaxxECU activates GPO 6
  3. GPO 6 pulls coil pin 85 to GND → completes the coil circuit → coil energizes
  4. Magnetic field closes the contact → pin 30 connects to pin 87
  5. BATT+ flows from F6 fuse → pin 30 → pin 87 → fan motor → GND
  6. Fan spins. When ECU deactivates GPO 6, coil de-energizes, contact opens, fan stops.

To create a schematic for a different circuit:
  - Copy this file and rename it
  - Change the elements and connections to match your circuit
  - See https://schemdraw.readthedocs.io for all available elements
  - Common elements: elm.Relay, elm.Fuse, elm.Motor, elm.Battery,
                     elm.Switch, elm.Resistor, elm.Capacitor, elm.Diode

Usage:
  pip install schemdraw matplotlib
  python3 schematics/fan-relay.py
  open schematics/fan-relay.svg
"""

import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')  # non-interactive backend — no display window needed
import os

OUT = os.path.join(os.path.dirname(__file__), "fan-relay.svg")

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=10.5)

    # ── Place the relay in the center of the diagram ─────────────────────────
    # elm.Relay draws the coil (left side) and the switch contact (right side)
    # with a dotted link showing they are mechanically coupled.
    relay = d.add(elm.Relay(switch='spst').at((4, 0)).label("RELAY_FAN\n(Bosch ISO mini)", loc="top"))

    # ── COIL CIRCUIT ─────────────────────────────────────────────────────────
    # IGN +12V → F3 fuse (5A) → relay pin 86 (coil+)
    d.add(elm.Line().left().at(relay.in1).length(1.5))
    d.add(elm.Fuse().left().label("F3 — 5A\n(IGN rail)", loc="top"))
    d.add(elm.Line().left().length(0.8))
    ign_node = d.add(elm.Dot())
    d.add(elm.Line().up().length(0.6))
    d.add(elm.Label().label("IGN +12V", loc="right"))

    # Relay pin 85 (coil-) → MaxxECU GPO 6 switch → GND
    # The switch symbol represents the ECU's internal transistor (low-side switch)
    d.add(elm.Line().left().at(relay.in2).length(1.0))
    d.add(elm.Switch().left().label("MaxxECU\nGPO 6", loc="bottom"))
    d.add(elm.Line().left().length(0.3))
    d.add(elm.Ground())

    # Pin labels on relay coil terminals
    d.add(elm.Label().at(relay.in1).label("  86", loc="right"))
    d.add(elm.Label().at(relay.in2).label("  85", loc="right"))

    # ── LOAD CIRCUIT ──────────────────────────────────────────────────────────
    # BATT+ → ANL fuse → F6 fuse (20A) → relay pin 30 → contact → pin 87 → fan → GND
    d.add(elm.Line().up().at(relay.a).length(1.4))
    d.add(elm.Line().left().length(0.6))
    d.add(elm.Fuse().left().label("F6 — 20A\n(batt rail)", loc="top"))
    d.add(elm.Line().left().length(0.6))
    batt_top_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT", loc="right"))
    batt_pos_top = d.add(elm.Dot())
    d.add(elm.Label().label("  ← main ANL fuse (close to batt)", loc="right"))

    # Battery negative → GND
    d.add(elm.Line().down().at(batt_top_node.end).length(3.6))
    d.add(elm.Ground())

    # Relay contact output: pin 87 → fan motor → GND
    d.add(elm.Line().right().at(relay.b).length(0.8))
    d.add(elm.Motor().right().label("SPAL Fan\nMotor", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    # Pin labels on relay contact
    d.add(elm.Label().at(relay.a).label("  30", loc="left"))
    d.add(elm.Label().at(relay.b).label("  87", loc="left"))

    # ── Explanation note at bottom ───────────────────────────────────────────
    d.add(elm.Label().at((4.5, -3.2)).label(
        "Coil circuit (left):  IGN on + ECU activates GPO 6 → coil energizes\n"
        "Load circuit (right): Contact closes → BATT+ reaches fan motor",
        loc="center"
    ))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/fan-relay.svg")
