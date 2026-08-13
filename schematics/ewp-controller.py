"""
CWA400 electric water pump circuit schematic
Pierburg CWA400 (PWM version) + MaxxECU RACE GPO control

This script generates a circuit schematic using schemdraw.
Run it to produce ewp-controller.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic).
The WireViz file (harnesses/ewp-controller.wv) shows WHERE each wire terminates.
You need both to build and troubleshoot the circuit.

CWA400 connector pinout (Kostal 2+2):
  Pin 1  PWM signal in  (MaxxECU GPO, 22 AWG shielded)
  Pin 2  BSD diagnostic (leave floating -- not used with MaxxECU)
  Pin 3  +12V power     (from 40A relay, 10 AWG)
  Pin 4  GND            (chassis ground, 10 AWG)

Standard Bosch ISO mini relay pin numbers:
  85  coil negative  -- chassis GND
  86  coil positive  -- BATT+ (always-on, fuse F9 5A -- MUST be BATT+ for post-shutdown cooling)
  30  common         -- BATT+ (always-on), fused at 40A
  87  normally open  -- output to CWA400 Pin 3 when relay is ON

How this circuit works:
  1. BATT+ always present on relay coil pin 86 (via fuse F9 -- NOT IGN switched)
  2. Coil pin 85 is at GND -> coil circuit complete -> relay energizes
  3. Relay contact closes -> pin 30 connects to pin 87 -> CWA400 Pin 3 gets +12V
  4. MaxxECU boots -> sends >=3ms high pulse on GPO -> CWA400 wakes from standby
  5. MaxxECU reads CLT -> outputs PWM at 680 Hz on GPO -> CWA400 adjusts speed
     (duty cycle map: 20% at 60C / 55% at 85C / 97% at 105C)
  6. Key off -> relay de-energizes -> Pin 3 loses power... BUT:
  7. MaxxECU power hold relay keeps ECU alive after key-off
  8. MaxxECU continues commanding pump via GPO until CLT < 70C
  9. Once CLT < 70C, MaxxECU releases power hold relay -> pump stops

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

with schemdraw.Drawing(figsize=(13, 8), show=False) as d:
    d.config(fontsize=9)

    # ── Relay center ──────────────────────────────────────────────────────────
    relay = d.add(elm.Relay(switch='spst').at((4.5, 0)).label(
        "MAIN_RELAY\n40A Bosch ISO mini", loc="top"))

    # ── Coil circuit (left): BATT+ -> 86 -> coil -> 85 -> GND (relay always energized) ─
    d.add(elm.Line().left().at(relay.in1).length(2.0))
    d.add(elm.Line().up().length(0.6))
    d.add(elm.Label().label("BATT+ / F9 (5A)\n(not IGN -- post-shutdown cooling)", loc="right"))

    d.add(elm.Line().left().at(relay.in2).length(2.0))
    d.add(elm.Ground())

    d.add(elm.Label().at(relay.in1).label("86 ", loc="left"))
    d.add(elm.Label().at(relay.in2).label("85 ", loc="left"))

    # ── Load circuit (top): BATT+ -> 40A fuse -> relay 30 -> 87 -> CWA400 ────
    d.add(elm.Line().up().at(relay.a).length(1.5))
    d.add(elm.Line().left().length(0.6))
    d.add(elm.Fuse().left().label("F_CWA 40A", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT / 10 AWG", loc="right"))

    d.add(elm.Line().down().at(batt_node.end).length(3.8))
    d.add(elm.Ground())

    # ── Load output (right): relay 87 -> CWA400 Pin 3 -> motor -> GND ────────
    d.add(elm.Line().right().at(relay.b).length(0.5))
    d.add(elm.Motor().right().label(
        "CWA400 (Pierburg 7.07223.10.0)\nPin 3 +12V / Pin 4 GND / 10 AWG", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    d.add(elm.Label().at(relay.a).label("30 ", loc="left"))
    d.add(elm.Label().at(relay.b).label("87 ", loc="left"))

    # ── PWM signal: MaxxECU GPO -> CWA400 Pin 1 (680 Hz) ────────────────────
    pwm_y = -2.2
    d.add(elm.Line().at((2.0, pwm_y)).right().length(5.0))
    d.add(elm.Label().label(
        "CWA400 Pin 1 (PWM in)\n680 Hz | 13-85% speed | 86-97% full\nPin 2 BSD: leave floating",
        loc="right"))
    d.add(elm.Label().at((2.0, pwm_y)).label(
        "MaxxECU GPO\n22 AWG shielded\n(drain at ECU end)", loc="left"))

    # ── Key note (bottom) ─────────────────────────────────────────────────────
    d.add(elm.Label().at((5.0, -4.5)).label(
        "Post-shutdown: MaxxECU power-hold keeps ECU alive -- GPO commands pump until CLT < 70C\n"
        "Wake pulse: >=3 ms high at key-on before CLT duty map\n"
        "VERSION: PWM only (pre-Mar 2024) -- NOT the LIN version (Pierburg 7.03665.66.0)",
        loc="center"))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/ewp-controller.svg")
