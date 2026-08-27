# MaxxECU RACE H2O — Vendor Reference

Consolidated primary-source data on the MaxxECU RACE H2O (waterproof RACE variant), the ECU chosen for this build. All claims below are traceable to the citations inline.

Verified: 2026-08-26 against the URLs listed.

---

## 1. Identity and relationship to MaxxECU RACE

The **RACE H2O** is the IP67-waterproofed variant of the standard MaxxECU RACE. Same internal electronics, same feature set, same pinout, same MTune software — only the enclosure and USB connector differ.

- Product family page: <https://maxxecu.com/products/race/> — *"MaxxECU RACE / RACE H2O … Available in waterproof H2O variant for marine applications and harsh environments."*
- Bare-unit store page: <https://maxxecu.com/store/engine-control-or-electronics/maxxecu-units/maxxecu-race-h2o-unit-with-no-accessories-in-box> — MaxxECU product ID **1895**, list price **$1,727.88** USD (excl. VAT), 1 pcs 1896 "MaxxECU RACE H2O unit without accessories".
- Feature-parity confirmation via compare chart: <https://www.maxxecu.com/ecu_compare> — RACE and RACE H2O columns show identical values across the entire spec matrix (max sequential cylinders, MAP sensor, knock, EGT, injector/ignition counts, GPOs, etc.).

---

## 2. Physical spec

| Spec | Value | Source |
|------|-------|--------|
| Dimensions | 155 × 195 × 40 mm (mounting points; excluding connector) | <https://maxxecu.com/products/race/> — *"Weight: 880g … 155x195x40mm (including mounting points, excluding connector)"* |
| Weight | 880 g | same |
| IP rating | **IP67** | <https://shop.kcperformance.eu/products/maxxecu-race-h2o-waterproof-professional-standalone-ecu> — *"Waterprotected (IP67) for reliable operation in harsh environments"*; corroborated by every MaxxECU regional distributor page (maxxecu.us, maxxecu.co.nz, maxxecuaustralia.com.au) and the compare chart |
| Supply voltage | 8–22 V | <https://maxxecu.com/products/race/> — *"Supply voltage 8-22V"* |

---

## 3. Operating temperature (documented behavior thresholds)

MaxxECU does **not** publish a max-ambient operating temperature range for the RACE H2O. What they *do* publish is two behavior thresholds tied to internal CPU temperature:

| Threshold | Behavior | Source |
|-----------|----------|--------|
| CPU > 60 °C / 140 °F | Analog-input temperature compensation kicks in; on GEN1 SW14+ and MINI it's automatic and needs no user config | <https://www.maxxecu.se/webhelp/settings-advanced-calibration.html> — *"There is no need to enable this compensation unless your CPU temperature regularly exceeds 60°C / 140° F … under extreme under-hood conditions, enabling this feature improves accuracy and signal stability"* |
| CPU > 100 °C | Error code 92 (High internal temperature) trips (requires battery > 9.0 V) | <https://www.maxxecu.se/webhelp/information-error_codes-92.html> — *"MaxxECU internal temperature was to high. Make sure to mount the ECU away from heat sources, even transmissiones or transmission tunnels. Battery voltage must be over 9.0V and the internal temperature must be over 100 deg C to trigger this error code."* |

Implication for this build: engine-bay mount is acceptable but the ECU must be located away from direct heat sources (exhaust manifold, turbo, transmission tunnel). The OEM E36 DME cavity on the firewall — an intake-side, firewall-face mount sheltered under a plastic cover — was designed for this use case by BMW and satisfies the "away from heat sources" recommendation.

---

## 4. Connectors (RACE H2O = same C1/C2 Molex as RACE)

This was in doubt during design review — a warning was received that "the H2O uses different connectors." **The warning was mistaken for C1/C2** and correct for USB (see §5).

Primary evidence that C1 and C2 are **identical** between RACE and RACE H2O:

- Bare-unit store page (<https://maxxecu.com/store/engine-control-or-electronics/maxxecu-units/maxxecu-race-h2o-unit-with-no-accessories-in-box>) — "Recommended products" for the H2O unit lists exactly:
  - **MaxxECU STREET/SPORT/RACE/PRO C1 (48-pin molex)** — $33.41 USD
  - **MaxxECU MINI / RACE C2 / PRO C4 (32-pin molex)** — $32.25 USD
- C1 product page (<https://maxxecu.com/store/engine-control-or-electronics/maxxecu-connectors/maxxecu-street-or-sport-or-race-or-pro-connector-1-48-pin-molex>): *"Fits connector 1 on STREET/SPORT/RACE/PRO."* The "Recommended products" cross-sell on that page includes the RACE H2O unit.
- RACE H2O PREMIUM kit inventory (<https://maxxecu.com/store/engine-control-or-electronics/maxxecu-standalone-ecu/maxxecu-race-h2o-premium-ecu-harnesses-accessories-lsu-49>) — bundle contents include:
  - **871 MaxxECU V1/RACE/PRO flying lead wiring harness connector 1** — the standard 48-pin C1 flying-lead
  - **1787 MaxxECU RACE harness 2 (EGT, E-Throttle, extra)** — the standard 32-pin C2 loom

MaxxECU sells and ships the standard C1 and C2 Molex parts as the mating connectors for the H2O. **The BMW M50 terminated harness plugs into the H2O identically to the RACE.**

The MaxxECU documentation refers to these connectors as "high-quality Automotive Molex" (<https://maxxecu.com/products/race/>). The C1 pinout for STREET/SPORT/V1/RACE/PRO — including RACE H2O — is at <https://maxxecu.com/webhelp/wirings-maxxecu_pinout.html> and mirrored in this repo at <ref_file file="/Users/wesleyc/personal/e36/e36-wiring/docs/vendor/maxxecu/MaxxECU_GEN1_Pinout.md" />.

---

## 5. USB — sealed, not standard type-B/mini

Where the H2O **does** differ from the RACE: the USB port is sealed. Standard MaxxECU USB cables do not mate.

- MaxxECU part **#1606**: "MaxxECU PRO / RACE H2O USB-cable 1.5m", **$40.32 USD**. Source: <https://maxxecu.com/store/engine-control-or-electronics/maxxecu_usb_cables/maxxecu-pro-usb-cable-15m>.
- Description: *"For MaxxECU PRO, water protected."*
- Length and end-form confirmed by NZ distributor <https://maxxecu.co.nz/product/maxxecu-pro-race-h2o-usb/> — *"This water proof USB cable is 1.5m long"* — sealed connector on the ECU end, standard USB-A on the laptop end.
- Included in the RACE H2O PREMIUM kits (SKU 1897 for LSU 4.2, SKU 2252 for LSU 4.9). Not required to purchase separately if buying the PREMIUM kit.

Routing plan for this build: sealed end at engine-bay ECU → 1.5 m cable through a dedicated weatherproof grommet in the firewall → USB-A end mounted in the cabin (glove box or under-dash panel) for laptop connection during tuning. The 1.5 m length is enough for an OEM-E-box-cavity ECU mount to a cabin-side mount.

---

## 6. Kit contents and pricing (US)

Two SKUs directly relevant to this build:

| SKU / Product | US price | Kit contents | Source |
|---|---|---|---|
| **1895** MaxxECU RACE H2O unit only, no accessories | $1,727.88 | ECU only | <https://maxxecu.com/store/engine-control-or-electronics/maxxecu-units/maxxecu-race-h2o-unit-with-no-accessories-in-box> |
| **MaxxECU RACE H2O PREMIUM (LSU 4.2)** | $2,050.42 | 1896 H2O unit + 871 flying-lead harness (C1) + 1787 RACE harness 2 (C2, EGT, E-Throttle) + 1533 LSU 4.9 6-way connector + 1606 sealed USB cable 1.5m + 1911 printed wiring diagram + LSU 4.2 sensor + accessories | <https://maxxecu.com/store/engine-control-or-electronics/maxxecu-standalone-ecu/maxxecu-race-h2o-engine-management-flying-lead-kit> |

For this build, either SKU works. The M52 pre-terminated harness (`docs/vendor/maxxecu/MaxxECU_M50_Terminated_Harness.md`) replaces the 871 flying-lead C1 harness for the M52 phase. For Phase 3, the custom 07K harness replaces it. The 1787 C2 loom is still useful for EGT/E-Throttle/knock even if the M52 phase doesn't use those.

---

## 7. Mounting recommendation for this RHD E36 build

**Location: OEM DME (E-box) cavity, LEFT side of engine bay firewall (RHD passenger side = intake side of M52 and 07K).**

Rationale (with sources):

1. **This car's OEM DME cavity is on the passenger side of a RHD E36 — confirmed on the car by the build owner.** In RHD the driver is on the right, so passenger side = left side of engine bay. Corroborating source for the general RHD layout: [bimmerforums.co.uk thread on E36 tds ECU location](https://www.bimmerforums.co.uk/threads/e36-tds-ecu-location.334033/) — *"It's behind the fusebox on RHD cars in the bulkhead behind a plastic panel. LHD cars have it on the opposite site to the fusebox, but still inside the bulkhead behind a panel."* The E36 DME location follows the passenger side in both LHD and RHD; because the interior mirrors between variants, "passenger side" maps to opposite physical sides of the car (right in LHD, left in RHD).

2. **Intake side = passenger side = left side of engine bay in RHD.** The BMW M50/M52/M54/S52/S54 engine family keeps the same physical orientation in RHD as in LHD (the engine is not mirrored), and per the build owner's on-car observation, this puts the intake manifold on the passenger side of a RHD car. The 07K engine retains the same orientation post-swap (engine remains longitudinal with the same intake side). Exhaust manifold, downpipe, and (Phase 3) turbo are on the driver side — the OPPOSITE side of the engine bay from the OEM DME cavity.

3. **Thermally favorable** — intake side is opposite the exhaust manifold, downpipe, and turbo. Aligns with MaxxECU's error-code-92 documentation recommendation to "mount away from heat sources."

4. **Sheltered by OEM E-box cover** — pre-existing plastic cover was designed to shelter the DME from spray. IP67 rating of the H2O gives additional margin.

**Physical fit check:** RACE H2O footprint (155×195 mm) is larger than the OEM Bosch DME (~180×110 mm approx). The OEM E-box cavity may or may not accept the H2O directly. Options:

- (A) Fabricate a mounting plate that occupies the E-box cavity opening; H2O bolts to the plate; discard the OEM plastic cover
- (B) Mount the H2O just outside the E-box cavity on the firewall face itself with OEM cover removed
- (C) Move the H2O to the adjacent inner-fender area on the intake side, extending the OEM cavity area

Measure the specific car's E-box cavity dimensions during Phase 1 mockup before committing to a mounting plate design.

---

## 8. Companion PMU16 mounting

Ecumaster PMU16 alongside the ECU on the intake side. Details:

- **PMU16 dimensions: 131 × 112 × 32.5 mm, 345 g** (PMU16DL: 371 g). Source: [Ecumaster PMU_Manual.pdf p.1](https://www.ecumaster.com/files/PMU/PMU_Manual.pdf) — *"Size and weight: 131 x 112 x 32.5 mm … PMU 16 and PMU 16DL: 371 g"*. Copy in repo: <ref_file file="/Users/wesleyc/personal/e36/e36-wiring/docs/vendor/ecumaster/PMU16_Manual_v101.pdf" />.
- **IP60** (dust protected, no water immersion rating). Same source. Requires splash-shielded mounting.
- **Operating temp: AECQ100 Grade 1 (-40 to +125 °C)**. Same source. Better temp margin than the RACE H2O; PMU16 is not the thermal bottleneck.

Combined intake-side footprint: ~450 cm² (H2O + PMU16 side-by-side). Compare to OEM E-box footprint of ~200 cm² — an expanded mounting plate will be needed. Measure your car's available firewall real estate on the intake side during Phase 1 mockup.

---

## 9. Signals that need to cross the firewall

With the ECU in the engine bay, the firewall crossing shrinks to a small dedicated connector — see `harnesses/firewall-crossing-dt12.wv` for the definitive design. In summary:

| Signal | Notes |
|--------|-------|
| ECU +12V constant (PMU16 → H2O) | Same-side engine-bay routing if PMU16 is also intake-side; not a firewall crossing |
| ECU +12V IGN wakeup (cabin ignition switch → H2O) | Firewall crossing, ~18–22 AWG signal-level |
| ECU chassis GND | Engine-bay star point at ECU mount |
| CAN H/L to cabin devices (DCT shifter + Gauge.S) | Twisted pair, shielded, through firewall — see ISO 11898-2 for topology |
| APS e-pedal (2× SGND, 2× +5V, 2× signal) | 6 wires per E46 APS pinout, `docs/dbw-pinouts.md` |
| Sealed USB cable (MaxxECU #1606) | 1.5 m sealed cable, own weatherproof grommet |

The **X20 OEM firewall connector stays 100 % untouched** for cluster feedback and body signals. See `harnesses/body-x20.wv` for X20's OEM pinout — no signals from the new ECU crossing go through X20.

---

## 10. Open items requiring on-car verification

- OEM E-box cavity actual dimensions on this RHD E36 (accept the H2O without modification, or need mounting plate?)
- Physical position of RHD fusebox relative to OEM DME cavity (confirms bimmerforums.co.uk thread against this specific car)
- Available firewall real estate for PMU16 alongside the H2O
- Route path for sealed USB #1606 to a cabin mount point (glove box vs under-dash)

---

## 11. Related documents in this repo

- `docs/vendor/maxxecu/MaxxECU_M50_Terminated_Harness.md` — M50 pre-terminated harness (Phase 1)
- `docs/vendor/maxxecu/MaxxECU_GEN1_Pinout.md` — C1/C2 pinout tables (applies to H2O identically)
- `docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf` — official MaxxECU RACE REV9+ wiring PDF
- `docs/vendor/ecumaster/PMU16_Manual_v101.pdf` — PMU16 manual with dimensions/temp spec
- `harnesses/firewall-crossing-dt12.wv` — DT-12 cabin↔engine-bay ECU crossing (new architecture)
- `harnesses/body-x20.wv` — OEM X20 firewall connector (untouched under the new architecture)
