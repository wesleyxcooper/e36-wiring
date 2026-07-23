# EWP Wiring Reference — Pierburg CWA400 + MaxxECU PWM Control

**Build context:** 07K / 8HP swap, MaxxECU RACE, Gauge.S E36 PNP cluster. CWA400 replaces OEM belt-driven 07K water pump. OEM pump impeller removed, housing stays mounted as coolant manifold. MaxxECU controls pump speed directly via PWM GPO. No separate pump controller needed. Confirmed approach: @wingman703 (07K/8HP Miata swap — identical drivetrain config).

> ⚠️ **Version warning:** Pierburg CWA400 production split ~March 2024. **Pre-March 2024 = PWM version** (MaxxECU-controllable). **Post-March 2024 = LIN bus version** (NOT directly PWM-controllable — requires LIN adapter). Verify part number before purchasing.

---

## Pump — Pierburg CWA400 (PWM Version)

| Item | Value |
| :--- | :--- |
| Manufacturer | Pierburg (Continental / Vitesco Technologies) — OEM BMW/VW |
| Type | Brushless centrifugal canned motor |
| Voltage | 8–16V (nominal 12.5V) |
| Flow rate | ~150 LPM @ 0.85 bar / ~220 LPM @ 0.55 bar |
| Max speed | ~5,900 RPM |
| Current draw | 35.5A nominal / 36.3A max |
| Coolant temp range | −40°C to +128°C |
| Ambient temp range | −40°C to +140°C |
| Protection | IP67 |
| Hose size | Ø 40mm (1.574") barb |

**Part numbers — PWM version (source these):**
| Part# | Application |
| :--- | :--- |
| Pierburg `7.07223.10.0` | Primary Pierburg catalog number — PWM version |
| BMW `11515A05704` | BMW OEM cross-reference — PWM version |
| BMW `11517563659` | BMW OEM cross-reference — PWM version |
| BMW `11517568594` | BMW OEM cross-reference — PWM version |

**Part numbers — LIN version (do NOT source these):**
| Part# | Notes |
| :--- | :--- |
| Pierburg `7.03665.66.0` | LIN bus only — NOT PWM-controllable via MaxxECU |
| BMW `11517604027` | LIN version OEM cross |
| BMW `11518625097` | LIN version OEM cross |

**Sourcing:**
- New from Dedicated Motorsports: ~$720 ([dedicatedmotorsports.com](https://dedicatedmotorsports.com/products/pierburg-cwa400-intercooler-pump-pwm-version.html))
- OEM pull (BMW parts car / eBay): $50–150 used — **must verify PWM part number before purchasing**

---

## Connector — Kostal 2+2 (4-pin)

The CWA400 uses a Kostal 2+2 connector. Pins 1–2 are small (2.8mm) for signal/diagnostic; Pins 3–4 are large (5.8mm) for power.

| Pin | Function | Wire gauge |
| :--- | :--- | :--- |
| 1 | PWM control signal (from MaxxECU GPO) | 22 AWG |
| 2 | BSD diagnostic (unused — leave floating or tie to GND) | 22 AWG |
| 3 | +12V power (via 40A relay) | 10 AWG |
| 4 | Ground | 10 AWG |

**Connector parts:**
| Part | Description | Kostal Part# |
| :--- | :--- | :--- |
| Plug (male) | Kostal 2+2 housing | `10098866` |
| Small terminal (×2) | Kostal SLK 2.8 ELA (Pins 1, 2) | `22124499560` |
| Small seal (×2) | Kostal SLK 2.8 ELA seal | `10800444522` |
| Large terminal (×2) | Kostal SLK 5.8 ELA (Pins 3, 4) | `22124544900` |
| Large seal (×2) | Kostal SLK 5.8 ELA seal | `10800583690` |

---

## MaxxECU PWM Configuration

| Parameter | Value |
| :--- | :--- |
| Output type | PWM GPO (General Purpose Output) |
| PWM frequency | **680 Hz** (recommended; acceptable range 50–1000 Hz) |
| Duty cycle 0% | Pump sleep / off |
| Duty cycle 1–12% | Emergency run or stop — **do not use in normal map** |
| Duty cycle 13–85% | **Controlled operation** — linear min to max speed |
| Duty cycle 86–97% | Maximum speed (full flow) |
| Duty cycle 98–100% | Emergency run (~5,900 RPM) |

**Recommended CLT-to-duty-cycle map:**
| CLT | Duty Cycle | Notes |
| :--- | :--- | :--- |
| ≤ 60°C | 20% | Warm-up — low flow |
| 75°C | 35% | Normal cruise |
| 85°C | 55% | Target operating temp |
| 95°C | 75% | Elevated — increase flow |
| 100°C | 90% | High load / boost |
| ≥ 105°C | 97% | Full speed — protect engine |

> ⚠️ **Wake pulse:** The CWA400 requires an uninterrupted high pulse of **≥ 3ms** at startup to wake from standby. At 680 Hz, a 50% duty cycle (≈0.74ms high) is insufficient alone — ensure MaxxECU outputs a brief 100% command at ignition-on before transitioning to the CLT map. Verify in MaxxECU output config (startup duty override or output enable delay).

> ⚠️ **PWM voltage:** MaxxECU GPO high = 12V. CWA400 requires V_Hi ≥ 0.6 × Ub (≥ 7.2V at 12V supply) — MaxxECU output voltage is compliant. No level shifting needed.

---

## Power Wiring

The CWA400 draws up to 35.5A — requires heavier wiring than the EWP150 setup.

| Wire | Spec | Notes |
| :--- | :--- | :--- |
| BATT+ to relay pin 30 | 10 AWG, fused 40A within 12" of battery | Always-on feed to relay |
| Relay pin 87 to pump Pin 3 | 10 AWG | Switched pump power |
| Pump Pin 4 to chassis GND | 10 AWG | Dedicated ground stud — do not share with signal grounds |
| MaxxECU GPO to pump Pin 1 | 22 AWG | PWM signal — short run preferred |
| Relay coil (pin 86) | Switched +12V IGN source (via MaxxECU relay output or IGN relay) | |
| Relay coil (pin 85) | Chassis GND | |

**Relay:** Use a 40A automotive relay (Bosch 0 332 002 150 or equivalent). Standard 4- or 5-pin relay.

---

## CLT Sensor Strategy

One sensor only — **MaxxECU CLT sensor** controls everything. No separate Davies Craig thermistor needed.

| Sensor | Location | Consumer |
| :--- | :--- | :--- |
| MaxxECU CLT (2-wire NTC, 10kΩ @ 25°C typical) | Engine coolant port — BBG rear coolant flange or block fitting (M10×1.0 or 1/8" NPT) | MaxxECU → CWA400 PWM duty map |

---

## Post-Shutdown Cooling

MaxxECU handles post-shutdown pump operation via its power hold relay output:

1. Key-off → MaxxECU power hold relay keeps ECU powered
2. MaxxECU continues commanding CWA400 via PWM until CLT drops below setpoint (configurable threshold)
3. MaxxECU powers down → relay releases → pump stops

Configure in MaxxECU: **Outputs → Power Hold Relay** — set condition to CLT < target temp (e.g., 70°C) AND engine-off. This replaces the Davies Craig controller's autonomous post-shutdown logic.

> ⚠️ A dedicated power hold relay is **required** for post-shutdown pump operation. Without it, MaxxECU shuts off at key-off and the pump stops immediately (no soak protection). Wire relay coil to MaxxECU power hold output; relay pin 87 to MaxxECU main 12V feed.

---

## Mechanical Pump Deletion — 07K Specific

OEM impeller removal / housing-in-place approach (this build retains heater core plumbing):

1. OEM pump `07K121011B` — bring to Euromotive at longblock dropoff
2. Instruct shop: **remove impeller only** — leave housing mounted and plumbed to coolant circuit
3. Housing serves as coolant distribution manifold; pulley freewheels passively in belt path (no load)
4. Remove thermostat from OEM housing (MaxxECU CLT map becomes effective thermostat)
5. Install CWA400 inline in **lower radiator hose** — outlet toward engine
6. Heater core circuit remains intact (returns through OEM housing to lower hose → CWA400 inlet)

> ⚠️ @wingman703 does a **full pump delete** (removes housing entirely, welds off rear coolant port, deletes heater core). This build retains housing-in-place **intentionally** to preserve heater core and cabin heat (street car).

---

## Bleeding Procedure (Pre-Fire Leak Test)

Advantage of electric pump: test and bleed before engine ever fires.

1. Fill cooling system with coolant
2. Wire CWA400 Pin 3 to battery +VE and Pin 4 to earth directly (bypassing relay)
3. Connect MaxxECU GPO or a signal generator to Pin 1 at ~50% duty / 680 Hz — pump runs
4. Alternatively: tie Pin 1 to +12V (forces emergency run / full speed) for bleed-only use
5. With radiator cap off, run 5–10 minutes — purge all air, top up coolant as air escapes
6. Check all connections for leaks under pump pressure
7. Restore normal wiring once system confirmed sealed and bled

---

## Reference

| Document | Link |
| :--- | :--- |
| Pierburg CWA400 PWM datasheet | [tecomotive.com PDF](https://tecomotive.com/download/datasheets/CWA400_PWM_EN.pdf) |
| Tecomotive CWA400 PWM product page | [tecomotive.com](https://tecomotive.com/en/products/CWA400_PWM.html) |
| Tecomotive CWA400 LIN product page (LIN version — do not use) | [tecomotive.com](https://tecomotive.com/en/products/CWA400.html) |
| Dedicated Motorsports (new, PWM version) | [dedicatedmotorsports.com](https://dedicatedmotorsports.com/products/pierburg-cwa400-intercooler-pump-pwm-version.html) |
| MaxxECU RACE output config (PWM GPO) | MaxxECU Software → Outputs → General Purpose Outputs |
