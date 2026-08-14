# Harness Build Discipline

Reference for connector pinning, depinning, and harness assembly across all e36-wiring harnesses.

---

## Overview — Pin Count by Connector Family

| Connector | Family | Pins populated | Tool |
|-----------|--------|---------------|------|
| MaxxECU RACE C1 | Molex 48-pin | ~40 (varies by harness) | 63811-9200 (small) · 63811-8900/9000 (big) |
| MaxxECU RACE C2 | Molex 32-pin | 0 (Phase 1/3) — defer | Same as C1 |
| Deutsch AS firewall bulkhead | AS series, size 20 | Up to 79 | Deutsch WT-0460-8-0800 |
| 07K cam sensor pigtail | 3B0973703G (3-pin VAG) | 3 | Knipex 97 52 68 |
| 07K crank sensor pigtail | 3B0973703G (3-pin VAG) | 3 | Knipex 97 52 68 |
| 07K MAP sensor pigtail | 3B0973703G (3-pin VAG) | 3 | Knipex 97 52 68 |
| CLT sensor pigtail | 1J0973702 (2-pin NTC) | 2 | Knipex 97 52 68 |
| IAT sensor pigtail | 1J0973702 (2-pin NTC) | 2 | Knipex 97 52 68 |
| Knock sensor pigtail | 1J0973712 (2-pin flat) | 2 | Knipex 97 52 68 |
| EV14 injector pigtails ×5 | USCAR EV14 | 2 each | Knipex 97 52 68 |
| COP pigtails ×5 | 4B0973724 (4-pin COP) | 4 each | Knipex 97 52 68 |
| EWP controller | Kostal 2+2 (4-pin) | 4 | Knipex 97 52 68 |
| PST-F1 sensor | BSP M10×1.0 pigtail | 2 | Knipex 97 52 68 |
| ATF temp sensor | 2-pin spliced to C1 | 2 | Knipex 97 52 68 |
| 8HP CAN harness | GT150 12-pin pre-term. | n/a (pre-made) | n/a |
| DCT shifter | 4-wire — bare ends | 4 | Open-barrel (IWISS IWS-2820M) |

**Estimated total pin insertions: ~200–230.** Budget at least one full day per major harness
(engine harness, bulkhead, cabin loom) — rushing pin work is the primary cause of
hard-to-trace shorts and intermittent sensor faults.

---

## Tools — Which Tool for Which Connector

| Tool | PN | Connector families |
|------|----|--------------------|
| Molex ratcheting crimper (small terminals) | 63811-9200 | MaxxECU C1/C2 small-gauge pins |
| Molex ratcheting crimper (big 0.5–1.0 mm²) | 63811-8900 | MaxxECU C1/C2 large-gauge pins |
| Molex ratcheting crimper (big 1–2 mm²) | 63811-9000 | MaxxECU C1/C2 large-gauge pins |
| Micro-pin ratcheting crimper | Knipex 97 52 68 | All VAG sensor pigtails, COP, EV14, NTC |
| Deutsch AS crimper | Deutsch WT-0460-8-0800 | Firewall bulkhead size 20 contacts |
| Open-barrel crimper | IWISS IWS-2820M | Ring terminals, relay contacts, general open-barrel |
| Ferrule crimper | IWISS IWS-10 | Screw-clamp terminals (ECU power/GND strands) |
| **Depin — Molex small terminals** | 638132400 | C1/C2 small-pin extraction |
| **Depin — Molex big terminals** | 638132300 | C1/C2 large-pin extraction |
| **Depin — VW/Bosch PTS connectors** | Lisle 57750 | All VAG push-to-seat pigtails (sensor, COP, injector) |
| **Depin — Deutsch AS size 20** | Deutsch 1680-73-01 | Firewall bulkhead contacts |

> ⚠️ **Depin tool matters:** Lisle 57750 works on push-to-seat (PTS) bodies only.
> Do NOT use it on pull-to-seat (PTLS) or Molex contacts — different locking geometry.
> Wrong pick damages the connector body and the terminal retention lance.

---

## Connector Families — Pinout Critical Warnings

### 3B0973703G — 3-pin VAG sensor (cam / crank / MAP)
All three connectors use the **identical physical housing**. The wiring is NOT identical:

| Sensor | Pin 1 | Pin 2 | Pin 3 |
|--------|-------|-------|-------|
| Crank (passive VR) | Signal+ | Signal− | Shield/GND |
| Cam (active Hall) | +5V | GND | Signal |
| MAP | +5V | GND | Signal |

> ⚠️ **Label pigtails at crimp time — before the connector body goes on.** Swapping cam
> and crank = no crank trigger = no-start. MaxxECU cannot distinguish the connectors
> physically. Use heat-shrink label sleeves or permanent marker on the wire before seating.

### MaxxECU C1 (Molex 48-pin) — terminal size by pin group

Not all C1 pins use the same terminal size. Check the MaxxECU RACE pinout PDF before
crimping — power and ground pins (ECU +12V, GND) take the large terminal; all signal
pins (AIN, DIN, GPO, SGND) take the small terminal. Wrong terminal in wrong cavity =
connector damage and a difficult extraction.

---

## Workflow — Pin Insertion Sequence

Follow this order on every connector. Do not deviate for speed.

1. **Strip** — target strip length per connector spec (typically 2.5–3 mm for VAG contacts; follow Molex spec sheet for C1)
2. **Crimp** — use the correct ratcheting die; verify the crimp did not cut strands
3. **Pull-test** — tug the wire firmly before seating. A terminal that pulls out under hand force will pull out under vibration
4. **Inspect** — check insulation crimp grips the jacket, conductor crimp grips the strands; no exposed bare copper between the two crimp wings
5. **Verify wire identity** — double-check which wire you are seating against the WireViz diagram before it goes in
6. **Seat** — insert until the audible click (terminal locking lance engages)
7. **Verify seating** — gentle tug after click; should not move
8. **Continuity check** — do NOT close the connector shell or sleeve the loom until every pin has been verified with a DMM against the `.wv` diagram end-to-end

> ⚠️ **Never sleeve before testing.** Expanding braid and heat-shrink make depin
> operations destructive. All connectors stay unsealed until the harness passes
> continuity + resistance checks on the bench.

---

## Depinning Procedure

**VW/Bosch PTS (Lisle 57750):**
1. Insert pick into the terminal cavity alongside the wire
2. Depress the locking lance while pulling the wire from the rear
3. The terminal slides out the back of the connector — do not pull from the front

**Deutsch AS size 20 (Deutsch 1680-73-01):**
1. Insert extraction tool into the front face of the bulkhead
2. Tool depresses the collet; pull wire from rear while holding tool engaged
3. Contact exits from the rear

**Molex C1/C2 (PN 638132400 / 638132300):**
1. Use the designated removal tool from the front face
2. Follow the MaxxECU webhelp extraction procedure exactly — the Molex housing has a secondary locking wedge that must be partially withdrawn first before individual contacts can be extracted

---

## Bench Test Before Install

Run each harness on the bench before it goes in the car:

1. **Continuity:** Every signal wire from ECU pin to sensor pigtail — verify against `.wv` file
2. **Isolation:** No contact between adjacent pins (especially power to signal grounds)
3. **Resistance:** Power and ground runs ≤ 0.1 Ω end-to-end for 12 AWG; sensor signal runs ≤ 0.5 Ω
4. **Connector retention:** Every pin survives a 5 N tug test in both directions

Only after bench pass → sleeve → route → install.
