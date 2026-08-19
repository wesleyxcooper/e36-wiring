"""
CWA400 electric water pump circuit schematic
Pierburg CWA400 (PWM version) + Ecumaster PMU16 O5+O14 parallel + MaxxECU GPO

This script generates a circuit schematic using schemdraw.
Run it to produce ewp-controller.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic).
The WireViz file (harnesses/ewp-controller.wv) shows WHERE each wire terminates.
You need both to build and troubleshoot the circuit.

CWA400 connector pinout (Kostal 2+2):
  Pin 1  PWM signal in  (MaxxECU GPO, 22 AWG shielded)
  Pin 2  BSD diagnostic (leave floating -- not used with MaxxECU)
  Pin 3  +12V power     (from PMU16 O5+O14 parallel, 8 AWG each)
  Pin 4  GND            (chassis ground, 10 AWG)

Ecumaster PMU16 O5 + O14 (parallel):
  Both outputs are high-side MOSFET switches, 25A each, combined 50A
  Configured as a parallel pair in PMU software
  PMU16 M6 stud is BATT+ always-on -- O5+O14 can activate post key-off
  Post-shutdown cooling: PMU16 keeps O5+O14 active after key-off until
    MaxxECU CAN CLT channel drops below 70C OR 3-min fallback timer
  No separate BATT+ relay or MaxxECU power-hold relay needed

Replaces: MAIN_RELAY (Bosch 40A) + BATT+ fuse feed + relay coil wires

Version warning:
  PWM version ONLY: Pierburg 7.07223.10.0 / BMW 11515A05704 / 11517563659
  LIN version (NOT compatible): Pierburg 7.03665.66.0 / BMW 11517604027
  Post-March 2024 production = LIN bus only -- verify part number before sourcing.

Usage:
  pip install schemdraw matplotlib
  python3 schematics/ewp-controller.py
  open schematics/ewp-controller.svg
"""

import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')  # non-interactive backend -- no display window needed
import os

OUT = os.path.join(os.path.dirname(__file__), "ewp-controller.svg")

with schemdraw.Drawing(figsize=(14, 9), show=False) as d:
    d.config(fontsize=9)

    # ── PMU16 O5 MOSFET switch (left of center) ─────────────────────────────
    sw_o5 = d.add(elm.Switch().right().at((3.0, 1.0)).label(
        "PMU16 O5\n(MOSFET 25A)\nPHYS pin 12", loc="top"))

    # ── PMU16 O14 MOSFET switch (right of center, parallel) ─────────────────
    sw_o14 = d.add(elm.Switch().right().at((3.0, -0.8)).label(
        "PMU16 O14\n(MOSFET 25A)\nPHYS pin TBD", loc="bottom"))

    # ── CAN control (below both) ─────────────────────────────────────────────
    d.add(elm.Line().down().at(sw_o5.start).length(0.6))
    d.add(elm.Label().label(
        "MaxxECU CAN → PMU16\nO5+O14 parallel enable\n(post-shutdown: active until CLT < 70C)",
        loc="right"))

    # ── Shared BATT+ feed (left side, feeds both switch inputs) ─────────────
    d.add(elm.Line().left().at(sw_o5.start).length(0.5))
    batt_join_top = d.add(elm.Dot())
    d.add(elm.Line().left().at(sw_o14.start).length(0.5))
    batt_join_bot = d.add(elm.Dot())
    # vertical line joining both input nodes
    d.add(elm.Line().up().at(batt_join_bot.end).toy(batt_join_top.end))

    # Battery + fuse feeding the join
    d.add(elm.Line().left().at(batt_join_top.end).length(0.6))
    d.add(elm.Fuse().left().label("ANL fuse\n(PMU16 M6 stud)", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.0))
    d.add(elm.Battery().up().reverse().label("12V BATT+\n(PMU16 M6)\n4 AWG", loc="right"))

    # Battery GND
    d.add(elm.Line().down().at(batt_node.end).length(3.8))
    d.add(elm.Ground())

    # ── Parallel outputs join then go to pump Pin 3 ──────────────────────────
    d.add(elm.Line().right().at(sw_o5.end).length(0.5))
    out_top = d.add(elm.Dot())
    d.add(elm.Line().right().at(sw_o14.end).length(0.5))
    out_bot = d.add(elm.Dot())
    # vertical join
    d.add(elm.Line().up().at(out_bot.end).toy(out_top.end))
    # combined run to pump
    d.add(elm.Line().right().at(out_top.end).length(0.5))
    d.add(elm.Motor().right().label(
        "CWA400 Pin 3\n(+12V supply)\n8 AWG ea", loc="top"))
    pump_top = d.add(elm.Dot())
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    # ── PWM signal: MaxxECU GPO → CWA400 Pin 1 ───────────────────────────────
    d.add(elm.Line().down().at(pump_top.end).length(1.2))
    pwm_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(0.5))
    d.add(elm.Label().label("MaxxECU GPO\n680 Hz PWM\n22 AWG shielded", loc="left"))
    d.add(elm.Line().right().at(pwm_node.end).length(0.5))
    d.add(elm.Label().label("CWA400 Pin 1\n(PWM signal in)", loc="right"))

    # ── Notes ────────────────────────────────────────────────────────────────
    d.add(elm.Label().at((5.5, -4.8)).label(
        "O5+O14 combined: 50A -- adequate for CWA400 35.5A nominal\n"
        "Configure as parallel pair in PMU software (both same channel group)\n"
        "Replaces: MAIN_RELAY 40A + BATT+ fuse feed + power-hold relay (3 parts → 0)",
        loc="center"))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/ewp-controller.svg")
