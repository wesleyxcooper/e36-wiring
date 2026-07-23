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

## SSR — DC Solid State Relay

| Item | Value |
| :--- | :--- |
| Recommended part | Crydom D1D40 |
| Alternative | Generic 40A DC-DC SSR (opto-isolated, 0-60V load, 3-32V control) |
| Control input | 3–32V DC, ~10–15mA |
| Load rating | 0–60V DC, 40A continuous |
| Max switching freq | 1kHz (Crydom D1D40) |
| Used PWM frequency | 100–500Hz (recommended for this circuit) |
| Why SSR not relay | Mechanical relays cannot switch PWM at 100Hz+ — contacts arc and weld |
| Heatsink | Required if sustained duty > 80% at high current |

---

## MaxxECU PWM Configuration

| Parameter | Value |
| :--- | :--- |
| Output function | PWM fuel pump control |
| GPO type | GEN1 low-drive (GND-sinking), max 2A |
| PWM frequency | 100–500 Hz |
| MTune path | Outputs → Output config → Function: PWM fuel pump control |
| SSR control wiring | GPO sinks Ctrl(-) to GND when active; IGN +12V feeds Ctrl(+) |

**Recommended duty table:**

| Operating condition | Duty Cycle | Notes |
| :--- | :--- | :--- |
| Key-on / pre-crank | 100% (brief) | Prime the rail — 2-3 seconds at startup |
| Idle / low load (Phase 1) | 65% | Adequate flow for M52 NA at ~200hp |
| Cruise (Phase 1) | 75% | Normal road load |
| WOT NA (Phase 1) | 90–95% | M52 / Turbo M50 high demand |
| Idle / low boost (Phase 3) | 75% | 07K at part load |
| Full boost / WOT (Phase 3) | 100% | 07K 600whp E85 — full duty |

> ⚠️ **Duty cycle floor:** Do not run a brushed pump below ~50% duty continuously — insufficient flow through the pump body causes heat buildup. At idle, 65% is the safe floor.

---

## Power Wiring

| Wire | Spec | Notes |
| :--- | :--- | :--- |
| BATT+ to SSR Load(+) | 12 AWG RED, fused 25A within 12" of battery | Always-on feed |
| SSR Load(-) to pump(+) stud | 12 AWG RED | Switched pump supply |
| Pump(-) stud to chassis GND | 12 AWG BLACK | Dedicated GND stud — not shared |
| IGN +12V to SSR Ctrl(+) | 22 AWG GREEN | Low current (~15mA) |
| MaxxECU GPO to SSR Ctrl(-) | 22 AWG VIOLET, shielded | PWM signal — drain at ECU end only |

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
| MaxxECU GEN1 GPO pinout | [maxxecu.com/webhelp/wirings-gpo.html](https://www.maxxecu.com/webhelp/wirings-gpo.html) |
| WireViz harness | `harnesses/fuel-pump-hanger.wv` |
| Circuit schematic | `schematics/fuel-pump-pwm.py` (run to generate SVG) |
