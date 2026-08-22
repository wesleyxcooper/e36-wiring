# Loom Routing Reference

Physical routing of harness loom runs through the E36 convertible body.

**Fill in during form-board layout / trial-fit session.**  
Electrical connections are in the `.wv` harness files. This document covers physical path, sleeving, breakout points, and heat/abrasion zones only.

---

## Loom Runs

### 1. Engine Bay Trunk Loom
**Path:** ECU bulkhead → PMU16 → firewall bulkhead (engine side)  
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
**Path:** PMU16 (engine bay) → transmission tunnel → rear of car  
**Route:** Along tunnel (left side), inside factory wiring channel where possible  
**Sub-looms:**

| Sub-loom | Harness file | Notes |
|----------|-------------|-------|
| Fuel pump (full run, ~3.5–4m estimated) | `harnesses/fuel-pump-hanger.wv` | 12 AWG min; run separately from CAN to avoid PWM noise on bus |
| ATF temp sensor (inline -8AN adapter) | `harnesses/atf-temp-sensor.wv` | Short stub from tunnel to bulkhead pin 56 |
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

## PMU16 — Mounting and Layout

The Ecumaster PMU16 replaces the relay board, blade fuse block, and Crydom SSR.
Mounting location: **engine bay, near ANL fuse / battery positive** — keeps the
high-current BATT+ run to the PMU16 M6 stud as short as possible (≤ 18 in from
battery preferred). The 39-pin Sicma connector faces toward the cabin for harness routing.

### Layout Workflow
1. **Mock-up placement with the PMU16 body in-hand.** Verify clearance for the 39-pin
   Sicma connector harness exit, the M6 BATT+ stud cable, and the CAN2 twisted pair run
   toward the firewall bulkhead.
2. **Rivnuts (riveted nut inserts)** are the correct technique for attaching the PMU16
   bracket to thin sheetmetal where backside nut access is impossible. M6 rivnuts for
   the bracket. Tool: Astro Pneumatic 1442 or equivalent manual rivnut setter.
   Source: StreetCarJoe Race Car Wiring Pt.3.
3. If mounting to cage tubing or a roll bar, weld tabs and touch up paint.

### Power Routing to/from PMU16
- **BATT+ input:** 4 AWG from battery through 150A ANL fuse to PMU16 M6 BATT+ stud.
  ANL fuse within 18 in of battery terminal. See `harnesses/power-distribution.wv`.
- **GND:** PMU16 GND lug → engine bay chassis star stud (M8). 6 AWG minimum.
- **IGN sense:** IGN switched +12V (X20 pin 21, green wire) → PMU16 39-pin pin 7.
  Switches PMU on/off with key. 22 AWG, protect with 5A inline fuse near X20.
- **CAN2:** PMU16 CAN2 H/L → MaxxECU CAN1 H/L via 22 AWG twisted pair through
  firewall bulkhead. 120Ω termination at both ends.

### Harness Organization at PMU16
- **Adhesive-backed zip tie anchor mounts (cable saddle clips)** on the chassis near
  the PMU16 keep harness runs clean without drilling additional holes.
  Source: StreetCarJoe Race Car Wiring Pt.3.
- Label all 39-pin Sicma pins at the PMU16 before final installation — access is
  restricted once the unit is mounted.

---

## TODO — Fill In During Build

- [ ] Confirm firewall bulkhead pass-through hole location (L/R side, height from floor)
- [ ] Confirm PMU16 mounting location in engine bay — verify M6 stud run ≤ 18 in to ANL fuse
- [ ] Measure engine bay trunk run: PMU16 → each sensor breakout → bulkhead
- [ ] Confirm fuel pump loom total length (PMU16 O4 → Radium hanger, est. 3.5–4m tunnel run)
- [ ] Confirm 8HP CAN run length (ECU → ZF 8HP TCU connector)
- [ ] Confirm EWP loom length (PMU16 O5+O14 → CWA400 mounting location)
- [ ] Confirm direct battery → engine block GND cable run length (battery location → block boss)
- [ ] Confirm 4-post cutoff switch (Moroso 74108) mounting location — driver accessible or external pull cable to HPDE cage requirement
- [ ] Identify and note existing E36 body grommets and P-clip anchor points usable for custom loom retention
- [ ] Trial-fit before final sleeve: verify no contact with hot or moving parts (exhaust, steering column, shifter linkage)
- [ ] PMU16 engine bay mock-up — confirm bracket placement, Sicma connector exit clearance, and ANL fuse run length before final mount
