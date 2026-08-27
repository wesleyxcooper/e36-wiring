# DBW Wiring Pinouts

Reference for `harnesses/maxxecu-07k.wv`, `harnesses/epedal-bmw-e46.wv`, and `harnesses/firewall-crossing-maven.wv`.

Under the H2O engine-bay-mount architecture (see `docs/vendor/maxxecu/MaxxECU_RACE_H2O.md`), the MaxxECU RACE H2O sits in the engine bay. The two DBW subsystems terminate as follows:

- **APS e-pedal (cabin footwell)**: 6 wires cross the firewall via **Maven HD30 Connector B pins 1–6** (Phase 3 install). Connector B is the *safety-critical* Maven connector — APS is the throttle command input, and any fault must trigger e-throttle shutdown. See "APS e-pedal" section below.
- **07K DBW throttle body (engine bay)**: 6 wires terminate directly at MaxxECU C1/C2 in the engine bay. **No firewall crossing** — both endpoints are engine-bay-side. See "07K DBW Throttle Body" section below.

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

**Sourcing — used E46 pedal (buy used, sensor does not wear):**

> [eBay saved search — `35426786282`](https://www.ebay.com/sch/i.html?_nkw=bmw+35426786282&_svsrch=1)

| eBay Item | Price | Condition | Notes |
|---|---|---|---|
| [407117477828](https://www.ebay.com/itm/407117477828) | $119.98 OBO | Used / US domestic | Lists multiple chassis (E46/E38/E39/X5) — confirm PN `35426786282` with seller before buying |
| [176400301948](https://www.ebay.com/itm/176400301948) | £59 (~$79 + intl. shipping) | Used / UK | E46 M3/330i/328i/325i manual — correct chassis |
| [176400305397](https://www.ebay.com/itm/176400305397) | £59 (~$79 + intl. shipping) | Used / UK | E46 330i manual — correct chassis |
| [176400302753](https://www.ebay.com/itm/176400302753) | £59 (~$79 + intl. shipping) | Used / UK | E46 323i/320i/318i/316i manual — correct chassis |

> ⚠️ **Do not buy** [176400306849](https://www.ebay.com/itm/176400306849) — listed alongside the above but is an **E39/E38/X5/E53** pedal with a different connector and pinout. Will not work.

UK listings land at ~$100–125 all-in after international shipping. US domestic listing with best offer is comparable and avoids customs. MaxxECU re-calibrates from scratch via wizard regardless of pedal age — buying used is correct here.

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

## Firewall Crossing Allocation (DBW)

### APS e-pedal — crosses firewall via Maven HD30 Connector B (safety-critical)

Connector B of the Maven HD30 dual bulkhead is **designated safety-critical** and reserved for APS wiring across the entire build. APS is the throttle command input — any fault (open wire, short, sensor mismatch between APS1 and APS2) must trigger MaxxECU e-throttle shutdown. Keeping APS on its own dedicated Maven connector prevents accidental mixing with less-critical CAN + DCT signals (which go on Connector A).

The 6 APS wires cross from cabin footwell (E46 pedal) to engine-bay MaxxECU via **Maven Connector B pins 1–6**. Cabin-side Maven receptacle is installed at Phase 3 (along with the pedal itself); engine-side plug on the 07K custom harness mates to it at 07K swap.

| Signal | From | Maven B pin | To (engine-bay MaxxECU) |
|---|---|---|---|
| APS GND 1 | E-pedal pin 1 | B1 | MaxxECU SGND (CMC H1, pin 29) |
| APS GND 2 | E-pedal pin 2 | B2 | MaxxECU SGND (CMC H1, pin 29) |
| APS VCC 2 | E-pedal pin 3 | B3 | MaxxECU +5V sensor rail (CMC G1, pin 25) |
| APS1 signal | E-pedal pin 4 | B4 | MaxxECU C2 E4 (AIN 6) |
| APS VCC 1 | E-pedal pin 5 | B5 | MaxxECU +5V sensor rail (CMC G1, pin 25) |
| APS2 signal | E-pedal pin 6 | B6 | MaxxECU C2 F1 (AIN 7) |

Connector B pins 7–16 (10 spare cavities) are cavity-plugged. Reserved for future safety-critical throttle-related expansion only (e.g., a redundant idle position sensor, a brake pressure input to Torque-Reduction-On-Brake logic).

Source: `harnesses/firewall-crossing-maven.wv`, `harnesses/epedal-bmw-e46.wv`.

### 07K DBW throttle body — engine-bay direct-terminate (NO firewall crossing)

Under the H2O arch, MaxxECU is engine-bay-mounted alongside the TB. All 6 TB wires (Motor+/−, TPS1, TPS2, +5V, SGND) run engine-bay-only and terminate directly at MaxxECU C1/C2. There is NO firewall bulkhead in this path. See `harnesses/maxxecu-07k.wv` "07K signal → MaxxECU pin destinations" block.

| Signal | MaxxECU terminal (direct-terminate at engine bay) | Wire |
|---|---|---|
| ETh Motor+ | C2 H4 (MOTOR 1+) | 22 AWG — 3A H-bridge peak at 0.5m engine-bay run |
| ETh Motor− | C2 H2 (MOTOR 1−) | 22 AWG (same) |
| TPS1 | C1 G2 (pin 26, was M52 TPS wire — reused) | 22 AWG shielded |
| TPS2 | C1 J2 (AIN 2, pin 34) | 22 AWG shielded |
| +5V sensor supply | C1 G1 (pin 25, shared sensor rail) | 22 AWG |
| Sensor GND | C1 H1 (pin 29, shared SGND) | 22 AWG |

TB motor polarity: verify with volt meter and MTune e-throttle wizard before final crimp — swap Motor+/− at the TB connector if throttle runs in the wrong direction during the e-throttle wizard.
