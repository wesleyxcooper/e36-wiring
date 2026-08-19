"""
12V Electric AC Compressor circuit schematic
Alibaba PD2-18012AJA (18cc, 3.65 kW / 12,454 BTU, R134a or R1234yf)
+ included 3-phase inverter/controller + MaxxECU RACE idle compensation
+ Ecumaster PMU16 O7 (relay coil) + PMU16 O6 (condenser fan direct)

This script generates a circuit schematic using schemdraw.
Run it to produce ac-compressor-pwm.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic, inverter speed control).
A WireViz harness file (harnesses/ac-compressor.wv) covers WHERE each wire terminates.

PD2-18012AJA motor type: Three-phase PMSM (Permanent Magnet Synchronous Motor)
The included "PWM controller" is a 3-phase inverter/VFD -- NOT a simple DC switch.
  Motor wires: U / V / W (3 orange pigtail wires confirmed from Alibaba product photos)
  Phase order: follow controller labeling -- swapping any two phases reverses rotation

AC relay (Bosch ISO mini, 100A rated):
  30   common          BATT+ always-on, fused at 100A within 12" of battery
  87   normally open   PWM controller +IN when relay closes
  86   coil positive   PMU16 O7 output (CAN-commanded by MaxxECU)
  85   coil negative   chassis GND

AC enable signal path (PMU16 architecture):
  AC switch pin 2 → MaxxECU DIN (direct, no relay tap)
  MaxxECU reads AC-on → prepares idle-up → CAN-commands PMU16 O7 → relay coil closes
  Old path (IGN → AC switch → relay coil 86) removed.

Condenser fan:
  PMU16 O6 (15A) drives condenser fan motor directly via CAN command.
  Old RELAY_CONDENSER_FAN (30A relay tapped from AC switch) removed.
  MaxxECU CAN signals PMU16 O6 whenever AC is active.

MaxxECU idle compensation:
  AC enable signal    AC switch pin 2 → MaxxECU DIN (direct wire, 22 AWG)
  MTune config        AC input type = ON/OFF, idle-up = +150-200 RPM when AC active
  Purpose             prevents idle dip when compressor engages under load

How this circuit works:
  1. Key on + AC switch pressed -> AC switch pin 2 goes high -> MaxxECU DIN sees +12V
  2. MaxxECU raises idle target (+150-200 RPM) for idle-up compensation
  3. MaxxECU sends CAN command to PMU16 -> O7 activates -> relay coil 86 gets +12V
  4. Coil (85) at GND -> coil energizes -> relay contact closes (30 to 87)
  5. BATT+ (through 100A fuse) flows to PWM controller +IN
  6. PMU16 also activates O6 -> condenser fan runs
  7. PWM controller powers compressor at set duty cycle (~45% start)
  8. AC switch off -> DIN drops -> MaxxECU removes CAN AC command -> O7 drops -> relay opens

Speed range (Alibaba PD2-18 spec table): 2,000 -- 6,000 RPM
Duty cycle guidance (from Rawrkee Episode 3, YouTube):
  95% (~6,000 RPM) -- maximum cooling but causes severe idle dip to near stall
  45% (~3,000 RPM) -- recommended start; 51-54 degF vent at 90 degF ambient, manageable idle
  Tune up from 45% in 5-10% increments -- monitor idle stability before increasing further

Cooling performance (Rawrkee, 90 degF ambient):
  Old 20cc unit:  61 degF vent temp
  PD2-18012AJA at 45%:  51-54 degF vent temp  (+7-10 degF improvement)

Pricing:
  DDP sea freight (recommended):  ~$340-360 all-in  (source: @jfantis YouTube comments, 4+ yr proven)
  FedEx Express (Rawrkee's method): ~$680 total ($280 unit + $50 tax + $200 shipping + $150 tariffs)

Usage:
  pip install schemdraw matplotlib
  python3 schematics/ac-compressor-pwm.py
  open schematics/ac-compressor-pwm.svg
"""

import schemdraw
import schemdraw.elements as elm
import matplotlib
matplotlib.use('Agg')  # non-interactive backend -- no display window needed
import os

OUT = os.path.join(os.path.dirname(__file__), "ac-compressor-pwm.svg")

with schemdraw.Drawing(figsize=(14, 10), show=False) as d:
    d.config(fontsize=9)

    # ── AC relay (center) ────────────────────────────────────────────────────
    relay = d.add(elm.Relay(switch='spst').at((5.0, 0)).label(
        "AC_RELAY / 100A Bosch ISO", loc="top"))

    # ── Coil circuit: PMU16 O7 → pin 86, chassis GND → pin 85 ───────────────
    d.add(elm.Line().left().at(relay.in1).length(1.5))
    d.add(elm.Switch().left().label(
        "PMU16 O7\n(MOSFET 15A)\nCAN cmd", loc="top"))
    d.add(elm.Line().left().length(0.5))
    d.add(elm.Line().up().length(0.6))
    d.add(elm.Label().label("BATT+ (PMU16 M6)\n18 AWG", loc="right"))

    d.add(elm.Line().left().at(relay.in2).length(2.8))
    d.add(elm.Ground())

    d.add(elm.Label().at(relay.in1).label("86 ", loc="left"))
    d.add(elm.Label().at(relay.in2).label("85 ", loc="left"))

    # ── AC switch → MaxxECU DIN (below coil, shows CAN chain) ───────────────
    d.add(elm.Line().down().at(relay.in1).length(1.0))
    can_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(0.8))
    d.add(elm.Switch().left().label("AC switch\n(cabin)", loc="top"))
    d.add(elm.Line().left().length(0.5))
    d.add(elm.Label().label("IGN +12V", loc="left"))
    d.add(elm.Line().right().at(can_node.end).length(0.3))
    d.add(elm.Label().label(
        "→ MaxxECU DIN\n(AC enable, direct wire)\n→ CAN → PMU16 O7",
        loc="right"))

    # ── Load circuit: BATT+ → 100A fuse → relay 30 → 87 → inverter → motor ──
    d.add(elm.Line().up().at(relay.a).length(1.5))
    d.add(elm.Line().left().length(0.6))
    d.add(elm.Fuse().left().label("F_AC 100A / within 12\" batt", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT / 8 AWG OFC", loc="right"))

    d.add(elm.Line().down().at(batt_node.end).length(3.8))
    d.add(elm.Ground())

    d.add(elm.Line().right().at(relay.b).length(0.5))
    d.add(elm.Motor().right().label(
        "PD2-18012AJA 3-ph PMSM\n12,454 BTU | 8 AWG OFC | 45% duty start", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    d.add(elm.Label().at(relay.a).label("30 ", loc="left"))
    d.add(elm.Label().at(relay.b).label("87 ", loc="left"))

    # ── Condenser fan: PMU16 O6 direct (bottom section) ─────────────────────
    d.add(elm.Switch().right().at((5.0, -5.0)).label(
        "PMU16 O6\n(MOSFET 15A)\nCAN cmd when AC on", loc="top"))
    d.add(elm.Line().right().length(0.5))
    d.add(elm.Motor().right().label(
        "Condenser fan motor\n(separate from radiator fan)", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())

    d.add(elm.Label().at((3.5, -5.0)).label(
        "BATT+\n(PMU16 M6)\n12 AWG", loc="left"))

    # ── Key notes (bottom) ───────────────────────────────────────────────────
    d.add(elm.Label().at((6.0, -8.2)).label(
        "Duty: 45% start (~3,000 RPM) -> 51-54 degF vent / 90 degF  |  95%+ = near-stall idle dip\n"
        "Motor: 3-phase PMSM -- inverter outputs U/V/W orange pigtails, NOT simple DC\n"
        "PMU16 O7 replaces: IGN→AC switch→relay coil wire | O6 replaces: RELAY_CONDENSER_FAN",
        loc="center"))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/ac-compressor-pwm.svg")
