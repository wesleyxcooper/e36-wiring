# DBW Wiring Pinouts

Reference for `harnesses/maxxecu-07k.wv` and `harnesses/firewall-bulkhead.wv`.

All signals pass through the Deutsch Autosport AS47/AS79 firewall bulkhead connector.
Six pins must be reserved in the bulkhead for e-pedal; six more for the throttle body (already part of the 07K engine harness side).

---

## E-Pedal Options

### Option A — BMW E46 Accelerator Pedal Module (preferred with adapter bracket)

**Part numbers:** `35426786282` (manual gearbox) · `35426786281` (auto gearbox)
PN split is **manual vs auto, not LHD vs RHD** — same physical module in all markets.

**Adapter brackets for E36:**
| Vendor | SKU / Link | RHD Status |
|---|---|---|
| Strom Motorsports | [E36 DBW E46 Adapter](https://strommotorsports.com/products/e36-dbw-e46-accelerator-pedal-adapter) | ⚠️ Unconfirmed — contact before ordering |
| Garagistic | [E46 Gas Pedal for E36](https://www.garagistic.com/products/e46-gas-pedal-for-e36-adapter-bracket) | ⚠️ Unconfirmed |
| Boost Monkey | [E36 DBW Gas Pedal Adapter](https://boostmonkey.com/products/e36-electronic-drive-by-wire-gas-pedal-adapter-brackey) | ⚠️ Unconfirmed |
| Drift HQ | [E46 Gas Pedal for E36](https://drifthq.com/products/e46-gas-pedal-for-e36-adapter-bracket) | ⚠️ Unconfirmed |

> **RHD note:** LHD brackets may misalign or crowd the brake pedal in RHD. Expect to trim carpet/sound deadening at the transmission tunnel edge. If the OEM pedal box geometry prevents fitment, use the Hella pedal (Option B) instead — it doesn't depend on the pedal box at all. Reference thread: [Bimmerforums 2072569 — Mounting E46 DBW throttle pedal in E36](https://www.bimmerforums.com/forum/showthread.php?2072569-Mounting-the-E46-DBW-electronic-throttle-pedal-in-an-E36).

**Connector:** 6-pin, dual independent hall-effect sensors. Bench-verified pinout:

| Pin | Function | Signal |
|---|---|---|
| 1 | Ground 1 (APS1 GND) | Sensor GND, circuit 1 |
| 2 | Ground 2 (APS2 GND) | Sensor GND, circuit 2 |
| 3 | VCC 2 (+5V) | 5V supply, circuit 2 |
| 4 | Output 1 — APS1 | 0.7 V idle → 4.5 V WOT |
| 5 | VCC 1 (+5V) | 5V supply, circuit 1 |
| 6 | Output 2 — APS2 | 0.36 V idle → 2.2 V WOT (half-ratio redundancy) |

Total current draw: ~20 mA. 24 AWG wire sufficient for all 6 pins.
Output 2 is intentionally ~half Output 1 at every position — MaxxECU uses the ratio to detect sensor failure and trigger e-throttle shutdown.

**Sources:** [HP Academy bench test](https://www.hpacademy.com/forum/efi-wiring-fundamentals/show/bmw-epedal-for-dbw-setup-wiring/) · [openinverter.org BMW Throttle Pedal wiki](https://openinverter.org/wiki/BMW_Electronic_Throttle_Pedal)

**MaxxECU mapping:**
```
APS1 signal  →  AIN (use lowest available number, e.g. AIN 5)
APS2 signal  →  AIN (e.g. AIN 6)
VCC 1 / 2   →  MaxxECU +5V sensor supply
GND 1 / 2   →  MaxxECU sensor GND
```
MTune path: Settings → E-Throttle → Pedal position

---

### Option B — Hella 6PV010946-141 (standalone floor-mount, RHD-flexible)

**Best choice if E46 bracket fitment fails in RHD pedal box.**
Fully standalone pedal module — no OEM pedal box geometry dependency. Mount anywhere with a fabricated plate. MaxxECU has a native pre-defined profile.

Used widely in Porsche 944/914 swaps, kit cars, and LS conversions.

| Pin | MaxxECU Function |
|---|---|
| 1 | Sensor (1) GND |
| 2 | +5V sensor (2) supply |
| 3 | TPS 2 (Analog input) |
| 4 | Sensor (2) GND |
| 5 | +5V sensor (1) supply |
| 6 | TPS 1 (Analog input) |

**Source:** [MaxxECU E-Pedals Wiring Docs](https://maxxecu.se/webhelp/wirings-e_pedals.html)

---

## 07K DBW Throttle Body

Stock 07K TB is a VDO/Continental unit in the **Bosch 0280 750 family** (6-pin connector).
MaxxECU has pre-defined profiles for this family. Use the identification method below if variant is unknown.

**Stock bore: ~65 mm.** Adequate for ~500 whp at 25 psi per Rennlist 07K community airflow calculations. For 600–750+ whp, plan upgrade to VW 3.6 VR6 TB `03H 133 062` (~74 mm, same VAG flange family, direct fit candidate on BBG manifold, ~$40–80 used).

### Bosch 0280 750 474 (common VAG/1.8T family — closest to stock 07K unit)

| Pin | MaxxECU Function |
|---|---|
| 1 | Motor − |
| 2 | Sensor GND |
| 3 | +5V power supply |
| 4 | Motor + |
| 5 | TPS 2 (Analog input) |
| 6 | TPS 1 (Analog input) |

### Bosch 0280 750 009 (Audi S3/A4 variant — same family, alternate pin order)

| Pin | MaxxECU Function |
|---|---|
| 1 | TPS 1 (Analog input) |
| 2 | Sensor GND |
| 3 | Motor − |
| 4 | TPS 2 (Analog input) |
| 5 | Motor + |
| 6 | +5V supply |

### Self-Identification Method (if exact variant unknown)

1. Measure resistance between all pin pairs. Two pins at **0.1–10 Ω** = motor (Motor+/Motor−).
2. Of remaining 4 pins: pair with **stable ~1–10 kΩ** resistance = 5V and GND.
3. Remaining two pins vary as throttle plate moves = TPS 1 and TPS 2.

**Source:** [MaxxECU E-Throttle Bodies Wiring Docs](https://maxxecu.se/webhelp/wirings-e-throttle_bodies.html)

### TB Upgrade Options (pre-defined MaxxECU profiles)

| TB | Bore | Part # | Notes |
|---|---|---|---|
| **VW 3.6 VR6 TB** | ~74 mm | `03H 133 062` | Best upgrade — same VAG flange, direct fit candidate on BBG manifold. Confirmed on MKV 2.5 (VW Vortex). ~$40–80 used. |
| Audi RS6 TB | ~70 mm | `077133062` | Native MaxxECU profile. VAG V8 origin — verify BBG flange compatibility. |
| Chrysler 80 mm | 80 mm | `53032801AC` | Needs adapter flange. |
| Corvette LS2 90 mm | 90 mm | `12570790` | Needs adapter flange. Very large for this application. |

> **Do not upgrade TB before tune is dialed in.** Start with stock 65 mm; revisit at 550–600+ whp if flow modeling shows restriction. Confirm BBG manifold flange spec directly with Boost Brothers Garage before ordering.

---

## Firewall Bulkhead Pin Allocation (DBW)

These 12 pins must be allocated in `harnesses/firewall-bulkhead.wv` before the Phase 1 bulkhead is built.

| Signal | From | To | Wire | Bulkhead Pin (TBD) |
|---|---|---|---|---|
| APS1 signal | E-pedal pin 4 | MaxxECU AIN x | 24 AWG shielded | reserve |
| APS2 signal | E-pedal pin 6 | MaxxECU AIN x | 24 AWG shielded | reserve |
| APS VCC 1 | MaxxECU +5V | E-pedal pin 5 | 24 AWG | reserve |
| APS VCC 2 | MaxxECU +5V | E-pedal pin 3 | 24 AWG | reserve |
| APS GND 1 | MaxxECU SGND | E-pedal pin 1 | 24 AWG | reserve |
| APS GND 2 | MaxxECU SGND | E-pedal pin 2 | 24 AWG | reserve |

TB wiring (Motor+, Motor−, TPS1, TPS2, 5V, GND) stays on the engine side of the bulkhead within the 07K harness — does not cross the firewall.
