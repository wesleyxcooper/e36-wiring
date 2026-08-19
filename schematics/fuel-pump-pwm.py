"""
Fuel pump PWM control circuit schematic
Radium Engineering 20-1170 hanger + Walbro F90000267 + Ecumaster PMU16 O4 PWM direct

This script generates a circuit schematic using schemdraw.
Run it to produce fuel-pump-pwm.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic).
The WireViz file (harnesses/fuel-pump-hanger.wv) shows WHERE each wire terminates.
You need both to build and troubleshoot the circuit.

F90000267 specs:
  465 LPH @ 40 PSI @ 13.5V
  14.1A max draw at 13.5V
  39mm upper body / 50mm lower body (DCSS format -- Radium 20-1170 compatible)
  E85 / gasoline rated

Ecumaster PMU16 Output O4 (PHYS pin 13):
  High-side MOSFET switch, 25A rated, PWM-capable
  No separate SSR or relay needed -- PMU16 output drives pump load directly
  PWM commanded by MaxxECU over CAN (load MaxxECU.canx template in PMU software)
  Output active when PMU16 receives CAN fuel pump duty command from MaxxECU

Radium 20-1170 hanger terminals:
  Stainless steel stud through top plate -- ring terminals + acorn nuts
  Pump(+) stud: receives switched 12V from PMU16 O4 output
  Pump(-) stud: to chassis GND (dedicated stud -- not ECU sensor ground)

How this circuit works:
  1. Key on -> PMU16 sees IGN +12V on +12V SW pin -> PMU16 activates
  2. MaxxECU boots -> sends fuel pump PWM duty over CAN to PMU16
  3. PMU16 O4 MOSFET switches at commanded duty cycle
  4. BATT+ -> main ANL fuse -> PMU16 M6 stud -> O4 MOSFET -> O4 output
  5. O4 output -> pump(+) stud -> pump motor -> pump(-) stud -> chassis GND
  6. Pump speed proportional to CAN-commanded PWM duty
  7. Key off -> MaxxECU signals PMU16 -> PMU16 deactivates O4 -> pump stops

PMU16 O4 replaces: Crydom D1D40 DC SSR + IGN fuse feed + GPO2 trigger wire

NOTE: fuel-pump-hanger.wv still models the full Crydom D1D40 SSR
architecture (DC_SSR connector, CABLE_SSR_CTRL_POS/NEG, MAXXECU_GPO
stub, IGN_12V feed) and needs a rewrite for PMU16 O4 direct output.
ewp-controller.wv has no SSR — it uses a MAIN_RELAY; that relay will
eventually be replaced by PMU16 O5, tracked in power-distribution.wv.

Usage:
  pip install schemdraw matplotlib
  python3 schematics/fuel-pump-pwm.py
  open schematics/fuel-pump-pwm.svg
"""

import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')  # non-interactive backend -- no display window needed
import os

OUT = os.path.join(os.path.dirname(__file__), "fuel-pump-pwm.svg")

with schemdraw.Drawing(figsize=(13, 8), show=False) as d:
    d.config(fontsize=9)

    # ── PMU16 O4 MOSFET switch (center) ─────────────────────────────────────
    # Model as a switch: top = load in (from BATT+), bottom = load out (to pump)
    # CAN command shown on left as the control signal
    pmu = d.add(elm.Switch().right().at((4.0, 0)).label(
        "PMU16 O4\n(MOSFET, 25A, PWM)\nPHYS pin 13", loc="top"))

    # ── CAN control signal (below) ──────────────────────────────────────────
    d.add(elm.Line().down().at(pmu.start).length(1.2))
    d.add(elm.Label().label(
        "MaxxECU CAN → PMU16\nPWM duty command\n(replaces GPO2 + SSR ctrl wires)",
        loc="right"))

    # ── Load circuit: BATT+ → ANL fuse → PMU16 M6 stud → O4 → pump ─────────
    d.add(elm.Line().left().at(pmu.start).length(0.6))
    d.add(elm.Fuse().left().label("ANL main fuse\n(within 18\" batt)", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT+\n(PMU16 M6 stud)\n12 AWG", loc="right"))

    d.add(elm.Line().down().at(batt_node.end).length(3.8))
    d.add(elm.Ground())

    # ── Output (right): O4 → pump(+) stud → motor → pump(-) stud → GND ────
    d.add(elm.Line().right().at(pmu.end).length(0.5))
    d.add(elm.Motor().right().label(
        "Walbro F90000267 (Radium 20-1170)\n465 LPH / E85 / 14.1A max / 12 AWG", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    # ── Duty cycle and PMU16 note (bottom) ──────────────────────────────────
    d.add(elm.Label().at((5.0, -4.5)).label(
        "PWM duty via CAN: 65% idle | 80% cruise | 90% WOT | 100% under boost\n"
        "PMU16 O4 logs actual current per channel -- anomaly detection built in\n"
        "Replaces: Crydom D1D40 SSR + F4 IGN fuse + GPO2 trigger wire (3 parts → 0)",
        loc="center"))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/fuel-pump-pwm.svg")
