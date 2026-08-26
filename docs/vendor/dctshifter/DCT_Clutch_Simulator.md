# DCT Clutch Simulator — Vendor Reference

Selected as the 8HP virtual-clutch input source for this build. All claims below are traceable to the citations inline.

Verified: 2026-08-26 against the URLs listed.

---

## 1. Identity and purpose

Purpose-built hydraulic clutch simulator with an optional integrated Clutch Pressure Sensor (CPS) that outputs a 0.5–4.5V analog signal for the transmission controller (MaxxECU RACE H2O in this build) to drive the 8HP virtual-clutch pressure control.

- Product family: <https://dctshifter.com/collections/clutch-simulators>
- Product (Remote variant): <https://dctshifter.com/products/dct-clutch-simulator-remote>
- Installation guide (all variants): <https://dctshifter.com/pages/installation> (§2–§4)
- Vendor origin: Sweden

Explicit MaxxECU compatibility on the product page: *"This Clutch Simulator is compatible to setup with most control systems that support clutch functionality for DCT/8HP transmissions, including popular solutions like Turbolamik and Maxxecu."* — [dctshifter.com/products/dct-clutch-simulator-remote](https://dctshifter.com/products/dct-clutch-simulator-remote)

E36 build precedent: one of the customer reviews on the product page is from *"Greg Drozd — Perfect companion to TurboLamik TCU — Feels absolutely amazing paired with a short carbon shifter in my Turbolamik 8HP swapped E36 M3"* — direct evidence this simulator has been fitted to an E36 with 8HP.

---

## 2. Selected variant for this build

**DCT Clutch Simulator — Remote mount, with CPS.**

Purchase options on the product page:

| Variant | Price (SEK) | ~USD @10 SEK/USD |
|---|---|---|
| Remote + CPS (Yes) | 4,995 | ~$475 |
| Remote — CPS (No) | 4,095 | ~$390 |

**Selected: Remote + CPS (Yes)** — the CPS output is required for MaxxECU virtual-clutch input.

Rationale for the remote (not firewall/pedalbox) mount:
- The engine-bay location keeps the CPS 3-wire output (+5V / SGND / signal) on the engine side — **zero electrical firewall crossing** for the CPS.
- Hydraulic line from the OEM E36 clutch master cylinder to the engine-bay simulator uses the **existing manual-transmission hydraulic clutch line provision** in the RHD E36 chassis — no new firewall penetration for the fluid line.
- Vendor Remote-mount kit contents explicitly support this: *"Comes with a M10x1.0 fitting, allowing it to connect seamlessly as a slave cylinder after your main clutch cylinder. Also comes with a mounting bracket in stainless steel."* — [dctshifter.com/products/dct-clutch-simulator-remote](https://dctshifter.com/products/dct-clutch-simulator-remote)

Firewall/pedalbox mount (not selected) would put the simulator in the cabin behind the pedal box and require its CPS 3 wires to cross the firewall on the Maven bulkhead — kept as a documented fallback if remote mount doesn't fit physically in the engine bay near the intake side.

---

## 3. Physical and electrical specs (from vendor product page)

Direct quotes from [dctshifter.com/products/dct-clutch-simulator-remote](https://dctshifter.com/products/dct-clutch-simulator-remote) "Specifications" section:

| Spec | Value |
|---|---|
| Inlet thread | **M10 × 1.0** (hydraulic fluid inlet) |
| Sensor thread | 1/8 NPT (CPS mounting) |
| Sensor power | **5V DC** |
| Sensor output | **0.5 – 4.5 V** (ratiometric) |
| Sensor range | 0 – 10 bar |
| Total height (with firewall bracket) | 110 mm |
| Body height | 85 mm |
| Width | 35 mm |
| Total length | 160 mm |
| Length from firewall to end of body | 125 mm |
| Length of rod (from firewall) | 110 mm + 40 mm clevis (firewall/pedalbox variant only) |
| Weight | 0.8 kg |
| Material | Aluminium (anodized) |

Note on the sensor output: the vendor's separate installation page ([dctshifter.com/pages/installation §4](https://dctshifter.com/pages/installation)) quotes the range as *"0.5V and 5.0V"*. The product page here gives *"0.5 – 4.5 V"* which is the more conservative and more specific spec for the actual CPS unit shipped. Use **0.5–4.5V** as the calibration range in MTune. The vendor also explicitly warns: *"When you set up (calibrate) your simulator to your gearbox controller, please leave some room from when clutch pedal is not pressed. So if you read ~0.5v when 0% pressed, set 0% to at least 0.6v."*

---

## 4. Electrical wiring (3 wires) — routes to MaxxECU RACE H2O

Under the H2O engine-bay-mount architecture (`docs/vendor/maxxecu/MaxxECU_RACE_H2O.md`), all three CPS wires stay on the engine-bay side because the simulator is engine-bay-mounted.

| CPS wire | Signal | MaxxECU destination |
|---|---|---|
| +5V | Sensor power | MaxxECU C1 G1 (+5V sensor rail) |
| SGND | Sensor ground | MaxxECU C1 H1 (SGND) |
| Signal | 0.5–4.5 V ratiometric CPS output | **MaxxECU C2 AIN 5 (C2 pin G3)** — configured as `Clutch Position` in MTune |

C2 AIN 5 pin location per <ref_snippet file="/Users/wesleyc/personal/e36/e36-wiring/docs/wiring-bom.md" lines="165-165" /> and the MaxxECU RACE REV9+ wiring diagram (repo-internal at `docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf`).

Requires MaxxECU **Binary5** 8HP TCU firmware + MTune 1.157+ per <https://www.maxxecu.com/webhelp/advanced-8hp-virtual_clutch.html> — see also the pre-swap Binary5 confirmation procedure at <ref_snippet file="/Users/wesleyc/personal/e36/e36-docs/walkthroughs/07-8hp-swap.md" lines="55-59" />.

---

## 5. Hydraulic plumbing (uses OEM E36 clutch line)

The E36 chassis (this build is a manual-transmission RHD car) has an existing hydraulic clutch line:
- OEM clutch master cylinder in the driver-side pedal box (RHD = right)
- Steel/rubber line through the firewall grommet (existing OEM provision)
- OEM slave cylinder near the transmission bellhousing (REMOVED at 8HP swap — no clutch to actuate on 8HP)

The DCT Clutch Simulator remote mount replaces the OEM slave cylinder as the endpoint of that hydraulic line. From the vendor product page:

> *"Comes with a M10x1.0 fitting, allowing it to connect seamlessly as a slave cylinder after your main clutch cylinder."*

Bleeding procedure per <https://dctshifter.com/pages/installation> §3:

> *"The system operates on standard brake fluid. Treat the installation and bleeding process with the same care and precision as a braking system.*
> *Run a high-pressure line from the clutch master cylinder to the simulator inlet, then fill the reservoir with the appropriate fluid.*
> *Bleeding Steps:*
> - *Open the bleed screw on the simulator.*
> - *Allow fluid to flow until there are no air bubbles.*
> - *Close the bleed screw.*
> - *Pump the clutch pedal 3–5 times.*
> - *Hold the pedal firmly to the floor.*
> - *Open the bleed screw briefly to release trapped air, then close it.*
> - *Repeat until pedal feel is firm and consistent."*

Small M3 screw is included on the simulator body for bleeding (per the Remote-mount product description).

Mount location note: *"It must be mounted lower than the clutch master cylinder reservoir to ensure proper fluid flow."* — [dctshifter.com/pages/installation §2](https://dctshifter.com/pages/installation)

Suggested engine-bay location for this RHD build: on the driver side of the engine bay (right side in RHD, exhaust side of engine bay) near where the OEM slave cylinder used to bolt to the bellhousing — well away from the intake-side H2O + PMU16 mount, keeping high-signal-integrity electronics apart from the hydraulic bleed area.

---

## 6. Help-spring caveat (from vendor)

Direct quote from the product page:

> *"Please be aware: you might need a 'help spring' to correctly pull the pedal back. We've noticed some setups work great without one, but it seems to depend on your pedal's geometry and cylinder size. We're actively working on a fix to eliminate the need for an extra spring, but for now, adding a help spring is the easiest solution."*

Action item for install: after mounting simulator + bleeding, test pedal return with foot off the pedal. If the pedal doesn't return fully, source a mechanical return spring (e.g., a light-tension coil spring anchored between the pedal arm and a fixed body point). This is only known at install time.

---

## 7. MTune calibration procedure

Per <https://dctshifter.com/pages/installation> §4 *"Controller Calibration (CPS)"* and MaxxECU virtual-clutch page <https://www.maxxecu.com/webhelp/advanced-8hp-virtual_clutch.html>:

1. Confirm CPS wired to MaxxECU C2 AIN 5 (C2 pin G3)
2. In MTune: **Analog Inputs → AIN 5 → type = 0-5V, function = Clutch Position**
3. Read voltage with pedal not pressed (should be ~0.5V); set MTune 0% clutch to at least **0.6V** (per vendor calibration note)
4. Press pedal fully; read voltage (should approach 4.5V); set MTune 100% clutch to just below that
5. In MTune: **Advanced → 8HP → 8HP clutch control → Enabled, Virtual clutch**
6. Set clutch clamp start / end per the [MaxxECU 8HP Settings page](https://www.maxxecu.com/webhelp/advanced-8hp-mtune_settings.html) — 5% slack at both ends per MaxxECU documentation
7. Test with car stopped in Neutral, brake applied, then engage 1st with slow pedal release

---

## 8. Purchase list impact

**Adds (Phase 1B — 8HP swap time):**
- **DCT Clutch Simulator Remote + CPS** — ~4,995 SEK (~$475 USD)
- ~0.5 m of hydraulic brake fluid line, M10×1.0 fitting to master cylinder side (existing E36 line likely reusable; verify at install)
- Stainless steel mounting bracket (included with the Remote kit)
- Possible help spring (source at install if needed — light-tension coil spring)

**Removes from previous plan** (`wiring-bom.md` §9F — the DIY approach):
- Rotary position sensor at OEM pedal pivot (~$30–50, e.g. Bosch TPS `0 280 122 001`)
- Custom bracket fabrication at pedal pivot
- Pedal return spring specification (still needed depending on Simulator behavior — see §6 above)

**Net cost delta**: approximately +$425 vs the DIY rotary sensor approach, in exchange for real hydraulic clutch feel and factory-calibrated CPS.

---

## 9. Phase timeline

- **Phase 1B (8HP swap)**: Install Simulator during the 8HP swap window. The 8HP swap removes the OEM slave cylinder anyway — replace with the Simulator at the same time. See `e36-docs/walkthroughs/07-8hp-swap.md` for the surrounding 8HP procedure.
- **Phase 2**: No changes to Simulator (it lives in the engine bay independent of engine choice).
- **Phase 3 (07K swap)**: Simulator stays. CPS wiring stays. No re-work.

---

## 10. Related documents in this repo

- `docs/vendor/maxxecu/MaxxECU_RACE_H2O.md` — ECU that reads the CPS input
- `docs/wiring-bom.md` §9F — Virtual clutch position section (to be updated: DIY rotary → DCT Clutch Simulator)
- `e36-docs/walkthroughs/07-8hp-swap.md` — 8HP swap procedure (to be updated: add Simulator install)
- `harnesses/firewall-crossing-maven.wv` — Maven HD30 dual bulkhead (CPS does NOT cross firewall, but this file documents the crossing context)
- MaxxECU 8HP virtual clutch: <https://www.maxxecu.com/webhelp/advanced-8hp-virtual_clutch.html>
- DCT vendor install page: <https://dctshifter.com/pages/installation>
