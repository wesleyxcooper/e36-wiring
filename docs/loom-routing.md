# Loom Routing Reference

Physical routing of harness loom runs through the E36 convertible body.

**Fill in during form-board layout / trial-fit session.**  
Electrical connections are in the `.wv` harness files. This document covers physical path, sleeving, breakout points, and heat/abrasion zones only.

---

## Loom Runs

### 1. Engine Bay Trunk Loom
**Path:** ECU bulkhead → fuse/relay board → firewall bulkhead (engine side)  
**Route:** Left inner fender rail (away from exhaust), secured to existing body grommets  
**Sleeve:** Expandable braid, DR-25 over sensor sub-looms  
**Sub-looms that branch off this trunk:**

| Sub-loom | Breakout point | Harness file |
|----------|---------------|--------------|
| Sensor bundle (CLT, IAT, TPS/crank/cam, PST-F1) | TODO — confirm at engine bay trial fit | `maxxecu-m52.wv` / `maxxecu-07k.wv` |
| Injector bundle (INJ 1–5/6) | TODO | `maxxecu-07k.wv` |
| Coil bundle (IGN 1–5/6) | TODO | `maxxecu-07k.wv` |
| EWP harness (CWA400) | TODO — near water pump mounting location | `ewp-controller.wv` |
| Wideband O2 (LSU 4.9) | TODO — route toward exhaust bung, DR-25 sleeve near turbo | `maxxecu-m52.wv` / `maxxecu-07k.wv` |
| Boost solenoid | TODO | `maxxecu-07k.wv` |

> **Isolation rule:** Injector and coil sub-looms get their own sleeve sleeves even where they run alongside the sensor trunk. Do not co-sleeve sensor signals with injector/coil wires — switching noise corrupts crank/knock signals.

---

### 2. Firewall Bulkhead
**Connector:** Deutsch AS79 (79-way) — cabin flange receptacle permanent; engine-side mating plug swaps M52↔07K  
**Location:** TODO — firewall pass-through location TBD at fitment (left of center stack preferred for short cabin→ECU run)  
**Harness file:** `harnesses/firewall-bulkhead.wv`

---

### 3. Cabin Loom
**Path:** ECU (under dash / tunnel-side) → pedal box, gauge cluster, shifter, DCT module  
**Route:** Behind lower dash panel, secured with P-clips to existing body studs  
**Sub-looms:**

| Sub-loom | Harness file |
|----------|-------------|
| E-pedal (E46 pedal → bulkhead) | `harnesses/epedal-bmw-e46.wv` |
| Gauge.S CAN (ECU → cluster) | `harnesses/gauge-s-can.wv` |
| DCT Shifter paddle (cabin-to-cabin) | `harnesses/dct-shifter.wv` |
| Body X20 signals | `harnesses/body-x20.wv` |

---

### 4. Transmission Tunnel / Rear Loom
**Path:** Engine bay fuse block → transmission tunnel → rear of car  
**Route:** Along tunnel (left side), inside factory wiring channel where possible  
**Sub-looms:**

| Sub-loom | Harness file | Notes |
|----------|-------------|-------|
| Fuel pump (full run, ~3.5–4m estimated) | `harnesses/fuel-pump-hanger.wv` | 12 AWG min; run separately from CAN to avoid PWM noise on bus |
| ATF temp sensor (inline -8AN adapter) | `harnesses/atf-temp-sensor.wv` | Short stub from tunnel to bulkhead pin 51 |
| 8HP CAN + power (engine bay → ZF 8HP) | `harnesses/8hp-can.wv` | Twisted pair — must maintain twist all the way to TCU plug |

---

## Sleeving Reference

| Zone | Sleeve type | Notes |
|------|------------|-------|
| Engine bay general | Expandable braid (Techflex F6) | Breathes, resists abrasion |
| Near turbo / exhaust | DR-25 heat-shrink tubing (1:2 ratio) | Rated to 135°C continuous, 175°C short-term |
| Sensor sub-looms (in sleeve) | DR-25 or Raychem SCL | Separate sleeve within engine bay trunk |
| Injector/coil sub-looms | DR-25 | Separate from sensor sleeve — isolation critical |
| Cabin / tunnel | Expandable braid | Lower heat exposure |
| Firewall transition boots | Adhesive-lined heat shrink + boot | Seal breakout from sleeve at bulkhead entry |

---

## Breakout Discipline

- Breakout = point where a sub-loom exits the main trunk sleeve
- Use **adhesive-lined heat-shrink transition** at each breakout — don't leave open braid ends
- **Label each leg** at the breakout with heat-shrink ID markers before sleeving
- Measure all runs on the form board **before** cutting wire to length — add 20% slack per BOM conventions

---

## TODO — Fill In During Build

- [ ] Confirm firewall bulkhead pass-through hole location (L/R side, height from floor)
- [ ] Measure engine bay trunk run: relay board → each sensor breakout → bulkhead
- [ ] Confirm fuel pump loom total length (battery/fuse block → Radium hanger -8AN port)
- [ ] Confirm 8HP CAN run length (ECU → ZF 8HP TCU connector)
- [ ] Confirm EWP loom length (relay board → CWA400 mounting location)
- [ ] Identify and note existing E36 body grommets and P-clip anchor points usable for custom loom retention
- [ ] Trial-fit before final sleeve: verify no contact with hot or moving parts (exhaust, steering column, shifter linkage)
