"""
Fuel pump PWM control circuit schematic
Radium Engineering 20-1170 hanger + Walbro F90000267 + MaxxECU RACE GPO + DC SSR

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

DC SSR (Crydom D1D40 or generic 40A DC-DC SSR):
  Control input: 3-32V DC, ~10-15mA (opto-isolated)
  Load:          0-60V DC, 40A continuous, 1kHz max switching
  SSR ON when:   IGN +12V at Ctrl(+) AND MaxxECU GPO sinks Ctrl(-) to GND

MaxxECU RACE GEN1 GPO (low-drive):
  Active = sinks output to GND (not a +12V source)
  Function: PWM fuel pump control (MTune: Outputs -> Output config)
  Frequency: 100-500 Hz (within Crydom D1D40 switching rating)

Radium 20-1170 hanger terminals:
  Stainless steel stud through top plate -- ring terminals + acorn nuts
  Pump(+) stud: receives switched 12V from SSR Load(-)
  Pump(-) stud: to chassis GND (dedicated stud -- not ECU sensor ground)

How this circuit works:
  1. Key on -> IGN relay energizes -> IGN +12V reaches SSR Ctrl(+)
  2. MaxxECU boots -> outputs PWM on GPO -> GPO sinks Ctrl(-) to GND
  3. Control circuit: IGN +12V -> SSR Ctrl(+) -> internal opto LED -> Ctrl(-) -> GPO -> GND
  4. Opto triggers internal MOSFET/SCR -> SSR load circuit closes
  5. BATT+ -> 25A fuse -> SSR Load(+) -> SSR Load(-) -> pump(+) stud -> pump motor
  6. Pump(-) stud -> chassis GND completes load circuit
  7. Pump speed proportional to PWM duty cycle (65% idle / 100% WOT)
  8. Key off -> IGN relay drops -> SSR Ctrl(+) loses 12V -> SSR opens -> pump stops

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

    # ── SSR center (elm.Relay: in1/in2 = Ctrl+/Ctrl-,  a/b = Load+/Load-) ─────
    ssr = d.add(elm.Relay(switch='spst').at((4.5, 0)).label(
        "DC SSR (Crydom D1D40)\n40A / 0-60V / 3-32V ctrl", loc="top"))

    # ── Control circuit (left): IGN +12V -> Ctrl(+) / GPO -> Ctrl(-) -> GND ───
    d.add(elm.Line().left().at(ssr.in1).length(2.0))
    d.add(elm.Line().up().length(0.6))
    d.add(elm.Label().label("IGN +12V / F4 (5A) / 22 AWG", loc="right"))

    d.add(elm.Line().left().at(ssr.in2).length(2.0))
    d.add(elm.Dot())
    d.add(elm.Line().down().length(0.4))
    d.add(elm.Label().label(
        "MaxxECU GPO (GND-sink)\nPWM 100-500 Hz / 22 AWG shielded", loc="right"))


    # ── Load circuit (top): BATT+ -> 25A fuse -> Load(+) -> Load(-) -> pump ───
    d.add(elm.Line().up().at(ssr.a).length(1.5))
    d.add(elm.Line().left().length(0.6))
    d.add(elm.Fuse().left().label("F_FP 25A / within 12\" batt", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT / 12 AWG", loc="right"))

    d.add(elm.Line().down().at(batt_node.end).length(3.8))
    d.add(elm.Ground())

    # ── Load output (right): Load(-) -> pump(+) stud -> motor -> GND ─────────
    d.add(elm.Line().right().at(ssr.b).length(0.5))
    d.add(elm.Motor().right().label(
        "Walbro F90000267 (Radium 20-1170)\n465 LPH / E85 / 14.1A max / 12 AWG", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    # ── Duty cycle note (bottom) ─────────────────────────────────────────────
    d.add(elm.Label().at((5.0, -4.2)).label(
        "PWM duty: 65% idle | 80% cruise | 90% WOT | 100% under boost\n"
        "SSR: mount to metal bracket for heat sinking (dissipates ~1 W/A)\n"
        "Return: 8.5 mm barb (included) or 20-1000-0606 6AN ORB swivel",
        loc="center"))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/fuel-pump-pwm.svg")
