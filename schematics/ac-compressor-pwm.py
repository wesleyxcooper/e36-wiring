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

with schemdraw.Drawing(show=False) as d:
    d.config(fontsize=10.5)

    # ── Place relay in center of diagram ──────────────────────────────────────
    relay = d.add(elm.Relay(switch='spst').at((4.5, 0)).label(
        "AC_RELAY\n100A (Bosch ISO mini)\nCoil: 86/85  Contact: 30/87",
        loc="top"
    ))

    # ── COIL CIRCUIT: IGN +12V -> AC button -> pin 86 -> coil -> pin 85 -> GND
    d.add(elm.Line().left().at(relay.in1).length(1.5))
    ac_tap = d.add(elm.Dot())  # junction: coil + MaxxECU DIN tap
    d.add(elm.Line().left().length(0.8))
    d.add(elm.Switch().left().label("AC switch\n(cabin)", loc="top"))
    d.add(elm.Line().left().length(0.5))
    d.add(elm.Line().up().length(0.6))
    d.add(elm.Label().label("IGN +12V\n(key-on)", loc="right"))

    # MaxxECU DIN tap from coil-positive side (after AC button, before relay coil)
    d.add(elm.Line().down().at(ac_tap.end).length(1.5))
    d.add(elm.Label().label(
        "MaxxECU DIN\n(AC enable signal)\n-> configure idle-up ~150-200 RPM",
        loc="right"
    ))

    # Coil negative to GND
    d.add(elm.Line().left().at(relay.in2).length(2.0))
    d.add(elm.Ground())

    # Pin labels
    d.add(elm.Label().at(relay.in1).label("  86", loc="right"))
    d.add(elm.Label().at(relay.in2).label("  85", loc="right"))

    # ── LOAD CIRCUIT: BATT+ -> 100A fuse -> relay 30 -> 87 -> PWM ctrl -> motor
    # Up from relay contact input (pin 30) -> fuse -> battery
    d.add(elm.Line().up().at(relay.a).length(1.5))
    d.add(elm.Line().left().length(0.6))
    d.add(elm.Fuse().left().label("F_AC_PWR -- 100A\n(within 12\" of battery)", loc="top"))
    d.add(elm.Line().left().length(0.5))
    batt_node = d.add(elm.Dot())
    d.add(elm.Line().left().length(1.2))
    d.add(elm.Battery().up().reverse().label("12V BATT\n(0 AWG OFC to trunk)", loc="right"))

    # Battery negative
    d.add(elm.Line().down().at(batt_node.end).length(3.8))
    d.add(elm.Ground())

    # Right from relay contact output (pin 87) -> PWM controller -> compressor motor
    d.add(elm.Line().right().at(relay.b).length(0.5))
    pwm_in = d.add(elm.Dot())
    d.add(elm.Label().label(
        "PWM CTRL (included kit)\nduty + freq knobs\n8 AWG OFC in/out",
        loc="top"
    ))
    d.add(elm.Line().right().length(0.5))
    d.add(elm.Motor().right().label(
        "PD2-18012AJA 3-phase PMSM\n18cc, 3.65 kW / 12,454 BTU\n~45% duty = ~3,000 RPM (start here)",
        loc="top"
    ))
    d.add(elm.Line().right().length(0.3))
    d.add(elm.Ground())
    d.add(elm.Label().at(relay.b).label(
        "  3-phase inverter out (U/V/W orange pigtails) -- NOT simple DC", loc="bottom"
    ))

    # Contact pin labels
    d.add(elm.Label().at(relay.a).label("  30", loc="left"))
    d.add(elm.Label().at(relay.b).label("  87", loc="left"))

    # ── Condenser fan relay (tapped from AC switch output) ──────────────────────────
    # AC switch output (ac_tap junction) also triggers condenser fan relay coil
    d.add(elm.Line().down().at(ac_tap.end).length(2.5))
    cfan_junction = d.add(elm.Dot())
    d.add(elm.Line().down().length(0.8))
    d.add(elm.Label().label(
        "MaxxECU DIN\n(AC enable -> idle-up ~150-200 RPM)",
        loc="right"
    ))

    # Condenser fan relay coil
    d.add(elm.Line().right().at(cfan_junction.end).length(1.5))
    fan_relay_coil_pos = d.add(elm.Dot())
    d.add(elm.Label().label("RELAY_CONDENSER_FAN 86", loc="top"))
    d.add(elm.Line().right().length(1.0))
    d.add(elm.Relay(switch='spst').right().label(
        "Condenser fan relay\n(Bosch ISO mini 30A)\n-- same relay as RELAY_CONDENSER_FAN",
        loc="top"
    ))
    # Fan relay coil GND
    d.add(elm.Line().down().at(fan_relay_coil_pos.end).length(1.2))
    d.add(elm.Ground())
    d.add(elm.Label().label("85 (GND)", loc="right"))

    # ── Explanation note at bottom ──────────────────────────────────────────────────
    d.add(elm.Label().at((6.0, -5.5)).label(
        "Duty cycle: start 45% (~3,000 RPM) -> 51-54 degF vent at 90 degF ambient\n"
        "At 95% (~6,000 RPM): max cooling but near-stall idle dip -- do not start here\n"
        "Motor: Three-phase PMSM -- inverter outputs U/V/W, NOT a simple DC motor\n"
        "Condenser fan relay coil tapped from AC switch output -- fires with compressor\n"
        "Fan: one shared unit for radiator + condenser (output parallel with RELAY_FAN)\n"
        "Oil: POE 68 ONLY -- flush all PAG before commissioning, replace receiver/drier",
        loc="center"
    ))

    d.save(OUT)

print(f"Saved: {OUT}")
print("Open with:  open schematics/ac-compressor-pwm.svg")
