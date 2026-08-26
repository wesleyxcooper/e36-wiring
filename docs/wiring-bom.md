# Wiring BOM — Consolidated by System

Aggregated from all WireViz harness source files.
Source harnesses: `maxxecu-m52.wv` · `maxxecu-07k.wv` · `firewall-crossing-maven.wv` · `power-distribution.wv` · `epedal-bmw-e46.wv` · `epedal-hella-6pv.wv` · `fuel-pump-hanger.wv` · `ewp-controller.wv` · `body-x20.wv` · `8hp-can.wv` · `gauge-s-can.wv` · `dct-shifter.wv` · `pst-f1-sensor.wv` · `atf-temp-sensor.wv` *(optional)*

> **Source-of-truth hierarchy:** `.wv` files → this BOM → CSVs (downstream purchase tracking)
>
> The `.wv` harness files define build architecture: what is custom-built vs. purchased,
> connector families, signal assignments, and cable specs. This BOM aggregates from them.
> The CSVs are downstream — they track purchase cost/status and reflect decisions already
> made in the `.wv` files.
>
> If a `.wv` file says "build it" but the actual approach is "buy it pre-made," the `.wv`
> file is wrong and must be corrected first. The BOM and CSVs follow from that correction.

> **⚠️ TODO** = placeholder in source `.wv` — gauge, model, or pin not yet confirmed. Buy only after resolving.
> **🔁 shared** = appears in multiple harnesses, buy once.
> All wire lengths include ~10% slack. Add more for complex routing runs.

---

## Wire Specification — Bulk Wire Purchasing

**Standard spec for all signal and low-current wiring in this build: TXL, 105°C, SAE J1128.**

TXL (thin-wall cross-linked polyethylene) is the consensus choice for custom automotive harness work. It has the same 105°C temperature rating and electrical properties as the common GXL spec, but thinner insulation wall — 22 AWG TXL is ~2.1mm OD vs ~2.7mm for GXL. On a 79-pin connector the difference is the loom fitting through a grommet without a fight. Every HPA course, StreetCarJoe, and Rywire build guide uses TXL. GXL is fine if TXL is unavailable locally, but buy TXL if you have the choice.

Do **not** use GPT (PVC insulation) — it is rated only 80°C and is not suitable for engine bay temperatures near turbocharged exhaust.

Mil-spec M22759 is what race teams use. It's fine but costs 5–10× more and is hard to source in the full color range you need. Not worth it here.

**Bulk spool shopping list (all 22 AWG TXL unless noted):**

| Color | Use in harness | Suggested qty | Notes |
|-------|---------------|---------------|-------|
| Red | +12V power, +5V sensor supply | 50m | Most frequently used power color |
| Black | Power/chassis GND (never sensor GND) | 50m | Convention: BK = high-current return only. Never use Black for sensor GND wires. |
| White | Sensor signal inputs (analog), WBO2 signals | 100m | Highest volume — sensors, triggers, cam, crank |
| **Brown** | **Sensor GND / VR Signal−** | **25m** | **Required — every sensor GND wire and crank VR− return. Without Brown the sensor sub-loom cannot be built. Source: `harness-build.md` § Wire Color Convention.** |
| **Blue** | **Ignition coil drive outputs (IGN 1–5)** | **25m** | **Required. Previously listed as Grey; correct color per MaxxECU convention and all .wv files is Blue (BU).** |
| Grey | Injector drive outputs (INJ 1–5) | 25m | INJ signal wires only — not IGN. Previously mislabeled as IGN. |
| Green | GPO actuator outputs only (VVT solenoid, boost solenoid) | 15m | GPO outputs only — not injectors. |
| **Yellow** | **Shield GND drain wire only** | **10m** | **Convention: YE = shield drain (single-end, ECU end). Crank, cam, knock shields. Never use Yellow for Starter trigger or Alt D+.** |
| Orange | DBW ETh Motor+ | 5m | **22 AWG** (adequate for 3A peak H-bridge current at short engine-bay runs — motor wires direct-terminate at engine-bay ECU per H2O arch). |
| Violet | DBW ETh Motor−, PWM signal wires | 5m | **22 AWG** for motor leads; 22 AWG for PWM signals. |
| White + Blue (WH/BU twisted pair) | CAN H / CAN L | 10m | Buy as pre-twisted pair (WiringPros sells by the foot). WH = CAN H, BU = CAN L — matches all .wv harness files. |

Heavier gauge for specific runs (buy short lengths, not full spools):

| Gauge | Use | Length |
|-------|-----|--------|
| 12 AWG GXL red/black | Fan relay output runs (after DT bypass connector, to fan motor) | 5m |
| 8 AWG GXL red | EWP output run (after DT bypass connector, to CWA400) | 2m |

> **Pigtail tail wire removed.** Previous BOM listed 18 AWG coil tails and 20 AWG injector tails for pigtail-to-harness splices. The build now uses direct termination — TXL 22 AWG runs end-to-end from the MaxxECU CMC to the sensor connector terminal; no intermediate splice and no heavier-gauge stub. See `walkthroughs/26-07k-harness.md` connector sourcing section.

**Supplier:** [WiringPros.com](https://www.wiringpros.com) — TXL by the foot in any color; also sells CAN twisted pair pre-twisted. [Del City](https://www.delcity.net) — bulk spools. Do not buy from generic electronics suppliers (not automotive-spec insulation).

---

---

---

## Harness Consumables — Sleeving, Splices, and Boots

Required to build and finish the engine harness. Separate from connectors, contacts, and wire.

### Sleeving

| Item | Spec | Use | Qty (engine harness) |
|------|------|-----|--------------------|
| Techflex F6 expandable braided sleeving — 1/2" | 13mm nominal OD | Main trunk | 2m |
| Techflex F6 expandable braided sleeving — 1/4" | 6mm nominal OD | Injector, coil, sensor, knock, trigger, WBO2 sub-looms (6× sub-looms ~300–500mm each) | 5m |
| Techflex F6 expandable braided sleeving — 1/8" | 3mm nominal OD | Individual shielded runs (crank/cam twisted pair, knock, WBO2) inside the trigger/knock sub-looms | 2m |

> Techflex nominal diameter = open/relaxed OD.

### Heat-zone sleeving (exhaust manifold / turbo proximity)

The WBO2 sensor bung and the CLT sensor (cylinder-1 exhaust face) are adjacent to the exhaust manifold. The knock sensors are on the exhaust side of the block. Standard Techflex F6 (PET braid) is not rated for sustained high-temperature exposure — add purpose-built heat sleeve before final looming. Sources: DEI product specs; `maxxecu-07k.wv` W_WBO2 and W_KNOCK notes.

| Item | Spec | Use | Qty |
|------|------|-----|-----|
| DEI Fire Sleeve — 3/8" ID × 36" kit | silicone-over-fiberglass, 500°F (260°C) continuous / 2000°F (1093°C) intermittent — **DEI p/n 010470, $26.99** — [designengineering.com](https://www.designengineering.com/fire-sleeve-tape-kit-0-375-id-x-36/) — includes 36" sleeve + 16" Fire Tape | WBO2 cable: first 300 mm (12 in) from sensor bung outward. CLT pigtail: first 150 mm (6 in) from sensor body. Both cables fit the 3/8" ID (10 mm). One 36" kit covers both runs (450 mm total needed). Applied over the bare cable before main loom assembly. | 1 kit |
| DEI Reflect-A-Gold — 1-1/2" × 15' roll | Metalized polyimide laminated glass cloth, 800°F continuous (adhesive rated to 325°F) — **DEI p/n 010394, $42.99** — [designengineering.com](https://www.designengineering.com/reflect-a-gold-heat-reflective-tape-1-5-x-15/) — NOT Reflect-A-Cool (different product, 400°F limit) | KNOCK sub-loom: wrap any section that routes within 100 mm (4 in) of exhaust manifold, over the Techflex sleeve. Applied after routing is confirmed. | 1 roll |

### Splice consumables

| Item | Use | Notes |
|------|-----|-------|
| Raychem SRGB solder sleeves — 22–26 AWG (small, blue band) | Sensors with integral moulded pigtails only (e.g. E46 APS pedal donor connector if sourced from a car rather than as a housing+terminal kit) | Buy Mouser/DigiKey — not Amazon. Qty: ~5 (not 25 — direct-terminated connectors need no splice). |
| Non-insulated butt splice + 3:1 adhesive-lined heat-shrink | Same application as SRGB — alternative for integral-pigtail sensors | IWISS IWS-2820M + ≥25mm adhesive-lined heat-shrink. |

> **Direct termination eliminates most pigtail splices.** Previous BOM specified ~20 SRGB solder sleeves for pigtail-to-harness splices at every injector, coil, and sensor connector. With direct termination (TXL runs end-to-end from MaxxECU CMC to sensor connector terminal), those joints are eliminated. Only sensors that ship with an integral moulded wire pigtail require a splice. See `walkthroughs/26-07k-harness.md` connector sourcing section.

> **Raychem SRGB technique (for any remaining integral-pigtail splices):** Overlap bare wire ends 5–10mm inside the sleeve. Heat gun at 50–75mm standoff, move slowly — solder ring melts and wicks, sleeve shrinks. No iron. Do NOT use a soldering iron on wires in the loom — rigid joint at the flex point fails under vibration.

### Breakout boots and end caps

| Item | Use | Source |
|------|-----|--------|
| 3:1 adhesive-lined heat-shrink, assorted sizes (1/4", 3/8", 1/2") | Trunk breakout transitions, sub-loom end terminations | Amazon — buy an assortment kit |
| Techflex split-loom conduit (optional) | Alternative to expandable braid where loom needs to be retrofitted to existing wiring without pre-threading | Same as Techflex F6 but pre-split — easier install on pre-run wires |

### Loom-level labels (in addition to wire-level PermaSleeve)

| Item | Cartridge PN | Use |
|------|-------------|-----|
| Brady M210 | — | Same label maker used for all wire labels |
| PermaSleeve — 3/8" cartridge | M21-375-C-342 | Sub-loom breakout labels (slides over 1/4" sub-loom before Techflex goes on). Print: `INJECTORS`, `COILS`, `SENSORS`, `TRIGGER`, `KNOCK`, `WBO2` |
| PermaSleeve — 1/2" cartridge | M21-500-C-342 | Main trunk label at MaxxECU CMC entry. Print: `ENGINE M52 PH1` or `ENGINE 07K PH3` |

> Do NOT use zip-tie flags for loom labeling. They rotate, collect oil, and protrude visually. PermaSleeve heat-shrink labels shrink flush to the loom surface — identical result to an OEM factory harness label.

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
| PMU16 CAN2 H/L → MaxxECU CAN1 H/L | GY/**VT** | 22 AWG shielded twisted pair | TBD | PMU16 pins 24/34 → MaxxECU CAN1H/CAN1L. Drain at MaxxECU end only. Route away from coil/injector wires. |
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

*Signal reference: `maxxecu-m52.wv` (reference only — not a build document)*

> **Phase 1 uses the MaxxECU M50 pre-terminated engine harness.** All engine sensor connectors
> (injectors, coils, CLT, IAT, TPS, crank, cam, VANOS solenoid, boost stub, WBO2 LSU 4.2, MAP)
> are pre-crimped and included. The C1 (48-pin Molex) ECU connector is also included.
> Source: https://www.maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html (verified 2026-08-26)
>
> Harness routes through the existing E36 firewall grommet/bushing to the engine-bay MaxxECU RACE H2O. No firewall bulkhead connector for Phase 1 — the Maven HD30 dual bulkhead is a Phase 2 install (see System 8).

### Connectors — additional items NOT included in the pre-terminated harness

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **BMW sensor PN `12141726590`** — VANOS cam sensor (sensor, not connector) | Required swap before Phase 1 can fire. The harness CAM connector is wired for non-VANOS M50 head; VANOS M52 cam sensor is a different type. Swap the sensor and the harness connector works as-is. Alternative: cut harness CAM connector and rewire with VANOS body + switched +12V (see `MaxxECU_M50_Terminated_Harness.md`). |
| 1 | **Molex 32-pin C2** — MaxxECU RACE connector 2 | [MaxxECU store ID 1982](https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-mini-or-race-c2-or-pro-c4-32-pin-molex), $32.25 — needed for 8HP virtual clutch pedal position (C2 pin G3 = AIN 5). C1 AIN 1–4 are consumed by PST-F1 and MAP via the harness 16-pin breakout; C2 is the only remaining path. Crimp tool: Molex 63811-9200. Source: MaxxECU RACE REV9+ wiring diagram, pin G3 = "Extra analog sensor / pedal main position 0-5V". |
| 1 | Bosch PST-F1 5-pin Bosch Trapezoid mating kit — F02U.B00.751-01 | Dual oil temp + pressure sensor connector. Wires to 16-pin breakout AIN 1 (temp) + AIN 3 (pressure). |
| 1 | 3-pin inline | Ethanol content / flex fuel sensor (Continental digital) — wires to 16-pin breakout DIN 3 |
| 1 | SPDT relay socket | SPAL fan relay (cross-ref `power-distribution.wv`) |
| 1 | SPDT relay socket | Fuel pump relay (cross-ref `power-distribution.wv`) |
| 1 | Splice / junction, 4-pin | CAN H/L shared bus junction (8HP + Gauge.S share 16-pin breakout CAN H/L) |
| 1 | DCT shifter paddle harness connector | 4-wire E36 fitment — wires to 16-pin breakout DIN 1 + DIN 2 |
| 1 | MaxxECU 8HP GEN1 CAN harness | ZF 8HP70 transmission CAN — pre-made harness #2287 from MaxxECU/LPS |
| 1 | Gauge.S E36 CAN input, 2-pin | Cross-ref `body-x20.wv` |
| 3 | Ring terminal | Batt +12V (fused), chassis GND, IGN switched +12V to 12-pin breakout |

### Cables

> No engine-side cable purchases needed — all engine sensor wiring is in the pre-terminated harness.
> What remains is wiring the 12-pin and 16-pin breakout connectors to cabin destinations (PDM/PMU16,
> relay board, CAN bus, additional sensors). Measure routing lengths on the car before cutting.

| Run | Notes |
|-----|-------|
| 12-pin extra connector → cabin | Power rails (+12V coil/ECU/starter/alternator), engine GND, GPO 2 (fuel pump), GPO 6 (fan). All 14–18 AWG. |
| 16-pin extra connector → cabin | CAN bus, AIN 1–4 sensor signals, DIN 1–3, GPO 3/7/8. All 18–22 AWG. |
| C2 pigtail (single wire) | AIN 5 (G3) for 8HP virtual clutch position sensor. 22 AWG. |

---

## System 3 — Drive-by-Wire: E-Pedal

*Source: `epedal-bmw-e46.wv` (primary) · `epedal-hella-6pv.wv` (RHD fallback — install one, not both)*

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **BMW E46 Accelerator Pedal Module** | PN `35426786282` (manual) / `35426786281` (auto) — used, ~$80–120. See `docs/dbw-pinouts.md` for sourcing table. |
| — | *OR* **Hella 6PV010946-141** | RHD fallback — standalone floor-mount, no OEM pedal box, ~$80–120 new |
| 1 | Maven HD30 dual 16+16 bulkhead — Connector B (Phase 3) | APS routes through **Connector B pins 1–6** (6 wires: ch1 SGND/+5V/sig, ch2 SGND/+5V/sig). Cabin-side receptacle installed at Phase 2; wires populated at Phase 3 with the E46 APS pedal. See System 8 for full Maven bulkhead spec. Source: `harnesses/firewall-crossing-maven.wv`; `harnesses/epedal-bmw-e46.wv`. |
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
| 1 | 40A automotive relay | **Phase 3 CWA400 control only — not used in Phase 1** (there is no EWP in Phase 1). Phase 3 supersedes this relay with PMU16 O5+O14 MOSFET direct drive. Relay listed here for reference only. Source: `34-ecu-harness-final.md` lines 144–147. |
| 1 | Battery positive terminal | 🔁 Shared |
| 1 | Chassis ground stud | 🔁 Shared |
| 1 | MaxxECU RACE GPO | 🔁 Shared — GPO pin TBD |

### Cables

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| CABLE_PWR_IN (BATT+ → PMU16 input) | RD | 10 AWG | 0.5 m | No | Fused 40A within 30 cm of battery. **Phase 3:** PMU16 O5+O14 (50A combined MOSFET) drives CWA400 directly — no relay. Ring terminal at battery. |
| CABLE_PWR_OUT (PMU16 O5+O14 → CWA400 Pin 3) | RD | 8 AWG | 1.5 m | No | Switched +12V pump supply. 35.5A nominal — **8 AWG** (10 AWG marginal at 35.5A / 1.5m in engine bay; System 1 and consolidated buy table both specify 8 AWG). PMU16 manages post-shutdown cooling hold. |
| CABLE_GND (CWA400 Pin 4 → chassis GND) | BK | 10 AWG | 1.5 m | No | Dedicated ground. 10 AWG minimum. Both phases. |
| CABLE_PWM (MaxxECU GPO → CWA400 Pin 1) | VT | 22 AWG | 2.0 m | Preferred | PWM signal (680 Hz). **Phase 3:** MaxxECU broadcasts EWP state over CAN1 to PMU16 — no direct GPO wire to CWA400. 22 AWG if retained for direct drive fallback. |
| *Phase 1 only* relay coil wire 1 (relay pin 86 → IGN +12V) | GN | 18 AWG | 0.5 m | No | **Not used in Phase 3 (PMU16 direct drive).** |
| *Phase 1 only* relay coil wire 2 (relay pin 85 → chassis GND) | BK | 18 AWG | 0.5 m | No | **Not used in Phase 3 (PMU16 direct drive).** |

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
| W_GAUGES_CAN (CAN H/L) | WH/BU | 22 AWG | 2.5 m | Preferred | MaxxECU CAN → Gauge.S cluster. Twisted pair. |

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

> Phase 3 engine harness — direct-terminate at the engine-bay MaxxECU RACE H2O CMC (C1/C2). Phase 1 used the pre-terminated M50 harness through the OEM firewall grommet; Phase 3 replaces that with a custom 07K harness that plugs into the same engine-bay ECU. See `harnesses/maxxecu-07k.wv`. The Maven bulkhead engine-side plugs (Connectors A + B) mate to the pre-installed cabin-side receptacles for cabin↔engine signals — see System 8.

### Connectors

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Maven HD30 dual bulkhead — engine-side plugs (Connectors A + B) | Included with the Maven kit (System 8). Populate engine-side pins with the 07K harness at Phase 3 build. See `harnesses/firewall-crossing-maven.wv` for pin assignments. |
| 5 | EV14 / USCAR injector connector housing + terminals | Direct termination — housing: Bosch `1 928 402 258` (or equiv USCAR 2-pin); terminal: Bosch `1 928 499 000` or Delphi `12129476`. ⚠️ `0 280 156 127` is a **Bosch injector** PN, not a connector PN — do not order it for wiring. |
| 5 | VAG 4-way COP connector | IGN 1-5 ignition coils (07K firing order 1-2-4-5-3) |
| 1 | VW 07K crank Hall sensor OE# 07K906433B, 3-pin | Hall effect (confirmed — Valeo 366675 datasheet "Sensor Type: Hall Sensor"). Connector body: 3B0973703G (same as cam — label CRANK at crimp time). Pinout: +5V/Signal/SensorGND. ⚠️ Verify exact body at install. |
| 1 | VW 07K cam Hall sensor, 3-pin | ⚠️ TODO: confirm exact body at install (+5V type — different from M52 +12V) |
| 1 | VW 07K CLT sensor connector | ⚠️ TODO: confirm connector body at install |
| 1 | VW 07K IAT sensor connector | ⚠️ TODO: confirm connector body at install |
| 1 | VW 07K DBW throttle body connector | ⚠️ TODO: confirm 6-pin body (Motor+/Motor−/TPS1+TPS2 +5V/GND) at install |
| 2 | Bosch flat knock sensor connector, 1-pin | KS1 + KS2 (Bosch flat-type, M8 mount) — signal only; GND via mounting bolt |
| 1 | Bosch LSU 4.9 6-way connector | WBO2 — new purchase for Phase 3. Phase 1 harness uses LSU 4.2 (different pinout — do NOT reuse). New bung required in 07K manifold. |
| 1 | Bosch PST-F1 5-pin Bosch Trapezoid | 🔁 Same connector as M52 — new mount on 07K oil housing iABED M10×1.0 port. Kit F02U.B00.751-01. |
| 1 | Superseal 2-way | 🔁 Same boost solenoid as M52 |
| 1 | VW/Tyco Micro Timer 1.5mm Sealed, 2-pin — `1J0 973 702` female pigtail | N205 VVT solenoid (cam adjustment valve). Solenoid male body: `1J0 973 802`. Pre-made pigtail: automotive-connectors.com `42121600-PT` (~30 cm leads) or Amazon B0D8FH4S8T (~170 mm leads). Terminals 0.35–0.5 mm² (22 AWG) — crimp with IWISS IWS-2820M. Source: VW BGP/BGQ workshop manual + automotivetechinfo.com 2010 Golf valve timing repair. |
| 1 | 3-pin inline | 🔁 Same Continental flex fuel sensor as M52 |

### Cables (additions over M52)

| Run | Color(s) | Gauge | Length | Shielded | Notes |
|-----|----------|-------|--------|----------|-------|
| DBW TB Motor +/− | OG, VT | 22 AWG | 0.5 m ea | No | H-bridge output — 22 AWG adequate for 3A peak at 0.5 m. Direct-terminate at engine-bay MaxxECU C2 H4/H2 — no bulkhead crossing. Verify polarity before crimping. |
| DBW TB TPS 4-wire | RD, BN, WH, WH | 22 AWG | 0.5 m | Preferred | +5V (RD), Sensor GND (BN — not BK; BK=chassis GND), TPS1 signal (WH), TPS2 signal (WH). Source: `maxxecu-07k.wv` W_DBW_TPS cable. |
| Knock sensor 1 signal | WH | 22 AWG | 0.4 m | Preferred | KS1 signal wire; shield drain at ECU end |
| Knock sensor 2 signal | WH | 22 AWG | 0.6 m | Preferred | KS2 signal wire |
| Knock shield drain | YE | 22 AWG | 0.5 m | No | Shared knock sensor shield drain — terminates at MaxxECU C1 H1 (Sensor GND) at the ECU end (single-end drain). Direct-terminate engine-bay; no bulkhead crossing. Source: `harnesses/maxxecu-07k.wv`. Color YE = shield drain — never BK (power GND). |

---

## System 8 — Firewall Bulkhead

*Source: `firewall-crossing-maven.wv`*

> **Active architecture: Maven HD30 dual 16+16 bulkhead.**
> With MaxxECU RACE H2O engine-bay-mounted (OEM DME E-box cavity, intake side per `docs/vendor/maxxecu/MaxxECU_RACE_H2O.md`), all engine sensor / IGN / INJ / GPO signals stay engine-bay entirely. The firewall crossing shrinks to a small dedicated Deutsch HD30 dual bulkhead for cabin-originated signals only.
>
> - **Connector A (16-pin, Phase 2 install):** CAN H/L/shield to Gauge.S cluster (3 pins) + DCT shifter paddle UP/DOWN/GND (3 pins). 8 spare cavities. Populated at Phase 2 offline harness build.
> - **Connector B (16-pin, Phase 3 population):** APS e-pedal — ch1 SGND/+5V/sig + ch2 SGND/+5V/sig (6 pins). 10 spare cavities. Cabin-side receptacle installed at Phase 2 with all cavities plugged; populated at Phase 3 when the E46 APS pedal is installed.
> - **NO high-current relay bypass needed:** with PMU16 engine-bay-mounted alongside the H2O (see `harnesses/power-distribution.wv`), fan / EWP / AC relay outputs are engine-bay-to-engine-bay direct — no firewall crossing.
>
> **OEM E36 X20 25-pin firewall connector (`harnesses/body-x20.wv`) stays 100% OEM body signals — no ECU signals traverse X20.**
>
> Phase 1 note: this Maven bulkhead is NOT installed for Phase 1. Phase 1 CAN + DCT wires (6 total) route through the existing OEM E36 firewall grommet as individual wires alongside the pre-terminated M50 harness. Phase 2 offline prep installs the Maven bulkhead and re-terminates the Phase 1 wires into Connector A.

### 8 — Maven HD30 Dual 16+16 Bulkhead Kit

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Maven Performance Products **Dual Connector Bulkhead — 16 PIN & 16 PIN** | [mavenspeed.com](https://mavenspeed.com/collections/b2t-engineering/products/dual-connector-bulkhead) — $274 USD (config: "16 PIN & 16 PIN"). Includes: CNC billet aluminum plate (2.6" × 5.25", black anodized) + 2× Deutsch HD30 shell-size-24 16-pin connectors (both sides — flange receptacle + jam-nut plug for each) + all size-16 solid contacts + paper installation template + stainless steel fasteners. Boots sold separately. |
| — | HD30 size-16 solid contacts (included in Maven kit) | Sockets and pins for both connectors both sides. 13A per contact rated continuous, 14-20 AWG. Signal-level wiring in this crossing is 22 AWG. |
| — | HD30 cavity plugs (order separately if not included) | Seal unused cavities on both sides — required for IP67. Connector A: 8 spare cavities Phase 2+. Connector B: 10 spare cavities Phase 3+ (16 spare Phase 2). |
| — | HD30 backshells / boots (optional, Maven or generic) | Recommended for cable strain relief and additional environmental sealing. Style depends on cable OD; not included with the Maven kit. |

> ⚠️ **Crimping tool:** **Deutsch HDT-48-00** — covers all Deutsch solid contacts across DT / DTM / DTP / DTHD / HD10 / HD30 / HDP20 / DRC series. Sources:
> - [deutschconnector.com HDT-48-00 product page](https://www.deutschconnector.com/products/deutsch_connector_tools/deutsch_connector_crimp_tools/HDT-48-00/)
> - [deutschconnector.com Crimp Tool Selection Guide](https://www.deutschconnector.com/technical/deutsch_connector_crimp_guide/) — *"The HDT-48-00 accommodates ALL solid pins and sockets for DT, DTM, DTP, Size 12 Jiffy Splice connectors, Size 12 DTHD connectors as well as Size 12, Size 16 and Size 20 cavities in Round Series connectors."*
> - Maven's own product page: *"USE OF THE CORRECT CRIMPING TOOL IS ESSENTIAL! MUST USE CRIMPERS SIMILAR TO THESE"* (points to a standard Deutsch HDT-48-00 crimper — no separate "Maven tool" exists)
> - Maven sells the tool at $197 (bundle available with kits): [mavenspeed.com/…/deutsch-crimp-tool-solid-contacts](https://mavenspeed.com/collections/b2t-engineering/products/deutsch-crimp-tool-solid-contacts)

> ⚠️ **Extraction tool:** Standard Deutsch round-shoulder removal tool ($10-35 depending on brand). Maven sells one at $34.97. Fits all HD-series contacts. Not the DT/DTM-specific extraction tool.

---

## System 9 — CAN Harnesses, DCT Shifter, PST-F1

### 9A — ZF 8HP70 TCU CAN (`8hp-can.wv`)

| Qty | Item | Notes |
|-----|------|-------|
| 1 | MaxxECU 8HP GEN1 CAN harness (~$368 pre-made kit) | Ships from MaxxECU — covers TCU power/GND/CAN. Plug-and-play kit; user does NOT build these wires. Under the H2O engine-bay arch, both the MaxxECU ECU and 8HP TCU are engine-bay-mounted, so this harness runs entirely on the engine-bay side of the firewall — no bulkhead crossing. See `harnesses/8hp-can.wv` (reference file only, not a build file). |

> Harness sourced as a unit from MaxxECU — no individual cable spec needed.

### 9B — Gauge.S CAN (`gauge-s-can.wv`)

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| MaxxECU CAN 1 → Gauge.S, CAN H | WH | 22 AWG | ~0.5 m | Preferred — STP | 500 kbps, Default 1.3 protocol. Cabin-to-cabin, no bulkhead crossing. |
| MaxxECU CAN 1 → Gauge.S, CAN L | BU | 22 AWG | ~0.5 m | Preferred — STP | Twisted pair with CAN H above. |

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

### 9F — 8HP Virtual Clutch — DCT Clutch Simulator Remote (`docs/vendor/dctshifter/DCT_Clutch_Simulator.md`)

> Enables full analog virtual clutch control of the ZF 8HP via MaxxECU. The DCT Clutch Simulator (Remote mount, with CPS) is a purpose-built hydraulic clutch simulator with an integrated Clutch Pressure Sensor that outputs 0.5–4.5V analog to MaxxECU C2 AIN 5. The E36 OEM clutch pedal + master cylinder are retained; the OEM hydraulic line (that used to drive the manual-trans slave cylinder) now drives the engine-bay-mounted Simulator instead.
>
> Vendor product page: [dctshifter.com/products/dct-clutch-simulator-remote](https://dctshifter.com/products/dct-clutch-simulator-remote) — Remote + CPS variant ~4,995 SEK (~$475 USD).
>
> Vendor MaxxECU compatibility confirmation: [dctshifter.com/pages/installation](https://dctshifter.com/pages/installation) §4 — *"The Clutch Pressure Sensor (CPS) translates clutch pressure into an electronic signal between 0.5V and 5.0V for the transmission controller… This is typically done in controllers such as TurboLamik & MaxxECU."*
>
> Full vendor doc: `docs/vendor/dctshifter/DCT_Clutch_Simulator.md`
>
> **Requires:** Binary5 8HP TCU firmware + MTune 1.157+. Source: [maxxecu.com/webhelp/advanced-8hp-virtual_clutch.html](https://www.maxxecu.com/webhelp/advanced-8hp-virtual_clutch.html)
>
> **⚠️ Binary5 availability must be confirmed before the bench flash.** Binary5 is labeled "BETA 1" and MaxxECU distributes firmware manually per-customer. When emailing `support@maxxecu.com` with the ACDP-2 binary dump, explicitly request Binary5 and confirm it is available for TCU `1034420288` / Bosch `0260550074`. If only Binary4 is provided, virtual clutch is unavailable — fall back to clutch kick (single DIN wire, binary behavior), C2 / AIN 5 wiring unneeded. Source: [maxxecu.com/webhelp/advanced-8hp-tcu_firmware.html](https://www.maxxecu.com/webhelp/advanced-8hp-tcu_firmware.html)
>
> **C2 is REQUIRED if Binary5 is confirmed** — AIN 5 lives on C2 pin G3 per MaxxECU RACE REV9+ wiring diagram. Defer C2 purchase until Binary5 is confirmed in writing from MaxxECU support.
>
> **Firewall crossing: ZERO wires.** The Remote-mount Simulator lives in the engine bay (mounted lower than the OEM clutch reservoir per vendor guidance). All 3 CPS wires stay engine-bay. The hydraulic line from the OEM E36 clutch master cylinder crosses the firewall via the existing OEM manual-trans clutch line provision — no new firewall penetration.

| Qty | Item | Notes |
|-----|------|-------|
| 1 | **DCT Clutch Simulator Remote + CPS** — dctshifter.com | Purpose-built hydraulic simulator with integrated CPS. Inlet M10×1.0. Sensor: 5V DC power, 0.5–4.5V output, 0–10 bar range, 1/8 NPT sensor thread. Body 160mm × 35mm × 85mm, 0.8kg anodized aluminum. Included: stainless steel mounting bracket, M3 bleed screw. ~4,995 SEK (~$475 USD). |
| 1 | Hydraulic line — OEM E36 clutch line reused | The OEM E36 manual-trans clutch line runs from cabin master cylinder to the (now-removed) slave cylinder near the bellhousing. Reuse it to feed the Simulator's M10×1.0 inlet — confirm fitting compatibility at install. Standard brake fluid. |
| — | Help spring (source at install if needed) | Vendor caveat: *"Please be aware: you might need a 'help spring' to correctly pull the pedal back… depends on your pedal's geometry and cylinder size."* — light-tension coil spring, anchored between pedal arm and a fixed body point. Order after fit-check. |

| Run | Color | Gauge | Length | Shielded | Notes |
|-----|-------|-------|--------|----------|-------|
| +5V supply | RD | 22 AWG | ~0.5 m | No | CPS +5V ← MaxxECU C1 G1 (+5V sensor rail, pin 25). Engine-bay direct, no crossing. |
| AIN 5 signal | WH | 22 AWG | ~0.5 m | No | CPS signal (0.5–4.5V) → MaxxECU C2 AIN 5 (C2 pin G3). Engine-bay direct. |
| Sensor GND | BN | 22 AWG | ~0.5 m | No | CPS SGND → MaxxECU C1 H1 (SGND, pin 29). Engine-bay direct. |

**MTune:** Advanced → 8HP → 8HP clutch control → `Enabled, Virtual clutch`. Analog Inputs → AIN 5 → type = `0-5V`, function = `Clutch Position`. Vendor calibration note: *"set 0% to at least 0.6V"* (0.5V is the sensor's resting value; leave headroom). Set clutch clamp start / end per MaxxECU 8HP settings page — these are critical for correct pressure modulation.

**Phase-to-phase:** Install at Phase 1B (8HP swap). Simulator + wiring carry unchanged through Phase 2 and Phase 3.

**Bleeding:** Standard brake-fluid bleeding procedure per [dctshifter.com/pages/installation](https://dctshifter.com/pages/installation) §3 — open Simulator bleed screw, pump pedal 3–5 times, close, repeat until pedal feel is firm.

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
| ~~Firewall bulkhead full pinout~~ | ✅ Done — `harnesses/firewall-crossing-maven.wv` (Maven HD30 dual 16+16). Superseded the AS79-based `firewall-bulkhead*.wv` files (deleted). |
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
| 22 AWG | WH/BU (CAN) | 2.5 m | 3.0 m | Body/Gauge.S CAN twisted pair — shielded |
| 24 AWG | BK (black) | 2.4 m (×2 conductors) | 3.0 m | E-pedal GND1 + GND2 both runs |
| 24 AWG | RD (red) | 2.4 m (×2 conductors) | 3.0 m | E-pedal VCC1 + VCC2 both runs |
| 24 AWG | GN (green) | 1.2 m (×1 conductor) | 1.5 m | E-pedal APS1 signal |
| 24 AWG | YE (yellow) | 1.2 m (×1 conductor) | 1.5 m | E-pedal APS2 signal |

> **Shielded runs — full list, consolidated from all systems (previous version of this note only covered Systems 3–5):**
>
> **Required (signal-critical, always shield):**
> | Run | System | Notes |
> |-----|--------|-------|
> | Crank trigger signal + supply/GND | M52 (Sys 2) + 07K (Sys 7) | M52: passive VR shielded pair (Signal+/Signal−/Shield→E3). 07K: Hall effect 3-wire (Signal/+5V/SensorGND); no dedicated shield drain — sensor GND to CMC H1 (pin 29). `.wv` source: `CRANK_HALL` in `maxxecu-07k.wv`. |
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
> | Fuel pump PWM ctrl (MaxxECU GPO → PMU16 CAN cmd; Phase 1: GPO → relay coil) | Fuel pump (Sys 4) |
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
| 1 | **Maven HD30 Dual 16+16 Bulkhead Kit** | mavenspeed.com/collections/b2t-engineering/products/dual-connector-bulkhead — $274 USD (config "16 PIN & 16 PIN"). Includes plate + both sides of both connectors + all size-16 contacts + template. See System 8 for full spec. | Cabin↔engine crossing |
| 1 | **BMW sensor PN `12141726590`** — VANOS cam sensor | Required before Phase 1 can fire — VANOS head cam sensor swap. Not a connector; this is the replacement sensor that matches the pre-terminated harness CAM connector. | M52 Phase 1 |
| 1 | MaxxECU RACE C2, 32-pin Molex harness connector | [MaxxECU store ID 1982](https://www.maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-mini-or-race-c2-or-pro-c4-32-pin-molex), $32.25 — C1 comes with the pre-terminated harness; C2 is separate. Phase 1: AIN 5 (G3) for 8HP virtual clutch. Phase 3: DBW, knock, e-pedal. Molex 63811-9200 crimp tool. | Phase 1 + 07K |
| 1 | VW `1J0 973 702` 2-pin Micro Timer pigtail | N205 VVT solenoid — automotive-connectors.com `42121600-PT` or Amazon B0D8FH4S8T | 07K harness |

---

## Harness Build Tools

One-time tooling purchase — covers all connector families in this build. See [`docs/harness-build.md`](harness-build.md) for the full pinning/depinning workflow, connector family warnings, and bench test procedure before install.

| Tool | Model | Price | Connector Family / Use |
|------|-------|-------|------------------------|
| Flush cutters | **Milwaukee 48-22-6106** ([Home Depot](https://www.homedepot.com/p/Milwaukee-6-in-Diagonal-Cutting-Pliers-48-22-6106/205652216) $19.97) | ~$20 | Essential for in-car wire trimming — angled jaw cuts flush to connector body, gets into tight spaces. Used constantly. Source: StreetCarJoe Race Car Wiring Pt.1. |
| Wire stripper | **Ideal Stripmaster 45-097** (~$60–90, [Amazon](https://www.amazon.com/dp/B000RFSWF8)) with included **L4994 blades** (16–26 AWG) | ~$65 | Community standard for motorsport harness work (HPA courses, StreetCarJoe, Rywire). Fixed-notch blades stop before the conductor — 22 AWG hole (0.039") prevents strand-nicking on TXL regardless of hand pressure. Works on TXL and GXL. Do NOT use auto-adjusting or general-purpose strippers on 22 AWG TXL — thin insulation wall means wrong-geometry blades nick strands. Source: [HPA forum](https://www.hpacademy.com/forum/practical-harness-construction-club-level/show/wire-stripper-1/). |
| VAG 1.5mm sensor contact crimper | **IWISS IWS-2820M** ([Amazon](https://www.amazon.com/dp/B078WNZ9FW) $19.99) | ~$20 | VAG 1.5mm sealed-series contacts (TE MCP 1.5) in sensor pigtail housings (3B0973703G cam/crank/MAP, 1J0973702 CLT/IAT). Wire range 28–20 AWG (0.08–0.5mm²) — matches the 0.35–0.5mm² signal wires in these connectors. Two-pass operation: conductor crimp first, then insulation crimp. Also handles general small open-barrel contacts, ring terminals, and relay socket contacts in this AWG range. |
| VAG 2.8mm COP contact crimper | **IWISS IWS-2412M** ([Amazon](https://www.amazon.com/dp/B07G98DLB8) $19.99) | ~$20 | VAG 2.8mm JPT-series contacts in COP coil pigtail housings (4B0973724 — 4-pin coil-on-plug connector, 0.5–1.0mm² / 18–20 AWG coil primary wires). Die widths: 2.2 / 2.5 / **2.8** / 3.1 / 3.4mm — the 2.8mm die is a direct match for VAG JPT contacts. Also covers any other open-barrel contact in AWG 24–12 range. Companion to IWS-2820M: together the two IWISS tools span AWG 28–12 with no gap. |
| Open-barrel engine bay (general) | _(use IWS-2820M or IWS-2412M above per AWG)_ | — | **In the engine bay and anywhere exposed to moisture/vibration: use non-insulated barrel + adhesive-lined heat shrink** over every crimp. Adhesive liner seals against capillary wicking that pre-insulated connectors allow. Interior/cabin: pre-insulated nylon-sleeve crimps acceptable with the correct ratcheting tool. Source: StreetCarJoe Race Car Wiring Pt.1. |
| **Deutsch solid barrel crimper** | **Deutsch HDT-48-00** | ~$197 ([mavenspeed.com/…/deutsch-crimp-tool-solid-contacts](https://mavenspeed.com/collections/b2t-engineering/products/deutsch-crimp-tool-solid-contacts)) | **Required for the Maven HD30 dual bulkhead kit (System 8) and all other Deutsch solid contacts in this build (DT 2-pin bypasses, PST-F1 pigtail, etc).** Covers ALL Deutsch solid pins and sockets across DT/DTM/DTP/DTHD/HD10/HD30/HDP20/DRC/DRB/DTV/AEC/STRIKE/Jiffy Splice series, contact sizes 12/16/20. Source: [deutschconnector.com HDT-48-00](https://www.deutschconnector.com/products/deutsch_connector_tools/deutsch_connector_crimp_tools/HDT-48-00/) and [Crimp Tool Selection Guide](https://www.deutschconnector.com/technical/deutsch_connector_crimp_guide/). One tool, one purchase — no additional positioners needed. |
| Ferrule crimper | **iCrimp AWG23-10** (HSC8 6-4A, [amazon.com/dp/B00XVB6B1C](https://www.amazon.com/dp/B00XVB6B1C)) | ~$25 | Stranded wire ends into screw-clamp terminals (ECU power/ground, DIN rail fuse block). Self-adjusting ratchet, 0.25–6mm² (AWG 23–10). ⚠️ PN IWS-10 does not exist in IWISS/iCrimp's catalog — corrected to AWG23-10. |
| Deutsch HD30/DT extraction tool | Standard round-shoulder extraction tool (Maven or generic) | ~$15–35 | Removes size-16/20 solid contacts from Deutsch HD30 (Maven bulkhead) and DT-series connectors. Push in from front, releases collet, contact exits rear. Maven sells one at $34.97 ([mavenspeed.com/…/deutsch-terminal-tool](https://mavenspeed.com/collections/b2t-engineering/products/deutsch-terminal-tool)). Do not use a screwdriver. |
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

> **Total non-Molex tools: ~$383** (flush cutters $20 + wire stripper $30 + IWS-2820M $20 + IWS-2412M $20 + Lisle $20 + rivnut tool ~$71 + Deutsch HDT-48-00 $197 + Deutsch extraction $15 + ferrule crimper $25). The Deutsch HDT-48-00 covers ALL Deutsch solid contacts across DT/DTM/DTP/DTHD/HD30/HDP20 series (per deutschconnector.com selection guide) — no separate AS-series crimper set needed under the H2O engine-bay-mount architecture (the deprecated AS79 bulkhead required a Daniels AFM8 + positioners bundle ~$808; the switch to Maven HD30 dual eliminates that).
>
> **Budget tracking:** Key tools above are also tracked in `e36-docs/E36_CSVs/E36_Phase1_Foundation.csv` (Tooling category) with purchase links and price ranges for build cost rollup.
> If using Souriau 8STA for the bulkhead instead of Deutsch AS, confirm the correct positioner for Souriau contacts at purchase — Souriau uses compatible tooling but a different positioner.
> **MaxxECU Molex C1/C2 connectors:** Molex crimp tool PNs confirmed from [MaxxECU RACE pinout webhelp](https://www.maxxecu.com/webhelp/wirings-maxxecu_pinout.html). The small tool (63811-9200) is the primary purchase — covers ~85% of C1 and ~75% of C2 pins. The big tools are expensive (~$200+ each); consider outsourcing the handful of large-terminal pins if budget is a concern. For extraction/repair: Molex removal tool 638132400 (small) or 638132300 (big).
