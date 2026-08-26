# Sensor & Actuator Pinout Reference

This document records the **physical pin layout and OEM wire colors** for every sensor,
actuator, and module in the build at the point where our new cables mate to the device.
It is the reference to use when crimping pigtails — the `.wv` schematic files show
pin *function* labels; this file adds the physical pin numbering and the OEM wire colors
so you can confirm the right wire at the connector face before crimping.

---

## Context: two sets of wires at every connector

Every connector in this build is a junction between two harnesses:

| Side | What it is | Wire colors |
|------|-----------|-------------|
| **Device / sensor side** | Pigtail or body wires integral to the sensor/coil/module | OEM manufacturer colors — documented here |
| **Build harness side** | Our new cables as defined in the `.wv` files | This build's convention (BN=Sensor GND, BU=IGN, GY=INJ, etc.) |

The OEM wire colors listed here are the colors on the **sensor/device side** of the
connector. Use them to verify correct pin orientation by looking at the device pigtail
before you seat the new pigtail's terminal. The colors on our cable side follow
`docs/harness-build.md § Color convention`.

---

## Confidence legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Confirmed from official manufacturer datasheet or official BMW documentation |
| 🟡 | Confirmed from community-verified source (BMW ETM excerpts, MaxxECU webhelp, well-cited forum thread with cross-reference) |
| 🔶 | Reported from forum post only — plausible but not independently verified against ETM |
| ❌ | Unknown / not found in any source |

---

## Connector families in this build

| Family | Common name | Physical description | BMW/VAG part number |
|--------|-------------|---------------------|---------------------|
| Bosch JPT 2-pin | Jetronic/Minitimer 2-way | Small rectangular, side-latch | Various; CLT/IAT use this |
| Bosch JPT 3-pin | Jetronic/Minitimer 3-way | Same housing, 3 cavities | Various |
| VAG 3-pin (3B0973703G) | VAG sensor plug, 3-way | Grey rectangular, top-latch | 3B0973703G / 1J0973703 |
| VAG 4-pin (1J0973724) | VAG ignition coil, 4-way | Black rectangular, top-latch | 1J0973724 |
| USCAR 2-pin (EV6) | EV6 / EV14 injector | Square compact with side-lock | See Delphi / TE pigtail kits |
| Bosch Trapezoid 5-pin | PST-F1 mating | Trapezoidal 5-pin | F02U.B00.751-01 |
| BMW APS 6-pin | E46 accelerator pedal | 6-pin rectangular | Pedal-integral; source pigtail from donor harness |

---

## Sensors

### Crank Position — M52 VR, front timing cover

| Field | Value |
|-------|-------|
| BMW part number | OEM M52 front crank sensor (sold as assembly with recall kit) |
| Sensor type | VR (variable reluctance) — passive, no power supply |
| Connector (sensor side) | Bosch JPT 3-pin |
| Connector (chassis side) | 3B0973703G — same housing as cam and MAP |
| Wheel | 60-2 missing tooth, MaxxECU trigger type: N-1 |

| Pin | Function | OEM chassis harness color | Confidence |
|-----|----------|--------------------------|------------|
| 1 | VR Signal+ | **Yellow** (YE) | 🔶 |
| 2 | VR Signal− | **Black** (BK) | 🔶 |
| 3 | Shield drain | Bare/uncolored | 🔶 |

Source: R3VLimited forum — S52 engine swap using 525i harness color codes:
"crankshaft sensor: yellow, black, no color."
([r3vlimited.com](https://www.r3vlimited.com/board/forum/e30-technical-forums/24v-engine-swaps/m50-52-s50-52/56173-s52-swap-using-1995-525i-harness-color-codes))
MoTeC forum thread corroborates Yellow = signal pin for M52/S52 crank sensor.
([forum.motec.com.au](https://forum.motec.com.au/viewtopic.php?f=11&t=628))

> ⚠️ **VR polarity matters.** Swapping Signal+ and Signal− produces 180° timing error or loss
> of sync. On the 60-2 wheel, MaxxECU may still find sync but with incorrect cylinder phasing.
> Verify with an oscilloscope before first start: Signal+ should go positive when the tooth
> leading edge approaches the sensor.
>
> ⚠️ **Post-recall crank sensor** (rear bell-housing, Hall effect, uses adapter harness) has
> a DIFFERENT pinout: VCC / Signal / GND. If this build ever transitions to the rear Hall
> sensor, the adapter harness wire colors are Red/White = VCC, Yellow = Signal, Brown = GND
> (Bimmerforums thread). The MaxxECU trigger type must also change.

---

### Cam Position — BMW 12141726590 (non-VANOS Hall)

| Field | Value |
|-------|-------|
| BMW part number | 12141726590 |
| Sensor type | Hall effect — no external +12V supply on this variant |
| Connector (sensor side) | 3-wire pigtail integral to sensor body |
| Connector (chassis side) | 3B0973703G — same housing as crank and MAP |

> ⚠️ **OBD2 M52 cam note.** The stock OBD2 M52 cam sensor is NOT a standard Hall type —
> it uses a proprietary Pulse Angle Generator (PAG) that sends/receives a sine wave from
> the OEM Siemens DME. Aftermarket ECUs cannot use this sensor. The build specifies
> BMW 12141726590 (non-VANOS M50TU/M52TU intake cam sensor) which is a standard Hall
> effect sensor and plugs into the OBD2 M52 cam connector after removing two locking tabs.
> Source: R3VLimited Ecumaster community thread.
> ([community.ecumaster.com](https://community.ecumaster.com/t/bmw-m50b25-trigger-wiring/4056))

| Pin | Function (non-VANOS pinout) | Sensor pigtail wire color | Confidence |
|-----|-----------------------------|--------------------------|------------|
| 1 | Signal (Hall output) | **Red** | 🔶 |
| 2 | Sensor GND | **Green** or **Black** — see note | 🔶 |
| 3 | Shield drain | Remaining of Green/Black | 🔶 |

Source for pin functions: MaxxECU M50 terminated harness webhelp — non-VANOS cam
sensor pinout table: "Pin 1 = Signal, Pin 2 = Sensor GND, Pin 3 = Shield."
([maxxecu.com](https://www.maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html))

Source for wire colors: Bimmerforums cam sensor thread — poster confirms sensor body
(part 12141726590, SWF branded) has "red, grn, blk on that side. This does confirm
the center is the signal." ([bimmerforums.com](https://www.bimmerforums.com/forum/showthread.php?2341402-Cam-sensor-wire-colors))

Wire color assignment for GND vs. Shield (Pin 2 vs. Pin 3) is **not confirmed** from
this source — "center" is ambiguous on a 3-pin inline connector. Before crimping,
measure resistance between Pin 2 and the sensor body/shield foil to identify the
shield pin. The shield will read near 0 Ω to the outer braid; GND will not.

> ⚠️ The VANOS-type cam sensor (opposite pinout: Pin 1 = +12V, Pin 2 = Signal, Pin 3 = GND)
> uses the same connector housing. The two sensors look identical from the outside. Do NOT
> swap them — the non-VANOS sensor has no internal current limiter for Pin 1 +12V; applying
> 12V to Signal will damage the sensor. Label the pigtail at crimp time.

---

### Coolant Temperature (CLT) — M52

| Field | Value |
|-------|-------|
| BMW part number | 13621703993 (ECU sensor); 61311366702 (cluster sensor — separate connector) |
| Sensor type | NTC thermistor — passive, symmetric, **not polarity sensitive** |
| Connector | Bosch JPT 2-pin |

| Pin | Function | OEM chassis harness color | Confidence |
|-----|----------|--------------------------|------------|
| 1 | Signal / GND (either) | **Brown** | 🔶 |
| 2 | Signal / GND (either) | **Red/Brown** (RD/BN stripe) | 🔶 |

Source: R3VLimited S52 swap color code thread: "DME coolant: brown, red/brown."
([r3vlimited.com](https://www.r3vlimited.com/board/forum/e30-technical-forums/24v-engine-swaps/m50-52-s50-52/56173-s52-swap-using-1995-525i-harness-color-codes))

Polarity insensitivity confirmed: NTC thermistors are passive resistors. Either
terminal can connect to the ECU signal input or to sensor GND — function is identical.

> Note: The M52 uses a combined CLT sensor (single housing, two connectors) for
> ECU + cluster. The ECU-side is the 2-pin JPT above. Do not confuse with the
> 1-pin cluster sensor connector on the same housing.

---

### Intake Air Temperature (IAT) — M52

| Field | Value |
|-------|-------|
| Sensor type | NTC thermistor — passive, symmetric, **not polarity sensitive** |
| Connector | Bosch JPT 2-pin |
| Location | Mounted in intake boot, upstream of throttle body |

| Pin | Function | OEM chassis harness color | Confidence |
|-----|----------|--------------------------|------------|
| 1 | Signal / GND (either) | **Grey** | 🔶 |
| 2 | Signal / GND (either) | **Brown** | 🔶 |

Source: R3VLimited S52 swap color code thread: "air intake temp: grey, brown."
([r3vlimited.com](https://www.r3vlimited.com/board/forum/e30-technical-forums/24v-engine-swaps/m50-52-s50-52/56173-s52-swap-using-1995-525i-harness-color-codes))

---

### MAP Sensor — aftermarket (3-pin VAG)

| Field | Value |
|-------|-------|
| Connector (sensor side) | 3-pin VAG sensor plug |
| Connector (chassis side) | 3B0973703G — same housing as cam and crank |
| Location | Engine bay, ported to intake manifold via vacuum line |

| Pin | Function | OEM wire color | Confidence |
|-----|----------|----------------|------------|
| 1 | +5V supply | ❌ unknown | ❌ |
| 2 | Sensor GND | ❌ unknown | ❌ |
| 3 | Signal (0–5V analog) | ❌ unknown | ❌ |

Pin functions confirmed from MS4X wiki (documents BMW/VAG 3-pin MAP connector used
with Siemens ECUs): "Pin 1 = +5V, Pin 2 = Ground, Pin 3 = Signal Output."
([ms4x.net](https://www.ms4x.net/index.php?title=Electrical_Connectors))

Wire colors depend on the specific MAP sensor model used. Since the M52 build
uses an aftermarket MAP (the OEM M52 uses MAF, not MAP), the wire colors on the
sensor pigtail will be specific to the chosen sensor. **Identify by function before
crimping — do not assume color.**

---

### Knock Sensors — M52 (×2)

| Field | Value |
|-------|-------|
| BMW part numbers | 12141703276 (cyl 1–3), 12141703278 (cyl 4–6) |
| Sensor type | Bosch KS piezoelectric — broadband vibration |
| Connector | Bosch round 1-pin + body thread |
| Mounting | M8 thread into block; body thread = second electrical contact (shield/GND path) |

| Connection | Function | OEM chassis harness color | Confidence |
|------------|----------|--------------------------|------------|
| Single wire pin | Knock signal (differential) | **Black** | 🔶 |
| Shield drain (separate from signal wire) | Shield GND — terminates at DME shield GND pin | Bare/uncolored | 🔶 |
| Sensor body / mounting bolt | **Not a separate wire** — sensor body seats to block | — | ✅ |

Source: R3VLimited S52 swap color thread: "knock sensors: black, no color."
([r3vlimited.com](https://www.r3vlimited.com/board/forum/e30-technical-forums/24v-engine-swaps/m50-52-s50-52/56173-s52-swap-using-1995-525i-harness-color-codes))
R3VLimited VANOS wiring thread corroborates: "knock sensor, 1-3 BLK NCA" (BLK = Black,
NCA = No Colour Assigned for shield drain).

> ⚠️ MaxxECU RACE wires each knock sensor as Signal + Shield drain to the same ECU
> connector entry. The shield drain runs separately from the signal wire back to CMC H1
> (Sensor GND / pin 29 via AS79 bulkhead pin 45 in the 07K build). Do not terminate the
> shield to chassis GND — it must go to ECU Sensor GND. See `maxxecu-07k.wv`
> connections block for the exact routing.

---

### TPS — M52 (OEM potentiometer)

| Field | Value |
|-------|-------|
| Sensor type | 3-wire potentiometer — directional, polarity sensitive |
| Connector | Bosch JPT 3-pin |

| Pin | Function | OEM chassis harness color | Confidence |
|-----|----------|--------------------------|------------|
| 1 | +5V reference | **Red/Yellow** | 🔶 |
| 2 | Signal | — | ❌ |
| 3 | Sensor GND | **Brown/Black** | 🔶 |

Source: R3VLimited VANOS wire identification thread — respondent identifies
"red/yellow - brown/black - brown = TPS" for M50/S50 harness.
([r3vlimited.com](https://www.r3vlimited.com/board/forum/e30-technical-forums/24v-engine-swaps/m50-52-s50-52/222909-halp-identifying-some-m50-vanos-wires-plz))

> ⚠️ TPS Pin 2 color not found in available sources. Verify with DMM before crimping:
> apply +5V to Pin 1, GND to Pin 3, measure voltage at Pin 2 while rotating the throttle.
> Should sweep ~0.4–4.8V from closed to WOT. Swap Pin 1 and Pin 3 if voltage moves
> in the wrong direction.

---

## Actuators

### Ignition Coils — VAG 4-pin COP, long type (06B905115 / R8 style)

| Field | Value |
|-------|-------|
| Connector (coil side) | 1J0973724 (VAG 4-pin, long body) |
| Coil PN (compatible) | 06B 905 115 (various suffix revisions); Audi R8 ignition coil |

| Pin | Function | Note |
|-----|----------|------|
| 1 | +12V Power (switched) | Connect to coil/INJ relay rail, fused 20A |
| 2 | Signal GND | Reference GND for ECU trigger logic — **connect to ECU power GND / engine block** |
| 3 | Trigger signal | ECU IGN output (Blue wire in this build) |
| 4 | Power GND | Engine block GND |

Sources (all agree on this pinout):
- Motorsport Electronics COP install guide: "Long/Normal Coil: Pin 1 = 12V Power, Pin 2 = Signal Ground (Cyl Head), Pin 3 = Trigger Signal, Pin 4 = Power Ground (Cyl Head)."
  ([motorsport-electronics.co.uk](https://motorsport-electronics.co.uk/onlinehelp/html/Coil-On-PlugCOPSInstall.html))
- MSExtra / MS2 hardware manual (community consensus): "Pin 1 = +12V, Pin 2 = Signal GND (engine block), Pin 3 = Spark Signal, Pin 4 = Power GND."
  ([msextra.com](https://www.msextra.com/doc/pdf/html/MS2V30_Hardware-3.4.pdf/MS2V30_Hardware-3.4-87.html))
- VEMS wiki IgnitionPage/COP: same pin assignments.
  ([vems.hu](https://www.vems.hu/wiki/index.php?page=IgnitionPage%2FCOP))

OEM wire colors at coil pigtail: ❌ not found in available sources. Identify
by continuity to coil body terminal before crimping.

> ⚠️ **Pin 2 is NOT sensor GND.** It is the reference ground for the ECU's driver
> logic signal. Wire it to ECU power GND (or directly to cylinder head GND). Wiring
> Pin 2 to the MaxxECU Sensor GND pin (CMC H1) will inject ignition switching noise
> into the sensor GND bus and corrupt all sensor readings.
> Source: Ecumaster community forum confirmation.
> ([community.ecumaster.com](https://community.ecumaster.com/t/wiring-for-vag-audi-4-pin-cop/3649))
>
> ⚠️ **Short type VAG coil has different pinout** — Pin 1 and 4 swap. This build uses
> long type only. Confirm coil body length before assuming pinout.

---

### Fuel Injectors — Bosch EV6 / EV14 (2-pin USCAR)

| Field | Value |
|-------|-------|
| Connector | USCAR 2-pin (EV6 / EV14 standard) |
| Polarity | **Not polarity sensitive** — solenoid is symmetric |

| Pin | Conventional assignment | Note |
|-----|------------------------|------|
| 1 | +12V supply | Either pin can be +12V |
| 2 | ECU low-side driver | Either pin can be ECU ground switch |

Source: Hang Tight fuel injector connector guide: "Injectors are not polarity sensitive.
One side is 12V and the other is a ground path, which is controlled by the ECU. Either
pin can be 12V or the ECU trigger, best practice to make them the same [across all injectors]."
([hangtight.io](https://hangtight.io/blogs/resources/identifying-your-fuel-injector-connector-a-how-to-guide))

> Best practice: wire all injectors with +12V on the same physical cavity position for
> consistency, even though polarity doesn't affect function. The MaxxECU is a low-side
> driver (switches GND to fire the injector).

---

### VANOS Solenoid — M52 single VANOS (on/off)

| Field | Value |
|-------|-------|
| Connector | 2-pin solenoid connector |
| Operation | Simple on/off; MaxxECU drives as low-side GPO |

| Pin | Function | OEM chassis harness color | Confidence |
|-----|----------|--------------------------|------------|
| 1 | +12V (switched) | **Red/White** (RD/WH) | 🔶 |
| 2 | GPO signal (low-side to ECU) | **Green/Blue** (GN/BU) | 🔶 |

Source: R3VLimited VANOS wire identification thread (M50/S50 harness):
"VANOS solenoid: RED/WHT GRN/BLU."
([r3vlimited.com](https://www.r3vlimited.com/board/forum/e30-technical-forums/24v-engine-swaps/m50-52-s50-52/222909-halp-identifying-some-m50-vanos-wires-plz))

> ⚠️ Source is M50/S50 — M52 harness wire colors may differ. Verify polarity before
> connecting: +12V should be present at the solenoid connector with ignition on and
> the ECU unplugged. If colors differ, trace from the ECU connector (GPO3 = CMC D4/pin 16).

---

## Accessories / Aftermarket

### E-Pedal — BMW E46 APS Module (35426786282 / 35426786281)

| Field | Value |
|-------|-------|
| BMW part numbers | 35426786282 (manual), 35426786281 (automatic) — same sensor, same pinout |
| Connector | 6-pin APS connector integral to pedal body |
| Sensor type | Dual Hall effect — two fully independent circuits |

| Pedal pin | Function | OEM chassis harness color | AWG | Confidence |
|-----------|----------|--------------------------|-----|------------|
| 1 | GND1 — APS1 Sensor GND | **Brown/Green** (BR/GN) | 0.35 mm² | 🟡 |
| 2 | GND2 — APS2 Sensor GND | **Brown** (BR) | 0.35 mm² | 🟡 |
| 3 | VCC2 — APS2 +5V supply | **Yellow/Green** (GE/GN) | 0.35 mm² | 🟡 |
| 4 | Output1 — APS1 signal | **White** (WS) | 0.35 mm² | 🟡 |
| 5 | VCC1 — APS1 +5V supply | **Yellow** (GE) | 0.35 mm² | 🟡 |
| 6 | Output2 — APS2 signal | **White/Green** (WS/GN) | 0.35 mm² | 🟡 |

Source: BMW MS45.1 DME pinout table — documents the APS connector wire colors from
the ECU's harness to the pedal module pins. The MS45.1 is the S54/M3 E46 ECU variant
but uses the same 35426786282 pedal assembly, and the APS sub-harness design is common
across E46 variants.
([bimmer-service.com](https://www.bimmer-service.com/2025/11/25/dme-ms45-1-pinout-service-manual/))

Voltage characteristics (source: `.wv` file notes, citing HP Academy forum + openinverter.org):
- APS1: idle ≈ 0.70V, WOT ≈ 4.50V
- APS2: idle ≈ 0.36V, WOT ≈ 2.20V — intentionally ≈ half of APS1 at every pedal angle
- MaxxECU cross-checks the ratio; mismatch triggers e-throttle shutdown

> ⚠️ Both GND pins (1 and 2) and both VCC pins (3 and 5) must be individually connected.
> The two APS circuits are electrically independent. Do not share a single GND or VCC wire
> between APS1 and APS2 circuits — MaxxECU monitors each circuit independently.

---

### Oil Pressure + Temperature — Bosch PST-F1

| Field | Value |
|-------|-------|
| Bosch motorsport order number | 0261 544 01F |
| OEM equivalent | 0281006414 |
| Connector | Bosch Trapezoid 5-pin |
| Mating connector kit | F02U.B00.751-01 |
| Thread | M10×1, 45° sealed cone, 27 mm hex, 40 Nm |

| Pin | Function | Note |
|-----|----------|------|
| 1 | Not used | Leave empty — no wire |
| 2 | Pressure signal (0.5–4.5V) | Ratiometric; 10 bar full scale |
| 3 | +5V supply | 4.75–5.25V, ~10 mA |
| 4 | Ground | |
| 5 | Temperature signal (NTC) | Use 4.6 kΩ pull-up to +5V at ECU AIN |

> ⚠️ **Physical vs functional pin mapping:** The `.wv` files (`maxxecu-07k.wv`, `pst-f1-sensor.wv`) describe the sensor as a **4-function connector** (pins 1–4 = +5V / GND / Pressure / Temp) in functional order. The physical housing `F02U.B00.751-01` is a **5-pin body** using the numbering above (physical pin 1 unused). Wire by function label — do **not** treat `.wv` pin 1 as physical housing pin 1. Mapping: `.wv` pin 1 (+5V) = physical pin 3; `.wv` pin 2 (GND) = physical pin 4; `.wv` pin 3 (Pressure) = physical pin 2; `.wv` pin 4 (Temp) = physical pin 5.

Source: Bosch Motorsport official datasheet for PST-F 1.
([bosch-motorsport.com PDF](https://www.bosch-motorsport.com/media/catalog_content/downloads_catalog/pdf_catalog/data_sheet_70496907_pressure_sensor_combined_pst-f_1.pdf))
Corroborated by Bosch Motorsport product page and xtramotorsport.com product listing.

Wire colors at the mating connector (F02U.B00.751-01 kit): ❌ kit ships with
contacts only, no pre-attached wires. Use build convention colors at this connector.

---

### Wideband O2 — Bosch LSU 4.2 / LSU 4.9

Wire colors are fully documented in the `.wv` files directly (the MaxxECU terminated
harness pre-wires the WBO2 connector):

| Pin | Function | LSU 4.2 wire color | LSU 4.9 wire color |
|-----|----------|-------------------|-------------------|
| 1 | VS (pump cell signal) | Black | Black |
| 2 | RCAL (calibration resistor) | Green | Green |
| 3 | H+ (heater +) | Grey | White |
| 4 | H− (heater −) | White | Grey |
| 5 | VREF (reference cell) | Yellow | Yellow |
| 6 | IP (pump current) | Red | Red |

Source: `.wv` inline notes — "Always verify by wire color — do not rely on pin number alone."
(`maxxecu-m52.wv` line ~316; `maxxecu-07k.wv` line ~534)

> ⚠️ LSU 4.2 and LSU 4.9 swap Pin 3 and Pin 4 (H+ and H−). The connector bodies look
> identical. Always verify the Bosch part number on the sensor body before connecting
> to the MaxxECU WBO2 controller circuit.

---

## Summary: sensors where polarity matters for correct function

These sensors will malfunction silently or damage if a pin is reversed. Verify
before first start.

| Sensor | Critical pins | Consequence of reversal |
|--------|--------------|------------------------|
| Crank VR | Signal+ / Signal− | 180° timing error or no sync |
| Cam Hall (12141726590) | Signal / GND | Sensor may not output; no cam sync |
| TPS (potentiometer) | +5V / GND | Signal moves wrong direction; inverted throttle |
| VAG COP coil | Pin 2 to correct GND bus | Noise on sensor GND bus if wrong |
| APS pedal | All 6 pins individually | APS mismatch triggers e-throttle fault |
| PST-F1 | +5V / GND | Sensor has reverse polarity protection — but verify anyway |

## Summary: sensors where polarity does NOT matter

| Sensor | Reason |
|--------|--------|
| CLT, IAT (NTC thermistor) | Symmetric passive resistor |
| Knock sensors | Piezoelectric element generates AC signal; polarity-independent at ECU input |
| Fuel injectors (EV6/EV14) | Solenoid coil is symmetric |
