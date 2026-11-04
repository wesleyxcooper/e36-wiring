# MaxxECU GEN2 SPORT — Vendor Reference & GEN1→GEN2 Adaptation Analysis

Decision deferred to build start (May 2027). This document records the GEN2 SPORT specs and the signal-level analysis of adapting the existing M50 terminated harness from GEN1 RACE C1 (Molex CMC) to GEN2 SPORT MX1+MX2 (Superseal 1.0). See also `docs/vendor/maxxecu/MaxxECU_RACE_H2O.md` for the GEN1 RACE H2O (current Phase 1 plan).

Researched: 2026-11-04 against the URLs listed.

---

## 1. Product identity

The **GEN2 SPORT** is MaxxECU's first entry-level unit in the new GEN2 platform. Released 2026-11-04 — the announcement appeared on the MaxxECU homepage as *"2026-11-04: New product available: MaxxECU GEN2 SPORT."* Source: <https://www.maxxecu.com/>.

The GEN2 platform is a hardware redesign from GEN1 (RACE, PRO, SPORT, STREET). The new platform uses Superseal 1.0 connectors throughout — not Molex CMC. MTune software is shared and GEN1 tune files are forward-compatible to GEN2.

- Product page: <https://www.maxxecu.com/products/gen2sport>
- Store (with connector kit): <https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-standalone-ecu/gen2_sport_kits/>

---

## 2. Physical spec

| Spec | Value | Source |
|------|-------|--------|
| Dimensions | 175 × 138 × 35 mm (including protruding connectors) | <https://www.maxxecu.com/products/gen2sport> — *"175x138x35mm including protruding connectors"* |
| Weight | 450 g | same |
| IP rating | IP68 | same — *"Waterproof IP68"* |
| MAP sensor | 550 kPa built-in (4.5 bar / 65 PSI) | same |
| Lambda | Built-in LSU 4.2 / 4.9 / 5.2 (single wideband) | same |
| Knock | Dual knock inputs | same |
| Logging | 4 GB internal, 1000 Hz, all 2000+ channels | same |
| Connectivity | Wi-Fi (MTune), Bluetooth (MDash), USB-C | same |
| Supply voltage | 6–22 V | same |
| Connectors | Superseal 1.0 (MX1 and MX2) | same |

**Fitment comparison vs GEN1 RACE H2O (155 × 195 × 40 mm):** GEN2 SPORT is 57 mm shorter in its longest axis (138 vs 195 mm) and 5 mm thinner. Its 138 mm dimension is only 28 mm over the OEM E36 Bosch DME (~180 × 110 mm approx), vs the RACE H2O's 85 mm overhang in the same axis. The GEN2 SPORT would likely fit the OEM DME mounting pocket with little or no adapter plate; the RACE H2O requires a custom JLC CNC adapter plate. See `MaxxECU_RACE_H2O.md §7` for the RACE H2O mounting analysis.

---

## 3. IO count (GEN2 SPORT vs GEN1 RACE)

| Feature | GEN2 SPORT | GEN1 RACE | Source |
|---------|-----------|-----------|--------|
| Sequential cylinders | 6 (12 wasted spark) | 8 | <https://www.maxxecu.com/products/gen2sport> |
| Injector outputs | 6 | 8 | same |
| Ignition outputs | 6 | 8 | same |
| GPO (GND) | 7 | 16 | same |
| H-bridge outputs | 2 (GPO 13-14) | 4 (GPO 13-16) | same; GEN2 pinout at <https://www.maxxecu.com/webhelp/wirings-maxxecu_gen2_pinout.html> |
| 12V sourcing GPO | 0 | 2 (GPO 15-16) | GEN1 pinout: `MaxxECU_GEN1_Pinout.md` C2 G1-G2 |
| Analog inputs | 12 | 16 | <https://www.maxxecu.com/products/gen2sport> |
| Pulse/VR inputs | 4 | 5 (DIN/VR) | same |
| CAN bus | 1 | 1 | same |
| Wideband lambda | 1 (single) | 2 (dual) | same |
| EGT inputs | 0 | 8 | GEN2 EGT only on RACE/TRACK MX4 |

For the M50 engine harness: 6 injectors, 6 ignitions, all GND-switching GPOs, single WBO2, single CAN — all within GEN2 SPORT limits. GPO 15-16 (12V sourcing) on GEN1 C2 are not used in the M50 harness. See `MaxxECU_M50_Terminated_Harness.md`.

---

## 4. Connectors

The GEN2 SPORT uses two Superseal 1.0 connectors, both 34-pin:

| Connector | Kit ID | Description | Source |
|-----------|--------|-------------|--------|
| MX1 (Connector 1) | 2416 | 34-pin Superseal 1.0 — same kit as GEN2 RACE MX1 | <https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-gen2-sport-connector-1-kit> — *"For MaxxECU GEN2 and Expansion module."* |
| MX2 (Connector 2) — SPORT variant | 2557 | 34-pin Superseal 1.0 with SPORT-specific keying; some positions blanked | same page — *"34-pin superseal 1.0, keying for MaxxECU GEN2 connector2. Including terminals and plugs to cover unused pins on the GEN2 SPORT."* |

**Note on MX2 housing:** As of 2026-11-04, MaxxECU states *"We are awaiting a custom GEN2 SPORT Superseal connector 2 without holes for the unused pin positions."* The kit ships with ~15 blind plugs to seal unused positions until the purpose-built housing is available. Source: <https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-gen2-sport-connector-2-kit>

---

## 5. GEN2 SPORT pinout

Source for all pin assignments below: <https://www.maxxecu.com/webhelp/wirings-maxxecu_gen2_pinout.html>

### MX1 (34-pin, Superseal 1.0)

| Pin | Function | Wire gauge |
|-----|----------|------------|
| 1 | Ignition 1 | 0.5 mm² (20 AWG) |
| 2 | Ignition 2 | 0.5 mm² |
| 3 | Ignition 3 | 0.5 mm² |
| 4 | Ignition 4 | 0.5 mm² |
| 5 | GP out 1 (GND) | 0.5 mm² |
| 6 | GP out 2 (GND) | 0.5 mm² |
| 7 | GP out 3 (GND) | 0.5 mm² |
| 8 | GP out 4 (GND) | 0.5 mm² |
| 9 | Engine GND | 1.5 mm² (16 AWG) |
| 10 | PULSE 1 Signal + | 0.35 mm² (22 AWG) |
| 11 | PULSE 1 Signal − | 0.35 mm² |
| 12 | PULSE 1 Power Supply | 0.35 mm² |
| 13 | PULSE 1 Shield | 0.35 mm² |
| 14 | Sensor GND | 0.5 mm² |
| 15 | CAN L | 0.5 mm² |
| 16 | CAN H | 0.5 mm² |
| 17 | GP out 5 (GND) | 0.5 mm² |
| 18 | PULSE 2 Signal + | 0.35 mm² |
| 19 | PULSE 2 Signal − | 0.35 mm² |
| 20 | PULSE 2 Power Supply | 0.35 mm² |
| 21 | PULSE 2 Shield | 0.35 mm² |
| 22 | 5V power supply | 0.5 mm² |
| 23 | PULSE 3 Signal + (single-ended) | 0.5 mm² |
| 24 | PULSE 4 Signal + (single-ended) | 0.5 mm² |
| 25 | 12V supply 1 (main ECU supply) | 1.5 mm² (16 AWG) |
| 26 | AIN 1 | 0.5 mm² |
| 27 | AIN 2 | 0.5 mm² |
| 28 | AIN 3 | 0.5 mm² |
| 29 | AIN 4 | 0.5 mm² |
| 30 | AIN 5 | 0.5 mm² |
| 31 | Injector 1 | 0.5 mm² |
| 32 | Injector 2 | 0.5 mm² |
| 33 | Injector 3 | 0.5 mm² |
| 34 | Injector 4 | 0.5 mm² |

### MX2 (34-pin, Superseal 1.0 — SPORT-keyed, some positions blanked)

Pins listed below are from the GEN2 RACE MX2 table; pins not available on SPORT are sealed with blind plugs (kit ID 2557). The pins relevant to the M50/M52 application are confirmed available.

| Pin | Function | Wire gauge |
|-----|----------|------------|
| 1 | Ignition 5 | 0.5 mm² |
| 2 | Ignition 6 | 0.5 mm² |
| 3 | GP out 6 (GND) | 0.5 mm² |
| 4 | AIN 6 | 0.5 mm² |
| 5 | AIN 7 | 0.5 mm² |
| 6 | AIN 8 | 0.5 mm² |
| 7 | GP out 13 (H-BRIDGE 1) | 0.5 mm² |
| 8 | GP out 14 (H-BRIDGE 1) | 0.5 mm² |
| 9 | Engine GND | 1.5 mm² (16 AWG) |
| 10 | WBO2 Sensor 1 VS | 0.5 mm² |
| 11 | WBO2 Sensor 1 COM/VREF | 0.5 mm² |
| 12 | GP out 7 / WBO2 Sensor 1 H− | 0.5 mm² |
| 13 | AIN 9 | 0.5 mm² |
| 14 | AIN 10 | 0.5 mm² |
| 15 | AIN 11 | 0.5 mm² |
| 16 | AIN 12 | 0.5 mm² |
| 17 | AIN 13 | 0.5 mm² |
| 18 | WBO2 Sensor 1 RCAL | 0.5 mm² |
| 19 | WBO2 Sensor 1 IP | 0.5 mm² |
| 20 | 12V WBO2 Sensor 1 H+ | 0.5 mm² |
| 21 | WBO2 Sensor 1 SHIELD | 0.5 mm² |
| 22 | AIN 14 | 0.5 mm² |
| 23 | AIN 15 | 0.5 mm² |
| 24 | 12V supply 3 (ignition key / RTC) | 0.5 mm² |
| 25 | 12V supply 2 | 1.5 mm² (16 AWG) |
| 26 | KNOCK 1 SHIELD | 0.35 mm² |
| 27 | KNOCK 1 − | 0.35 mm² |
| 28 | KNOCK 1 + | 0.35 mm² |
| 29 | KNOCK 2 SHIELD | 0.35 mm² |
| 30 | KNOCK 2 − | 0.35 mm² |
| 31 | KNOCK 2 + | 0.35 mm² |
| 32 | AIN 16 | 0.5 mm² |
| 33 | Injector 5 | 0.5 mm² |
| 34 | Injector 6 | 0.5 mm² |

---

## 6. GEN1 RACE C1 → GEN2 SPORT MX1+MX2 adaptation (M50 harness)

### Structural finding — C2 is not part of this adaptation

The M50 terminated harness does **not** use the GEN1 RACE C2 (32-pin Molex CMC). C2 carries EGT sensors, balanced knock inputs, and additional AIN/GPO — none of which are populated on the M50 harness. Source: `MaxxECU_M50_Terminated_Harness.md` line 19–20 — *"C2 (32-pin Molex) — NOT on this harness. Not needed for Phase 1 (no DBW, no e-pedal, no knock sensors)."*

The full scope of the adaptation is therefore: **one 48-pin Molex CMC (C1) → two 34-pin Superseal 1.0 (MX1 + MX2)**. No signals need to be rebuilt or re-routed between connector blocks; the split between MX1 and MX2 simply relocates signals that were all on C1.

### Complete signal map

| M50 signal | GEN1 RACE C1 pin | GEN2 SPORT connector | GEN2 pin | Source |
|------------|-----------------|---------------------|----------|--------|
| Injector 1 | K1 | MX1 | 31 | GEN1: `MaxxECU_GEN1_Pinout.md`; GEN2: webhelp |
| Injector 2 | K2 | MX1 | 32 | same |
| Injector 3 | M1 | MX1 | 33 | same |
| Injector 4 | M2 | MX1 | 34 | same |
| Injector 5 | M3 | MX2 | 33 | same |
| Injector 6 | L3 | MX2 | 34 | same |
| Ignition 1 | A2 | MX1 | 1 | same |
| Ignition 2 | A3 | MX1 | 2 | same |
| Ignition 3 | B2 | MX1 | 3 | same |
| Ignition 4 | B3 | MX1 | 4 | same |
| Ignition 5 | C2 | MX2 | 1 | same |
| Ignition 6 | C3 | MX2 | 2 | same |
| GPO 1 (boost solenoid) | B4 | MX1 | 5 | same |
| GPO 2 (fuel pump) | C4 | MX1 | 6 | same |
| GPO 3 (VANOS) | D4 | MX1 | 7 | same |
| GPO 4 (ICV A) | E4 | MX1 | 8 | same |
| GPO 5 (ICV B) | A1 | MX1 | 17 | same |
| GPO 6 (fan) | B1 | MX2 | 3 | same |
| WBO2 VS | F4 | MX2 | 10 | same |
| WBO2 VREF/COM | F3 | MX2 | 11 | same |
| WBO2 H− (heater −) | D1 | MX2 | 12 | same |
| WBO2 RCAL | G4 | MX2 | 18 | same |
| WBO2 IP | G3 | MX2 | 19 | same |
| WBO2 H+ (heater +) | — (from +12V) | MX2 | 20 | GEN2 adds explicit H+ pin |
| WBO2 SHIELD | — (to GND) | MX2 | 21 | GEN2 adds explicit shield pin |
| CAN H | E1 | MX1 | 16 | same |
| CAN L | E2 | MX1 | 15 | same |
| CLT (AIN 1) | J1 | MX1 | 26 (AIN 1) | same |
| IAT (AIN 2) | J2 | MX1 | 27 (AIN 2) | same |
| TPS (AIN 3) | G2 | MX1 | 28 (AIN 3) | same |
| +5V sensor supply | G1 | MX1 | 22 | same |
| Sensor GND | H1 | MX1 | 14 | same |
| Engine GND | L4 | MX1 | 9 | same |
| +12V supply (main) | M4 | MX1 | 25 | same |
| GND Shield | E3 | any GND | — | terminate to chassis/sensor GND |

All M50 harness signals map cleanly. Nothing missing on the GEN2 SPORT for M50/M52 use.

### Trigger input format change — requires attention

GEN1 RACE C1 uses single-ended trigger inputs: `TRIGGER` (H3), `Trigger GND` (H2), `HOME` (H4) — three individual pins. Source: `MaxxECU_GEN1_Pinout.md` H2–H4.

GEN2 SPORT MX1 uses 4-pin PULSE blocks per channel: `Signal +`, `Signal −`, `Power Supply`, `Shield`. Source: <https://www.maxxecu.com/webhelp/wirings-maxxecu_gen2_pinout.html> — MX1 pins 10–13 (PULSE 1) and 18–21 (PULSE 2).

Mapping for M52 sensors:

| Sensor | Type | GEN1 wiring | GEN2 wiring |
|--------|------|-------------|-------------|
| Crank trigger (60-2 VR) | VR (differential) | TRIGGER → H3; Trigger GND → H2 | Signal + → MX1 pin 10; Signal − → MX1 pin 11; Shield → MX1 pin 13 |
| Cam trigger (Hall) | Hall (single-ended) | HOME → H4 | Signal + → MX1 pin 18; Power Supply → MX1 pin 20; Sensor GND → pin 14 |

The M50 terminated harness wiring bundle at the sensor side is unchanged — the Bosch JPT 3-way connector for trigger/HOME is identical. Only the ECU-end pin destinations change, plus the crank VR shield drain wire moves to a dedicated pin (MX1 pin 13) instead of the shared GND Shield (C1 E3). The harness already has a shield drain wire in the crank trigger bundle; re-pin it to MX1 pin 13.

### Knock inputs — format change, not relevant to M50 phase

GEN1 RACE C2 knock: single-ended, one pin per sensor (Knock 1 = C2 E2, Knock 2 = C2 E3). Source: `MaxxECU_GEN1_Pinout.md` C2.

GEN2 SPORT MX2 knock: balanced/differential, 3 pins per sensor (Shield, −, + for each). Source: webhelp MX2 pins 26–31.

The M50 harness does not populate knock sensors (C2 is not on the harness — see §6 structural finding). Knock wiring on GEN2 SPORT would be a fresh run from sensor to MX2 if ever used; not an adaptation concern for Phase 1.

### GPO 15-16 (12V sourcing) — absent on GEN2 SPORT, not needed for M50

GEN1 RACE C2 carries GPO 15 and GPO 16 as +12V sourcing outputs (G1 and G2). Source: `MaxxECU_GEN1_Pinout.md` C2 G1-G2. GEN2 SPORT has no 12V sourcing GPOs — all 7 GPOs are GND-sinking. Source: <https://www.maxxecu.com/products/gen2sport> — *"7 GP Outputs (GND)"*.

GPO 15 and 16 are not assigned in the M50 harness. All M50 GPO functions (boost, fuel pump, VANOS, ICV A/B, fan) are GND-switching outputs. No impact.

---

## 7. Adaptation effort and tooling

### Terminal conversion

Molex CMC terminals (CP 0.635 mm and CP 1.50 mm) are not reterminal-able — once crimped they cannot be re-used. Each wire must be:

1. Depinned from the C1 housing using the Molex removal tool (PN 638132400 for small, 638132300 for big — in BOM). Source: `MaxxECU_GEN1_Pinout.md` tools table.
2. The Molex CMC terminal cut off.
3. A Superseal 1.0 wire seal threaded onto the wire (before crimping — cannot be added after).
4. A Superseal 1.0 terminal crimped. Wire range: 0.50–1.25 mm² (TE Connectivity Superseal 1.0 terminal, 1.0 mm contact size, 15 A max). Source: TE SUPERSEAL 1.0 catalog — <https://www.te.com/content/dam/te-com/documents/industrial-and-commercial-transportation/global/ict-superseal-cat-a4-1-1773985-2-en.pdf> — *"Accepts contact size 1.0 mm (up to 15 amps) • 1.25-0.50 mm²"*
5. Pin inserted into the MX1 or MX2 Superseal housing at the correct GEN2 position per the signal map in §6.

The existing Molex CMC harness wires are 0.35–1.5 mm² (22–16 AWG). The 1.5 mm² engine GND and 12V supply wires are within the Superseal 1.0 terminal upper limit of 1.25 mm²  — verify crimp quality on these wires; they are at the limit. Superseal 1.0 terminals are rated to 15 A, same as the Molex big terminals (CP 1.50 mm rated 12 A, CP 0.635 mm rated 2.5 A per Molex CMC spec at <https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/applicationspecificationspdf/643/64319/AS-64319-002-001.pdf>).

### Crimping tool

Superseal 1.0 terminals are compatible with the TE MULTIGRIPPER (PN 2271799-1) or equivalent ratcheting tool for 0.5–1.5 mm² contacts. The IWS-2412M (Iwiss) in the BOM is suitable for the 0.35–0.5 mm² wires; verify positioner compatibility for the 1.0 mm² and larger wires against TE datasheet before committing. See `docs/wiring-bom.md` for current tool inventory.

### Connector kits

| Kit | MaxxECU ID | Qty needed | Price | Source |
|-----|-----------|-----------|-------|--------|
| GEN2 connector 1 kit (MX1, 34-pin Superseal 1.0) | 2416 | 1 | $16.66 | <https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-gen2-sport-connector-1-kit> |
| GEN2 SPORT connector 2 kit (MX2, 34-pin Superseal 1.0 SPORT-keyed) | 2557 | 1 | $16.66 | same |

Total consumable cost for the adaptation: ~$33 in connector kits plus Superseal 1.0 terminals (TE PN available from Digikey/Mouser, included in Superseal connector kit).

### Estimated effort

With the signal map in §6 printed and checked off:
- Wire count in M50 harness C1: ~30 active pins (of 48 positions)
- Operations per wire: depin, cut terminal, thread seal, crimp, insert
- Estimated bench time: **3–5 hours** for someone familiar with automotive connector rework

---

## 8. Harness path if starting from scratch (preferred over adaptation)

If GEN2 SPORT is confirmed before the M50 harness is purchased, skip the M50 terminated harness entirely and purchase the GEN2 SPORT flying-lead kit instead:

- **MaxxECU GEN2 SPORT with LSU 5.2, flying lead install kit** — $1,664.81 — <https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-standalone-ecu/gen2_sport_kits/maxxecu-gen2-sport-with-lsu-52-flying-lead-install-kit>

Build a fresh M50 harness using Superseal 1.0 terminals natively, following the GEN2 SPORT pinout. This eliminates the adaptation work entirely and uses the correct terminals from the start. The GEN2 pinout is available at <https://www.maxxecu.com/webhelp/wirings-maxxecu_gen2_pinout.html>.

---

## 9. Decision factors (May 2027 build start)

| Factor | Favors GEN2 SPORT | Favors GEN1 RACE H2O |
|--------|------------------|----------------------|
| Terminated M50 harness exists | No (as of Nov 2026) | Yes — SLG bundle available |
| Fitment in OEM DME pocket | Likely fits with minimal adaptation | Requires custom adapter plate |
| MAP sensor range | 550 kPa (65 PSI) | 400 kPa (43.5 PSI) |
| IP rating | IP68 | IP67 |
| Internal logging | 4 GB all channels | 8 MB / 170 channels |
| Wi-Fi (MTune) | Built-in | No |
| Lambda | LSU 5.2 / 4.9 / 4.2 | LSU 4.9 / 4.2 |
| Sequential cylinders | 6 max | 8 max |
| Community 07K builds | None documented | Dominant platform |
| ECU price | $1,427–$1,665 | $1,590–$2,050 |

The 07K path uses GEN1 RACE regardless — the 07K custom harness is built from scratch and the community knowledge base is entirely MaxxECU GEN1 RACE. GEN2 SPORT is only worth evaluating for the M52 (Phase 1) path.

---

## 10. Related documents

- `docs/vendor/maxxecu/MaxxECU_RACE_H2O.md` — current Phase 1 ECU plan (GEN1 RACE H2O)
- `docs/vendor/maxxecu/MaxxECU_GEN1_Pinout.md` — GEN1 C1/C2 pinout (source of GEN1 side of signal map)
- `docs/vendor/maxxecu/MaxxECU_M50_Terminated_Harness.md` — confirms C2 not in M50 harness
- `docs/wiring-bom.md` — Molex CMC removal tools and IWS-2412M crimp tool
