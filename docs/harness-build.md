# Harness Build Discipline

Reference for connector pinning, depinning, and harness assembly across all e36-wiring harnesses.

---

## Overview — Pin Count by Connector Family

| Connector | Family | Pins populated | Tool |
|-----------|--------|---------------|------|
| MaxxECU RACE C1 | Molex 48-pin | ~40 (varies by harness) | 63811-9200 (small) · 63811-8900/9000 (big) |
| MaxxECU RACE C2 | Molex 32-pin | 0 (Phase 1/3) — defer | Same as C1 |
| Deutsch AS firewall bulkhead | AS series, **size 22** | Up to 79 | Daniels M22520/2-01 (AFM8) + **K42** positioner (pin) / **K40** positioner (socket). Source: m-cal.com AS020-35SN; ecuplus.de AS620-35PN. |
| 07K cam sensor connector | 3B0973703G (3-pin VAG JMT) | 3 | Engineer PA-09 |
| 07K crank sensor connector | 3B0973703G (3-pin VAG JMT) | 3 | Engineer PA-09 |
| 07K MAP sensor connector | 3B0973703G (3-pin VAG JMT) | 3 | Engineer PA-09 |
| CLT sensor connector | 1J0973702 (2-pin NTC JPT) | 2 | Engineer PA-09 |
| IAT sensor connector | 1J0973702 (2-pin NTC JPT) | 2 | Engineer PA-09 |
| Knock sensor connector | 1J0973712 (2-pin flat) | 2 | Engineer PA-09 |
| EV14 injector connectors ×5 | USCAR EV14 | 2 each | Engineer PA-09 |
| M52 coil connectors ×6 | Pre-wired in MaxxECU M50 terminated harness — **not applicable to custom 07K harness build** | 2 each | n/a (pre-made) |
| 07K COP connectors ×5 | 4B0973724 (4-pin COP) | 4 each | Engineer PA-09 |
| EWP controller | Kostal 2+2 (4-pin) | 4 | Engineer PA-09 |
| PST-F1 sensor | Bosch Trapezoid 5-pin (`F02U.B00.751-01`) | 4 active (pin 1 unused) | Engineer PA-09 |
| ATF temp sensor | 2-pin spliced to C1 | 2 | Engineer PA-09 |
| 8HP CAN harness | GT150 12-pin pre-term. | n/a (pre-made) | n/a |
| DCT shifter | 4-wire — bare ends | 4 | Open-barrel (IWISS IWS-2820M) |

**Estimated total pin insertions: ~200–230.** Budget at least one full day per major harness
(engine harness, bulkhead, cabin loom) — rushing pin work is the primary cause of
hard-to-trace shorts and intermittent sensor faults.

### Direct termination — no pigtail splices

All sensor connectors in the engine harness (injector, COP coil, cam/crank/MAP 3-pin, CLT/IAT 2-pin, knock 2-pin) use **direct termination**: the build TXL wire runs end-to-end from the AS79 contact to the sensor connector terminal. There is no intermediate pigtail wire and no splice joint.

**Why:** Every splice is a potential failure point. Pigtail assemblies add one extra joint per connector — ~17 connectors across the engine harness. Direct termination eliminates those joints entirely. Source: Drive, Revive, Tinker harness build series ([youtube.com/watch?v=Z3hmNz64Gw8](https://www.youtube.com/watch?v=Z3hmNz64Gw8)) — "minimize joints = minimize failure points."

**What to buy:** Connector housings + individual terminals only. Preferred sources: ProWire USA, Del City, Waytek, ECS Tuning, or FCP Euro. For OEM part numbers (e.g. `3B0973703G`, `4B0973724`, EV14 USCAR kits), Amazon is acceptable when the listing is clearly an OEM or named-brand part with reviews confirming authenticity — not for generic unbranded terminals. Do not buy pre-made pigtail assemblies (housing + pre-wired stub) regardless of source. See `walkthroughs/26-07k-harness.md` Parts section for connector families and OE part numbers.

**When a splice is unavoidable:** Sensors that ship with an integral moulded pigtail (wire bonded to sensor body, no removable connector housing) require one splice to join the sensor's pigtail wire to the build harness. Use a Raychem SRGB heat-activated solder sleeve — heat gun only, not iron. A soldering iron creates a rigid joint at the flex point that cracks under vibration.

**Deutsch connectors and sensor pigtails:** This build already uses Deutsch Autosport AS series (AS79 firewall bulkhead) and Deutsch DT 2-pin (high-current bypass connectors for fan/EWP/AC relay). Those are correct applications. Deutsch DT or DTM connectors are **not** suitable as sensor pigtail connectors — they do not mate with OEM sensor bodies (VW 3B0973703G, 1J0973702, USCAR EV14, VAG 4-pin COP). Swapping to Deutsch at the sensor end would require an adapter that adds a connector interface back in. Use the OEM connector housings + terminals and direct-terminate into those.

---

## Tools — Which Tool for Which Connector

| Tool | PN | Connector families |
|------|----|--------------------|
| Molex ratcheting crimper (small terminals) | 63811-9200 | MaxxECU C1/C2 small-gauge pins |
| Molex ratcheting crimper (big 0.5–1.0 mm²) | 63811-8900 | MaxxECU C1/C2 large-gauge pins |
| Molex ratcheting crimper (big 1–2 mm²) | 63811-9000 | MaxxECU C1/C2 large-gauge pins |
| **Micro-pin crimper — VAG JMT/JPT pigtails** | **Engineer PA-09** (~$30–40, Amazon) — community standard for Bosch JMT 1.5mm and JPT 2.8mm contacts. Covers VAG cam/crank/MAP/CLT/IAT/knock/COP pigtail terminals in one tool. Budget: IWISS SN-2549 (~$17). ⚠️ `Knipex 97 52 68` (previously listed here) does not exist — that PN is not in the Knipex catalog. The Knipex 97 52 67 DT (~$427) is for Deutsch DT contacts only, not for Bosch JMT/JPT. | All VAG sensor pigtails, COP, EV14 injector connectors |
| **Deutsch HD30 / DT contacts crimper** | **Deutsch HDT-48-00** (~$350–465) or **JRready NEW-DT2** (~$169 budget) | Maven HD30 35-pin connector (size-16 and size-20) + DT 2-pin bypass connectors |
| **AS solid barrel crimper** | Daniels M22520/2-01 (**AFM8**) handle — $601.65 ([dmctools.com](https://dmctools.com/afm8)) | **Firewall bulkhead Deutsch AS size-22 solid barrel contacts.** Mil-spec tool for AS contacts — NOT the HDT-48-00 or clones (DT/DTM/DTP only, different contact geometry). No cheap substitute — wrong die geometry produces cold crimps that pass pull-test but fail under vibration. Source: m-cal.com AS020-35SN "Primary Contacts Size: 22 AWG"; ecuplus.de AS620-35PN "79x 22 AWG". |
| AS crimper positioner — pin | Daniels **K42** (M22520/2-09) — $112.64 ([deltaintl.com](https://deltaintl.com/products/k42)) | Size-22 **pin** contacts (38941-22), 22–26 AWG. Use with AFM8 frame for all AS79 pin crimps (engine-side plug). NOT K43 — that is for size-20 contacts. |
| AS crimper positioner — socket | Daniels **K40** (M22520/2-07) — $93.86 ([dmctools.com](https://dmctools.com/k40)) | Size-22 **socket** contacts (38943-22), 22–26 AWG. Use with AFM8 frame for all AS79 socket crimps (cabin-side receptacle). |
| Open-barrel crimper | IWISS IWS-2820M | Ring terminals, relay contacts, general non-insulated open-barrel splices. Use non-insulated + adhesive-lined heat shrink — never pre-insulated crimps. |
| Ferrule crimper | **iCrimp AWG23-10** (HSC8 6-4A, ~$25 — [amazon.com/dp/B00XVB6B1C](https://www.amazon.com/dp/B00XVB6B1C)) — self-adjusting ratchet, 0.25–6mm² (AWG 23–10) | Screw-clamp terminals (ECU power/GND strands) |
| Wire stripper | **Ideal Stripmaster 45-097** (~$60–90, [Amazon](https://www.amazon.com/dp/B000RFSWF8)) with included **L4994 blades** (16–26 AWG) — community standard for motorsport harness work (HPA, StreetCarJoe, Rywire). Fixed-notch blades sized so the 22 AWG hole (0.039") stops physically before reaching the conductor — works correctly on TXL and GXL. | Primary gauge is 22 AWG TXL. Do NOT use auto-adjusting or general-purpose electrician strippers on 22 AWG TXL — thin insulation wall means wrong-geometry blades nick strands even with careful technique. |
| Flush cutters | Milwaukee 48-22-6106 or equiv | In-car wire trimming, flush cuts near connector bodies. Buy before starting any connector work. Source: StreetCarJoe Race Car Wiring Pt.1. |
| Rivnut tool | Astro Pneumatic 1442 or equiv manual tool | M4/M6 rivnuts for PMU16 bracket and ECU bracket mounting to thin sheetmetal / carbon panels (no backside access needed). Source: StreetCarJoe Race Car Wiring Pt.3. |
| **Depin — Molex small terminals** | 638132400 | C1/C2 small-pin extraction |
| **Depin — Molex big terminals** | 638132300 | C1/C2 large-pin extraction |
| **Depin — VW/Bosch PTS connectors** | Lisle 57750 | All VAG push-to-seat pigtails (sensor, COP, injector) |
| **Depin — Deutsch AS size 22** | Tool included with AS79 connector body (or M81969/14-01 equiv) — ⚠️ `0411-240-2005` is DT/DTM size-16/20 only, does not fit AS79 size-22 solid barrel contacts | Firewall bulkhead contacts only |

> ⚠️ **Depin tool matters:** Lisle 57750 works on push-to-seat (PTS) bodies only.
> Do NOT use it on pull-to-seat (PTLS) or Molex contacts — different locking geometry.
> Wrong pick damages the connector body and the terminal retention lance.

---

## Wire Color Convention

Wire colors in this build are a consistent, intentional scheme. They do **not** follow SAE J1128 consumer-automotive conventions or any single OEM scheme — they follow the motorsport/standalone-ECU convention used by HPA, StreetCarJoe, Rywire, and others for aftermarket ECU installs. Every color meaning below is verified against the actual `.wv` source files.

> **Source-of-truth priority for color decisions:** (1) MaxxECU RACE wiring diagram PDF, (2) Ecumaster PMU16 manual, (3) internal `.wv` files, (4) other references (Rob Dahm, HPA, etc.). Both manufacturer documents have been archived locally — see `docs/vendor/`. **Ecumaster publishes no wire color convention for the PMU16** (pin functions and current ratings only). The MaxxECU RACE REV9+ wiring diagram does publish colors for their pre-made harnesses; where this build diverges, the divergence is documented in the cross-reference table below.

### Definitive color table for this build

Source: `docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf` — aligned where possible. See cross-reference below for the two intentional divergences.

| Color | Code | Circuit types | Example runs |
|-------|------|--------------|--------------|
| **Red** | RD | +12V power — all rails; +5V sensor supply | ECU power, coil/inj rail, +5V to sensors, fuel pump supply, PMU16 outputs, WBO2 heater+, relay supply wires, battery+ |
| **Black** | BK | **Power / chassis GND only — not sensor GND** | Engine GND, chassis GND, battery −, coil power return, ICV coil return, WBO2 heater−, relay coil return, fuel pump GND |
| **Brown** | BN | **Sensor GND**; VR trigger return (Signal−); switch / paddle GND | All sensor GND runs to MaxxECU Sensor GND pins (CLT, IAT, TPS, MAP, CAM, PST-F1, APS, ATF temp, clutch pos); crank VR− wire; DCT shifter paddle GND |
| **White** | WH | Analog sensor signals; CAN H (in WH/BU twisted pair) | CLT, IAT, TPS1/TPS2, crank VR+, cam Hall, knock signal, WBO2 signals, APS1/APS2, ATF temp, flex fuel signal, clutch position; CAM/HOME trigger |
| **White + Blue** | WH/BU | CAN bus twisted pair — **WH = CAN H, BU = CAN L** | MaxxECU CAN1 ↔ 8HP TCU, MaxxECU CAN1 ↔ Gauge.S — every CAN trunk run in the build |
| **Blue** | BU | **Ignition coil drive outputs** | IGN 1–6 (MaxxECU IGN outputs to COP/pencil coil signal pin); also CAN L conductor in WH/BU twisted pair |
| **Grey** | GY | **Injector drive outputs**; PMU16 CAN2 H | INJ 1–6 (MaxxECU INJ outputs to injector signal pin); PMU16 CAN2 H conductor (in GY/VT pair) |
| **Green** | GN | GPO outputs — actuator / relay / solenoid drives | Fan relay GPO; fuel pump relay GPO; VANOS solenoid; boost solenoid; ICV coil drives (GPO 4/5); VVT solenoid N205 |
| **Yellow** | YE | **Shield GND drain wire** | Crank VR shield drain; cam sensor shield drain (m52); knock sensor shield drain; all shielded cable drain wires |
| **Orange** | OG | H-bridge motor drive + | DBW throttle body motor+ (MaxxECU C2 H4 MOTOR 1+) |
| **Violet** | VT | H-bridge motor drive −; PWM control signals | DBW throttle body motor−; EWP (CWA400) PWM signal; AC compressor enable; PMU16 CAN2 L conductor (in GY/VT pair) |
| **Grey + Violet** | GY/VT | PMU16 CAN2 twisted pair (GY = H, VT = L) | PMU16 CAN2 H/L → MaxxECU CAN1 H/L — separate from the main WH/BU CAN trunk |
| **Pink** | PK | Serial control link | EPS column CTRL_LINK (one conductor of 2-wire EPS serial bus) |

### Cross-reference — where this build diverges from other sources

#### MaxxECU RACE REV9+ wiring diagram (archived: `docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf`)

MaxxECU's official RACE wiring diagram specifies the following colors for their pre-terminated harnesses. The `.wv` files have been updated to align where practical; two divergences remain intentional.

| Signal type | MaxxECU RACE official | **This build** | Status |
|-------------|----------------------|---------------|--------|
| +12V power rails | Red | **Red** | ✓ Aligned |
| Sensor GND | **Brown** | **Brown** | ✓ Aligned |
| CAM / HOME trigger signal | White | **White** | ✓ Aligned |
| Shield GND drain wire | Yellow | **Yellow** | ✓ Aligned |
| Ignition coil drives (IGN 1–6) | **Blue** | **Blue** | ✓ Aligned |
| Injector drives (INJ 1–6) | **Grey** | **Grey** | ✓ Aligned |
| GPO outputs (GP OUT 2–8) | **Green** | **Green** | ✓ Aligned |
| Analog sensor signals (TPS, CLT, IAT, AIN) | **Black** | **White** | ✗ Diverges — Black-for-signal conflicts with the universal Black = ground safety convention. White is retained for technician legibility. |
| CAN H / CAN L | Grey / Pink | **White / Blue** | ✗ Diverges — WH=H / BU=L is the industry-standard aftermarket CAN convention (Motec, Haltech, AEM, etc.) and is more widely understood than MaxxECU's grey/pink. Retained for compatibility with other CAN devices on the bus. |

**Two remaining mismatches:** sensor signal color (White vs MaxxECU's Black) and CAN bus colors (WH/BU vs MaxxECU's GY/PK). All other MaxxECU RACE color assignments are now reflected in the `.wv` files. If you ever splice a MaxxECU pre-terminated pigtail into this loom, the signal wire colors will differ — MaxxECU's signal wires are Black; this build's are White.

#### Rob Dahm — *"Building a race car harness from scratch"* ([YouTube](https://www.youtube.com/watch?v=EA-oVJCnjZM))

Rob Dahm's convention on his four-rotor build (Haltech + Ecumaster PDM):

| Signal type | Rob Dahm | **This build** | Notes |
|-------------|----------|---------------|-------|
| Sensor signals | White | **White** ✓ | Agree |
| Power (+12V, 5V ref) | Red | **Red** ✓ | Agree |
| Ignition coil drives | **Yellow** | **Blue** | Rob uses Yellow for coil drives; this build uses Blue (aligned with MaxxECU RACE convention) |
| Injector drives | **Blue** | **Grey** | Rob uses Blue for injectors; this build uses Grey (aligned with MaxxECU RACE convention) |
| Actuator GPOs | Green | **Green** ✓ | Agree (broadly) |

Neither convention is wrong — the critical requirement is **internal consistency**. Do not mix the two schemes within this build.

#### SAE J1128 — general North American automotive convention

SAE J1128 specifies wire insulation materials and temperature ratings; it does not mandate specific colors for specific functions. The general consumer-automotive convention (often cited alongside J1128) diverges significantly in a motorsport context:

| Color | SAE/OEM automotive typical use | **This build** | Why different |
|-------|-------------------------------|---------------|---------------|
| Yellow | Constant battery power / keep-alive / airbag SRS | Secondary analog signals | Motorsport builds rarely route constant-battery keep-alive lines; Yellow freed for signal use |
| Green | Exterior lighting circuits | GPO outputs, actuator drives | OEM lighting convention irrelevant in a custom standalone ECU harness |
| White | Speaker / audio signals (consumer electronics) | Analog sensor signals | Sensor-signal convention is universal in standalone ECU community (HPA, StreetCarJoe, Rywire) |
| Blue | Antenna / amplifier remote turn-on | CAN L, digital inputs | CAN bus convention overrides OEM antenna use in ECU harness context |
| Orange | Interior illumination / dimmer | DBW motor+ (H-bridge) | OEM dimmer convention irrelevant here |

> **Practical note:** If you ever hand this harness to an OEM-trained technician unfamiliar with standalone ECU conventions, the Grey-for-ignition and Green-for-injector assignments will be the biggest source of confusion. Label sub-looms with PermaSleeve heat-shrink labels (`IGNITION`, `INJECTORS`) at the main trunk breakouts so function is readable without tracing wire color.

#### HPA — motorsport harness courses

High Performance Academy does not prescribe a mandatory color standard in their harness courses. One specific note from their course material: **Violet is used for filler wires** in concentric twist layer design (wires added to complete a layer with no electrical function). This build **diverges**: violet is used here for functional circuits (DBW motor−, EWP PWM, AC enable, PMU16 CAN2). If concentric twist is ever adopted for a trunk segment in this build, choose a different color for filler wires — suggest Pink (PK) or Turquoise (TQ), which are otherwise unused in this harness.

### Sensor GND vs. power GND — distinct colors (BN vs BK)

Sensor GND and power GND use **different wire colors**:

- **Power GND (BK — Black):** High-current return path. Terminates at engine block M8 GND stud or chassis stud. Carries coil power return, ICV coil return, WBO2 heater−, relay return currents. Never connects to MaxxECU Sensor GND pins.
- **Sensor GND (BN — Brown):** Low-current, noise-sensitive return. Terminates at MaxxECU dedicated Sensor GND pins only — never share with power GND on the ECU connector. See `maxxecu-m52.wv` / `maxxecu-07k.wv` for which ECU pins are Sensor GND.

The color difference enforces correct routing — a Brown wire on a chassis GND lug or a Black wire at a MaxxECU Sensor GND pin is visually wrong and catchable at bench continuity check. No label gymnastics required; the colors tell the story.

### Sensor GND trunk topology — star, not shared bus

Each sensor gets its own individual Brown (BN) Sensor GND wire in its branch cable. Those individual wires **run separately through the trunk** all the way to the ECU's Sensor GND pin. They do not splice together mid-loom.

**Why — common-impedance coupling:**
If multiple sensor GND wires share a common return conductor in the trunk, each sensor's return current flows through that shared impedance before reaching the ECU reference. The resulting voltage drop appears as a ground-offset error on every other sensor sharing the wire:

```
V_error = I_other_sensor × R_shared_trunk
```

For slow NTC sensors (CLT, IAT) this error is negligible. For the knock sensors, crank VR, or wideband O2 — all high-frequency or precision signals — shared ground return impedance injects measurable noise into the reference.

**How the `.wv` model reflects this:**
Each sensor cable has its own BN wire (e.g., `W_CLT`, `W_IAT`, `W_TPS`, `W_CAM` all have a discrete BN "Sensor GND" wire). In the `connections:` blocks, all of them individually target `ECU_CMC: [29]` (H1 — Sensor GND) or `ECU_16PIN: [2]` (aux Sensor GND). This models star topology: each return path is independent from sensor to ECU. No trunk-level splice node is modeled.

**Physical implementation note:**
The MaxxECU CMC connector has one physical Sensor GND pin (H1 = pin 29) and one dedicated GND Shield pin (E3 = pin 19). These are two separate ground buses — do not commingle them.

- **BN sensor GND wires** (CLT, IAT, TPS, MAP, CAM signal return, knock shield drain via pin 45) → all terminate at CMC H1 (pin 29)
- **YE shield drain wires** (crank, cam, WBO2 shields) → all terminate at CMC E3 (pin 19) — the dedicated shield ground, isolated from the sensor GND bus

Mixing crank/cam shield drains into the H1 sensor GND bus injects switching noise from other sensor return currents into the VR trigger signal path, which can cause crank dropout at high RPM.

**Physical implementation note for the H1 group:** The MaxxECU CMC has one physical H1 pin (29). All the individual BN sensor GND wires need to join somewhere before that pin. The correct approach:

- Run individual BN wires separately through the trunk bundle (they are separate conductors, just co-routed)
- Join them at a short Raychem or solder-and-shrink splice **within 150 mm of the ECU connector** (AS79 bulkhead cavity or ECU connector area)
- A single short stub then runs to CMC pin 29

The shared segment is at most 150 mm — negligible impedance. The long trunk runs remain independent. This is the same approach used in MaxxECU's own pre-terminated RACE harnesses (source: `docs/vendor/maxxecu/MaxxECU_RACE_REV9plus_Wiring.pdf`, sensor GND routing).

> ⚠️ **Never** splice all sensor GNDs together mid-loom at a Sector 1/Sector 2 branch point and run a single BN wire to the ECU. That creates the shared-impedance problem across the longest and noisiest part of the run.

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

**Deutsch AS size 22 — use the insertion/extraction tool included with the AS79 connector** (or M81969/14-01 equivalent):
1. Insert extraction tool into the front face of the bulkhead
2. Tool depresses the collet; pull wire from rear while holding tool engaged
3. Contact exits from the rear

> ⚠️ The Deutsch `0411-240-2005` is a DT/DTM series tool for size-16/20 contacts — it does **not** fit AS79 size-22 solid barrel contacts. Use only the tool that ships with the AS79 connector body.

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

### Ground Contact Surfaces — No Paint, No Coating, No Oxide

Every ground lug attachment point must be **bare, clean metal** — not painted, powder-coated, anodised, or corroded. This applies to:

| Location | Notes |
|----------|-------|
| Engine block → chassis bonding strap lug | Wire-brush or sand to bare metal before reinstalling lug; add a star washer |
| Cylinder head → MaxxECU engine GND wire | Clean the bolt boss on the head; use a star washer |
| Chassis GND stud (engine bay M8) | Strip the mounting point if inside a painted engine bay |
| **07K knock sensor mounting boss** | **Critical.** The Bosch flat knock sensors (passive piezoelectric) ground through their M8 mounting bolt and the sensor face-to-block contact. Any paint, sealer, or coating at the mounting pad adds resistance in the signal return path and degrades knock detection sensitivity. Wire-brush or lightly sand the sensor mounting area on the block to bare aluminium before torquing the sensor. Re-apply corrosion protection (thin wipe of anti-seize) only to the threads, not the sensor face contact area. |

> Source: Drive, Revive, Tinker harness build and lessons-learned videos ([youtube.com/watch?v=Z3hmNz64Gw8](https://www.youtube.com/watch?v=Z3hmNz64Gw8)); HP Academy EFI Wiring Fundamentals.

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

### Tier 3 — Sensor connectors (direct termination)

At the end of each sub-loom, individual wires branch to the component connector. This build uses **direct termination**: the harness wire runs end-to-end from the AS79 contact to the sensor connector terminal. There is no intermediate pigtail wire and no splice joint at the sensor end.

**What to buy and how:** Purchase connector housings + individual terminals for each sensor connector family (EV14 injector, 4B0973724 COP coil, 3B0973703G 3-pin sensor, 1J0973702 2-pin NTC, 1J0973712 knock). Crimp a terminal directly onto the harness wire using the Engineer PA-09, then insert the terminal into the connector housing until the locking lance clicks. See the connector table at the top of this document for part numbers and the `26-07k-harness.md` Parts section for OE part numbers and sources.

### Wires per component — injectors and coils are not 1 wire each

Every component has multiple wires. The EV14 injector connector has 2 pins and requires 2 wires from the harness:

| EV14 pin | Wire | Source |
|----------|------|--------|
| Pin 1 | +12V switched | Shared coils/inj power rail (tapped via Raychem splice from the bus wire running along the injector rail) |
| Pin 2 | INJ-N signal | Individual wire from AS79 pin 8–13 — unique to each injector |

The shared +12V bus runs as one continuous wire the full length of the injector rail. At each injector, a Raychem sleeve taps it: one wire in from the upstream bus, one stub out to EV14 pin 1, one wire out continuing the bus downstream. The INJ signal wire (unique per injector) runs **directly** from the AS79 contact (pin 8–12) to EV14 pin 2 — no splice, no pigtail.

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
- Twisting the whole bundle as a unit makes it rigid and adds length, making it difficult to branch individual wires at different component positions along the sub-loom
- The Techflex expandable braid holds the bundle together and provides abrasion resistance without any twisting underneath
- For the breakout transition from main trunk to sub-loom, a few wraps of Tesa 51036 fabric tape (or similar) under the Techflex consolidates the bundle at the branch point — optional but keeps things clean

#### Concentric twist — real technique, not applicable here

**Concentric stranding** (also called concentric twist or helical layering) is a distinct technique from bulk-twisting the bundle as a unit. Wires are arranged in concentric layers, each layer wound helically in the opposite direction to the one inside it. The geometry forces specific wire counts per layer:

| Layers | Total wire count |
|--------|-----------------|
| Core only | 1 |
| Core + 1st layer | 7 (1 + 6) |
| Core + 2 layers | 19 (1 + 6 + 12) |
| Core + 3 layers | 37 (1 + 6 + 12 + 18) |

**Real advantages** (from professional harness practice, confirmed by [High Performance Academy — "You Don't Need 'PRO' Level Wiring....Do You?"](https://www.youtube.com/watch?v=K12VFuqbeD4)):
- Maintains flexibility along the harness run — opposite-direction layers allow the bundle to bend without individual wires buckling or kinking
- Smaller bundle OD than loosely parallel wires — mathematically optimal round-wire packing reduces diameter under the Techflex
- **Thicker wires belong in the center.** High-gauge power and ground wires at the core provide a rigid center spine; lighter sensor wires in the outer layers are also the ones most likely to exit early along the route — natural organization

**Why it is not used here:**
- The wire counts in this harness's sub-looms do not match the valid fill numbers (7, 19, 37). An incomplete outer layer creates an uneven bundle OD and loses the flexibility and compactness advantages — you get the labor cost with none of the benefit.
- Sub-loom wires branch to individual components at multiple points along the run. In a concentrically stranded bundle, a wire buried in the center layer must cross through all outer layers to exit — this creates a messy, difficult-to-execute breakout at every branch point.
- The Techflex F6 sleeve provides adequate shape retention and abrasion protection over a parallel bundle without any stranding complexity underneath.

Concentric stranding is worth considering for a long fixed-count trunk that terminates at a single connector with no intermediate branches — but that geometry does not exist in this build.

**The one exception is the crank VR pair.** The VR+ and VR− wires **must be twisted together** before going into the TRIGGER sub-loom:
- Twist rate: ~1 twist per 25mm (1 twist per inch) — twist by hand from tip to tip before routing
- **Twist direction: does not matter.** The noise-cancellation physics work identically with clockwise or counterclockwise lay — both wires still intercept the same magnetic field simultaneously. Twist whichever way feels natural.
- The only case where twist direction matters: if two twisted pairs run inside the same sleeve side-by-side, twist them in opposite directions to minimize inductive coupling between pairs. In the TRIGGER sub-loom the crank pair is the only twisted pair, so this is not relevant here.
- The twist causes both wires to intercept identical electromagnetic interference simultaneously; the ECU's differential input subtracts the common-mode noise, leaving only the real crank signal
- Laying them parallel instead of twisted degrades trigger signal quality and can cause dropout at high RPM under electrical load
- After twisting, both wires run inside the TRIGGER sub-loom sleeve alongside the shield drain wire — do not separate them at any point in the routing

The CAM Hall signal wire does not need twisting — it is a single-ended digital output with its own dedicated +5V and GND, not a differential pair.

### Branch points — technique and strain relief

Source: HPA — *"It's So Easy To Get This Wrong | Wiring Harness Branching"* ([YouTube](https://www.youtube.com/watch?v=XBnADm1SHoI))

Branch points (breakouts from main trunk to sub-loom) are the most structurally complex sections of the harness. Nothing about the finished result is as tidy as a uniform trunk run — and that is expected and normal. The only thing that matters at a branch is **zero strain on every wire**.

#### Zero tension is the only success criterion

Every wire must arrive at its exit direction without being pulled. If a wire needs to travel from one side of the trunk to exit the opposite side, let it loop or cross — that crossing will be hidden inside the Kapton wrap and boot. A wire under tension at the branch point will work loose or crack at the insulation over vibration cycles regardless of how well the boot looks on the outside.

#### Pre-design exit order before you touch the harness

Before any wires are moved, decide which branch section exits in which direction and in what radial order around the trunk. The goal: no branch section should have to cross another after the boot is shrunk. This is a planning step from the `.wv` diagram and loom routing plan — if the routing hasn't been designed to avoid cross-overs at the branch, fix the routing plan first.

#### Build sequence at each branch point

1. Loosely gather the wires into their branch groups using temporary cable ties a few inches down each branch. Keep the cable ties well clear of where the Kapton will go — they will need to come off before taping.
2. Arrange the branch groups in their designed exit order. Wires may twist across the trunk face to reach their direction — this is fine.
3. Wrap the entire bare junction with **Kapton tape** in a confined area, covering all wires completely. Kapton serves two purposes:
   - **Strain relief** — locks the exit angles in place; nothing moves once wrapped
   - **Adhesive barrier** — the 3:1 adhesive-lined shrink boot that goes over this point contains hot-melt adhesive on the inside. If bare wire insulation contacts that adhesive when the boot is recovered, the wires bond permanently to the boot. Future repair requires cutting the boot off and possibly damaging the wires. Kapton prevents contact.
4. **Keep the Kapton within the boot's working zone.** Each molded shrinkable boot has a maximum recovered length specified in its datasheet. The Kapton-wrapped area must fit inside that length — measure the boot before wrapping, not after.
5. After Kapton, sleeve each branch section in Techflex to its end. Then recover the molded boot over the junction.

#### Between branch points — uniform construction throughout

The harness section between any two branch points must not change: same wire count, same parallel layout, same sleeve diameter all the way through. All changes happen at branch points, not mid-run. If a wire gauge or routing needs to change, place a new branch point there.

#### Bench wire prep — cut to longest run, trim down

Source: Rob Dahm — *"Building a race car harness from scratch"* ([YouTube](https://www.youtube.com/watch?v=EA-oVJCnjZM))

When preparing wires for a harness section, cut all wires to the length of the **longest run in that section**, then trim individual wires to their final length after routing and checking position on the engine. Measuring and cutting each wire individually before routing wastes far more time than the small amount of wire lost by trimming. Do this before any crimping — once a terminal is on, the wire cannot be shortened without re-crimping.

### Harness finishing methods — Techflex vs. lacing vs. individual sheaths

What you see in high-end motorsport harness photos is not always the same as Techflex F6:

| Method | What it is | Used where | DIY suitability |
|--------|-----------|-----------|----------------|
| **Techflex F6 expandable braid** | Woven nylon braid that slides over the bundle; this build's standard | Street, club motorsport, OEM-style custom harnesses | High — fast, clean, adequate protection |
| **Mil-spec waxed lacing** | Waxed nylon cord wound in tight spiral or cross-stitch directly around the wire bundle — no outer sleeve | Aerospace, Formula 1, professional race shops | Low — hours per sub-loom, specialized technique |
| **Individually sheathed wires** | Each wire gets its own expandable cloth braid or PTFE sleeve before going into the outer loom | Ultra-high-end show/motorsport builds | Low — significant per-wire cost and added diameter that makes contact insertion harder |
| **Hand-braided bundles** | Wires braided together like hair braiding — structural, distributes strain across the bundle | Formula 1 territory only | Not applicable |

For this build, Techflex F6 + P-clips + heat-shrink boots at breakouts is correct. The mil-spec lacing look is genuine craftsmanship (not pure aesthetics), but the labor cost — easily 20+ additional hours for an engine harness — is not justified on a street/drift E36. The electrical performance difference comes from the twisted crank pair, shield grounding, and Sensor GND isolation — not from the sleeving method.

### Service loops at connectors

A service loop is a small coil of extra wire (1–2 turns, ~30–50mm diameter) left between the sub-loom Techflex end and the connector entry, captured inside the heat-shrink boot when shrunk. Invisible from outside. Worth the extra minute per connector.

**Why:** The crimp terminal is designed to carry current, not cyclic mechanical load. Without a loop, vibration and thermal expansion load pull directly on the terminal. The loop intercepts that motion before it reaches the crimp. A service loop also provides material for re-termination if a terminal ever needs rework — without one, re-crimping requires splicing in new wire.

**Where to apply in this harness:**

| Connector | Method | Rationale |
|-----------|--------|-----------|
| AS79 engine-side mating plug | No individual loops — leave 200–300mm of harness slack near the connector exit, route with a gentle curve before the first P-clip | ~45 active wires (07K Phase 3 — only mating plug built; Phase 1 uses OEM grommet, no AS79 mating plug) through a 79-pin shell; individual loops inside the backshell are not practical at that density. Bundle-level slack provides the same function |
| Maven HD30 35-pin accessories | ✓ Individual loop per wire + intermediate heat-shrink wrap over bundle before boot | 35 wires. Loop each wire, wrap the coiled bundle in 3:1 adhesive heat-shrink before sliding the boot on — holds loops organized and gives the boot a clean round profile to seat against |
| Crank VR+/VR− connector end | ✓ Individual loop, 1–2 turns | Most vibration-sensitive signal; crank sensor at front of block sees belt-drive vibration |
| CAM sensor connector end | ✓ Individual loop, 1–2 turns | Same rationale |
| MaxxECU C1/C2 | ✓ Individual loop per wire + intermediate heat-shrink wrap over bundle before backshell | Molex backshell has enough internal volume; intermediate wrap holds loops organized during backshell installation. Loop protects terminals during ECU removal/reinstall |
| EV14 injector pigtails | No | The ~50mm bare wire between sub-loom exit and connector already provides compliant slack |
| CLT / IAT / MAP connectors | Optional | Same — bare wire section is usually sufficient |

**No special tool required.** For 22 AWG TXL, coil the wire by hand around a Sharpie body (~13mm diameter) or your index finger (~18mm). One or two turns is all you need. TXL wire holds the loop shape without tape at this gauge.

**Exact sequence — critical order:**

1. **Slide the heat-shrink boot onto the wire before any terminal work** — the boot cannot pass over a terminated connector body after the fact. Do this at the same time as PermaSleeve label sleeves.
2. Crimp contacts onto the harness wire ends
3. Insert contacts into connector body — verify seating click on each
4. Coil 1–2 turns per wire around a Sharpie body or finger — wire holds shape on its own
5. **For multi-wire connectors (Maven 35-pin, MaxxECU C1/C2): wrap the entire coiled bundle in a single piece of 3:1 adhesive-lined heat-shrink and shrink it** — locks all loops in their organized shape and gives the boot a clean round profile to seat against. Skip for single/dual-wire sensor connectors (crank, cam).
6. Slide the boot forward to cover the connector body exit AND the wrapped loops
7. Shrink the boot with a heat gun — loops permanently captured inside
8. The connector is complete. **Plug into the component sensor last** — after the boot is fully shrunk.

The finished result looks identical to a boot with no loop. The loop is visible only during build, before the boot is shrunk.

### Splice types — no iron soldering

Splices are only needed for sensors that ship with an integral moulded pigtail (wire bonded to sensor body — e.g., a donor WBO2 sensor). All other sensor connectors use direct termination (no splice). Where a splice is unavoidable, two acceptable methods:

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
| Wire — sensor connector end (before body snaps on) | Signal + cylinder number (e.g., `INJ1`, `COL3`, `CAM`, `CRANK`) | Same |
| Wire — AS79 terminal end (within 50mm of connector body) | AS79 pin number + signal name (e.g., `8 INJ1`) | Same |
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
- **End 2 — sensor connector end:** slide onto wire before cutting to length; position within ~50mm of the terminal/connector end. This label sits right at the sensor connector during build so you can confirm the signal identity without tracing back to the AS79. It is at the connector end of the wire, not at the sub-loom breakout (the sub-loom breakout has its own separate Type C label).

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
| 16 | `16 CRANK-SIG` | TRIGGER | ✓ (VR+) | ✓ (Hall signal — same ECU pin CMC H3) |
| 17 | `17 CRANK-P2` | TRIGGER | ✓ (VR−→CMC H2) | ✓ (+5V→CMC G1; **cabin re-terminate at swap**) |
| 18 | `18 CRANK-P3` | TRIGGER | ✓ (shield→CMC E3) | ✓ (SensorGND→CMC H1; **cabin re-terminate at swap**) |
| 19 | `19 CAM-HALL` | TRIGGER | ✓ | ✓ (same pin both phases; connector body changes) |
| 22 | `22 MOTOR+` | SENSORS | — (07K only) | ✓ |
| 23 | `23 MOTOR-` | SENSORS | — (07K only) | ✓ |
| 25 | `25 CLT` | SENSORS | ✓ | ✓ |
| 26 | `26 IAT` | SENSORS | ✓ | ✓ |
| 27 | `27 FLEX-12V` | SENSORS | ✓ | ✓ |
| 29 | `29 +12V-COILS` | COILS | ✓ | ✓ |
| 30 | `30 +12V-COILS` | COILS | ✓ | ✓ |
| 31 | `31 ENG-GND` | COILS | ✓ | ✓ |
| 32 | `32 IGN5` | COILS | ✓ | ✓ |
| 33 | `33 IGN6` | COILS | ✓ (M52) | — (cavity-plug) |
| 34 | — cavity-plug — | COILS | — (cavity-plug) | — (cavity-plug; IGN 5 = pin 32) |
| 35 | `35 VANOS` / `35 VVT-SOL` | ACTUATORS | ✓ (M52: VANOS) | ✓ (07K: VVT solenoid — same pin, relabel) |
| 36 | `36 ICV-A` | ACTUATORS | ✓ (M52) | — |
| 37 | `37 ICV-B` / `37 REV-LT` | ACTUATORS | ✓ (M52: GPO5 ICV-B) | ✓ (07K: GPO5 → rev light relay, MTune reassign, same wire) |
| 38 | `38 STARTER` | ACTUATORS | ✓ | ✓ |
| 39 | `39 ALT-D+` | ACTUATORS | ✓ | ✓ |
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

**Type A totals:** M52 Phase 1 plug — 37 wires × 2 = **74 labels**. 07K Phase 3 plug adds 6 new-position wires (pins 14, 22, 23, 43, 44, 45) × 2 = **12 more labels → 86 total**. Pins 16/17/18/19/35/37 reuse M52 positions (relabel on 07K plug only — same physical positions). Pins 20, 24, 34, 41 = cavity-plug both phases (no label needed).

---

**Type B — Sensor connector labels** (Brady M21-125-C-342, ×1 per sensor connector, applied near connector end before body snaps on)

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

**Type B total:** M52 — 18 labels. 07K — 19 labels (adds KS1/KS2, swaps to 07K COP 4-pin format).

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
| B — sensor connector labels | M21-125-C-342 | 18 | 19 |
| C — sub-loom breakout | M21-375-C-342 | 5 | 6 |
| D — main trunk | M21-500-C-342 | 1 | 1 |
| **Total** | | **98** | **126** |

Print all Type A and B labels before touching any wire. Print Type C and D labels before sleeving begins.

---

## Build Sequence

1. **Plan** — With the 07K engine on a stand in its intended orientation, dry-route a tape mock-up of the main trunk. Confirm routing path, bracket attachment points, and connector reach. Measure wire lengths per signal with 10% slack added. Record lengths against the `.wv` file before cutting anything.

2. **Bench build the main trunk** — Cut and label all wires (label sleeves on before cutting to length). Crimp AS79 engine-side contact onto each wire. Insert into the AS79 mating plug body one pin at a time, verifying pin identity against the `.wv` file at each insertion. Bundle wires loosely — **do not sleeve yet.**

3. **Route the engine-side loom** — Lay the harness along the engine with the AS79 mating plug at the firewall position and the wire ends at their intended destinations. Confirm lengths reach components with sufficient slack. Trim or add at this stage — not after sleeving.

4. **Terminate sensor connectors** — At each branch point: cut the main harness wire to length, apply a PermaSleeve label to the wire end (signal name + cylinder), crimp a terminal directly onto the wire end using the Engineer PA-09, and insert the terminal into the sensor connector housing until the locking lance clicks. Connector body plugs onto the component. Exception: sensors with an integral moulded pigtail (e.g., donor WBO2) require one Raychem SRGB splice to join the sensor pigtail to the harness wire — see Splice types section.

5. **Continuity test** — With the harness fully wired but completely un-sleeved, verify every signal end-to-end with a DMM against the `.wv` file. Verify no shorts between adjacent pins. **Do not sleeve until this step passes.**

6. **Sleeve** — Main trunk first with 1/2" Techflex, sub-looms with 1/4" Techflex. Secure breakout transitions with 3:1 adhesive heat-shrink boots. Apply sub-loom PermaSleeve breakout labels before Techflex goes on each sub-loom.

7. **Mount and connect** — Secure the loom to the engine with P-clips. Plug all sensor connectors onto their components. Photograph the complete installed harness before the hood goes on.

---

## Bench Test Before Install

Run each harness on the bench before it goes in the car. All checks are done with a multimeter — no car battery connected, no ECU powered.

### Multimeter setup

Set the dial to **continuity mode** (symbol: `)))` or a speaker/wave icon — the meter beeps when the circuit is closed). Continuity mode generates its own internal test signal (~0.5–1.5V, a few milliamps) — you are not applying battery voltage. The voltage and current range settings on the dial are for measuring live circuits and are not used for harness testing.

If your multimeter does not have a dedicated continuity mode, use **resistance (Ω) mode** at the 200Ω range. A good 22 AWG wire ≤2m reads <0.5Ω. Higher = partial break or bad crimp.

### Test procedure — four checks in order

**Check 1 — Continuity (every signal wire)**
1. Open the `.wv` file (`firewall-bulkhead.wv` for the engine harness)
2. For each populated pin: touch one probe to the AS79 cabin-side wire end (or the ECU C1/C2 connector pin), touch the other probe to the expected sensor connector pin at the far end
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

---

## External References

### Workbench jig / harness template method
**[@cabellomotorsportwiring](https://www.instagram.com/cabellomotorsportwiring/) — Instagram reel**
https://www.instagram.com/p/DcJ6gkXySDT/

Brazilian motorsport wiring shop (Fueltech / Motec work). Reel shows each harness segment printed as a physical diagram, cut out, and pinned/taped to the workbench surface. Connector photos for each segment are mounted alongside the diagram. Every wire run is physically mapped to scale before a single wire is cut.

Caption (translated from Portuguese): *"Template/jig idea for building harnesses in series. The more details on the workbench, the easier and faster the construction. Planning is the most important part of the process."*

Notable comment (translated): *"I used to do it on a board with nails"* — the classic low-tech version of the same concept.

**Relevance for this build:** The video shows the same documentation approach used in this project — per-segment diagrams, pinouts, wire routing detail — but physically laid out on the workbench. The one thing they have that this project does not: a physical connector reference for each sub-loom/harness segment (the actual connector body, pinout card, and wire termination shown together). That gap is worth closing — adding a connector photo + pinout card per segment to the build docs would replicate what they show here.

---

### Service loops — individual wire loops before boot
**[@oshin_prowiring](https://www.instagram.com/oshin_prowiring/) (collab @afterfix.pro) — Instagram reel**
https://www.instagram.com/p/Dcat40oslGu/

Mil-spec wiring shop. Reel shows the full service loop sequence on a multi-wire connector: each wire labeled before looping, individual wire coiled around a pin/mandrel, all loops heat-shrunk together as a bundle, then the boot slid over and shrunk. Tags: #raychem #milspecwiring #autosportwiring.

Notable comment: *"Did you add RT125 or other types of epoxy around the boots?"* — RT125 is Raychem adhesive-lined compound; gives the boot a fused/OEM appearance vs. just slipped on.

**Relevance:** Confirms and visually demonstrates the technique described in the service loops section above, including the intermediate heat-shrink-over-bundle step added after seeing this reel.
