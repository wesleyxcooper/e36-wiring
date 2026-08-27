"""
BMW E46 DBW accelerator pedal dual-track hall-effect sensor schematic
PN 35426786282 (manual) / 35426786281 (auto) wired to MaxxECU RACE

This schematic shows HOW the dual-track sensor circuit works.
See harnesses/epedal-bmw-e46.wv for WHERE each wire terminates.

E46 pedal connector pin assignment (bench-verified, HP Academy + openinverter.org):
  Pin 1  GND 1     sensor ground, track 1
  Pin 2  GND 2     sensor ground, track 2
  Pin 3  VCC 2     +5V sensor supply, track 2
  Pin 4  APS1 out  track 1 signal  (0.70V idle, 4.50V WOT)
  Pin 5  VCC 1     +5V sensor supply, track 1
  Pin 6  APS2 out  track 2 signal  (0.36V idle, 2.20V WOT)

How this circuit works:
  1. MaxxECU provides two independent +5V sensor supplies (SENS1, SENS2)
  2. Each supply feeds one half of the dual-track hall-effect pedal assembly
  3. As pedal angle increases, Hall IC output voltage rises proportionally
  4. Track 1 (APS1): 0.70V at idle, 4.50V at WOT -- commands e-throttle
  5. Track 2 (APS2): 0.36V at idle, 2.20V at WOT -- redundant safety track
  6. MaxxECU continuously cross-checks APS1:APS2 ratio at all times
  7. If ratio exceeds tolerance (sensor fault), MaxxECU cuts TB motor output
  8. Each track has its own independent ground to prevent common-mode fault
  Total draw: ~20 mA. 24 AWG shielded cable, drain at MaxxECU end only.

For the Hella 6PV010946-141 fallback option, see harnesses/epedal-hella-6pv.wv.
For PID tuning procedure after wiring, see docs/etb-pid-tuning.md.

Usage:
  pip install schemdraw matplotlib
  python3 schematics/epedal-dbw.py
  open schematics/epedal-dbw.svg
"""

import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')  # non-interactive backend -- no display window needed
import os

OUT = os.path.join(os.path.dirname(__file__), "epedal-dbw.svg")

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=10.5)

    # ── E46 Pedal Module (IC block) ──────────────────────────────────────────
    # Left side pins: power and ground inputs from MaxxECU
    # Right side pins: analog signal outputs to MaxxECU AIN
    pedal = d.add(elm.Ic(pins=[
        elm.IcPin(name='VCC1', side='left',  pin='5', rotation=0),
        elm.IcPin(name='VCC2', side='left',  pin='3', rotation=0),
        elm.IcPin(name='GND1', side='left',  pin='1', rotation=0),
        elm.IcPin(name='GND2', side='left',  pin='2', rotation=0),
        elm.IcPin(name='APS1', side='right', pin='4', rotation=0),
        elm.IcPin(name='APS2', side='right', pin='6', rotation=0),
    ], edgepadW=0.6, edgepadH=0.6, pinspacing=1.2).at((6, 0)).anchor('center').label(
        'E46 Pedal\n35426786282\nDual Hall-Effect', loc='center'))

    # ── Left side: power and ground connections from MaxxECU ─────────────────

    # VCC1 (Pin 5): MaxxECU +5V SENS1 -> pedal supply, track 1
    d.add(elm.Line().left().at(pedal.VCC1).length(5.5))
    d.add(elm.Label().label('+5V SENS 1\n(MaxxECU RACE)', loc='left'))

    # VCC2 (Pin 3): MaxxECU +5V SENS2 -> pedal supply, track 2
    d.add(elm.Line().left().at(pedal.VCC2).length(5.5))
    d.add(elm.Label().label('+5V SENS 2\n(MaxxECU RACE)', loc='left'))

    # GND1 (Pin 1): MaxxECU sensor GND, track 1
    d.add(elm.Line().left().at(pedal.GND1).length(4.0))
    d.add(elm.Ground())
    d.add(elm.Label().at(pedal.GND1).label('SGND 1 (MaxxECU)', loc='bottom'))

    # GND2 (Pin 2): MaxxECU sensor GND, track 2
    d.add(elm.Line().left().at(pedal.GND2).length(4.0))
    d.add(elm.Ground())
    d.add(elm.Label().at(pedal.GND2).label('SGND 2 (MaxxECU)', loc='bottom'))

    # ── Right side: analog signal outputs to MaxxECU AIN ─────────────────────

    # APS1 (Pin 4): track 1 output -> MaxxECU AIN x
    d.add(elm.Line().right().at(pedal.APS1).length(4.5))
    d.add(elm.Label().label(
        'AIN x -- APS1\n0.70 V idle  /  4.50 V WOT\n(MaxxECU RACE)',
        loc='right'))

    # APS2 (Pin 6): track 2 output -> MaxxECU AIN y
    d.add(elm.Line().right().at(pedal.APS2).length(4.5))
    d.add(elm.Label().label(
        'AIN y -- APS2\n0.36 V idle  /  2.20 V WOT\n(MaxxECU RACE)',
        loc='right'))

    # ── Firewall bulkhead marker ──────────────────────────────────────────────
    # Vertical marker showing where wires cross from cabin to engine bay.
    # In the actual harness, 6 APS wires cross via Maven HD30 dual bulkhead
    # Connector B pins 1-6 (Phase 3 install). See harnesses/firewall-crossing-maven.wv.
    d.add(elm.Line().at((1.5, 3.0)).down().length(6.5).color('#888888'))
    d.add(elm.Label().at((1.5, 3.3)).label('FIREWALL\nMaven HD30\nConnector B', loc='center'))
    d.add(elm.Label().at((1.5, -3.5)).label('cabin side    |    engine side', loc='center'))

    # ── Notes at bottom ───────────────────────────────────────────────────────
    d.add(elm.Label().at((6, -4.8)).label(
        'APS1:APS2 ratio cross-checked by MaxxECU at all times. '
        'Ratio fault or open circuit cuts TB motor output immediately.\n'
        'Do NOT disable pedal safety monitoring in MTune. '
        'Total draw ~20 mA -- 24 AWG shielded, single drain at MaxxECU SGND.\n'
        'PID tuning required after wiring -- see docs/etb-pid-tuning.md.',
        loc='center'))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/epedal-dbw.svg")
