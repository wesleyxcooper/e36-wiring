# Wiring BOM — Consolidated by System

Aggregated from all WireViz harness source files.
Source harnesses: `maxxecu-m52.wv` · `power-distribution.wv` · `epedal-bmw-e46.wv` · `epedal-hella-6pv.wv` · `fuel-pump-hanger.wv` · `ewp-controller.wv` · `body-x20.wv`

> **⚠️ TODO** = placeholder in source `.wv` — gauge, model, or pin not yet confirmed. Buy only after resolving.
> **🔁 shared** = appears in multiple harnesses, buy once.
> All wire lengths include ~10% slack. Add more for complex routing runs.

---

## System 1 — Power Distribution

*Source: `power-distribution.wv`*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Battery positive terminal | Ring terminal, trunk/engine bay |
| 1 | Battery negative terminal | Ring terminal |
| 1 | Chassis ground stud, M8 | Engine bay |
| 4 | Bosch ISO mini relay, 12V coil / 30A contacts | `0 332 002 150` or equiv — ECU main, coil/inj, fan, fuel pump |
| 1 | Mini blade fuse block, 8-position | ⚠️ TODO: source specific block |
| 1 | Inline ANL or MAXI fuse holder | ⚠️ TODO: size — likely 60–80A main fuse |
| 1 | IGN switched 12V source connector | ⚠️ TODO: confirm X20 pin |
| 1 | Fuel pump motor connector, 2-pin | ⚠️ TODO: confirm connector type (Walbro replaced by Radium hanger in Phase 1 — see System 4) |
| 1 | Radiator fan motor connector, 2-pin | ⚠️ TODO: SPAL fan model — source correct connector end |

### Cables

> ⚠️ All cable runs in `power-distribution.wv` are stubs — gauge and length TBD pending physical routing measurement. Do not buy until resolved.

| Run | Color | Gauge | Est. Length | Notes |
|-----|-------|-------|-------------|-------|
| BATT_POS_MAIN | RD | ≥4 AWG | TBD | Battery + → main ANL/MAXI fuse → relay board |
| BATT_NEG_MAIN | BK | ≥4 AWG | TBD | Battery − → chassis ground stud M8 |
| Relay coil feeds × 4 | GN | 18 AWG | TBD | IGN switched +12V → relay pin 86 |
| ECU / coil / inj relay outputs | RD | 12–14 AWG | TBD | Relay pin 87 → downstream loads |
| Fan load feed | RD | 12 AWG | TBD | Relay 87 → SPAL fan |
| Pump load feed | RD | 12 AWG | TBD | Relay 87 → fuel pump (Phase 1 Walbro; replaced by Radium hanger in Phase 1B) |
| GPO trigger wires (GPO 2, GPO 6) | VT | 22 AWG | TBD | MaxxECU GND-sink → relay pin 85 |

---

## System 2 — Engine Management (M52 Phase 1)

*Source: `maxxecu-m52.wv`*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Cinch CMC 26-pin (MaxxECU Race main) | `ECU_CMC` — pin assignment stub, not yet confirmed |
| 1 | Cinch 12-pin power/chassis | `ECU_12PIN` |
| 1 | Cinch 16-pin auxiliary | `ECU_16PIN` |
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
| 1 | Deutsch Autosport AS-series bulkhead — **cabin side** | Size 20 contacts, 6 pins reserved for e-pedal (pins TBD) |
| 1 | Deutsch Autosport AS-series bulkhead — **engine side** | Size 20 contacts, 6 pins reserved for e-pedal (pins TBD) |
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

> Replaces the M52 in-tank Walbro 255 + relay from Phase 1 with the Radium 20-1170 hanger + F90000267 + DC SSR + MaxxECU PWM control. No re-work at Phase 3 07K swap.

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **DC Solid State Relay (DC-DC, 40A)** | Crydom D1D40 preferred (40A, 0–60V load, 3–32V ctrl, opto-isolated, rated to 1 kHz). Generic 40A DC-DC SSR acceptable. Requires heatsink at sustained duty. |
| 1 | Radium Engineering 20-1170 hanger terminals | Top-plate external studs (pump+ and pump−) — anti-rotation, hermetically sealed. Comes with hanger kit, not sourced separately. |
| 1 | Battery positive terminal | 🔁 Shared with power distribution |
| 1 | Chassis ground stud | 🔁 Shared with power distribution |
| 1 | IGN switched 12V source | 🔁 Shared with power distribution |
| 1 | MaxxECU RACE GPO (GND-sinking) | 🔁 Shared — GPO pin TBD, same physical CMC connector |

### Cables

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| CABLE_PWR_BATT (BATT+ → SSR load+) | RD | 12 AWG | 0.5 m | No | Inline 25A AGC fuse within 30 cm of battery. Ring terminal at battery, blade/ring at SSR. |
| CABLE_PWR_PUMP (SSR load− → hanger pump+) | RD | 12 AWG | 1.5 m | No | Switched +12V to pump stud. Route through tunnel, clear of exhaust. |
| CABLE_GND (hanger pump− → chassis GND) | BK | 12 AWG | 0.5 m | No | Dedicated ground — do not share with ECU sensor GND. Ring terminals both ends. |
| CABLE_SSR_CTRL_POS (IGN 12V → SSR ctrl+) | GN | 22 AWG | 0.3 m | No | Low current (~15 mA opto draw). Short run fuse block → SSR. |
| CABLE_SSR_CTRL_NEG (MaxxECU GPO → SSR ctrl−) | VT | 22 AWG | 2.0 m | Preferred | PWM signal (GND-sink, 100–500 Hz). Drain at ECU end only. Keep away from coil primary wires. |

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

## TODOs / Open Items

| Item | Blocker |
|------|---------|
| All `power-distribution.wv` cable gauges and lengths | Physical routing not yet measured |
| All `maxxecu-m52.wv` cable gauges | WV stubs — need actual wire spec |
| MaxxECU CMC pin assignment | `ECU_CMC` in `maxxecu-m52.wv` is a stub — confirm before building |
| GPO pin assignments (fan, pump, EWP, fuel pump PWM) | MaxxECU pin map not yet finalized |
| Main fuse size | Depends on total current calc — likely 60–80A ANL |
| Mini blade fuse block model | 8-position, source specific unit |
| SPAL fan model + connector | Fan not yet selected |
| Body-x20 wire colors and gauge | Colors visible in SVG diagram — gauge TBD |
| Firewall bulkhead full pinout | `harnesses/firewall-bulkhead.wv` not yet authored — see README Open TODOs |
| 07K engine harness | `maxxecu-07k.wv` exists but outputs not generated — Phase 3 |

---

## Consolidated Wire to Buy

> Covers Systems 3–5 where gauge + color + length are fully specified. Systems 1, 2, 6 are TBD pending routing measurement — add to this table when resolved.
> Add 20% to all lengths for routing slack, drip loops, and service loops.

| Gauge | Color | Total Length (specified) | With 20% slack | Systems |
|-------|-------|--------------------------|----------------|---------|
| 10 AWG | RD (red) | 2.0 m | 2.5 m | EWP (power in + power out) |
| 10 AWG | BK (black) | 1.5 m | 2.0 m | EWP (ground) |
| 12 AWG | RD (red) | 2.0 m | 2.5 m | Fuel pump (BATT→SSR + SSR→pump) |
| 12 AWG | BK (black) | 0.5 m | 0.7 m | Fuel pump (ground) |
| 18 AWG | GN (green) | 0.5 m | 0.7 m | EWP relay coil supply |
| 18 AWG | BK (black) | 0.5 m | 0.7 m | EWP relay coil return |
| 22 AWG | VT (violet) | 4.0 m | 5.0 m | Fuel pump PWM ctrl (2.0 m) + EWP PWM (2.0 m) |
| 22 AWG | GN (green) | 0.3 m | 0.4 m | Fuel pump SSR ctrl+ |
| 22 AWG | YE/GN (CAN) | 2.5 m | 3.0 m | Body/Gauge.S CAN twisted pair — shielded |
| 24 AWG | BK (black) | 2.4 m (×2 conductors) | 3.0 m | E-pedal GND1 + GND2 both runs |
| 24 AWG | RD (red) | 2.4 m (×2 conductors) | 3.0 m | E-pedal VCC1 + VCC2 both runs |
| 24 AWG | GN (green) | 1.2 m (×1 conductor) | 1.5 m | E-pedal APS1 signal |
| 24 AWG | YE (yellow) | 1.2 m (×1 conductor) | 1.5 m | E-pedal APS2 signal |

> **Shielded runs:** E-pedal cable (2 × 6-conductor shielded, 24 AWG), EWP PWM (22 AWG shielded preferred), fuel pump SSR ctrl− (22 AWG shielded preferred), Gauge.S CAN (shielded twisted pair preferred).
> Single-end drain only on all shielded runs — drain at MaxxECU / ECU side.

---

## Consolidated Connectors to Buy

Only items not already included with their respective purchased components (e.g. Radium hanger studs come with the kit).

| Qty | Item | PN / Source | System |
|-----|------|-------------|--------|
| 1 | BMW E46 Accelerator Pedal Module `35426786282` | eBay used ~$80–120 — see `docs/dbw-pinouts.md` sourcing table | E-pedal |
| 1 | DC Solid State Relay, 40A DC-DC, opto-isolated | Crydom D1D40 (preferred) or generic 40A DC-DC SSR | Fuel pump |
| 1 | 40A automotive relay, 4-pin | Bosch `0 332 002 150` or equiv | EWP |
| 4 | Bosch ISO mini relay, 12V / 30A, 4-pin | Bosch `0 332 002 150` or equiv | Power dist |
| 1 | Pierburg CWA400 PWM version connector | Kostal 2+2 `10098866` — SLK 2.8 ELA terminals `22124499560` (pins 1–2), SLK 5.8 ELA `22124544900` (pins 3–4) | EWP |
| 1 | Inline 25A AGC fuse + holder | Standard AGC glass fuse holder | Fuel pump |
| 1 | Inline 40A fuse + holder | ANL or MAXI blade fuse holder | EWP |
| 1 | Main ANL/MAXI fuse + holder | 60–80A ⚠️ size TBD | Power dist |
| 1 | Mini blade fuse block, 8-position | ⚠️ TODO: source specific unit | Power dist |
| 4 | Bosch ISO mini relay socket / base | Matches relay above | Power dist |
| 1 | BMW E36 X20 25-pin connector (cabin) | OEM or aftermarket — source from E36 donor or Molex catalog | Body |
| 1 | BMW E36 X20 25-pin connector (engine side) | OEM | Body |
| 1 | Gauge.S E36 PNP cluster connector, 6-pin | Ships with Gauge.S unit | Body |
| 1 | Deutsch Autosport AS-series bulkhead shell + contacts | Cabin side + engine side mating pair — Size 20 contacts for all signal pins | E-pedal / all engine crossing |
| — | Cinch CMC connector set | MaxxECU CMC — ships with ECU; backshell + contacts from MaxxECU or Cinch direct | M52 harness |
| 1 | Bosch JPT 2-way (×2) | M52 CLT + VANOS solenoid | M52 harness |
| 1 | Bosch JPT 3-way | M52 crank VR trigger | M52 harness |
| 1 | BMW `12141726590` 3-pin | M52 VANOS cam Hall sensor | M52 harness |
| 1 | Superseal 2-way | Turbosmart boost solenoid | M52 harness |
