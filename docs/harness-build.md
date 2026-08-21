# Harness Build Discipline

Reference for connector pinning, depinning, and harness assembly across all e36-wiring harnesses.

---

## Overview — Pin Count by Connector Family

| Connector | Family | Pins populated | Tool |
|-----------|--------|---------------|------|
| MaxxECU RACE C1 | Molex 48-pin | ~40 (varies by harness) | 63811-9200 (small) · 63811-8900/9000 (big) |
| MaxxECU RACE C2 | Molex 32-pin | 0 (Phase 1/3) — defer | Same as C1 |
| Deutsch AS firewall bulkhead | AS series, size 20 | Up to 79 | Daniels M22520/2-01 + K43 positioner (M22520/2-10) |
| 07K cam sensor pigtail | 3B0973703G (3-pin VAG JMT) | 3 | Engineer PA-09 |
| 07K crank sensor pigtail | 3B0973703G (3-pin VAG JMT) | 3 | Engineer PA-09 |
| 07K MAP sensor pigtail | 3B0973703G (3-pin VAG JMT) | 3 | Engineer PA-09 |
| CLT sensor pigtail | 1J0973702 (2-pin NTC JPT) | 2 | Engineer PA-09 |
| IAT sensor pigtail | 1J0973702 (2-pin NTC JPT) | 2 | Engineer PA-09 |
| Knock sensor pigtail | 1J0973712 (2-pin flat) | 2 | Engineer PA-09 |
| EV14 injector pigtails ×5 | USCAR EV14 | 2 each | Engineer PA-09 |
| M52 coil pigtails ×6 | ⚠️ TODO — BMW 2-pin pencil coil connector PN to verify at build; common source: BMW e36 coil pigtail from ECS/FCP or aftermarket | 2 each | Engineer PA-09 |
| 07K COP pigtails ×5 | 4B0973724 (4-pin COP) | 4 each | Engineer PA-09 |
| EWP controller | Kostal 2+2 (4-pin) | 4 | Engineer PA-09 |
| PST-F1 sensor | BSP M10×1.0 pigtail | 2 | Engineer PA-09 |
| ATF temp sensor | 2-pin spliced to C1 | 2 | Engineer PA-09 |
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
| **Micro-pin crimper — VAG JMT/JPT pigtails** | **Engineer PA-09** (~$30–40, Amazon) — community standard for Bosch JMT 1.5mm and JPT 2.8mm contacts. Covers VAG cam/crank/MAP/CLT/IAT/knock/COP pigtail terminals in one tool. Budget: IWISS SN-2549 (~$17). ⚠️ `Knipex 97 52 68` (previously listed here) does not exist — that PN is not in the Knipex catalog. The Knipex 97 52 67 DT (~$427) is for Deutsch DT contacts only, not for Bosch JMT/JPT. | All VAG sensor pigtails, COP, EV14 injector pigtails |
| **Deutsch HD30 / DT contacts crimper** | **Deutsch HDT-48-00** (~$350–465) or **JRready NEW-DT2** (~$169 budget) | Maven HD30 35-pin connector (size-16 and size-20) + DT 2-pin bypass connectors |
| **AS solid barrel crimper** | Daniels M22520/2-01 (AFM8) handle + K43 positioner (M22520/2-10) | **Firewall bulkhead Deutsch AS size-20 solid barrel contacts.** TE-specified mil-spec tool for AS contacts — NOT the HDT-48-00 or clones (those cover DT/DTM/DTP only, different contact geometry). No cheap substitute — wrong die produces cold crimps that pass pull-test but fail under vibration. Best value: Fischer Motorsports "DMC Deutsch Size 20 AS Tool Kit" (~$426, includes handle + both positioners). K43 positioner alone: ~$80–94 surplus (dmctools.com). Source: TE Autosport technical datasheet (1-1773721-9), Fischer Motorsports. |
| AS crimper positioner | Daniels K43 (M22520/2-10) | Included in Fischer kit above. Locates size-20 AS pin and socket contacts in the M22520/2-01 frame. Single positioner covers both pin and socket. |
| Open-barrel crimper | IWISS IWS-2820M | Ring terminals, relay contacts, general non-insulated open-barrel splices. Use non-insulated + adhesive-lined heat shrink — never pre-insulated crimps. |
| Ferrule crimper | IWISS IWS-10 | Screw-clamp terminals (ECU power/GND strands) |
| Flush cutters | Milwaukee 48-22-6106 or equiv | In-car wire trimming, flush cuts near connector bodies. Buy before starting any connector work. Source: StreetCarJoe Race Car Wiring Pt.1. |
| Rivnut tool | Astro Pneumatic 1442 or equiv manual tool | M4/M6 rivnuts for PMU16 bracket and ECU bracket mounting to thin sheetmetal / carbon panels (no backside access needed). Source: StreetCarJoe Race Car Wiring Pt.3. |
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

## Power & Ground Rules

These rules cover EFI grounding on a dual-duty street/drift E36 with MaxxECU.
Sources: MaxxECU GEN2 RACE quick-start guide (maxxecu.com/files/Documentation/Manuals/...),
MaxxECU webhelp error code 19, HP Academy EFI Wiring Fundamentals, ShopECU grounding guide.

### Battery Cutoff Switch — Optional for This Build
A cutoff switch is **not required** on a dual-duty street car with a working ignition key.
Install one only if your HPDE org or track mandates it, or if you plan wheel-to-wheel racing.
(Grassroots drift tandems typically do not require a cutoff switch.)

**If you do install one:** it must be 4-post (Moroso 74108 or equiv), NOT 2-post.
A 2-post switch only disconnects the battery; with an alternator present the engine
continues running because the alternator keeps producing current. The 4-post type
routes the alternator through the switch so both are disconnected simultaneously.

### Ground Strategy — What MaxxECU Actually Requires
Per the MaxxECU GEN2 RACE quick-start guide:

> "Battery negative (−) must connect to the chassis or cylinder head.
> Engine must be grounded to the chassis.
> **ECU engine ground must connect to the cylinder head.**"

In practice for this build:
1. **Battery negative → chassis stud** (engine bay M8 stud): PMU16 GND, body electrics,
   fan/pump motor returns. Keep the factory cable or run a new 4 AWG if needed.
2. **Engine block → chassis bonding strap**: keep the M52 factory strap. This is the
   starter and alternator current return path. Verify it is clean — no paint under the lug,
   star washer, tight nut. This is the most commonly overlooked step after a repaint.
3. **MaxxECU ENGINE GND pin → cylinder head**: this is a signal-level wire in the engine
   harness, not a heavy power cable. It is MaxxECU’s own mandatory requirement.

**Optional (not required):** run a second 4 AWG cable directly from battery negative to the
engine block — belt-and-suspenders for a pure race build where factory bonding straps are
removed. Not needed on this build while factory straps are retained and clean.

### ECU Sensor Grounds — The One Rule You Cannot Break
MaxxECU sensor GND pins are **not** chassis ground and **not** engine block ground.
They connect only to sensors whose analog signal returns to the ECU. Wiring a sensor
GND pin to chassis or engine block is the most common MaxxECU install mistake and
triggers MTune error 19: *"Sensor GND is somehow wired to engine ground. <-- big no no."*
Source: maxxecu.com/webhelp/information-error_codes-19.html

Keep ECU power ground returns separate from high-current devices (fuel pump, fans, starter).
Do not stack multiple systems on the same ground lug as the ECU.

### Coil Pack Secondary Ground
Each bank of coils needs a secondary ground to the cylinder head (one ground strap per bank).
This is separate from the main coil power/GND supply wire. The coil will run without it,
but with elevated secondary voltage noise. Do not share with any sensor ground path.

### One-to-Many 5V Reference Distribution
When multiple sensors share the MaxxECU 5V SENS OUT: use a **non-insulated 1→4 crimp
junction** (one wire in, 4 wires out). Crimp, heat-shrink, done. Keeps star topology on
the 5V rail, avoids daisy-chain voltage drop sensor-to-sensor.
Applies to: TPS, MAP sensor, APS (e-pedal), and any 0–5V ratiometric sensor.

---

---

## Harness Architecture — Trunk, Sub-Looms, and Pigtails

A properly built engine harness has three tiers. Each tier has a distinct role.

### Tier 1 — Main trunk

Runs from the AS79 firewall connector along the length of the engine. Contains all wires for the duration of their shared routing path. Sleeved in 1/2" (13mm) Techflex F6 expandable braid. Secured to engine brackets or valve cover rail with P-clips at ~250mm intervals.

### Tier 2 — Sub-looms

At defined breakout points, groups of wires exit the main trunk and run as a shorter sub-loom toward a cluster of related components. Each sub-loom has its own Techflex sleeve (1/4" / 6mm) and is labeled at the breakout with a Brady M210 + PermaSleeve heat-shrink label — **not a zip-tie flag**. See Labeling section below.

**Standard sub-loom groupings for the 07K/M52 engine harness:**

| Sub-loom | Contents | Sleeve OD | Runs to |
|----------|----------|-----------|---------|
| Injector | INJ 1–5 + shared +12V Coils/Inj rail wires | 1/4" (6mm) | Along injector rail |
| Coil | IGN 1–5 + shared +12V Coils/Inj rail wires | 1/4" (6mm) | Along valve cover rail |
| Trigger | Crank VR+/VR−/shield, Cam Hall — **shielded runs only, own sleeve, away from injector and coil primaries at all points** | 1/4" (6mm) | Front of engine toward sensors |
| Sensor | CLT, IAT, MAP, TPS, +5V, Sensor GND | 1/4" (6mm) | Around intake manifold |
| Knock | KS1, KS2, Knock GND — shielded, 07K only | 1/4" (6mm) | Below intake manifold |
| WBO2 | Wideband signal, shielded own run | 1/4" (6mm) | WBO2 controller to ECU; away from coil primaries |

### Tier 3 — Pigtails

At the end of each sub-loom, individual wires branch and join to pre-bought pigtails via a splice. The pigtail bridges from the harness splice point to the component connector (e.g., EV14 injector connector, 3B0973703G sensor connector).

Pigtails are **pre-bought items with the correct mating connector already on the component end.** You never make the component-side connector with raw terminals. See connector table at the top of this document for part numbers.

### Wires per component — injectors and coils are not 1 wire each

Every component has multiple wires. The EV14 injector connector has 2 pins and requires 2 wires from the harness:

| EV14 pin | Wire | Source |
|----------|------|--------|
| Pin 1 | +12V switched | Shared coils/inj power rail (tapped via Raychem splice from the bus wire running along the injector rail) |
| Pin 2 | INJ-N signal | Individual wire from AS79 pin 8–13 — unique to each injector |

The shared +12V bus runs as one continuous wire the full length of the injector rail. At each injector, a Raychem sleeve taps it: one wire in from the upstream bus, one stub out to the pigtail pin 1, one wire out continuing the bus downstream. The INJ signal wire (unique per injector) is a separate Raychem splice at the same pigtail, going to pin 2.

The 07K COP coil (4B0973724, 4-pin) has 3 active wires:

| 4-pin COP pin | Wire | Source |
|--------------|------|--------|
| Pin 1 | +12V switched | Shared coils/inj power rail (same bus as injectors) |
| Pin 2 | GND | Shared engine-head GND strap; do NOT connect to sensor GND |
| Pin 3 | IGN-N signal | Individual wire from AS79 pin 4–7 or 32–34 — unique to each coil |
| Pin 4 | Not connected (or diagnostic — leave unconnected unless specified by ECU) | — |

> **The +12V shared bus is a single wire, not 5 separate wires.** It runs the length of the injector (or coil) rail and gets tapped at each component with a Raychem splice. Think of it as a power chain — one wire in, stub out, same wire continues to the next injector.

### Wire bundling inside sub-looms — parallel, not twisted or braided

Individual wires within a sub-loom run **side-by-side in parallel**. Do not twist the bundle, do not braid individual wires together. Reasons:
- Twisting the whole bundle makes it rigid and adds length, making it difficult to branch individual wires at different component positions along the sub-loom
- The Techflex expandable braid holds the bundle together and provides abrasion resistance without any twisting underneath
- For the breakout transition from main trunk to sub-loom, a few wraps of Tesa 51036 fabric tape (or similar) under the Techflex consolidates the bundle at the branch point — optional but keeps things clean

**The one exception is the crank VR pair.** The VR+ and VR− wires **must be twisted together** before going into the TRIGGER sub-loom:
- Twist rate: ~1 twist per 25mm (1 twist per inch) — twist by hand from tip to tip before routing
- The twist causes both wires to intercept identical electromagnetic interference simultaneously; the ECU's differential input subtracts the common-mode noise, leaving only the real crank signal
- Laying them parallel instead of twisted degrades trigger signal quality and can cause dropout at high RPM under electrical load
- After twisting, both wires run inside the TRIGGER sub-loom sleeve alongside the shield drain wire — do not separate them at any point in the routing

The CAM Hall signal wire does not need twisting — it is a single-ended digital output with its own dedicated +5V and GND, not a differential pair.

### Splice types — no iron soldering

The joint between a harness wire and a pigtail bare end is the only permanent connection in the system. Two acceptable methods:

| Method | How | When to use |
|--------|-----|-------------|
| **Raychem SRGB solder sleeve** | Overlap bare wire ends inside sleeve, heat gun from 50–75mm — sleeve shrinks and solder ring wicks simultaneously | Preferred — fully encapsulated, strain-relieved by the sleeve |
| **Non-insulated butt crimp + adhesive heat-shrink** | Crimp barrel over overlapping bare ends, slide 3:1 adhesive heat-shrink over crimp, heat | Alternative if Raychem sleeves unavailable |

**Do not use a soldering iron.** An iron creates a rigid joint at exactly the flex point. Under engine vibration the wire cracks at the solder/insulation boundary — the break is invisible inside the heat-shrink. Raychem sleeves avoid this because the joint is fully encapsulated and the sleeving provides strain relief.

---

## Labeling — Where, What, and How

Labels are the only way to identify wires and looms once the harness is sleeved. Apply before sleeving — you cannot add labels through closed Techflex.

### What gets labeled

| Location | Label content | Tool |
|----------|--------------|------|
| Every main harness wire — both ends | AS79 pin number + signal name (e.g., `8 INJ1`) | Brady M210 + PermaSleeve M21-125-C-342 (22–16 AWG) |
| Pigtail wire — connector end (before body snaps on) | Signal + cylinder number (e.g., `INJ1`, `COL3`, `CAM`, `CRANK`) | Same |
| Pigtail wire — splice end (within 20mm of splice) | Signal name | Same |
| Sub-loom at breakout from main trunk | Sub-loom name (e.g., `INJECTORS`, `COILS`, `SENSORS`) | Brady M210 + PermaSleeve M21-375-C-342 (3/8" cartridge, slides over 1/4" sub-loom before Techflex goes on) |
| Main trunk at AS79 exit | Harness name (e.g., `ENGINE 07K PH3`) | Brady M210 + PermaSleeve M21-500-C-342 (1/2" cartridge) |

### Breakout labeling — PermaSleeve, not zip-tie flags

The correct method for labeling sub-loom breakout points is a **Brady PermaSleeve heat-shrink sleeve**, the same tool used for individual wire labels. Slide the appropriately sized PermaSleeve over the sub-loom at the breakout point *before* Techflex sleeving goes on. Print the sub-loom name, position the sleeve, shrink with heat gun. Result: flush with the loom surface, oil-resistant, cannot rotate.

Zip-tie flag labels (a printed tab folded through a zip-tie cinched to the loom) are shop-grade — they rotate around the loom, collect oil, and protrude visually. Do not use them on a finished harness.

### Labeling sequence — critical order

1. Print all wire labels before any assembly begins
2. **Slide label sleeves onto wires before crimping terminals** — labels cannot pass through terminal bodies after the fact
3. Route and crimp all terminals; slide labels to final position (within 50mm of connector body)
4. Shrink labels in place with heat gun
5. Build and route the harness, leaving all splices and connectors accessible
6. Slide sub-loom breakout PermaSleeve labels into position **before** Techflex sleeving goes on
7. Install Techflex sleeving and secure breakout boots
8. Run full bench continuity test (see next section)
9. Only after passing continuity: close connector shells, install sealing boots

### Complete label inventory — AS79 engine harness

Print this list before touching any wire. Source: `firewall-bulkhead.wv` — BULKHEAD_ENGINE_M52 pinlabels. 07K additions (Phase 3 plug) noted separately.

**Type A — Main harness wire labels** (Brady M21-125-C-342, ×2 per wire)

- **End 1 — AS79 end:** slide onto wire before crimping the AS79 contact; position within ~50mm of the connector body after insertion. This is what you read when tracing wires at the bulkhead.
- **End 2 — splice end:** slide onto wire before cutting to length; position within ~20mm of the bare wire tip. This label sits right at the splice point during Phase C so you can match each harness wire to the correct pigtail without tracing back to the AS79. It is at the tip of the wire, not at the sub-loom breakout (the sub-loom breakout has its own separate Type C label).

| Pin | Label text | Sub-loom | M52 | 07K |
|-----|-----------|---------|-----|-----|
| 1 | `1 +12V-COILS` | COILS | ✓ | ✓ |
| 2 | `2 +12V-COILS` | COILS | ✓ | ✓ |
| 3 | `3 ENG-GND` | COILS | ✓ | ✓ |
| 4 | `4 IGN1` | COILS | ✓ | ✓ |
| 5 | `5 IGN2` | COILS | ✓ | ✓ |
| 6 | `6 IGN3` | COILS | ✓ | ✓ |
| 7 | `7 IGN4` | COILS | ✓ | ✓ |
| 8 | `8 INJ1` | INJECTORS | ✓ | ✓ |
| 9 | `9 INJ2` | INJECTORS | ✓ | ✓ |
| 10 | `10 INJ3` | INJECTORS | ✓ | ✓ |
| 11 | `11 INJ4` | INJECTORS | ✓ | ✓ |
| 12 | `12 INJ5` | INJECTORS | ✓ | ✓ |
| 13 | `13 INJ6` | INJECTORS | ✓ (M52) | — (cavity-plug) |
| 14 | `14 INJ7` | INJECTORS | — (stub) | ✓ (07K 5th cyl) |
| 16 | `16 CRANK-VR+` | TRIGGER | ✓ | — (07K uses pin 41) |
| 17 | `17 CRANK-VR-` | TRIGGER | ✓ | — |
| 18 | `18 CRANK-SHLD` | TRIGGER | ✓ | ✓ |
| 19 | `19 CAM-HALL` | TRIGGER | ✓ (M52) | — (07K uses pin 20) |
| 20 | `20 CAM-07K` | TRIGGER | — (stub) | ✓ (07K cam) |
| 22 | `22 DBW-SIG` | SENSORS | — (stub) | ✓ (07K DBW TB signal) |
| 23 | `23 DBW-5V` | SENSORS | — (stub) | ✓ (07K DBW TB +5V) |
| 24 | `24 DBW-GND` | SENSORS | — (stub) | ✓ (07K DBW TB GND) |
| 25 | `25 CLT` | SENSORS | ✓ | ✓ |
| 26 | `26 IAT` | SENSORS | ✓ | ✓ |
| 27 | `27 FLEX-12V` | SENSORS | ✓ | ✓ |
| 29 | `29 +12V-COILS` | COILS | ✓ | ✓ |
| 30 | `30 +12V-COILS` | COILS | ✓ | ✓ |
| 31 | `31 ENG-GND` | COILS | ✓ | ✓ |
| 32 | `32 IGN5` | COILS | ✓ | ✓ |
| 33 | `33 IGN6` | COILS | ✓ (M52) | — (cavity-plug) |
| 34 | `34 IGN7` | COILS | — (stub) | ✓ (07K 5th cyl) |
| 35 | `35 VANOS` | ACTUATORS | ✓ (M52) | — |
| 36 | `36 ICV-A` | ACTUATORS | ✓ (M52) | — |
| 37 | `37 ICV-B` | ACTUATORS | ✓ (M52) | — |
| 38 | `38 STARTER` | ACTUATORS | ✓ | ✓ |
| 39 | `39 ALT-D+` | ACTUATORS | ✓ | ✓ |
| 41 | `41 CRANK-07K` | TRIGGER | — (stub) | ✓ (07K crank VR+) |
| 43 | `43 KNOCK1` | KNOCK | — (stub) | ✓ |
| 44 | `44 KNOCK2` | KNOCK | — (stub) | ✓ |
| 45 | `45 KNOCK-GND` | KNOCK | — (stub) | ✓ |
| 47 | `47 +5V-SENS` | SENSORS | ✓ | ✓ |
| 48 | `48 TPS` | SENSORS | ✓ | ✓ |
| 49 | `49 MAP` | SENSORS | ✓ | ✓ |
| 50 | `50 PST-F1-P` | SENSORS | ✓ | ✓ |
| 51 | `51 PST-F1-T` | SENSORS | ✓ | ✓ |
| 52 | `52 ENG-GND` | COILS | ✓ | ✓ |
| 56 | `56 ATF-TEMP` | SENSORS | optional | optional |
| 64 | `64 FLEX-SIG` | SENSORS | ✓ | ✓ |
| 79 | `79 SENS-GND` | SENSORS | ✓ | ✓ |

**Type A totals:** M52 Phase 1 plug — 37 wires × 2 = **74 labels**. 07K Phase 3 plug adds 13 wires (pins 14, 20, 22–24, 34, 41, 43–45 + 3 DBW) × 2 = **26 more labels → 100 total**.

---

**Type B — Pigtail connector labels** (Brady M21-125-C-342, ×1 per pigtail, applied near connector end before body snaps on)

| Label text | Connector type | Critical warning |
|-----------|---------------|-----------------|
| `INJ1` | EV14 2-pin | — |
| `INJ2` | EV14 2-pin | — |
| `INJ3` | EV14 2-pin | — |
| `INJ4` | EV14 2-pin | — |
| `INJ5` | EV14 2-pin | — |
| `INJ6` | EV14 2-pin | M52 only |
| `COL1` | M52: 2-pin pencil coil / 07K: 4B0973724 4-pin COP | — |
| `COL2` | Same | — |
| `COL3` | Same | — |
| `COL4` | Same | — |
| `COL5` | Same | — |
| `COL6` | M52 pencil coil only | M52 only |
| `CAM` | 3B0973703G (3-pin VAG) | ⚠️ Label before body snaps on — identical housing to CRANK |
| `CRANK` | 3B0973703G (3-pin VAG) | ⚠️ Label before body snaps on — identical housing to CAM |
| `CLT` | 1J0973702 (2-pin JPT) | — |
| `IAT` | 1J0973702 (2-pin JPT) | — |
| `MAP` | 3B0973703G (3-pin VAG) | — |
| `KS1` | 1J0973712 (2-pin flat) | 07K only |
| `KS2` | 1J0973712 (2-pin flat) | 07K only |

**Type B total:** M52 — 18 labels. 07K — 19 labels (adds KS1/KS2, swaps to COP pigtail format).

---

**Type C — Sub-loom breakout labels** (Brady M21-375-C-342 3/8" cartridge, ×1 per sub-loom, slides over bare sub-loom bundle before Techflex goes on)

| Label text | Sub-loom | Applies to |
|-----------|---------|-----------|
| `INJECTORS` | INJ 1–5/6 wires | M52 + 07K |
| `COILS` | IGN 1–5/6 + +12V rail wires | M52 + 07K |
| `TRIGGER` | Crank VR+/VR−/shield + Cam Hall | M52 + 07K |
| `SENSORS` | CLT, IAT, MAP, TPS, +5V, SENS-GND, PST-F1, Flex | M52 + 07K |
| `KNOCK` | KS1, KS2, KNOCK-GND | 07K only |
| `ACTUATORS` | VANOS, ICV-A, ICV-B, Starter, Alt-D+ | M52 (subset 07K) |

**Type C total:** 5 labels (M52), 6 labels (07K).

---

**Type D — Main trunk label** (Brady M21-500-C-342 1/2" cartridge, ×1, at AS79 exit from main trunk)

| Label text | When |
|-----------|------|
| `ENGINE M52 PH1` | M52 Phase 1 engine-side plug |
| `ENGINE 07K PH3` | 07K Phase 3 engine-side plug |

---

**Print queue summary:**

| Type | Cartridge | M52 count | 07K count |
|------|----------|----------|----------|
| A — wire labels | M21-125-C-342 | 74 | 100 total |
| B — pigtail labels | M21-125-C-342 | 18 | 19 |
| C — sub-loom breakout | M21-375-C-342 | 5 | 6 |
| D — main trunk | M21-500-C-342 | 1 | 1 |
| **Total** | | **98** | **126** |

Print all Type A and B labels before touching any wire. Print Type C and D labels before sleeving begins.

---

## Build Sequence

1. **Plan** — With the 07K engine on a stand in its intended orientation, dry-route a tape mock-up of the main trunk. Confirm routing path, bracket attachment points, and connector reach. Measure wire lengths per signal with 10% slack added. Record lengths against the `.wv` file before cutting anything.

2. **Bench build the main trunk** — Cut and label all wires (label sleeves on before cutting to length). Crimp AS79 engine-side contact onto each wire. Insert into the AS79 mating plug body one pin at a time, verifying pin identity against the `.wv` file at each insertion. Bundle wires loosely — **do not sleeve yet.**

3. **Route the engine-side loom** — Lay the harness along the engine with the AS79 mating plug at the firewall position and the wire ends at their intended destinations. Confirm lengths reach components with sufficient slack. Trim or add at this stage — not after sleeving.

4. **Splice pigtails** — At each branch point: cut the main harness wire to length, apply a PermaSleeve label to the wire end (signal name), apply a PermaSleeve label to the pigtail near its connector body (signal + cylinder), then join wire to pigtail with a Raychem SRGB solder sleeve or butt crimp. The pigtail connector body snaps onto the component.

5. **Continuity test** — With the harness fully wired but completely un-sleeved, verify every signal end-to-end with a DMM against the `.wv` file. Verify no shorts between adjacent pins. **Do not sleeve until this step passes.**

6. **Sleeve** — Main trunk first with 1/2" Techflex, sub-looms with 1/4" Techflex. Secure breakout transitions with 3:1 adhesive heat-shrink boots. Apply sub-loom PermaSleeve breakout labels before Techflex goes on each sub-loom.

7. **Mount and connect** — Secure the loom to the engine with P-clips. Connect all pigtail connectors. Photograph the complete installed harness before the hood goes on.

---

## Bench Test Before Install

Run each harness on the bench before it goes in the car. All checks are done with a multimeter — no car battery connected, no ECU powered.

### Multimeter setup

Set the dial to **continuity mode** (symbol: `)))` or a speaker/wave icon — the meter beeps when the circuit is closed). Continuity mode generates its own internal test signal (~0.5–1.5V, a few milliamps) — you are not applying battery voltage. The voltage and current range settings on the dial are for measuring live circuits and are not used for harness testing.

If your multimeter does not have a dedicated continuity mode, use **resistance (Ω) mode** at the 200Ω range. A good 22 AWG wire ≤2m reads <0.5Ω. Higher = partial break or bad crimp.

### Test procedure — four checks in order

**Check 1 — Continuity (every signal wire)**
1. Open the `.wv` file (`firewall-bulkhead.wv` for the engine harness)
2. For each populated pin: touch one probe to the AS79 cabin-side wire end (or the ECU C1/C2 connector pin), touch the other probe to the expected sensor pigtail pin at the far end
3. Beep (or <0.5Ω) = wire seated correctly and circuit complete
4. No beep = break — bad crimp, pin not fully seated, or wrong pin. Do NOT sleeve until resolved. Depin, inspect, re-crimp.
5. Work through every signal pin in the label inventory table above, in pin order — check them off on a printed copy of the label inventory

**Check 2 — Isolation (no shorts between adjacent pins)**
1. For each pair of adjacent signal pins (especially power pins adjacent to signal pins), touch one probe to pin A and the other to pin B
2. Should get **no** beep / open circuit (infinite Ω)
3. Any beep between adjacent signal pins = short — strands bridging inside the connector or a crimped terminal touching its neighbor. Find and fix before sleeving.
4. Critical pairs to test: every IGN pin against every adjacent INJ pin; every +12V pin against every SENS-GND pin; SENS-GND (pin 79) against chassis GND (they must NOT be shorted together — see Power & Ground Rules)

**Check 3 — Resistance (power and ground runs)**

| Wire type | Spec |
|-----------|------|
| 12–14 AWG power/GND wire, ≤2m | ≤0.1Ω |
| 22 AWG signal wire, ≤2m | ≤0.5Ω |
| Any wire | >2Ω = investigate (bad crimp or wrong gauge) |

Measure resistance end-to-end using resistance mode (200Ω range). Values above spec indicate a marginal crimp — rework before sleeving. A crimp that passes the pull-test but reads high resistance will cause voltage drop and intermittent sensor errors at temperature.

**Check 4 — Connector retention (pull-test)**
1. Grip each wire within 50mm of the connector body (not the wire far from the terminal — grip near the barrel)
2. Apply a firm hand tug toward the wire exit (~5 N, roughly 1.1 lb-force)
3. Any terminal that moves or pulls out = bad crimp or lance not engaged. Depin, inspect barrel for cut strands, re-crimp.

### Pass criteria

All four checks must pass before sleeving begins:

| Check | Pass | Action on fail |
|-------|------|---------------|
| Continuity | Beep on every signal wire end-to-end | Depin, inspect, re-crimp |
| Isolation | Open (no beep) between all adjacent pins | Find bridging strands or touching terminals, fix |
| Resistance | Within spec for each wire type | Re-crimp or replace wire |
| Pull-test | No terminal movement under hand tug | Depin, inspect, re-crimp |

**Only after all four checks pass → sleeve → route → install.**
