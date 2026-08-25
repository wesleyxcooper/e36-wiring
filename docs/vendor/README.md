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

> ⚠️ **This build's `.wv` files do not match MaxxECU's color convention.** See `docs/harness-build.md § Wire Color Convention` for the full divergence table and rationale. The `.wv` convention was established before the MaxxECU wiring diagram was consulted.

---

## Ecumaster PMU16 (`ecumaster/`)

| File | Source URL | Notes |
|------|-----------|-------|
| `PMU16_Manual_v101.pdf` | https://www.ecumaster.com/files/PMU/PMU_Manual.pdf | Current manual — v101.2.1 (April 2026). Full pinout, wiring schematics, CAN configuration, output specs. **No wire color convention specified.** |
| `PMU16_Manual_v1.04.pdf` | https://www.ecumaster.com/files/PMU/PMU_Manual_1_04.pdf | Older manual — v1.04. Contains basic wiring diagrams and wire size recommendations by current rating. |
| `PMU16_Pinout_v1.1.pdf` | https://www.ecumaster.com/files/PMU/PMU-16_Pinout_v1.1.pdf | Standard PMU16 pinout — Sicma/FCI 39-pos connector. Power pins, CAN1/2 H/L, analog inputs A1–A16, outputs O1–O16. |
| `PMU16-AS_Pinout_v1.3.pdf` | https://www.ecumaster.com/files/PMU/PMU-16AS_Pinout_v1.3.pdf | PMU16-AS variant — uses Deutsch AS + Radlok connectors (37-pin signal + 19-pin high-current). Keep for reference if connector variant changes. |

**Wire color convention:** Ecumaster does not specify wire colors in any PMU16 document. Pin functions and current ratings only. Color choice is entirely up to the builder.

**Wire size guide (from `PMU16_Manual_v1.04.pdf`):**

| Max continuous current | Recommended wire (chassis, Tefzel/TXL) |
|----------------------|----------------------------------------|
| 5 A | 1 mm² / AWG 18 |
| 10 A | 1.5 mm² / AWG 16 |
| 15 A | 2.5 mm² / AWG 14 |
| 25 A | 4 mm² / AWG 12 |
| ≥ 25 A (power connector) | 25 mm² / AWG 3 minimum |
