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

## Relay Board — Mounting and Layout

The relay board (fuse block + relay sockets) lives **under the dash, behind the lower
dash trim panel** — accessible for field relay/fuse swap but out of sight when the dash
is in. This is the same approach used across FuelTech and K&R relay-board builds.

Source: StreetCarJoe Race Car Wiring Pt.3 (youtube.com/watch?v=l59_-01VgEc)

### Layout Workflow
1. **Mock-up in cardboard first.** Cut cardboard to your planned dimensions and place it
   in the intended location with relays and fuses dry-fitted. Verify clearance to dash
   trim, steering column, and any cabin components (HVAC box, airbag modules if retained).
   The cardboard step reveals interference early — the video builder planned 18"×10" and
   had to extend to 24"×10" once harness relay modules were laid out.
2. Measure and verify with cardboard. Then cut the final material (aluminum sheet or
   carbon fibre panel per preference).
3. Mark and drill relay/fuse mounting positions from the cardboard template.

### Mounting to Chassis / Dash Structure
- **Rivnuts (riveted nut inserts)** are the correct technique for attaching the relay
  board to thin sheetmetal or carbon panels where backside nut access is impossible.
  Drill the correct clearance hole, thread the rivnut onto the tool mandrel, insert,
  pull the tool handle — the insert expands and locks permanently. Leaves a clean M4/M6
  threaded hole. Far cleaner than welding tabs or using self-tappers.
  Tool: Astro Pneumatic 1442 or equivalent manual rivnut setter.
  Source: StreetCarJoe Race Car Wiring Pt.3.
- If mounting to the cage or a roll bar, weld tabs and touch up paint.

### Harness Organization on the Relay Board Rear Face
- **Adhesive-backed zip tie anchor mounts (cable saddle clips)** on the back face of
  the panel hold harness runs cleanly without drilling additional holes. Clean the
  panel surface, stick the mount, route the zip tie through. Prevents harness from
  sagging or shifting behind the panel.
  Source: StreetCarJoe Race Car Wiring Pt.3.
- All relay and fuse labels must be visible from the front (or from a directed light)
  without removing the panel. If you blow a fuse at the track, you need to locate and
  replace it in under 2 minutes. Label everything before sealing the board in place.

### Power Routing to/from Relay Board
- Relay board input power: **6 AWG minimum from main ANL fuse output** to the relay
  board buss bar (not 12 AWG — voltage drop on a shared rail at startup current).
- Relay board chassis GND: chassis star stud is acceptable for the relay board ground
  (fans, pumps, body electrics). The relay board does NOT need to run its ground
  directly to the battery — only the ECU and coil packs require that. See
  `docs/harness-build.md` Power & Ground Rules section.

---

## TODO — Fill In During Build

- [ ] Confirm firewall bulkhead pass-through hole location (L/R side, height from floor)
- [ ] Measure engine bay trunk run: relay board → each sensor breakout → bulkhead
- [ ] Confirm fuel pump loom total length (battery/fuse block → Radium hanger -8AN port)
- [ ] Confirm 8HP CAN run length (ECU → ZF 8HP TCU connector)
- [ ] Confirm EWP loom length (relay board → CWA400 mounting location)
- [ ] Confirm direct battery → engine block GND cable run length (battery location → block boss)
- [ ] Confirm 4-post cutoff switch (Moroso 74108) mounting location — driver accessible or external pull cable to HPDE cage requirement
- [ ] Identify and note existing E36 body grommets and P-clip anchor points usable for custom loom retention
- [ ] Trial-fit before final sleeve: verify no contact with hot or moving parts (exhaust, steering column, shifter linkage)
- [ ] Relay board cardboard mock-up at dash — confirm 18–24" width clears dash trim and steering column before cutting final material
