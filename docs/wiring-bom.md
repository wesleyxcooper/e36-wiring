# Wiring BOM — Consolidated by System

Aggregated from all WireViz harness source files.
Source harnesses: `maxxecu-m52.wv` · `maxxecu-07k.wv` · `firewall-bulkhead.wv` · `power-distribution.wv` · `epedal-bmw-e46.wv` · `epedal-hella-6pv.wv` · `fuel-pump-hanger.wv` · `ewp-controller.wv` · `body-x20.wv` · `8hp-can.wv` · `gauge-s-can.wv` · `dct-shifter.wv` · `pst-f1-sensor.wv` · `atf-temp-sensor.wv` *(optional)*

> **⚠️ TODO** = placeholder in source `.wv` — gauge, model, or pin not yet confirmed. Buy only after resolving.
> **🔁 shared** = appears in multiple harnesses, buy once.
> All wire lengths include ~10% slack. Add more for complex routing runs.

---

## System 1 — Power Distribution

*Source: `power-distribution.wv`*

> **Architecture:** Ecumaster PMU16 replaces relay board, blade fuse block, and Crydom D1D40 SSR. MaxxECU controls PMU16 via CAN. Load `MaxxECU.canx` template in PMU software before first run.

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Battery positive terminal | Ring terminal, trunk/engine bay |
| 1 | Battery negative terminal | Ring terminal — chassis stud. Engine block direct cable is **optional** (see below) |
| 1 | Chassis ground stud, M8 | Engine bay — PMU16 GND lug + body electrical returns. MaxxECU engine GND goes to cylinder head (in ECU harness, not here) |
| 1 (optional) | Engine block ground stud, M8 | **Optional** — only if running a dedicated battery→engine block direct cable (belt-and-suspenders; not required while factory M52 bonding straps are intact and clean) |
| 1 (optional) | **4-post battery cutoff switch — Moroso 74108** ([Amazon](https://www.amazon.com/Moroso-74108-Battery-Alternator-Disconnect/dp/B01GWD2XUS) ~$101 / [moroso.com](https://www.moroso.com/battery-and-alternator-disconnect-switch74108/) $113) | **Optional** — not required on a dual-duty street/drift car with a working ignition key. Install only if HPDE org or track rules require it. If installed: must be 4-post (NOT 2-post). |
| 2–3 | **Amphenol Radlok 8mm — M8×1.25 Male** | [Racing History Co.](https://www.racinghistorycompany.com/product/radlok-8mm-stud-m8x1-25-male/), ~$15 CAD ea — thread into cylinder head and engine block GND strap bosses. Tool-free press-lock disconnect. Speeds up M52→07K swap. Secure cable within 3 cm; inspect annually. |
| 1 | **Amphenol Radlok 8mm — M8×1.25 Female** | [Racing History Co.](https://www.racinghistorycompany.com/product/radlok-8mm-stud-m8x1-25-female/), ~$22 CAD — threads onto M8 B+ stud of 07K alternator (`07K 903 023 A`). Tool-free disconnect at alternator removal. |
| 1 | **Ecumaster PMU16** ([ecumasterusa.com](https://ecumasterusa.com/products/ecumaster-pmu16-power-management-unit) ~$500) | 16-output MOSFET PDM. Replaces relay board + fuse block + Crydom SSR. Outputs: O1 ECU logic · O2 coil/inj · O3 fan (PWM) · O4 pump (PWM) · O5+O14 EWP parallel (50A combined) · O6 condenser fan · O7 AC relay coil · O8 EPS Controller (Phase 3). Connector: 39-way Sicma/FCI. Power via M6 BATT+ stud. Manual: [ecumaster.com/files/PMU/PMU_Manual.pdf](https://www.ecumaster.com/files/PMU/PMU_Manual.pdf) · Pinout: [PMU-16_Pinout_v1.2.pdf](https://www.ecumaster.com/files/PMU/PMU-16_Pinout_v1.2.pdf) |
| 1 | **Ecumaster USB-CAN adapter** ([ecumasterusa.com](https://ecumasterusa.com) ~$85) | Required for initial PMU16 programming. One-time setup tool. |
| 1 | Inline ANL or MAXI fuse holder, **150A** | Channel peaks: ECU 8A + coil/inj 20A + fan 15A + pump 14A + EWP 35.5A + condenser 12A + AC coil 0.2A = 104.8A worst-case all-on. ×1.2 headroom = 125.8A → **150A** (matches PMU16 M6 stud 150A continuous rating). Blue Sea 5191 MRBF 150A or equiv. |
| 1 | IGN switched 12V source — **X20 pin 21** (GN, green wire) | Confirmed: X20 pin 21 = ignition switch terminal 15 = IGN-switched +12V. Green wire. Feeds PMU16 39-pin pin 7 (+12V SW on/off sense). Fuse at X20 source: 5A. Source: E36 ETM / r3vlimited / megasquirt.325ix.com X20 pinout. |
| 1 | **SPAL 30102049** radiator fan, 16" puller, ~$130 | 16-inch puller, ~2070 CFM, ~15A, 2-wire brushed motor. Standard for turbo E36 track/competition builds (Zionsville competition kit, M5board SPAL install thread). PMU16 O3 control modes: **(a) on/off** — O3 fires fully when CLT threshold hit, recommended starting point; **(b) direct PWM** — PMU16 O3 outputs 4–400 Hz PWM (confirmed from PMU_Manual.pdf); brushed motor accepts this natively for variable speed, audible hum at partial duty is normal. 30102049 is explicitly listed as compatible with SPAL FAN-PWM-V3 module if a standalone temp-based controller is preferred instead. Source: PMU16 manual [ecumaster.com/files/PMU/PMU_Manual.pdf](https://www.ecumaster.com/files/PMU/PMU_Manual.pdf) · [a1electric.com SPAL FAN-PWM-V3 compat list](https://www.a1electric.com/spal/specs/FAN-PWM-V3.pdf) · [zionsvilleautosport.com/bmw-e36-competition-cooling-kit](https://www.zionsvilleautosport.com/bmw-e36-competition-cooling-kit/) |

### Cables

> ⚠️ All cable runs in `power-distribution.wv` are stubs — gauge and length TBD pending physical routing measurement. Do not buy until resolved.

| Run | Color | Gauge | Est. Length | Notes |
|-----|-------|-------|-------------|-------|
| BATT_POS → ANL fuse | RD | 4 AWG welding cable | TBD | Battery + → main ANL fuse (within 18 in of battery) → PMU16 M6 stud |
| **(optional) BATT_POS → cutoff switch → ANL fuse** | RD | 4 AWG welding cable | TBD | If cutoff switch installed: BATT_POS → CUTOFF_4POST → ANL fuse → PMU16 M6 stud |
| ANL fuse → PMU16 M6 stud | RD | 4 AWG welding cable | TBD | Fused batt+ directly to PMU16 power stud (replaces fuse block feed) |
| PMU16 GND lug → chassis stud | BK | 4–8 AWG | TBD | PMU16 body GND lug → chassis ground stud M8. Keep short. All PMU output return currents flow here. |
| BATT_NEG → chassis stud | BK | 4 AWG welding cable | TBD | Battery − → chassis ground stud M8 — body electrical returns |
| **(optional) BATT_NEG → engine block (direct)** | BK | 4 AWG welding cable | TBD | Optional dedicated battery negative → engine block cable. Not required while factory M52 bonding strap is clean. |
| IGN +12V → PMU16 pin 7 (+12V SW) | RD | 18 AWG | TBD | IGN-switched +12V → PMU16 on/off sense. Fuse at source: 5A. |
| PMU16 CAN2 H/L → MaxxECU CAN1 H/L | GY/PU | 22 AWG shielded twisted pair | TBD | PMU16 pins 24/34 → MaxxECU CAN1H/CAN1L. Drain at MaxxECU end only. Route away from coil/injector wires. |
| PMU16 O1 → ECU logic +12V | RD | 16 AWG | TBD | O1 (pin 38, 25A) → MaxxECU 12-pin pin 7 |
| PMU16 O2 → coil+inj +12V | RD | 12 AWG | TBD | O2 (pin 39, 25A) → MaxxECU 12-pin pin 1 |
| PMU16 O3 → SPAL fan | RD | 12 AWG | TBD | O3 (pin 26, 25A PWM) → fan motor + terminal |
| PMU16 O4 → fuel pump (PWM) | RD | 12 AWG | TBD | O4 (pin 13, 25A PWM) → Radium hanger pump+ stud. Replaces Crydom SSR. |
| PMU16 O5 → EWP supply (A) | RD | 8 AWG | TBD | O5 (pin 12, 25A) → CWA400 pin 3 in parallel with O14. Join at pin 3 terminal. |
| PMU16 O14 → EWP supply (B) | RD | 8 AWG | TBD | O14 (pin 14, 25A) → CWA400 pin 3 in parallel with O5. 50A combined handles CWA400 35.5A. Configure O5+O14 as parallel pair in PMU software. |
| PMU16 O6 → condenser fan | RD | 12 AWG | TBD | O6 (pin 11, 15A) → condenser fan motor + terminal. CAN-commanded when AC on. |
| PMU16 O7 → AC relay coil 86 | RD | 18 AWG | TBD | O7 (pin 10, 15A) → ac-compressor.wv AC_RELAY pin 86. Low current (~200mA). AC switch feeds MaxxECU DIN directly — MaxxECU CAN-commands O7. |

---

## System 2 — Engine Management (M52 Phase 1)

*Source: `maxxecu-m52.wv`*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **Molex 48-pin C1** — MaxxECU RACE/STREET/SPORT/PRO connector 1 | [MaxxECU store ID 925](https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-street-or-sport-or-race-or-pro-connector-1-48-pin-molex), $33.41 — **REQUIRED** (all current harnesses). Special Molex crimp tool required (63811-9200 primary). Pin assignments in `maxxecu-m52.wv` / `maxxecu-07k.wv`. |
| 1 | **Molex 32-pin C2** — MaxxECU RACE connector 2 | [MaxxECU store ID 1982](https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-mini-or-race-c2-or-pro-c4-32-pin-molex), $32.25 — **OPTIONAL / DEFER**: C2 carries EGT 1–8 (A–D rows), knock 2, AIN 5–6, GPO 15/16, and DBW motor 1/2 H-bridge outputs. None of these are used in Phase 1/3 harnesses as currently designed. Purchase only if adding EGT probes or need the extra AIN/GPO capacity. Same crimp tools as C1. |
| 1 | Bosch JPT 3-way | M52 60-2 VR crank trigger |
| 1 | BMW `12141726590` 3-pin | M52 VANOS cam Hall sensor |
| 1 | Bosch JPT 2-way | M52 coolant temp NTC |
| 1 | OEM M52 2-pin | Intake air temp NTC |
| 1 | OEM M52 3-pin | Throttle position sensor (0–5V) |
| 1 | Bosch JPT 2-way | M52 VANOS intake solenoid |
| 1 | Superseal 2-way | Turbosmart boost solenoid (2-port PWM) |
| 1 | Bosch PST-F1 4-pin | Dual oil temp + pressure sensor |
| 1 | 3-pin inline | Ethanol content / flex fuel sensor (digital) |
| 1 | SPDT relay socket | SPAL fan relay (cross-ref `power-distribution.wv`) |
| 1 | SPDT relay socket | Fuel pump relay (cross-ref `power-distribution.wv`) |
| 1 | Splice / junction, 4-pin | CAN H/L shared bus junction |
| 1 | DCT shifter paddle harness connector | 4-wire E36 fitment |
| 1 | MaxxECU 8HP GEN1 CAN harness connector | ZF 8HP70 transmission CAN |
| 1 | Gauge.S E36 CAN input, 2-pin | Cross-ref `body-x20.wv` |
| 3 | Ring terminal | Batt +12V (fused), chassis GND, IGN switched +12V |

### Cables

> Gauge and per-run lengths are stubs in `maxxecu-m52.wv` — buy after measuring physical routing. Colors are defined in the source file and visible in the SVG diagram.

| Run | Color(s) | Type | WV Total | Notes |
|-----|----------|------|----------|-------|
| W_CAN, W_CAN_8HP, W_CAN_GAUGES | YE/GN (CAN H/L convention) | 2-wire twisted | 6.9 m total across all 2-wire runs | Use shielded twisted pair for CAN runs |
| W_CLT, W_IAT, W_VANOS, W_FAN, W_FUELPUMP, W_BOOST | RD/BK or signal-specific | 2-wire | included in above total | |
| W_CRANK, W_CAM, W_TPS | varies | 3-wire | 3.3 m total | |
| W_FLEXFUEL | — | 3-wire | included above | |
| W_PST_F1, W_SHIFTER | — | 4-wire | 2.1 m total | |
| W_COIL_PWR, W_ECU_PWR, W_ENGINE_GND | RD, RD, BK | single-wire | ⚠️ stub (0 m) | Lengths TBD — size based on fused current |

---

## System 3 — Drive-by-Wire: E-Pedal

*Source: `epedal-bmw-e46.wv` (primary) · `epedal-hella-6pv.wv` (RHD fallback — install one, not both)*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **BMW E46 Accelerator Pedal Module** | PN `35426786282` (manual) / `35426786281` (auto) — used, ~$80–120. See `docs/dbw-pinouts.md` for sourcing table. |
| — | *OR* **Hella 6PV010946-141** | RHD fallback — standalone floor-mount, no OEM pedal box, ~$80–120 new |
| 1 | Deutsch Autosport AS-series bulkhead — **cabin side** | Size 20 contacts, **pins 72-77** reserved for e-pedal (GND1/GND2/VCC2/APS1/VCC1/APS2) |
| 1 | Deutsch Autosport AS-series bulkhead — **engine side** | Size 20 contacts, **pins 72-77** — engine side of same pass-through, wires to MaxxECU APS AIN |
| 1 | MaxxECU RACE CMC — APS analog inputs | 6-pin CMC section — AIN, 5V SENS OUT, SGND — pins TBD |

### Cables

| Run | Colors (pin order) | Gauge | Length | Shielded | Notes |
|-----|--------------------|-------|--------|----------|-------|
| Pedal → bulkhead (cabin side) | BK, BK, RD, RD, GN, YE | 24 AWG | 0.8 m | Yes — drain at MaxxECU end only | Pin1=APS1 GND, Pin2=APS2 GND, Pin3=VCC2, Pin4=APS1 sig, Pin5=VCC1, Pin6=APS2 sig |
| Bulkhead → MaxxECU (engine side) | BK, BK, RD, RD, GN, YE | 24 AWG | 0.4 m | Yes — drain here (this end only) | Same color order as cabin side — label both ends |

> **Hella fallback color order differs:** BK, RD, YE, BK, RD, GN — label both ends clearly, do not assume same pinout as E46 variant.

---

## System 4 — Fuel System

*Source: `fuel-pump-hanger.wv`*

> Replaces the M52 in-tank Walbro 255 + relay from Phase 1 with the Radium 20-1170 hanger + F90000267 driven by PMU16 O4 direct (PWM). No DC SSR — PMU16 O4 (25A, PWM-capable) sources current from its BATT+ stud and runs 12 AWG through the tunnel to the hanger. MaxxECU commands speed via CAN to PMU16. No re-work at Phase 3 07K swap.

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | PMU16 O4 output stub (engine bay) | 🔁 Shared with power-distribution.wv — RADIUM_HANGER_STUB. PMU16 O4 (PHYS pin 13, 25A PWM). |
| 1 | Radium Engineering 20-1170 hanger terminals | Top-plate external studs (pump+ and pump−) — anti-rotation, hermetically sealed. Comes with hanger kit, not sourced separately. |
| 1 | Chassis ground stud | 🔁 Shared with power distribution |

### Cables

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| CABLE_PWR (PMU16 O4 → hanger pump+) | RD | 12 AWG | 4.0 m | No | Full run engine bay → fuel tank (est. 3.5–4m; measure on car). Route through transmission tunnel. No separate fuse — PMU16 O4 overcurrent protection handles this. |
| CABLE_GND (hanger pump− → chassis GND) | BK | 12 AWG | 0.5 m | No | Dedicated ground — do not share with ECU sensor GND. Ring terminals both ends. |

---

## System 5 — Cooling: Electric Water Pump

*Source: `ewp-controller.wv`*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **Pierburg CWA400 (PWM version)** | Kostal 2+2 connector, 150 LPM @ 0.85 bar — installed in lower radiator hose |
| 1 | 40A automotive relay | Bosch `0 332 002 150` or equiv — standard 4- or 5-pin |
| 1 | Battery positive terminal | 🔁 Shared |
| 1 | Chassis ground stud | 🔁 Shared |
| 1 | MaxxECU RACE GPO | 🔁 Shared — GPO pin TBD |

### Cables

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| CABLE_PWR_IN (BATT+ → relay pin 30) | RD | 10 AWG | 0.5 m | No | Fused 40A within 30 cm of battery. Ring terminal at battery. |
| CABLE_PWR_OUT (relay pin 87 → CWA400 Pin 3) | RD | 10 AWG | 1.5 m | No | Switched +12V pump supply. 35.5A nominal draw — 10 AWG minimum. |
| CABLE_GND (CWA400 Pin 4 → chassis GND) | BK | 10 AWG | 1.5 m | No | Dedicated ground. 10 AWG minimum. |
| CABLE_PWM (MaxxECU GPO → CWA400 Pin 1) | VT | 22 AWG | 2.0 m | Preferred | PWM signal (680 Hz). Drain at ECU end only. Keep from coil wires. |
| CABLE_RELAY_COIL wire 1 (relay pin 86 → IGN +12V) | GN | 18 AWG | 0.5 m | No | Relay coil supply. |
| CABLE_RELAY_COIL wire 2 (relay pin 85 → chassis GND) | BK | 18 AWG | 0.5 m | No | Relay coil return. |

---

## System 6 — Body / Instruments

*Source: `body-x20.wv`*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | BMW E36 X20 — cabin side, 25-pin | OEM firewall bulkhead — body harness side |
| 1 | BMW E36 X20 — engine bay side, 25-pin | OEM firewall bulkhead — engine side |
| 1 | Gauge.S E36 PNP cluster connector, 6-pin | Direct OEM cluster replacement |
| 1 | Alternator terminal, 07K D+ | `07K903023A` charge excite — D+ signal |
| 1 | MaxxECU 16-pin aux connector | GPO 8 / TACHO output |
| 1 | MaxxECU GPO | Check engine light drive |
| 1 | OEM oil pressure switch | Simple on/off, ~0.5 bar |
| 1 | CAN bus splice, 2-pin | MaxxECU CAN → Gauge.S cluster |

### Cables

> Colors defined in `body-x20.wv` and visible in diagram. Gauges TBD — these are low-current signal runs (22–24 AWG typical).

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| W_TACHO, W_TACH_BODY | — | 22 AWG (TBD) | ~1.0 m | No | Tacho signal — MaxxECU GPO 8 → X20 |
| W_CHECK_ENG | — | 22 AWG (TBD) | ~0.5 m | No | Check engine light drive |
| W_OIL_PRESS | — | 22 AWG (TBD) | ~0.5 m | No | OEM oil pressure switch signal |
| W_IGN_POWER | — | 22 AWG (TBD) | ~0.5 m | No | IGN-switched power reference |
| W_ALT_D_PLUS | — | 22 AWG (TBD) | ~0.6 m | No | Alternator D+ charge excite |
| W_GAUGES_CAN (CAN H/L) | YE/GN | 22 AWG | 2.5 m | Preferred | MaxxECU CAN → Gauge.S cluster. Twisted pair. |

---

## Cross-Harness Shared Items (buy once)

These connectors/termination points appear in multiple harness BOMs — source once, connect to multiple circuits.

| Item | Used In |
|------|---------|
| Battery positive terminal (ring) | Power dist · EWP · Fuel pump |
| Chassis ground stud (M8, engine bay) | Power dist · EWP · Fuel pump |
| IGN switched 12V source | Power dist · Fuel pump |
| MaxxECU RACE GPO (GND-sinking) | EWP (GPO-PWM) · Fuel pump (GPO-PWM) · Fan/pump relays (Power dist) |
| Deutsch Autosport AS-series bulkhead | E-pedal (6 pins) · Firewall bulkhead master harness (all engine-crossing signals) |

---

## System 7 — VW 07K Engine Harness (Phase 3)

*Source: `maxxecu-07k.wv`*

> Phase 3 engine harness — replaces M52 engine-side mating plug. MaxxECU ECU, 12-pin, and 16-pin connectors carry over unchanged.

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Deutsch AS79 jam nut plug — engine side (07K) | Replaces M52 mating plug at bulkhead; same pin-numbering |
| 5 | Bosch EV14 / USCAR injector pigtail, 2-pin | Replace M50 harness EV1 ends with EV14 (ID1050x). PN `0 280 156 127` pigtail or equivalent |
| 5 | VAG 4-way COP connector | IGN 1-5 ignition coils (07K firing order 1-2-4-5-3) |
| 1 | VW 07K crank VR sensor, 3-pin | ⚠️ TODO: confirm exact body (Bosch Kombi-F or similar) at install |
| 1 | VW 07K cam Hall sensor, 3-pin | ⚠️ TODO: confirm exact body at install (+5V type — different from M52 +12V) |
| 1 | VW 07K CLT sensor connector | ⚠️ TODO: confirm connector body at install |
| 1 | VW 07K IAT sensor connector | ⚠️ TODO: confirm connector body at install |
| 1 | VW 07K DBW throttle body connector | ⚠️ TODO: confirm 6-pin body (Motor+/Motor−/TPS1+TPS2 +5V/GND) at install |
| 2 | Bosch flat knock sensor connector, 1-pin | KS1 + KS2 (Bosch flat-type, M8 mount) — signal only; GND via mounting bolt |
| 1 | Bosch LSU 4.9 6-way connector | WBO2 — same as M52 harness (new bung in 07K manifold) |
| 1 | Bosch PST-F1 4-pin | 🔁 Same as M52 — new mount on 07K oil housing iABED M10×1.0 port |
| 1 | Superseal 2-way | 🔁 Same boost solenoid as M52 |
| 1 | 3-pin inline | 🔁 Same Continental flex fuel sensor as M52 |

### Cables (additions over M52)

| Run | Color(s) | Gauge | Length | Shielded | Notes |
|-----|----------|-------|--------|----------|-------|
| DBW TB Motor +/− | OG, VT | 20 AWG | 0.5 m ea | No | H-bridge output — 20 AWG min (3A). Verify polarity before crimping. |
| DBW TB TPS 4-wire | RD, BK, WH, GN | 22 AWG | 0.5 m | Preferred | +5V, GND, TPS1, TPS2 signals |
| Knock sensor 1 signal | WH | 22 AWG | 0.4 m | Preferred | KS1 signal wire; shield drain at ECU end |
| Knock sensor 2 signal | WH | 22 AWG | 0.6 m | Preferred | KS2 signal wire |
| Knock GND | BK | 22 AWG | 0.5 m | No | Shared knock GND (via bulkhead pin 71) |

---

## System 8 — Firewall Bulkhead

*Source: `firewall-bulkhead.wv`*

> Deutsch Autosport AS79 79-way firewall pass-through. Cabin side is permanent. M52 and 07K each have their own engine-side mating plug.

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Deutsch Autosport AS79 panel-mount receptacle | Cabin side — permanent installation |
| 1 | Deutsch AS79 jam nut plug — M52 engine side | Phase 1 mating plug; ~59 pins assigned, remainder cavity-plugged |
| 1 | Deutsch AS79 jam nut plug — 07K engine side | Phase 3 mating plug; same pin numbers as M52 for pins 1-53 + adds pins 72-77 (APS) |
| — | Deutsch AS79 size-20 contacts (sockets) | Cabin side contacts — source with AS79 housing kit |
| — | Deutsch AS79 size-20 contacts (pins) | Engine-side mating plug contacts |
| — | Deutsch AS79 cavity plugs | Seal unused pins on both sides — required for IP67 rating |

---

## System 9 — CAN Harnesses, DCT Shifter, PST-F1

### 9A — ZF 8HP70 TCU CAN (`8hp-can.wv`)

| Qty | Item | Notes |
|-----|------|-------|
| 1 | MaxxECU 8HP GEN1 CAN harness | Ships from MaxxECU — covers TCU power/GND/CAN. Bulkhead pins 2/3/9/47/48 |

> Harness sourced as a unit from MaxxECU — no individual cable spec needed.

### 9B — Gauge.S CAN (`gauge-s-can.wv`)

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| MaxxECU CAN 1 → Gauge.S, CAN H | YE | 22 AWG | ~0.5 m | Preferred — STP | 500 kbps, Default 1.3 protocol. Cabin-to-cabin, no bulkhead crossing. |
| MaxxECU CAN 1 → Gauge.S, CAN L | GN | 22 AWG | ~0.5 m | Preferred — STP | Twisted pair with CAN H above. |

### 9C — DCT Shifter Paddle (`dct-shifter.wv`)

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| UP signal | BK | 22 AWG | 1.5 m | No | Paddle UP → MaxxECU DIN 2 |
| DOWN signal | BU | 22 AWG | 1.5 m | No | Paddle DOWN → MaxxECU DIN 1 |
| GND | BN | 22 AWG | 1.5 m | No | Common GND — sensor GND |

> Wire colors match DCT Shifter OEM harness convention. Route away from ignition primaries.

### 9D — Bosch PST-F1 Sensor (`pst-f1-sensor.wv`)

> Same wiring as M52 phase — connector, gauge, and routing unchanged. New mounting location: iABED M10×1.0 port on 07K oil housing. No new wire purchases required for Phase 3.

### 9E — ATF Temperature Sensor *(optional — logging / MaxxECU cold-shift protection)*

> **Necessity:** Low. The TCH-102-T2 mechanical thermostat handles overcooling protection automatically with no ECU input. This sensor adds ATF temp to MaxxECU real-time data for logging, shift-map conditioning (cold ATF protection), and verifying cooler sizing. Most 8HP swap builds run without it. Add if you want the data; omit if simplifying.

| Qty | Item | PN / Source | Price |
|-----|------|-------------|-------|
| 1 | **Vibrant 16488** inline -8AN male→female union adapter with 1/8 NPT sensor port | [KamiSpeed](https://www.kamispeed.com/products/vibrant-8an-male-to-8an-female-union-adapter-fitting-w-1-8in-npt-port) — universal | ~$20 |
| 1 | **MaxxECU 1/8 NPT NTC temp sensor** (ID: 1280) — CLT/water/oil type | [MaxxECU store](https://www.maxxecu.com/store/engine-control-or-electronics/sensors/temperature/temperature-sensor-1-8-npt-clt-water-or-oil) | $48.39 |
| 1 | 2-way DTM socket housing (sensor connector) | MaxxECU store | $5.53 |

**Install location:** Vibrant 16488 installed in the **return line** (Setrab cooler → TCH-102-T2 → trans). Measures post-cooled ATF temp entering the transmission — more representative of actual operating temp than pre-cooler.

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| ATF sensor signal | WH | 22 AWG | ~2.5 m | Preferred | Sensor → MaxxECU AIN (TEMPERATURE) pin — 2.5k internal pullup, no external resistor needed |
| ATF sensor GND | BK | 22 AWG | ~2.5 m | (shared with above shield) | Sensor → MaxxECU Sensor GND — non-polarity sensitive sensor, either wire can be GND |

**MTune:** Analog Inputs → type = `TEMPERATURE` → calibrate to NTC curve: `-20°C = 15,462 Ω`, `130°C = 89 Ω` → assign function as extra temperature channel.

---

## TODOs / Open Items

| Item | Blocker |
|------|---------|
| All `power-distribution.wv` cable gauges and lengths | Physical routing not yet measured |
| All `maxxecu-m52.wv` cable gauges | WV stubs — need actual wire spec |
| MaxxECU C1/C2 Molex pin assignment | C1 (48-pin) + C2 (32-pin) confirmed as Molex harness connectors; specific pin assignments in `maxxecu-m52.wv` still stubs — confirm from [MaxxECU RACE pinout doc](https://www.maxxecu.com/webhelp/wirings-maxxecu_pinout.html) before building |
| GPO pin assignments (fan, pump, EWP, fuel pump PWM) | MaxxECU pin map not yet finalized |
| ~~Main fuse size~~ | ✅ **150A ANL** — confirmed from channel peak sum (104.8A × 1.2 headroom = 125.8A → 150A to match PMU16 M6 stud 150A rating). Blue Sea 5191 MRBF 150A or equiv. |
| SPAL 30102049 connector pigtail | 2-pin pigtail for chosen mounting method — confirm on delivery |
| Body-x20 wire colors and gauge | Colors visible in SVG diagram — gauge TBD |
| ~~Firewall bulkhead full pinout~~ | ✅ Done — `harnesses/firewall-bulkhead.wv` authored, outputs generated |
| ~~07K engine harness outputs~~ | ✅ Done — `maxxecu-07k.wv` authored, HTML/SVG generated |
| 07K VW connector bodies | TODO at install — crank VR, cam Hall, CLT, DBW TB connector types unconfirmed (see maxxecu-07k.wv TODOs) |
| 07K DBW TB motor polarity | TODO — verify with volt meter before final crimp |
| MaxxECU AIN assignment for APS1/APS2 | TODO — assign in MTune, update epedal-bmw-e46.wv and maxxecu-07k.wv |
| M52 wideband O2 (LSU 4.2) harness unmodeled | `maxxecu-m52.wv` has ECU_CMC pins reserved for WBO2 but no WIDEBAND connector, W_WBO2 cable, or connections block — must be authored (with `shield: true`) before Phase 1 harness build. Do not copy the 07K LSU 4.9 pinout verbatim — LSU 4.2 pin numbering needs independent confirmation. |

---

## Consolidated Wire to Buy

> Covers Systems 3–5 where gauge + color + length are fully specified. Systems 1, 2, 6 are TBD pending routing measurement — add to this table when resolved.
> Add 20% to all lengths for routing slack, drip loops, and service loops.

| Gauge | Color | Total Length (specified) | With 20% slack | Systems |
|-------|-------|--------------------------|----------------|---------|
| 8 AWG | RD (red) | 1.0 m × 2 runs | 1.2 m each | EWP O5 power + EWP O14 power (parallel, joined at CWA400 pin 3) |
| 10 AWG | BK (black) | 1.5 m | 2.0 m | EWP (ground) |
| 12 AWG | RD (red) | 4.0 m | 5.0 m | Fuel pump (PMU16 O4 → Radium hanger pump+ stud, full tunnel run) |
| 12 AWG | BK (black) | 0.5 m | 0.7 m | Fuel pump (ground) |
| 22 AWG | YE/GN (CAN) | 2.5 m | 3.0 m | Body/Gauge.S CAN twisted pair — shielded |
| 24 AWG | BK (black) | 2.4 m (×2 conductors) | 3.0 m | E-pedal GND1 + GND2 both runs |
| 24 AWG | RD (red) | 2.4 m (×2 conductors) | 3.0 m | E-pedal VCC1 + VCC2 both runs |
| 24 AWG | GN (green) | 1.2 m (×1 conductor) | 1.5 m | E-pedal APS1 signal |
| 24 AWG | YE (yellow) | 1.2 m (×1 conductor) | 1.5 m | E-pedal APS2 signal |

> **Shielded runs — full list, consolidated from all systems (previous version of this note only covered Systems 3–5):**
>
> **Required (signal-critical, always shield):**
> | Run | System | Notes |
> |-----|--------|-------|
> | Crank VR sensor (Signal+/Signal−/Shield) | M52 (Sys 2) + 07K (Sys 7) | Passive VR signal — most noise-sensitive wire in the harness. `.wv` source models shield explicitly (`CRANK_VR:3:Shield`), drains at ECU CMC pin 19 (E3). |
> | Cam Hall sensor (+5V/GND/Signal + shield) | M52 (Sys 2) + 07K (Sys 7) | Shares E3 drain point with crank shield. |
> | E-pedal cable, both legs (cabin + engine side) | E-pedal (Sys 3) | 6-conductor shielded, 24 AWG. Single-end drain at MaxxECU end only. |
> | Wideband O2 (WBO2) — VS/VREF/IP/RCAL | 07K (Sys 7) | ⚠️ **Fixed in this pass** — `maxxecu-07k.wv` W_WBO2 previously had no shield attribute despite being low-level analog signal near the turbo/exhaust bung; now `shield: true`. **M52 (Sys 2) WBO2 harness is a larger gap — entirely unmodeled in `maxxecu-m52.wv`** (no connector, cable, or connections block, only reserved ECU_CMC pin labels). See TODO block at top of `maxxecu-m52.wv` — must be authored (with shield) before Phase 1 harness build. |
> | CAN bus — 8HP TCU, Gauge.S cluster, and general CAN per Sys 2 note | 8HP CAN (Sys 9A) + Gauge.S CAN (Sys 9B) + Sys 2 | Twisted pair shielded (STP) throughout. MaxxECU 8HP GEN1 harness ships pre-shielded from MaxxECU. |
>
> **Recommended ("Preferred" in per-system tables — shield if practical, not a hard requirement):**
> | Run | System |
> |-----|--------|
> | Knock sensor 1 + 2 signal wires | 07K (Sys 7) |
> | DBW TB TPS 4-wire | 07K (Sys 7) |
> | EWP PWM control (MaxxECU GPO → CWA400 Pin 1) | EWP (Sys 5) |
> | Fuel pump SSR ctrl− (MaxxECU GPO → SSR) | Fuel pump (Sys 4) |
> | ATF temp sensor signal *(optional system)* | Sys 9E |
>
> **Explicitly NOT shielded (confirm this is still correct, don't shield by default):**
> | Run | System | Why not |
> |-----|--------|---------|
> | DCT shifter UP/DOWN/GND | Sys 9C | Momentary GND-closure signal, not analog — but `E36_DIY_Build_Checklist.md` says *"use shielded wire if routing near the engine harness loom"* while this table says flat "No" for all three wires. **Reconcile at physical routing stage** — if the final route runs alongside the engine harness trunk, shield it; if it stays in the cabin loom away from injector/coil wires, unshielded is fine per the checklist's own conditional. |
>
> Single-end drain only on all shielded runs — drain at MaxxECU / ECU side, never both ends (avoids ground loops).

---

## Consolidated Connectors to Buy

Only items not already included with their respective purchased components (e.g. Radium hanger studs come with the kit).

| Qty | Item | PN / Source | System |
|-----|------|-------------|--------|
| 1 | BMW E46 Accelerator Pedal Module `35426786282` | eBay used ~$80–120 — see `docs/dbw-pinouts.md` sourcing table | E-pedal |
| 1 | Pierburg CWA400 PWM version connector | Kostal 2+2 `10098866` — SLK 2.8 ELA terminals `22124499560` (pins 1–2), SLK 5.8 ELA `22124544900` (pins 3–4) | EWP |
| 1 | **Main ANL fuse + holder, 150A** | Blue Sea 5191 MRBF 150A or equiv ANL fuse holder. Confirmed: channel peak sum 104.8A × 1.2 = 125.8A → 150A matches PMU16 M6 stud 150A continuous rating. | Power dist |
| 1 | **4-post battery cutoff switch — Moroso 74108** (or Longacre equiv) | **Optional** — not required on a dual-duty street/drift car with a working ignition key. Install only if your HPDE org or track rules require it. If installed: must be 4-post (NOT 2-post) — a 2-post switch will not shut off the engine on an alternator-equipped car. ~$60–80 at Summit Racing / Jegs. | Power dist |
| 1 | Engine block ground stud (M8 bolt + lug) | Dedicated M8 bolt or welded stud on engine block for direct 4 AWG battery-negative ground cable. Separate from chassis stud. | Power dist |

| 1 | BMW E36 X20 25-pin connector (cabin) | OEM or aftermarket — source from E36 donor or Molex catalog | Body |
| 1 | BMW E36 X20 25-pin connector (engine side) | OEM | Body |
| 1 | Gauge.S E36 PNP cluster connector, 6-pin | Ships with Gauge.S unit | Body |
| 1 | Deutsch Autosport AS-series bulkhead shell + contacts | Cabin side + engine side mating pair — Size 20 contacts for all signal pins | E-pedal / all engine crossing |
| 1 | MaxxECU RACE C1, 48-pin Molex harness connector | [MaxxECU store ID 925](https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-street-or-sport-or-race-or-pro-connector-1-48-pin-molex), $33.41 — **does NOT ship with ECU**; special Molex crimp tool required | M52 harness |
| 1 | MaxxECU RACE C2, 32-pin Molex harness connector | [MaxxECU store ID 1982](https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-mini-or-race-c2-or-pro-c4-32-pin-molex), $32.25 — same Molex crimp tool as C1 | M52 harness |
| 1 | Bosch JPT 2-way (×2) | M52 CLT + VANOS solenoid | M52 harness |
| 1 | Bosch JPT 3-way | M52 crank VR trigger | M52 harness |
| 1 | BMW `12141726590` 3-pin | M52 VANOS cam Hall sensor | M52 harness |
| 1 | Superseal 2-way | Turbosmart boost solenoid | M52 harness |

---

## Harness Build Tools

One-time tooling purchase — covers all connector families in this build. See [`docs/harness-build.md`](harness-build.md) for the full pinning/depinning workflow, connector family warnings, and bench test procedure before install.

| Tool | Model | Price | Connector Family / Use |
|------|-------|-------|------------------------|
| Flush cutters | **Milwaukee 48-22-6106** ([Home Depot](https://www.homedepot.com/p/Milwaukee-6-in-Diagonal-Cutting-Pliers-48-22-6106/205652216) $19.97) | ~$20 | Essential for in-car wire trimming — angled jaw cuts flush to connector body, gets into tight spaces. Used constantly. Source: StreetCarJoe Race Car Wiring Pt.1. |
| Wire stripper | **Southwire 45578001** (adjustable-tension auto-strip) | ~$30 | 22–10 AWG, adjustable tension. Adjustable tension avoids nicking strands on thin-sheathed Teflon wire. |
| VAG 1.5mm sensor contact crimper | **IWISS IWS-2820M** ([Amazon](https://www.amazon.com/dp/B078WNZ9FW) $19.99) | ~$20 | VAG 1.5mm sealed-series contacts (TE MCP 1.5) in sensor pigtail housings (3B0973703G cam/crank/MAP, 1J0973702 CLT/IAT). Wire range 28–20 AWG (0.08–0.5mm²) — matches the 0.35–0.5mm² signal wires in these connectors. Two-pass operation: conductor crimp first, then insulation crimp. Also handles general small open-barrel contacts, ring terminals, and relay socket contacts in this AWG range. |
| VAG 2.8mm COP contact crimper | **IWISS IWS-2412M** ([Amazon](https://www.amazon.com/dp/B07G98DLB8) $19.99) | ~$20 | VAG 2.8mm JPT-series contacts in COP coil pigtail housings (4B0973724 — 4-pin coil-on-plug connector, 0.5–1.0mm² / 18–20 AWG coil primary wires). Die widths: 2.2 / 2.5 / **2.8** / 3.1 / 3.4mm — the 2.8mm die is a direct match for VAG JPT contacts. Also covers any other open-barrel contact in AWG 24–12 range. Companion to IWS-2820M: together the two IWISS tools span AWG 28–12 with no gap. |
| Open-barrel engine bay (general) | _(use IWS-2820M or IWS-2412M above per AWG)_ | — | **In the engine bay and anywhere exposed to moisture/vibration: use non-insulated barrel + adhesive-lined heat shrink** over every crimp. Adhesive liner seals against capillary wicking that pre-insulated connectors allow. Interior/cabin: pre-insulated nylon-sleeve crimps acceptable with the correct ratcheting tool. Source: StreetCarJoe Race Car Wiring Pt.1. |
| **AS solid barrel crimper** | **Daniels M22520/2-01 (AFM8)** handle + **K43 positioner (M22520/2-10)** | ~$426 kit / ~$570+ separate | **Required for Deutsch Autosport AS79 size-20 solid barrel contacts** (firewall bulkhead). TE-specified mil-spec tooling per Autosport technical datasheet 1-1773721-9 — NOT the HDT-48-00 or any clone (HDT-48-00 and JRready NEW-DT2 cover DT/DTM/DTP contacts only; AS contacts use different geometry and different part numbers). Best value: Fischer Motorsports ["DMC Deutsch Size 20 AS Tool Kit"](https://www.fischermotorsports.com/fm-store/electrical-systems/dmc-tooling/dmc-crimpers/dmc-deutsch-size-20-as-tool-kit/) (~$426, includes M22520/2-01 handle + K43 positioner for pin and socket). Handle alone: ~$495 (EMH Motorsports). K43 positioner alone: ~$80–94 surplus (dmctools.com). No cheap substitute: wrong die geometry produces cold crimps that pass initial pull-test but fail under vibration. |
| Ferrule crimper | **IWISS IWS-10** | ~$25 | Stranded wire ends into screw-clamp terminals (ECU power/ground, DIN rail fuse block). Covers 0.5–10mm² ferrules. |
| Deutsch contact extraction | **Deutsch 1680-73-01** | ~$15 | AS bulkhead size 20 contact removal — push in, releases retention lock cleanly. Do not use a screwdriver. |
| VW/Bosch connector de-pinning picks | **Lisle 57750** | ~$20 | Sensor pigtails (3B0973703G, 1J0973702, 1J0973712), COP connectors — push-to-release housings. |
| Rivnut tool + rivnut assortment | **Astro Pneumatic 1442** ([Amazon](https://www.amazon.com/Astro-Pneumatic-Tool-1442-Setter/dp/B003TODXQW) ~$71) + M4/M6 zinc rivnut kit | ~$75–90 | Installs threaded inserts into thin sheetmetal or carbon panels without backside access. Required for PMU16 bracket and ECU bracket mounting. Source: StreetCarJoe Race Car Wiring Pt.3. |
| **Molex CMC crimp — small** | **63811-9200** | ~$200–250 | MaxxECU C1/C2 small terminals (643221029, 0.75mm²/~20 AWG) — 40 of 48 C1 pins and 24 of 32 C2 pins are this size. **Primary tool for ECU connector wiring.** Source: Digikey, Mouser. |
| **Molex CMC crimp — big (0.5–1mm²)** | **63811-8900** | ~$200–250 | MaxxECU C1/C2 big terminals (643231029) — 7 on C1, 8 on C2. Used for heavier signal and power wires (18–20 AWG). Source: Digikey, Mouser. |
| **Molex CMC crimp — big (1–2mm²)** | **63811-9000** | ~$200–250 | MaxxECU C1 big terminals (643231039) — 1 pin on C1 only (engine GND/ECU power, 14–16 AWG). Optional if routing large wires through C1. Source: Digikey, Mouser. |

### Hardware — Harness Support

| Qty | Item | Notes |
|-----|------|-------|
| 1 bag | Non-insulated butt splices — 22–16 AWG assorted | Uninsulated crimp barrel + adhesive-lined heat shrink over top. Do NOT use pre-insulated butt splices. |
| 1 bag | **One-to-many (1→4) non-insulated crimp junctions** | Branches one input wire to 4 outputs. Use for 5V SENS OUT distribution from MaxxECU to multiple sensors (TPS, MAP, APS, etc.) from a single ECU pin. Keeps star topology. Source: StreetCarJoe Race Car Wiring Pt.1. |
| 1 roll | Adhesive-lined heat shrink 3:1 — assorted (1/4", 3/8", 1/2") | Required over every non-insulated crimp. Adhesive liner is essential — non-adhesive slides and leaves the crimp exposed. |
| 1 roll | **Tesa 51608 Fleece Harness Tape** (or 3M 1300E equiv) | Cloth harness tape for binding loom and holding sleeving ends closed. Use at all breakout points and sleeve terminations. More durable than PVC electrical tape. Source: StreetCarJoe Race Car Wiring Pt.2. |
| 1 bag | Adhesive-backed zip tie anchor mounts (cable saddle clips) | Stick to panel backs for routing harness without drilling. Key for PMU16 mounting surface, dash inner panel, anywhere drilling is impractical. Source: StreetCarJoe Race Car Wiring Pt.3. |
| 1 roll | Alex Tech / Techflex split loom — 1/4" + 3/8" + 1/2" assorted | Split loom for cabin and engine bay runs. Tesa tape on both ends holds sleeve closed. |
| 1 set | P-clamps — 1/4", 3/8", 1/2", 5/8" | Secure main power cables every 12 inches minimum. |
| 1 bag | M4 / M6 rivnuts (steel or zinc) — assorted | Used with rivnut tool for PMU16 bracket and ECU bracket mounting. |

> **Total non-Molex tools: ~$186** (flush cutters $20 + wire stripper $30 + IWS-2820M $20 + IWS-2412M $20 + Lisle $20 + rivnut tool ~$71 + Deutsch extraction $15 + ferrule crimper $25). Add ~$426 for the Fischer Motorsports DMC AS size-20 kit (M22520/2-01 handle + K43 positioner — the correct tool for AS79 contacts; HDT-48-00 and JRready clones are DT/DTM/DTP only). Total with AS crimper: **~$612** one-time purchase.
>
> **Budget tracking:** Key tools above are also tracked in `e36-docs/E36_CSVs/E36_Phase1_Foundation.csv` (Tooling category) with purchase links and price ranges for build cost rollup.
> If using Souriau 8STA for the bulkhead instead of Deutsch AS, confirm the correct positioner for Souriau contacts at purchase — Souriau uses compatible tooling but a different positioner.
> **MaxxECU Molex C1/C2 connectors:** Molex crimp tool PNs confirmed from [MaxxECU RACE pinout webhelp](https://www.maxxecu.com/webhelp/wirings-maxxecu_pinout.html). The small tool (63811-9200) is the primary purchase — covers ~85% of C1 and ~75% of C2 pins. The big tools are expensive (~$200+ each); consider outsourcing the handful of large-terminal pins if budget is a concern. For extraction/repair: Molex removal tool 638132400 (small) or 638132300 (big).
