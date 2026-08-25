# MaxxECU GEN1 Pinout

Archived from: https://www.maxxecu.com/webhelp/wirings-maxxecu_pinout.html  
Wiring diagrams PDF index: https://www.maxxecu.com/downloads

> **Note:** The webhelp page is JavaScript-rendered and cannot be saved as static HTML.
> This file preserves the pin function tables. For wire colors, see the RACE REV9+ wiring PDF.

---

## MaxxECU RACE / STREET / SPORT / V1 — Connector 1 (48-pin, C1)

> Text in red on the original diagram = difference between ECU variants.

| Position | V1/RACE/PRO function | STREET function | SPORT function | Notes |
|----------|---------------------|-----------------|----------------|-------|
| A1 | GPO 5 | — | GPO 4 | |
| A2 | IGN 1 | IGN 1 | IGN 1 | |
| A3 | IGN 2 | IGN 2 | IGN 2 | |
| A4 | GPO 8/TACHO | GPO 8/TACHO | GPO 8/TACHO | 660 Ω pullup |
| B1 | GPO 6 | — | GPO 5 | |
| B2 | IGN 3 | IGN 3 | IGN 3 | |
| B3 | IGN 4 | IGN 4 | IGN 4 | |
| B4 | GPO 1 | GPO 1 | GPO 1 | |
| C1 | GPO 7 | — | AIN 5 (0-5V) | |
| C2 | IGN 5 | IGN 5 | IGN 5 | |
| C3 | IGN 6 | IGN 6 | IGN 6 | |
| C4 | GPO 2 | GPO 2 | GPO 2 | |
| D1 | WBO2 Heater− | WBO2 Heater− | WBO2 Heater− | |
| D2 | IGN 7 | — | AIN 6 (0-5V) | |
| D3 | IGN 8 | — | AIN 7 (0-5V) | |
| D4 | GPO 3 | GPO 3 | GPO 3 | |
| E1 | CAN H | CAN H | CAN H | |
| E2 | CAN L | CAN L | CAN L | |
| E3 | GND Shield | GND Shield | GND Shield | |
| E4 | GPO 4 | — | AIN 8 (0-5V) | |
| F1 | CLT | CLT | CLT | |
| F2 | IAT | IAT | IAT | |
| F3 | WBO2 VREF | WBO2 VREF | WBO2 VREF | |
| F4 | WBO2 VS | WBO2 VS | WBO2 VS | |
| G1 | +5V sensor supply | +5V sensor supply | +5V sensor supply | peak 0.5A, max 150mA |
| G2 | TPS/AIN | TPS/AIN | TPS/AIN | |
| G3 | WBO2 IP | WBO2 IP | WBO2 IP | |
| G4 | WBO2 RCAL | WBO2 RCAL | WBO2 RCAL | |
| H1 | Sensor GND | Sensor GND | Sensor GND | |
| H2 | Trigger GND | Trigger GND | Trigger GND | |
| H3 | TRIGGER | TRIGGER | TRIGGER | |
| H4 | HOME | HOME | HOME | |
| J1 | AIN 1 (Temperature) | AIN 1 (Temperature) | AIN 1 (Temperature) | |
| J2 | AIN 2 (Temperature) | AIN 2 (Temperature) | AIN 2 (Temperature) | |
| J3 | AIN 3 (0-5V) | AIN 3 (0-5V) | AIN 3 (0-5V) | |
| J4 | AIN 4 (0-5V) | AIN 4 (0-5V) | AIN 4 (0-5V) | |
| K1 | INJ 1 | INJ 1 | INJ 1 | |
| K2 | INJ 2 | INJ 2 | INJ 2 | |
| K3 | DIN/VR 1 | DIN 1 | DIN 1 | |
| K4 | DIN/VR 2 | DIN 2 | DIN 2 | |
| L1 | INJ 8 | — | GPO 11/Motor 1− | |
| L2 | INJ 7 | — | GPO 12/Motor 1+ | |
| L3 | INJ 6 | INJ 6 | INJ 6 | |
| L4 | Engine GND | Engine GND | Engine GND | |
| M1 | INJ 3 | INJ 3 | INJ 3 | |
| M2 | INJ 4 | INJ 4 | INJ 4 | |
| M3 | INJ 5 | INJ 5 | INJ 5 | |
| M4 | +12V ECU power supply | +12V ECU power supply | +12V ECU power supply | |

### C1 Molex part numbers

| Part | Molex PN | Qty (STREET) | Qty (STREET/SPORT/V1/RACE/PRO) |
|------|----------|-------------|--------------------------------|
| Connector | 643203311 | 1 | 1 |
| Cable cover | 643201301 | 1 | 1 |
| Terminal / pin (big 1–2 mm²) | 643231039 | 1 | 1 |
| Terminal / pin (big 0.5–1 mm²) | 643231029 | 5 | 7 |
| Terminal / pin (small 0.75 mm²) | 643221029 | 35 | 40 |

---

## MaxxECU RACE — Connector 2 (32-pin black, C2)

> C2 is the black 32-pin connector. RACE-specific — not present on STREET/SPORT/V1.

| Position | RACE C2 function | Notes |
|----------|-----------------|-------|
| A1 | EGT 5+ | |
| A2 | EGT 6+ | |
| A3 | EGT 7+ | |
| A4 | EGT 8+ | |
| B1 | EGT 5− | |
| B2 | EGT 6− | |
| B3 | EGT 7− | |
| B4 | EGT 8− | |
| C1 | EGT 1+ | |
| C2 | EGT 2+ | |
| C3 | EGT 3+ | |
| C4 | EGT 4+ | |
| D1 | EGT 1− | |
| D2 | EGT 2− | |
| D3 | EGT 3− | |
| D4 | EGT 4− | |
| E1 | KNOCK GND | |
| E2 | Knock 1 | |
| E3 | Knock 2 | |
| E4 | AIN 6 (0-5V) | |
| F1 | AIN 7 (0-5V) | |
| F2 | AIN 8 (0-5V) | |
| F3 | DIN/VR 4 | |
| F4 | DIN/VR 5 | |
| G1 | GPO 15 (+12V) | |
| G2 | GPO 16 (+12V) | |
| G3 | AIN 5 (0-5V) | **AIN 5 for virtual clutch position sensor** — C2 pin G3 |
| G4 | Engine GND | |
| H1 | Motor 2+ | |
| H2 | Motor 1− | |
| H3 | Motor 2− | |
| H4 | Motor 1+ | |

> EGT pins use regular contacts. Cold junction compensation done by a temp sensor in thermal contact with the pins.

### C2 Molex part numbers

| Part | Molex PN | Qty |
|------|----------|-----|
| Connector | 0643193211 | 1 |
| Cable cover | 0643191201 | 1 |
| Terminal / pin (big 0.5–1 mm²) | 643231029 | 8 |
| Terminal / pin (small 0.75 mm²) | 643221029 | 24 |

---

## Molex terminals and tools (all connectors)

| Part | Molex PN |
|------|----------|
| Terminal / pin (small 0.5 mm²) | 643221039 |
| Terminal / pin (small 0.75 mm²) | 643221029 |
| Terminal / pin (big 0.5–1 mm²) | 643231029 |
| Terminal / pin (big 1–2 mm²) | 643231039 |
| Plug (small) | 0643251010 |
| Plug (big) | 0643251023 |
| Removal tool (small terminals) | 638132400 |
| Removal tool (big terminals) | 638132300 |
| Crimp tool (big 0.5–1.0 mm²) | 63811-8900 |
| Crimp tool (big 1–2 mm²) | 63811-9000 |
| Crimp tool (small) | 63811-9200 |

Distributors: Digikey, Mouser.

---

## ⚠️ CAN H/L swap warning — early MaxxECU MINI batch

The first ~100 MaxxECU MINIs (early 2019) shipped with CAN H and CAN L swapped in the harness
(wrong color/label/documentation). Regardless of wire color or harness label:

**CAN H = C1 pin E1**  
**CAN L = C1 pin E2**

Verify against pin position, not wire color, on any unit of unknown history.
