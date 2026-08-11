"""
12V Electric AC Compressor circuit schematic
Alibaba PD2-18012AJA (18cc, 3.65 kW / 12,454 BTU, R134a or R1234yf)
+ included 3-phase inverter/controller + MaxxECU RACE idle compensation

This script generates a circuit schematic using schemdraw.
Run it to produce ac-compressor-pwm.svg in the same directory.

The schematic shows HOW the circuit works (current flow, switching logic, inverter speed control).
A WireViz harness file (harnesses/ac-compressor.wv) covers WHERE each wire terminates.

PD2-18012AJA motor type: Three-phase PMSM (Permanent Magnet Synchronous Motor)
The included "PWM controller" is a 3-phase inverter/VFD -- NOT a simple DC switch.
  Motor wires: U / V / W (3 orange pigtail wires confirmed from Alibaba product photos)
  Phase order: follow controller labeling -- swapping any two phases reverses rotation

Included inverter/controller:
  DC in +     BATT+ through 100A fuse via relay contact         (8 AWG OFC)
  DC in -     chassis ground                                    (8 AWG OFC)
  Phase U     3-phase output to motor                           (8 AWG OFC)
  Phase V     3-phase output to motor                           (8 AWG OFC)
  Phase W     3-phase output to motor                           (8 AWG OFC)
  Duty cycle  manual knob -- ~45% start point (3,000 RPM), 95% = ~6,000 RPM (excessive idle dip)
  Frequency   manual knob -- set per controller default

AC relay (Bosch ISO mini, 100A rated):
  85   coil negative   chassis GND
  86   coil positive   IGN +12V via AC button/cabin switch
  30   common          BATT+ always-on, fused at 100A within 12" of battery
  87   normally open   PWM controller +IN when relay closes

MaxxECU idle compensation:
  AC enable signal    tapped from relay coil (86) side after AC button
                      -> MaxxECU DIN (digital input, any spare)
  MTune config        AC input type = ON/OFF, idle-up = +150-200 RPM when AC active
  Purpose             prevents idle dip when compressor engages under load

How this circuit works:
  1. Key on + AC button pressed -> relay coil (86) gets IGN +12V
  2. Coil (85) at GND -> coil energizes -> relay contact closes (30 to 87)
  3. BATT+ (through 100A fuse) flows to PWM controller +IN
  4. PWM controller powers compressor at set duty cycle (~45% start)
  5. AC enable tap also wires to MaxxECU DIN -> ECU raises idle target by ~150-200 RPM
  6. AC button off / key off -> relay opens -> compressor stops

Speed range (Alibaba PD2-18 spec table): 2,000 -- 6,000 RPM
Duty cycle guidance (from Rawrkee Episode 3, YouTube):
  95% (~6,000 RPM) -- maximum cooling but causes severe idle dip to near stall
  45% (~3,000 RPM) -- recommended start; 51-54 degF vent at 90 degF ambient, manageable idle
  Tune up from 45% in 5-10% increments -- monitor idle stability before increasing further

Cooling performance (Rawrkee, 90 degF ambient):
  Old 20cc unit:  61 degF vent temp
  PD2-18012AJA at 45%:  51-54 degF vent temp  (+7-10 degF improvement)

Condenser fan:
  One shared fan serves both radiator and AC condenser.
  Condenser fan relay (RELAY_CONDENSER_FAN in power-distribution.wv) tapped from AC switch
  output -- fires simultaneously with AC relay coil. Output wired in parallel with
  RELAY_FAN (radiator fan) output so one fan handles both cooling duties.

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

    # ── AC relay (top section) ───────────────────────────────────────────────────
    relay = d.add(elm.Relay(switch='spst').at((4.5, 0)).label(
        "AC_RELAY / 100A Bosch ISO", loc="top"))

    # Coil: IGN +12V -> AC switch -> ac_tap junction -> pin 86 -> coil -> 85 -> GND
    d.add(elm.Line().left().at(relay.in1).length(1.5))
    ac_tap = d.add(elm.Dot())  # junction: fan relay coil tap + MaxxECU DIN
    d.add(elm.Line().left().length(0.8))
    d.add(elm.Switch().left().label("AC switch", loc="top"))
    d.add(elm.Line().left().length(0.5))
    d.add(elm.Line().up().length(0.6))
    d.add(elm.Label().label("IGN +12V / F10 (5A)", loc="right"))

    d.add(elm.Line().left().at(relay.in2).length(2.0))
    d.add(elm.Ground())

    d.add(elm.Label().at(relay.in1).label("86 ", loc="left"))
    d.add(elm.Label().at(relay.in2).label("85 ", loc="left"))

    # MaxxECU DIN tap (down from ac_tap junction -- long drop to clear relay body)
    d.add(elm.Line().down().at(ac_tap.end).length(2.5))
    d.add(elm.Label().label(
        "MaxxECU DIN (AC enable)\nidle-up ~150-200 RPM", loc="left"))

    # Load: BATT+ -> 100A fuse -> relay 30 -> 87 -> inverter -> motor
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

    # ── Condenser fan relay (bottom section -- separate, no overlap) ──────────
    fan_relay = d.add(elm.Relay(switch='spst').at((4.5, -4.5)).label(
        "RELAY_CONDENSER_FAN / 30A", loc="top"))

    # Fan relay coil: same AC switch output signal as ac_tap
    d.add(elm.Line().left().at(fan_relay.in1).length(2.0))
    d.add(elm.Label().label(
        "AC switch output tap\n(same signal as AC_RELAY 86)", loc="left"))
    d.add(elm.Line().left().at(fan_relay.in2).length(2.0))
    d.add(elm.Ground())
    d.add(elm.Label().at(fan_relay.in1).label("86 ", loc="left"))
    d.add(elm.Label().at(fan_relay.in2).label("85 ", loc="left"))

    # Fan relay load: BATT+ via inline 20A -> relay 30 -> 87 -> fan motor
    d.add(elm.Line().up().at(fan_relay.a).length(1.0))
    d.add(elm.Label().label("BATT+ / 20A inline / 12 AWG", loc="right"))
    d.add(elm.Label().at(fan_relay.a).label("30 ", loc="left"))

    d.add(elm.Line().right().at(fan_relay.b).length(0.5))
    d.add(elm.Motor().right().label(
        "Shared fan (radiator + condenser)\n|| with RELAY_FAN output", loc="top"))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())
    d.add(elm.Label().at(fan_relay.b).label("87 ", loc="left"))

    # ── Key notes (bottom) ─────────────────────────────────────────────────
    d.add(elm.Label().at((5.5, -8.5)).label(
        "Duty: 45% start (~3,000 RPM) -> 51-54 degF vent / 90 degF  |  95%+ = near-stall idle dip\n"
        "Motor: 3-phase PMSM -- inverter outputs U/V/W orange pigtails, NOT simple DC\n"
        "Oil: POE 68 ONLY -- flush all PAG, replace receiver/drier before commissioning",
        loc="center"))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/ac-compressor-pwm.svg")
