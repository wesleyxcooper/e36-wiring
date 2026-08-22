# Fuel Pump Hanger Wiring Reference — Radium 20-1170 + F90000267 + MaxxECU PWM

**Build context:** E36 restomod, 07K / 8HP swap, MaxxECU RACE, Aeromotive 13129 FPR (return-style). Radium 20-1170 hanger installed at Phase 1 — carries through 07K Phase 3 with zero re-work. F90000267 is a single-pump install covering all phases through 600whp E85. MaxxECU controls pump speed via PWM GPO through a DC solid state relay (SSR).

---

## Hanger — Radium Engineering 20-1170

| Item | Value |
| :--- | :--- |
| Part number | `20-1170` |
| Price | $549.95 (radiumauto.com, in stock) |
| Application | BMW E36 1990–1999 (all variants incl. M3) |
| Construction | Aluminum + stainless steel |
| Pump-out port | 10AN ORB female (7/8"-14) on top plate |
| Return-in port | 10AN ORB female (7/8"-14) on top plate |
| OEM feed adapter | SAE quick-connect barb (included) |
| OEM return adapter | 8.5mm barbed adapter (included) |
| Pump slots | 1 or 2 aftermarket pumps |
| Pump compatibility | 2-wire brushed OR 3-4 wire brushless |
| Fuel compatibility | Gasoline, E85, methanol |
| Level sensor | Reuses OEM active + passive sensors |
| Saddle crossover | PRV venturi jet pump siphon — replaces OEM passive crossover |
| Tank modification | None — drop-in, no cutting |
| Install PDF | [radiumauto.com/pages/instructions (20-1170)](https://cdn.shopify.com/s/files/1/0887/4193/7449/files/19-0359.pdf) |

**Electrical terminals:** Custom stainless steel studs through top plate. Anti-rotation feature. Hermetically sealed. Ring terminals + anodized aluminum acorn nuts (provided). In-tank wiring insulated with ETFE.

---

## Pump — Walbro F90000267

| Item | Value |
| :--- | :--- |
| Part number | `F90000267` |
| Price | $181.12 (realstreetperformance.com, pump only) |
| Type | Brushed DC, dual-channel turbine (DCSS) |
| Flow rate | 465 LPH @ 40 PSI @ 13.5V |
| Current draw | 14.1A @ 13.5V |
| Upper body diameter | 39mm (fits Radium 20-1170 directly) |
| Lower body diameter | 50mm |
| Outlet diameter | 10mm (3/8") |
| Fuel compatibility | E85, gasoline (all fuels) |
| Made in | USA (TI Automotive / Walbro) |
| Target power (E85) | 600whp+ (single pump at full duty — covers all phases) |

**Hanger compatibility:** Confirmed — Radium 20-1170 is designed around the 39/50mm DCSS body format shared by the F90000267, GSS342, and most Walbro high-flow pumps.

---

## AN Fittings — Radium 20-1000-1010 (Feed Port)

| Item | Value |
| :--- | :--- |
| Part number | `20-1000-1010` |
| Price | $34.95/ea (radiumauto.com) |
| Type | Low Profile Swiveling Banjo — 10AN ORB to 10AN Male |
| Thread | 10AN ORB (7/8"-14) into hanger top plate pump-out port |
| Rotation | 360° swivel after install |
| Construction | Stainless steel + aluminum |
| Fuel compatibility | All fuels |
| Quantity needed | 1× (feed only) |
| Return port | Use included 8.5mm barb adapter (OEM return line size) |
| Optional return upgrade | `20-1000-0606` (6AN ORB Swivel to 6AN Male, $34.95) for full AN return |

**Install tip:** Thread hand-tight first, then attach -10AN braided line before final torque — this lets the swivel rotate to the correct routing angle before locking down.

---

## PMU16 Output — O4

The Crydom D1D40 SSR from earlier design revisions has been removed. The Ecumaster PMU16 output O4
(25A, PWM-capable) drives the pump directly. MaxxECU commands pump speed via CAN to the PMU16, which
outputs PWM on O4. No separate SSR or relay needed. Source: `harnesses/power-distribution.wv`.

| Item | Value |
| :--- | :--- |
| PMU16 output | O4 (25A max) |
| PWM-capable | Yes — software-configurable PWM on O4 |
| BATT+ path | PMU16 M6 stud (always-on) → O4 switches load |
| Load wire gauge | 12 AWG (14.1A draw well within O4 25A rating) |

---

## MaxxECU PWM Configuration

| Parameter | Value |
| :--- | :--- |
| Output function | PWM fuel pump control |
| Control method | MaxxECU CAN broadcast → PMU16 maps to O4 PWM |
| PWM frequency | 100–500 Hz (set in PMU software on O4) |
| MTune path | Outputs → Output config → Function: PWM fuel pump control |

**Phase 3 PWM duty table** (PMU16 O4; not applicable to Phase 1 relay):

| Operating condition | Duty Cycle | Notes |
| :--- | :--- | :--- |
| Key-on / pre-crank | 100% (brief) | Prime the rail — 2-3 seconds at startup |
| Idle / low boost (Phase 3) | 75% | 07K at part load |
| Full boost / WOT (Phase 3) | 100% | 07K 600whp E85 — full duty |

> ⚠️ **Duty cycle floor:** Do not run a brushed pump below ~50% duty continuously — insufficient flow through the pump body causes heat buildup. At idle, 75% is the safe floor.

Phase 1 (relay, no PWM): pump runs at 100% whenever key is on. This is fine for the F90000267 at M52 NA fuel demand (~14.1A continuous is within the pump's rated duty).

---

## Power Wiring — Phase 1 (M52, M50 harness, no PMU16)

Phase 1 uses a standard 30A automotive relay. MaxxECU GPO 2 (ECU_16PIN pin 4) sinks the relay coil.
The Walbro F90000267 draws 14.1A — well within relay spec. No PWM in Phase 1; pump runs at full
speed whenever the relay closes. Full-speed continuous operation is safe for the Walbro.

| Wire | Spec | Notes |
| :--- | :--- | :--- |
| BATT+ to relay pin 30 | 12 AWG RED, fused 20A within 12" of battery | Always-on feed |
| Relay pin 87 to pump(+) stud | 12 AWG RED | Switched pump supply |
| Pump(-) stud to chassis GND | 12 AWG BLACK | Dedicated GND stud — not shared |
| IGN +12V to relay coil pin 86 | 18 AWG | Key-switched supply |
| MaxxECU GPO 2 to relay coil pin 85 | 18 AWG | GPO 2 = ECU_16PIN pin 4 (GND-sink) |

**Relay:** Bosch 0 332 002 150 or equivalent 4-pin 30A automotive relay.

---

## Power Wiring — Phase 3 (07K, PMU16)

Phase 3 replaces the relay with **PMU16 O4** (25A, PWM-capable). MaxxECU commands pump speed
via CAN → PMU16 maps to O4 PWM. No physical relay. Source: `harnesses/power-distribution.wv`.

| Wire | Spec | Notes |
| :--- | :--- | :--- |
| PMU16 O4 to pump(+) stud | 12 AWG RED | Switched pump supply from PMU16 |
| Pump(-) stud to chassis GND | 12 AWG BLACK | Dedicated GND stud — not shared |

**Ground rule:** Pump(-) must go to a dedicated chassis bolt/stud. Mixing pump ground with ECU sensor grounds injects pump switching noise into the analog signal bus — causes erratic MAP, TPS, wideband readings at high RPM/duty.

---

## Fuel Line Routing (Phase 1)

| Segment | Spec |
| :--- | :--- |
| Hanger pump-out → FPR inlet | -10AN braided (PTFE-lined, E85-rated) via 20-1000-1010 swivel |
| FPR outlet (return) | OEM 8.5mm barb adapter (included) → OEM rubber return line |
| FPR reference | See Aeromotive 13129 install — vacuum/boost reference to MAP port |

---

## Post-Phase 3 Notes (07K)

No fuel system changes required at 07K swap. The Radium 20-1170 hanger, F90000267 pump, and swivel fittings are already Phase 3 spec. Re-tune the MaxxECU fuel pump duty table for 07K boost map — all hardware stays.

If future dual-pump is ever needed (e.g., wet nitrous or methanol injection): Radium 20-1170 supports a second pump slot. Add second pump, new dedicated relay/fuse circuit per Radium's dual-pump wiring note — the hanger is already pre-drilled.

---

## Reference

| Document | Link |
| :--- | :--- |
| Radium 20-1170 install instructions (PDF) | [radiumauto.com](https://cdn.shopify.com/s/files/1/0887/4193/7449/files/19-0359.pdf) |
| Radium 20-1170 product page | [radiumauto.com/products/bmw-e36-fuel-pump-hanger](https://www.radiumauto.com/products/bmw-e36-fuel-pump-hanger) |
| Radium Low Profile Swiveling Fittings | [radiumauto.com/products/low-profile-swiveling-banjo-fittings](https://www.radiumauto.com/products/low-profile-swiveling-banjo-fittings) |
| Walbro F90000267 (pump only) | [realstreetperformance.com](https://www.realstreetperformance.com/walbro-universal-450lph-in-tank-fuel-pump-e85-version.html) |
| MaxxECU PWM fuel pump control | [maxxecu.se/webhelp/output_functions-pwm_fuel_pump_control.html](https://www.maxxecu.se/webhelp/output_functions-pwm_fuel_pump_control.html) |
| PMU16 power distribution | `harnesses/power-distribution.wv` |
| WireViz harness | `harnesses/fuel-pump-hanger.wv` |
