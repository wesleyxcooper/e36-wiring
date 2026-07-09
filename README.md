# e36-wiring

Version-controlled wiring harness documentation for an RHD E36 convertible restomod.
Engine: VW 07K 2.5L I5 (turbo, longitudinal) · ECU: MaxxECU Race · Trans: ZF 8HP70

Diagrams are authored in [WireViz](https://github.com/wireviz/WireViz) YAML format — plain text,
git-diffable, outputs SVG/PNG/HTML/BOM automatically.

## Harnesses

| File | Description | Phase |
|---|---|---|
| `harnesses/maxxecu-m52.wv` | MaxxECU Race ↔ M52 engine harness (Phase 1) | 1 |
| `harnesses/maxxecu-07k.wv` | MaxxECU Race ↔ 07K engine harness (Phase 3) | 3 |
| `harnesses/8hp-can.wv` | MaxxECU ↔ 8HP70 CAN harness | 1 |
| `harnesses/gauge-s-can.wv` | MaxxECU ↔ Gauge.S cluster CAN | 1 |
| `harnesses/firewall-bulkhead.wv` | Deutsch AS47/AS79 firewall bulkhead connector | 1 |
| `harnesses/body-x20.wv` | E36 X20 body connector interface (MaxxECU outputs → dash/instruments) | 1 |
| `harnesses/dct-shifter.wv` | DCT Shifter paddle → MaxxECU DIN wiring | 1 |
| `harnesses/pst-f1-sensor.wv` | Bosch PST-F1 oil temp/pressure → Gauge.S analog inputs | 1 |

## Key interfaces

- **MaxxECU Race connector:** CMC (Cinch Modular Connector) multi-pin — see `connectors/maxxecu-cmc.wv`
- **Firewall bulkhead:** Deutsch Autosport AS series 47-way (expand to 79-way if needed) — permanent cabin side; engine harnesses mate at the plug
- **E36 X20:** Chassis-to-engine-bay interface — MaxxECU RPM/temp/pressure signals to OEM instrument cluster
- **8HP CAN:** MaxxECU GEN1 8HP CAN harness (native control — no TurboLamik)
- **Gauge.S CAN:** 500kbps, MaxxECU Default 1.3 output protocol

## Reference documentation

- [MaxxECU Race pinout](https://www.maxxecu.com/webhelp/wirings-maxxecu_pinout.html)
- [MaxxECU wiring index](https://www.maxxecu.com/webhelp/wirings.html)
- [MaxxECU M50 terminated harness pinout](https://www.maxxecu.com/webhelp/wirings-terminated_engine_harness-bmw_m50.html)
- [MaxxECU downloads (PDFs, wiring diagrams)](https://www.maxxecu.com/downloads)
- [E36 X20 connector pinout (Scribd)](https://www.scribd.com/document/649295040/bmw-e36-x20-pinout)
- [MaxxECU 8HP GEN1 CAN harness](https://www.maxxecu.com/store/gearbox/8hp/maxxecu-8hp-gen1-cable-harness)
- [WireViz documentation](https://github.com/wireviz/WireViz)

## Setup

```bash
pip install -r requirements.txt
```

Generate all diagrams:

```bash
wireviz harnesses/*.wv -o output/
```

Generate a single harness:

```bash
wireviz harnesses/maxxecu-07k.wv -o output/
```

Output files go to `output/` — SVGs are committed, PNGs/HTML are gitignored.

## 07K harness signal map

The M52 and 07K share MaxxECU trigger type (`N-1 missing tooth`, 60-2 wheel). Signal-level changes at engine swap:

| Signal | M52 Phase | 07K Phase | Change |
|---|---|---|---|
| Crank sensor | BMW 60-2 VR | VW 60-2 VR | Different connector, re-calibrate angle offset |
| Cam/home sensor | BMW Hall effect | VW Hall effect | Different connector |
| CLT sensor | BMW NTC | VW NTC | Different connector + recalibrate curve |
| TPS | BMW M52 TPS | VR6 throttle body | Different connector, same 0–5V signal |
| Injectors | Bosch JPT ×6 (EV1) | Bosch EV14 ×5 | Different connector end, 5-cyl |
| VANOS solenoid | GPO 3 active | Not applicable | Disable in tune |
| Wideband O2 | LSU 4.2 | Same | Nothing |
| MAP sensor | Same | Same | Nothing |
| Flex fuel | Digital input | Same | Nothing |
| 8HP CAN | Connected | Still connected | Nothing |

## Contributing

This is a personal build document. If you're doing a similar swap and have confirmed pinouts or connector part numbers, PRs welcome.
