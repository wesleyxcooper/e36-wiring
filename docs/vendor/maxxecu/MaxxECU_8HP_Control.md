# MaxxECU 8HP GEN1 Control — Vendor Reference

Primary-source data on MaxxECU's native ZF 8HP GEN1 transmission control. All claims are cited inline.

---

## 1. Supported variants

GEN1 only: 8HP45, 8HP70, 8HP90. 8HP51 and 8HP76 require additional parts.
GEN2 (F-series/G-series donor) is not supported by this protocol.
Source: [maxxecu.com/features/8hp_gearbox](https://maxxecu.com/features/8hp_gearbox)

---

## 2. Hardware required

| Item | PN / Source | Price |
| :---- | :---- | :---- |
| BMW 8HP shifter cable harness (pre-made PnP kit) | [maxxecu.com/store/gearbox/8hp/maxxecu-8hp-gen1-cable-harness-bmw-8hp-shifter](https://maxxecu.com/store/gearbox/8hp/maxxecu-8hp-gen1-cable-harness-bmw-8hp-shifter) | $368.61 |
| Yanhua ACDP-2 TCU flash tool (purchase) | [maxxecu.com/store/gearbox/tools/yanhua-acdp-2-8hpxx-tcu-tool-package](https://maxxecu.com/store/gearbox/tools/yanhua-acdp-2-8hpxx-tcu-tool-package) | $737.80 |
| Yanhua ACDP-2 TCU flash tool (rental from MaxxECU) | [maxxecu.com/store/gearbox/tools/rental-of-yanhua-acdp-2-8hpxx-tcu-tool-package](https://maxxecu.com/store/gearbox/tools/rental-of-yanhua-acdp-2-8hpxx-tcu-tool-package) | $138.23 |

The Yanhua ACDP-2 flashes MaxxECU's custom DEMON firmware into the 8HP's existing internal TCU. No PCB soldering, no internal wiring modification. Source: [maxxecu.com/features/8hp_gearbox](https://maxxecu.com/features/8hp_gearbox) — *"Controls the stock TCU, no internal wiring or soldering needed."*

To obtain the DEMON firmware files, email `support@maxxecu.com` with a screenshot of the TCU ident + binary readouts of internal flash + EEPROM + vehicle/transmission info. Source: [maxxecu.com/webhelp/advanced-8hp-tcu_firmware.html](https://maxxecu.com/webhelp/advanced-8hp-tcu_firmware.html)

**Pitfall:** Do not use DEMON firmware with any OE ECU/PCM. It will not work and may damage the transmission. DEMON firmware is for MaxxECU engine management only.

---

## 3. TCU firmware vs OEM comparison

Source: [maxxecu.com/webhelp/advanced-8hp-tcu_firmware.html](https://maxxecu.com/webhelp/advanced-8hp-tcu_firmware.html)

| Parameter | OE Dodge | MaxxECU DEMON |
| :---- | :---- | :---- |
| Max engine RPM | 7650 rpm | 9200 rpm |
| Controllable shift RPM | — | 1500–9000 rpm |
| Transbrake RPM window | 1400/2500 rpm | 1200/7000 rpm |
| Max transbrake torque | 800 Nm | 1547 Nm |
| Max torque limit (all gears) | 760 Nm | 1547 Nm |
| Max torque limit (engagement clutch) | 1000 Nm | 1547 Nm |
| Drive map count | ~100 | 5 (4 modes + manual) |
| Transbrake timeout | short | 25 s |

---

## 4. Torque management

MaxxECU sends a torque value (-500 to 1547 Nm) to the 8HP internal TCU over CAN. This value is **directly linked to the final clutch pressures** inside the TCU. Source: [maxxecu.com/webhelp/advanced-8hp-mtune_control.html](https://maxxecu.com/webhelp/advanced-8hp-mtune_control.html) — *"Dynamic Torque table. -500 to 1547Nm. This value should represent the engine torque and is transferred to the TCU, directly linked to the final clutch pressures."*

A separate torque correction table allows per-shift torque reduction. Default configuration reduces torque during active upshifts at lower pedal positions for smoother shifts.

**Pitfall:** Clutch slip on the 8HP causes rapid heat buildup and clutch failure. The torque table must be accurate before driving under load. Source: [maxxecu.com/webhelp/advanced-8hp-mtune_control.html](https://maxxecu.com/webhelp/advanced-8hp-mtune_control.html) — *"slipping on the 8HP clutches is NOT a good idea, they will get hot and die pretty fast."*

**Direction of error:** Too-high torque values → too much clutch pressure → harsh shifts. Too-low torque values → clutch slip → heat → failure. Start high and reduce. Never start low.

### Torque table commissioning sequence

1. **Build initial table from known M52B28 curve.** Stock M52B28 peak: approximately 280 Nm at 3500 rpm. Set table values to stock curve + 20–30% across all cells. For the turbo phase, add a MAP axis and populate boost cells at proportionally higher values.
2. **Lock torque correction table at 100%.** No shift reduction until the base table is validated. 100% = no adjustment.
3. **First shifts: light throttle, low RPM only.** Under 2000 rpm, 20% pedal max. Monitor:
   - `TRANSMISSION oil temp` — baseline it; any sharp rise during a shift = slip. Source: [maxxecu.com/webhelp/advanced-8hp-realtime_data.html](https://maxxecu.com/webhelp/advanced-8hp-realtime_data.html)
   - `Transmission Clutch A/B/C/D/E Pressure` — requires Binary 4+ firmware. Clutch pressure should be proportional to your sent torque value.
   - `Dodge 8HP Last Shift Time` — shift time in ms. Unusually long shift times indicate insufficient clutch pressure (slip during the shift).
4. **If shifts are harsh but oil temp is stable:** table is working safely. Reduce values in 5–10% steps until quality is acceptable.
5. **If oil temp rises during shifts:** torque table is too low for the actual engine output. Increase values before continuing.
6. **Final calibration on dyno.** Dyno pull gives measured wheel torque. Convert to engine torque: `engine torque = wheel torque / drivetrain efficiency`. With the 8HP: drivetrain efficiency approximately 85–88% at the wheel. Remap torque table against measured values.

For the turbo phases (3a and 3b): torque output varies significantly with boost. Use a 2D table with MAP on the load axis. Set values conservatively at first boost levels and increment boost only after each table row is validated.

---

## 5. Drive modes

Source: [maxxecu.com/webhelp/advanced-8hp-mtune_settings.html](https://maxxecu.com/webhelp/advanced-8hp-mtune_settings.html)

| Mode | Value | Notes |
| :---- | :---- | :---- |
| STREET | 1 | Relaxed shift points |
| SPORT | 3 | |
| TRACK | 5 | |
| DRAG | 10 | Required for transbrake feature |

Modes are switchable via an analog input or user table in MTune — a physical toggle, rotary switch, or tune selector maps to mode values 1/3/5/10.

---

## 6. Clutch and shift control

Source: [maxxecu.com/webhelp/advanced-8hp-mtune_settings.html](https://maxxecu.com/webhelp/advanced-8hp-mtune_settings.html), [maxxecu.com/webhelp/advanced-8hp-shift_control.html](https://maxxecu.com/webhelp/advanced-8hp-shift_control.html)

- **Full clutch pressure control** (Binary 5 firmware): ramp-controlled takeoff, launch, clutchkick. Individual A/B/C/D/E clutch pressures reported to MaxxECU in real time.
- **Virtual clutch mode**: full 0–100% clutch pressure control. For clutchkick / drift use.
- **Upshift shiftcut**: TCU sends a torque reduction request; MaxxECU activates shiftcut (fuel/ignition cut + retard) in response. Timing is internally coordinated.
- **Downshift blip**: optional rev-match blip for faster downshifts. Not required for a correct downshift.
- **Transbrake**: DRAG mode only. 1st+R or 2nd+R, up to 1547 Nm, 25 s timeout.
- **Kickdown**: available for fast downshifts.

---

## 7. MaxxECU native vs Turbolamik

Source (Turbolamik): [turbolamik.help/ecus/maxxecu](https://turbolamik.help/ecus/maxxecu/), [turbolamik.us/tcu-2-0-turbolamik](https://www.turbolamik.us/tcu-2-0-turbolamik/)

| | MaxxECU native | Turbolamik TCU 2.0 |
| :---- | :---- | :---- |
| Torque → clutch pressure | Yes | Yes |
| Drive modes | 4 (STREET/SPORT/TRACK/DRAG) | 8 |
| Transbrake | Yes | Yes |
| Virtual clutch / clutchkick | Yes | Yes |
| Full clutch pressure control | Yes (Binary 5+) | Yes |
| Dedicated 8HP adaptation logic | Within OEM TCU (DEMON fw) | External TCU, purpose-built |
| Hardware modification | Firmware flash (Yanhua ACDP-2), no PCB soldering | PCB soldered into mechatronic (permanent) |
| Additional cost | $368 harness + $138 tool rental = ~$507 | $2,365 full kit (TCU + PCB + harness + display) |
| Software | MTune (same as engine) | Turbolamik Map Studio (separate) |
| MaxxECU integration | Native, built-in | *"Cleanest integration: no raw CAN IDs to enter by hand"* (turbolamik.help) |
| Firmware status | Public beta (Binary 5) | Established, 10+ years |

Turbolamik requires MaxxECU firmware 10.73+ and 500 kbps CAN. The footbrake is not sent over CAN in the MaxxECU integration — wire brake switch to Turbolamik pin 11 (A7) directly.

---

## 8. MTune configuration pointers

- Torque table: set before any load driving. Use TPS + MAP as axes; output = engine torque in Nm.
- Transmission mode input: wire a switch to a MaxxECU analog input; map values 1/3/5/10 in MTune user table.
- Shift strategy: set to "MaxxECU TCU maps (1500–9000 rpm)" for custom shift points via table.
- Shiftcut: enable in MTune Motorsport → Shiftcut; set input as "input controlled" so shiftcut duration tracks the TCU's torque reduction request.
- CAN bus: 8HP uses MaxxECU CAN 1 at 500 kbps. Source: `harnesses/8hp-can.wv`. PMU16 is on CAN 2 — no conflict.

Full MTune 8HP documentation: [maxxecu.com/webhelp/advanced-8hp.html](https://www.maxxecu.com/webhelp/advanced-8hp.html)
