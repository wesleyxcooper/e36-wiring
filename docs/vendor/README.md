# Vendor Reference Docs

Offline archive of manufacturer documentation used in this build.
Saved so the correct version is accessible without internet on the bench.

---

## MaxxECU (`maxxecu/`)

| File | Source URL | Notes |
|------|-----------|-------|
| `MaxxECU_RACE_REV9plus_Wiring.pdf` | https://www.maxxecu.se/files/Documentation/Wirings/MaxxECU%20RACE%20(REV9+)%20-%20Wiring-en.pdf | **Primary reference** — RACE variant REV9+. Contains wire color scheme and complete connector diagrams for C1 (48-pin) and C2 (32-pin). See `MaxxECU_GEN1_Pinout.md` for pin function table. |
| `MaxxECU_GEN1_Pinout.md` | https://www.maxxecu.com/webhelp/wirings-maxxecu_pinout.html | Saved text of the GEN1 pinout webhelp page (JavaScript-rendered, cannot be saved as HTML). Contains C1, C2, and Molex part numbers. Archived from live page. |
| `MaxxECU_M50_Terminated_Harness.md` | https://www.maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html | Saved text of the M50 terminated engine harness page. Source of truth for VANOS cam sensor swap requirement and which engine signals the pre-terminated harness covers. |

**Wire color convention (from `MaxxECU_RACE_REV9plus_Wiring.pdf`):**

| Color | MaxxECU RACE use |
|-------|-----------------|
| Red | +12V — ECU power (M4), coil/inj power rail, 5V sensor supply output (G1) |
| Black | Analog sensor signal wires — TPS (G2), CLT (F1), IAT (F2), all AIN (J1–J4), all DIN (K3–K4) |
| Brown | Sensor GND (H1); WBO2 signals (F4) |
| Yellow | Shield GND (F3) |
| White | CAM/HOME trigger signal (H4) |
| Blue | Ignition coil drives — IGN 1–6 (A2, A3, B2, B3, C2, C3) |
| Grey | Injector drives — INJ 1–6 (K1, K2, M1–M3, L3); CAN H (E1) |
| Green | GPO outputs — GP OUT 2–8 (C4, D4, E4, A1, B1, C1, A4) |
| Pink | CAN L (E2) |

> ⚠️ **This build's `.wv` files diverge from MaxxECU's color convention — intentionally.** The MaxxECU RACE wiring diagram was reviewed and the divergences were evaluated; the build's convention was retained for reasons documented in `docs/harness-build.md § Wire Color Convention`. If you ever splice a MaxxECU pre-terminated pigtail into this loom, expect a color conflict.

---

## Video & Community Resources

Build videos and reference sheets from similar MaxxECU standalone harness builds. Saved here for reference even where the engine differs — the methodology (wire selection, connector sourcing, build sequence, labeling) is directly transferable.

All three are from the same builder (Drive, Revive, Tinker) documenting a Volvo 242 T5 swap with MaxxECU Race. Same ECU family, same 55-pin mil-spec bulkhead connector strategy, same Raychem heat-shrink hierarchy as this build.

| Resource | Type | URL | Key takeaways for this build |
|----------|------|-----|------------------------------|
| "Everything I Wish I Knew Before My First ECU Harness" | YouTube (40 min) | [youtube.com/watch?v=Z3hmNz64Gw8](https://www.youtube.com/watch?v=Z3hmNz64Gw8) | Avoid generic/unbranded wiring supplies from Amazon — OEM part numbers from verified listings are fine. Preferred suppliers: ProWire USA, Waytek, Del City — same three already in this BOM. TXL is the right choice. **Minimize joints = minimize failure points** — each pigtail splice is an extra joint. Cost reality: ~$3,000 for a complete engine harness **plus full front-half body rewire** (all lighting, dash, etc.); that scope is far larger than this build's engine ECU harness only. Material cost for the ECU/engine harness alone is more in the $500–$1,000 range. |
| "Custom Wiring Harness Build for the Volvo 242 T5 5 Cyl Turbo Swap" | YouTube (28 min) | [youtube.com/watch?v=G3fSqfpBi1U](https://www.youtube.com/watch?v=G3fSqfpBi1U) | Build-video companion to the above. **String template before cutting any wire** (confirms routing lengths first). Builds harness in two halves split at the 55-pin bulkhead — same architecture as this build. Start from center pins of bulkhead and radiate outward. **Kapton tape before adhesive heat-shrink** on wire bundles (adhesive won't bond permanently to bundle; eases future service). Label every connector with heat-shrink labels + clear overwrap. Spare wires terminated at accessible stub under coil cover for future use. |
| "Volvo 242 /// T5 Engine /// MaxxECU Race Wiring" Google Sheet | Public spreadsheet | [docs.google.com/spreadsheets/d/1Dwv_uEoKL6w67gxhPlAi09J_1L7u3MWiEvI8ZP8SWDo](https://docs.google.com/spreadsheets/d/1Dwv_uEoKL6w67gxhPlAi09J_1L7u3MWiEvI8ZP8SWDo) | Spreadsheet companion to the build videos (linked from Video 1 description). Tabs: ECU pin assignments by component, bulkhead pin map, 12-pin connector, 12V/5V/sensor GND distribution. Functionally the same data model as this build's `.wv` files — useful cross-reference for knock sensor grounding policy (shields drain to ECU only, never chassis), WBO2 wiring, and sensor GND star topology. |

### Key cross-references from this resource set

**Knock sensor shield drain:** Both the Google Sheet notes and this build's `.wv` files confirm the same policy: knock shield drain wires terminate inside the ECU only — no chassis termination. The Volvo build splices both knock GND wires to a shared pin; this build stars them separately to the same H1 pin. Either approach is valid for knock sensors specifically.

**Shield drain policy (general):** For all shielded cables (crank, cam, WBO2, knock), drain the shield at the ECU end only. Never at both ends — ground loop introduces exactly the noise you are trying to suppress.

**Heatshrink hierarchy (confirmed matches this build):** Raychem DR-25 (non-adhesive, main body) → Raychem ATUM or SCL (adhesive, joints and ends) → 90° Raychem boot at bulkhead connector. Apply Kapton tape first whenever adhesive shrink contacts wire bundles directly.

**DBW e-throttle:** The Volvo build runs MaxxECU Race with full e-throttle (Saab/Hella pedal, Volvo ETB) — confirms the same ECU family supports DBW, though pedal and TB sourcing differ from this build's E46 APS + 07K ETB path.

---

## Ecumaster PMU16 (`ecumaster/`)

| File | Source URL | Notes |
|------|-----------|-------|
| `PMU16_Manual_v101.pdf` | https://www.ecumaster.com/files/PMU/PMU_Manual.pdf | Current manual — v101.2.1 (April 2026). Full pinout, wiring schematics, CAN configuration, output specs. **No wire color convention specified.** |
| `PMU16_Manual_v1.04.pdf` | https://www.ecumaster.com/files/PMU/PMU_Manual_1_04.pdf | Older manual — v1.04. Contains basic wiring diagrams and wire size recommendations by current rating. |
| `PMU16_Pinout_v1.1.pdf` | https://www.ecumaster.com/files/PMU/PMU-16_Pinout_v1.1.pdf | Standard PMU16 pinout — Sicma/FCI 39-pos connector. Power pins, CAN1/2 H/L, analog inputs A1–A16, outputs O1–O16. |

> **PMU16 variant note:** This build uses the standard PMU16 (39-pin Sicma/FCI connector). The PMU16-AS variant uses Deutsch AS connectors (same family as the firewall bulkhead) and would reuse the AFM8 + K40/K42 tooling already in the build. The standard PMU16 Sicma contacts require a separate crimp tool **not yet in the BOM** — see `docs/harness-build.md § Tools` and `docs/wiring-bom.md`. If the PMU16 has not been purchased yet, the PMU16-AS is worth evaluating. PMU16-AS pinout: https://www.ecumaster.com/files/PMU/PMU-16AS_Pinout_v1.3.pdf

**Wire color convention:** Ecumaster does not specify wire colors in any PMU16 document. Pin functions and current ratings only. Color choice is entirely up to the builder.

**Wire size guide (from `PMU16_Manual_v1.04.pdf`):**

| Max continuous current | Recommended wire (chassis, Tefzel/TXL) |
|----------------------|----------------------------------------|
| 5 A | 1 mm² / AWG 18 |
| 10 A | 1.5 mm² / AWG 16 |
| 15 A | 2.5 mm² / AWG 14 |
| 25 A | 4 mm² / AWG 12 |
| ≥ 25 A (power connector) | 25 mm² / AWG 3 minimum |
