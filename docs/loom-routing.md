# Loom Routing Reference

Physical routing of harness loom runs through the E36 convertible body.

**Fill in during form-board layout / trial-fit session.**  
Electrical connections are in the `.wv` harness files. This document covers physical path, sleeving, breakout points, and heat/abrasion zones only.

---

## Loom Runs

### 1. Engine Bay Trunk Loom
**Path:** MaxxECU RACE H2O (OEM E-box cavity, intake side of RHD car) → PMU16 (co-mounted alongside H2O) → engine-bay actuators / sensors  
**Route:** Intake side inner fender rail (RHD passenger side, away from exhaust which is on driver side), secured to existing body grommets  
**Sleeve:** Expandable braid, DR-25 over sensor sub-looms  
**Sub-looms that branch off this trunk:**

| Sub-loom | Breakout point | Harness file |
|----------|---------------|--------------|
| Sensor bundle (CLT, IAT, TPS/crank/cam, PST-F1) | TODO — confirm at engine bay trial fit | `maxxecu-m52.wv` / `maxxecu-07k.wv` |
| Injector bundle (INJ 1–5/6) | TODO | `maxxecu-07k.wv` |
| Coil bundle (IGN 1–5/6) | TODO | `maxxecu-07k.wv` |
| EWP harness (CWA400) | TODO — near water pump mounting location | `ewp-controller.wv` |
| Wideband O2 — Ph1 (LSU 4.2, terminated harness) | TODO — route toward exhaust bung | `maxxecu-m52.wv` |
| Wideband O2 — Ph3 (LSU 4.9, custom harness) | TODO — route toward exhaust bung, DR-25 sleeve near turbo | `maxxecu-07k.wv` |
| Boost solenoid | TODO | `maxxecu-07k.wv` |

> **Isolation rule:** Injector and coil sub-looms get their own sleeve sleeves even where they run alongside the sensor trunk. Do not co-sleeve sensor signals with injector/coil wires — switching noise corrupts crank/knock signals.

---

### 2. Firewall Bulkhead
**Connector:** Maven HD30 Dual 16+16 kit ($274) — Phase 2 install.
- Connector A (16-pin, populated Phase 2): CAN + DCT shifter (6 wires used, 8 spare)
- Connector B (16-pin, populated Phase 3): APS e-pedal (6 wires used, 10 spare)
- Plate: 2.6" × 5.25" CNC billet aluminum, black anodized, template included
- Phase 1: no bulkhead — 6 wires (CAN + DCT) route through OEM E36 firewall grommet as individual wires alongside the pre-terminated M50 harness  
**Location:** TODO — firewall pass-through location TBD at fitment. Recommended: driver-opposite side of firewall (intake side = passenger side of RHD car) for shortest run to the engine-bay MaxxECU  
**Harness file:** `harnesses/firewall-crossing-maven.wv`
**Vendor:** [mavenspeed.com/collections/b2t-engineering/products/dual-connector-bulkhead](https://mavenspeed.com/collections/b2t-engineering/products/dual-connector-bulkhead)

---

### 3. Cabin Loom
**Path:** Maven Connector A (CAN + DCT cabin electronics) and Connector B (safety-critical APS throttle input, populated Phase 3) at the firewall face → cabin destinations: pedal box (E46 APS pedal wires terminate at Connector B), gauge cluster (Gauge.S — CAN from Connector A), shifter (DCT paddle)  
**Route:** Behind lower dash panel, secured with P-clips to existing body studs  
**Sub-looms:**

| Sub-loom | Harness file | Firewall crossing |
|----------|-------------|-------------------|
| E-pedal (E46 pedal → Maven Connector B) | `harnesses/epedal-bmw-e46.wv` | Maven Connector B (6 wires, Phase 3) |
| Gauge.S CAN (ECU → cluster) | `harnesses/gauge-s-can.wv` | Maven Connector A pins 1/2/3 (Phase 2+; Phase 1 uses OEM grommet) |
| DCT Shifter paddle | `harnesses/dct-shifter.wv` | Maven Connector A pins 4/5/6 (Phase 2+; Phase 1 uses OEM grommet) |
| Body X20 signals | `harnesses/body-x20.wv` | OEM X20 (unchanged from OEM E36 — no ECU signals traverse X20) |

---

### 4. Transmission Tunnel / Rear Loom
**Path:** PMU16 (engine bay) → transmission tunnel → rear of car  
**Route:** Along tunnel (left side), inside factory wiring channel where possible  
**Sub-looms:**

| Sub-loom | Harness file | Notes |
|----------|-------------|-------|
| Fuel pump (full run, ~3.5–4m estimated) | `harnesses/fuel-pump-hanger-phase1.wv` (Phase 1: discrete relay + JDT kit) → `harnesses/fuel-pump-hanger-phase3.wv` (Phase 3: PMU16 O4 direct) | 12 AWG min; run separately from CAN to avoid PWM noise on bus |
| ATF temp sensor (inline -8AN adapter) | `harnesses/atf-temp-sensor.wv` | Runs along tunnel forward to engine-bay ECU (no bulkhead crossing under H2O arch — sensor and ECU both engine-bay-side of firewall) |
| 8HP CAN + power (engine bay → ZF 8HP TCU) | `harnesses/8hp-can.wv` (reference only — pre-made MaxxECU 8HP GEN1 kit, plug-and-play) | Twisted pair — engine-bay-to-engine-bay under H2O arch |

---

## Sleeving Reference

| Zone | Sleeve type | Notes |
|------|------------|-------|
| Engine bay general | Expandable braid (Techflex F6) | Breathes, resists abrasion |
| Near turbo / exhaust | DR-25 heat-shrink tubing (1:2 ratio) | Rated to 135°C continuous, 175°C short-term |
| Sensor sub-looms (in sleeve) | DR-25 or Raychem SCL | Separate sleeve within engine bay trunk |
| Injector/coil sub-looms | DR-25 | Separate from sensor sleeve — isolation critical |
| Cabin / tunnel | Expandable braid | Lower heat exposure |
| Firewall transition boots | Adhesive-lined heat shrink + boot | Seal breakout from sleeve at Maven bulkhead entry (Phase 2+); OEM firewall grommet (Phase 1) |

---

## Breakout Discipline

- Breakout = point where a sub-loom exits the main trunk sleeve
- Use **adhesive-lined heat-shrink transition** at each breakout — don't leave open braid ends
- **Label each leg** at the breakout with heat-shrink ID markers before sleeving
- Measure all runs on the form board **before** cutting wire to length — add 20% slack per BOM conventions

---

## PMU16 — Mounting and Layout

The Ecumaster PMU16 replaces the relay board, blade fuse block, and Crydom SSR.
Mounting location: **engine bay, intake side (RHD passenger side), alongside the
MaxxECU RACE H2O in / adjacent to the OEM DME E-box cavity area**. This keeps:
- MaxxECU H2O and PMU16 physically adjacent for the shortest ECU +12V feed run
- Both units on the intake side, away from exhaust heat (driver side in RHD)
- BATT+ run from ANL fuse to PMU16 M6 stud as short as practical
See docs/vendor/maxxecu/MaxxECU_RACE_H2O.md and `harnesses/power-distribution.wv`.

The 39-pin Sicma connector faces down/inboard for harness routing to engine-bay loads.

### Layout Workflow
1. **Mock-up placement with the PMU16 and RACE H2O bodies in-hand.** Verify clearance
   for the 39-pin Sicma connector harness exit on the PMU16, the M6 BATT+ stud cable,
   the CAN2 twisted pair run to MaxxECU C1 pins E1/E2, and the RACE H2O 155×195×40mm
   footprint alongside.
2. **Rivnuts (riveted nut inserts)** are the correct technique for attaching the PMU16
   and H2O brackets to thin firewall sheetmetal where backside nut access is impossible.
   M6 rivnuts for each bracket. Tool: Astro Pneumatic 1442 or equivalent manual rivnut setter.
   Source: StreetCarJoe Race Car Wiring Pt.3.
3. If mounting to cage tubing or a roll bar, weld tabs and touch up paint.

### Power Routing to/from PMU16
- **BATT+ input:** 4 AWG from battery through 150A ANL fuse to PMU16 M6 BATT+ stud.
  ANL fuse within 18 in of battery terminal. See `harnesses/power-distribution.wv`.
- **GND:** PMU16 GND lug → engine bay chassis star stud (M8). 6 AWG minimum.
- **IGN sense:** IGN switched +12V (X20 pin 21, green wire) → PMU16 39-pin pin 7.
  Switches PMU on/off with key. X20 pin 21 already runs to the engine bay in the OEM
  E36 body harness — tap it engine-side. 22 AWG, protect with 5A inline fuse.
- **CAN2:** PMU16 CAN2 H/L → MaxxECU CAN1 H/L (C1 pins E1/E2). Engine-bay-to-engine-bay
  under H2O arch — no bulkhead crossing. 22 AWG twisted pair. 120Ω termination at
  MaxxECU (built-in on CAN 1 per maxxecu.com/webhelp/can-information.html); enable
  120Ω software termination on PMU16 CAN2 end.
- **ECU +12V:** PMU16 O1 (or similar high-side output configured for constant +12V) →
  MaxxECU CMC pin (see maxxecu-m52.wv / maxxecu-07k.wv). Engine-bay-to-engine-bay.

### Harness Organization at PMU16
- **Adhesive-backed zip tie anchor mounts (cable saddle clips)** on the chassis near
  the PMU16 keep harness runs clean without drilling additional holes.
  Source: StreetCarJoe Race Car Wiring Pt.3.
- Label all 39-pin Sicma pins at the PMU16 before final installation — access is
  restricted once the unit is mounted.

---

## TODO — Fill In During Build

- [ ] Confirm Maven bulkhead pass-through hole location (intake side preferred; height from floor)
- [ ] Confirm PMU16 + RACE H2O co-mount location on intake-side firewall — verify OEM DME E-box cavity accepts the H2O 155×195mm footprint (may need fabricated mounting plate — measure during Phase 1 mockup)
- [ ] Measure engine bay trunk run: PMU16 → each sensor breakout → MaxxECU CMC
- [ ] Confirm fuel pump loom total length (PMU16 O4 → Radium hanger, est. 3.5–4m tunnel run)
- [ ] Confirm 8HP CAN run length (ECU → ZF 8HP TCU connector)
- [ ] Confirm EWP loom length (PMU16 O5+O14 → CWA400 mounting location)
- [ ] Confirm direct battery → engine block GND cable run length (battery location → block boss)
- [ ] Confirm 4-post cutoff switch (Moroso 74108) mounting location — driver accessible or external pull cable to HPDE cage requirement
- [ ] Identify and note existing E36 body grommets and P-clip anchor points usable for custom loom retention
- [ ] Trial-fit before final sleeve: verify no contact with hot or moving parts (exhaust, steering column, shifter linkage)
- [ ] PMU16 engine bay mock-up — confirm bracket placement, Sicma connector exit clearance, and ANL fuse run length before final mount
