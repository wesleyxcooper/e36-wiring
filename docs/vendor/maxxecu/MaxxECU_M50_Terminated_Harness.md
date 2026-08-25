# MaxxECU M50 Terminated Engine Harness

Archived from: https://www.maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html  
Product page: http://www.maxxecu.com/products/terminated_engine_harness/bmw_m50

> **Note:** This build does NOT use the pre-terminated harness. This page is kept as reference for
> signal assignments, connector types, and the VANOS CAM sensor wiring requirement.

Compatible with: MaxxECU STREET / V1 / RACE / PRO

---

## VANOS Head — CAM Sensor Compatibility

The harness is built for a **non-VANOS head**. VANOS heads use a different CAM/HOME sensor
connector and pinout and will NOT work without modification.

Two options to resolve this on a VANOS head:

1. Change the CAM sensor to BMW PN **12141726590**
2. Cut the CAM connector in the harness, replace with a fitting connector, and add switched +12V

| Pin | VANOS CAM sensor pinout | Non-VANOS CAM sensor pinout |
|-----|------------------------|-----------------------------|
| 1 | +12V | Signal |
| 2 | Signal | Sensor GND |
| 3 | Sensor GND | Shield |

---

## Harness Signal Support

| Terminated engine harness | MaxxECU I/O | Notes |
|--------------------------|-------------|-------|
| +12V to injectors, ignition, solenoids | Yes | |
| Cylinder head GND | Yes | |
| OEM generator | Yes | |
| OEM engine starter | Yes | |
| Injectors (Bosch JPT connectors) | INJ | |
| Ignition (VAG 1.8T coil-on-plug) | IGN | |
| OEM intake temperature sensor | IAT | |
| OEM coolant temperature sensor | CLT | |
| OEM throttle position sensor | TPS | |
| OEM idle valve solenoid | GPO 4, 5 | Not available on STREET |
| OEM crank trigger | TRIGGER | |
| OEM CAM trigger | HOME | |
| VANOS solenoid | GPO 3 | |
| Boost solenoid | GPO 1 | No solenoid included |
| Fuel pump control | GPO 2 or any available output | |
| Engine FAN control | GPO 6 or any available output | Not available on STREET |
| Wideband LSU connector | Yes | LSU 4.2 |
| MAP sensor hose in harness | Yes | |

---

## Harness Lengths

| Start | End | Total length |
|-------|-----|--------------|
| MaxxECU CMC connector | Firewall entry/bushing | 850 mm |
| MaxxECU CMC connector | LSU connector | 1600 mm |
| MaxxECU CMC connector | IGN 1 coil connector | 1950 mm |

---

## Harness Connectors

- **Injectors** — Bosch JPT 2-way
- **Trigger/HOME** — Bosch JPT 3-way
- **CLT** — Bosch JPT 2-way
- **IDLE solenoid** — Bosch JPT 3-way
- **VANOS solenoid** — Bosch JPT 2-way
- **Lambda (WBO2)** — Bosch LSU 4.2 6-way
- **Boost** — Superseal 2-way
- **Ignition coils** — VAG 4-way (COP); wired for **long coils**
- Ignition coils ground — mount in cylinder head, do not forget

---

## 12-Pin Extra Connector (viewed from wire side)

> REV 2 is the current harness revision.

| Pin | REV 1 function | REV 2 function |
|-----|---------------|----------------|
| 1 (A) | — | +12V ignition coils power supply |
| 2 (B) | Alternator pin 3 (battery+) | Engine ground |
| 3 (C) | Alternator pin 1 (light) | GPO 2 (fuel pump) |
| 4 (D) | Alternator pin 2 (ignition+) | GPO 6 (FAN) |
| 5 (E) | — | — |
| 6 (F) | — | Engine starter (+12V) — connect to ignition key/switch |
| 7 (G) | — | +12V ECU power supply |
| 8 (H) | Engine starter (+12V) | — |
| 9 (J) | +12V ignition coils power supply | — |
| 10 (K) | +12V ECU power supply | Sensor GND (see cable printing) |
| 11 (L) | Engine ground | — |
| 12 (M) | — | Alternator +12V |

> If the cable harness is unmarked, treat as REV 1.

---

## 16-Pin Extra Connector (viewed from wire side)

| Pin | REV 1/2 function | Notes |
|-----|-----------------|-------|
| 1 (H) | +5V power supply | |
| 2 (G) | INJ 8 (REV1) / Sensor GND (REV2) | INJ 8 not on STREET |
| 3 (F) | INJ 7 | Not on STREET |
| 4 (E) | GPO 8/TACHO | |
| 5 (D) | GPO 7/DIN 3 | Not on STREET |
| 6 (C) | GPO 6 | Not on STREET |
| 7 (B) | GPO 3 | Parallel-wired with VANOS connector |
| 8 (A) | GPO 2 | |
| 9 (S) | CAN L | |
| 10 (R) | CAN H | |
| 11 (P) | AIN 4 (0-5V) | |
| 12 (N) | AIN 3 (0-5V) | |
| 13 (M) | AIN 2 (temperature) | |
| 14 (L) | AIN 1 (temperature) | |
| 15 (K) | DIN 2 | |
| 16 (J) | DIN 1 | |
