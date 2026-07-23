"""
EWP controller circuit schematic
Davies Craig Digital Controller (#8002 LCD) + EWP150 (40 LPM)

This script generates a circuit schematic using schemdraw.
Run it to produce ewp-controller.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic).
The WireViz file (harnesses/ewp-controller.wv) shows WHERE each wire terminates.
You need both to build and troubleshoot the circuit.

Davies Craig controller wire colors:
  RED         always-on BATT+ (controller internal power + post-shutdown run-on)
  BROWN       chassis earth
  GREEN       ignition sense +12V (relay output ONLY -- see warning below)
  GREEN/BLK   fan relay pin 85 output (controller earths pin 85)
  BLUE        pump motor + (PWM variable voltage -- speed control)
  BLACK       pump motor GND

CRITICAL WIRING WARNING:
  The GREEN ignition wire is a sense input only -- it does NOT power the pump.
  The pump is powered from BATT+ (RED, always-on) through the controller.
  GREEN must connect to a RELAY pin 87 output providing clean switched +12V.
  DO NOT connect GREEN to the MaxxECU or ignition coil circuit.
  Davies Craig explicitly warns this can cause controller malfunction or ECU damage.

How this circuit works:
  1. Key on -> IGN relay energizes -> pin 87 output goes to +12V
  2. GREEN wire goes high -> controller wakes up and begins monitoring CLT sensor
  3. Controller reads NTC thermistor in upper/hot-side hose
  4. Controller PWMs voltage on BLUE wire to pump motor, adjusting speed with temp
  5. Key off -> GREEN goes low -> controller detects shutdown
  6. Controller continues running pump from BATT+ (RED, always-on) until CLT
     drops 10C below setpoint OR 3 minutes elapse -- whichever comes first
  7. Post-shutdown run-on eliminates turbo heat soak without MaxxECU power latch

MaxxECU integration:
  - MaxxECU uses a SEPARATE NTC sensor in its own coolant port (BBG rear flange)
  - No shared sensors between MaxxECU and Davies Craig controller
  - MaxxECU does not command the EWP -- controller is the sole PWM driver
  - EWP150 has no external signal input for ECU override

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

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=10.5)

    # ── BATT+ always-on power: BATT+ -> 10A fuse -> controller RED ───────────
    # Draw left to right across the top
    batt = d.add(elm.Battery().at((0, 4)).right().reverse().label("12V BATT+\n(always-on)", loc="top"))
    d.add(elm.Line().right().length(0.4))
    d.add(elm.Fuse().right().label("F_EWP_PWR\n10A", loc="top"))
    d.add(elm.Line().right().length(0.4))
    pwr_in = d.add(elm.Dot())
    d.add(elm.Label().label("  RED", loc="right"))

    # Battery negative bus -- drop down from battery left terminal
    d.add(elm.Line().down().at(batt.start).length(4.5))
    batt_gnd = d.add(elm.Ground())

    # ── IGN sense input: IGN relay pin 87 -> 7.5A fuse -> controller GREEN ───
    # Below the BATT+ circuit; IGN does NOT power the pump -- sense input only
    d.add(elm.Line().at((0, 2.2)).right().length(0.3))
    d.add(elm.Fuse().right().label("F_EWP_IGN\n7.5A", loc="top"))
    d.add(elm.Line().right().length(0.4))
    ign_in = d.add(elm.Dot())
    d.add(elm.Label().label("  GREEN (IGN sense)", loc="right"))

    # IGN source label at left
    d.add(elm.Label().at((0, 2.2)).label("IGN relay pin 87", loc="left"))

    # Warning annotation below IGN line
    d.add(elm.Label().at((2.2, 1.6)).label(
        "!! relay pin 87 output ONLY --\nNOT MaxxECU, NOT coil circuit !!",
        loc="center"
    ))

    # ── Controller BROWN -> chassis GND ──────────────────────────────────────
    # Branch downward from the controller side
    d.add(elm.Line().at((5.2, 0.8)).down().length(0.6))
    d.add(elm.Ground())
    d.add(elm.Label().at((5.2, 0.8)).label("BROWN  ", loc="right"))
    ctrl_gnd = d.add(elm.Dot().at((5.2, 0.8)))

    # ── Controller vertical bus (left edge of controller region) ──────────────
    # Vertical line connecting pwr_in (top) down through ign_in to ctrl_gnd
    # This represents the controller's left terminal cluster
    d.add(elm.Line().at(pwr_in.end).down().length(3.2))

    # Connect ign_in into this vertical bus
    d.add(elm.Line().at(ign_in.end).right().length(0.3))
    ctrl_ign_join = d.add(elm.Dot())

    # ── Controller output -> EWP150 pump motor ────────────────────────────────
    # From the controller right side, draw pump output circuit
    ctrl_out_y = 2.8
    d.add(elm.Line().at((5.5, ctrl_out_y)).right().length(0.5))
    d.add(elm.Label().at((5.5, ctrl_out_y)).label("BLUE (PWM)", loc="top"))
    d.add(elm.Motor().right().label("EWP150\n40 LPM", loc="top"))
    d.add(elm.Line().right().length(0.4))
    d.add(elm.Ground())

    # BLACK return label (below motor)
    d.add(elm.Label().at((7.2, 2.4)).label("BLACK (motor GND)", loc="center"))

    # Controller right-side annotation
    d.add(elm.Label().at((5.5, ctrl_out_y)).label("  controller varies\n  voltage for speed", loc="bottom"))

    # ── NTC thermistor sensor circuit ─────────────────────────────────────────
    # Thermistor in upper/hot-side hose -> controller sensor input
    # Draw from left, terminating at controller sensor input node
    d.add(elm.Resistor().at((1.2, -0.8)).right().label("NTC thermistor\n(upper hose -- engine exit,\npre-radiator)", loc="top"))
    d.add(elm.Line().right().length(0.4))
    sensor_in = d.add(elm.Dot())
    d.add(elm.Label().label("  SENSOR", loc="right"))

    # Thermistor other end -> GND (sensor return)
    d.add(elm.Line().down().at((1.2, -0.8)).length(0.6))
    d.add(elm.Ground())

    # ── Controller box label (center of diagram) ──────────────────────────────
    d.add(elm.Label().at((5.0, 3.8)).label(
        "Davies Craig Digital\nController (#8002 LCD)\n-- mounted in cabin --",
        loc="center"
    ))

    # ── Explanation note at bottom ────────────────────────────────────────────
    d.add(elm.Label().at((3.5, -2.2)).label(
        "Power: pump runs from BATT+ (RED, always-on) -- IGN is sense input only, does not power pump\n"
        "Post-shutdown: controller runs pump after key-off until CLT drops 10C below setpoint or 3 min\n"
        "MaxxECU: separate NTC in own coolant port -- no shared sensors, no MaxxECU pump command",
        loc="center"
    ))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/ewp-controller.svg")
