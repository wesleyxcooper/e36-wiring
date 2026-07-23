# EWP Wiring Reference — Davies Craig EWP150 + Digital Controller

**Build context:** 07K / 8HP swap, MaxxECU RACE, Gauge.S E36 PNP cluster. EWP replaces OEM belt-driven 07K water pump entirely. OEM pump 07K121011B is excluded.

---

## Official Documentation

| Document | Link |
| :--- | :--- |
| EWP Kit Install Instructions (latest, Feb 2024) | [daviescraig.com.au PDF](https://daviescraig.com.au/media/2717/1709873550.EWPKitInstructions27Feb202429823.pdf) |
| Digital Controller #8002 (LCD) Install Instructions | [daviescraig.com.au PDF](https://daviescraig.com.au/media/2087/1616455861.8002-EWPControllerInstructions2982123-March-2021.pdf) |
| Digital Controller #8020 Install Instructions | [daviescraig.com.au PDF](https://daviescraig.com.au/media/2372/1668738780.8020-DigitalControllerPartNo.892703Apr14.pdf) |
| All Davies Craig Instructions Index | [daviescraig.net/instructions](https://daviescraig.net/instructions) |
| Davies Craig Video Library | [daviescraig.com.au/video](https://daviescraig.com.au/video) |

---

## YouTube Resources

| Video | Channel | Notes |
| :--- | :--- | :--- |
| [Everything you need to know about Davies Craig electric water pumps](https://www.youtube.com/watch?v=mmkogcmocc0) | fullBOOST (6:39) | Best overview — covers EWP + digital controller, PWM speed control, ECU integration concept, post-shutdown cooling. Watch first. |
| [Electric Water Pump Upgrade & Wiring Harness — SR86 build](https://www.youtube.com/watch?v=piNQ68a7qSk) | High Performance Academy | Shows EWP install in context of a full custom motorsport wiring harness (MoTeC M150 ECU). Directly analogous to the MaxxECU harness build here. |
| [EWP & Digital Controller Installation](https://daviescraig.com.au/video) | Davies Craig official | See Davies Craig video library → "EWP & Digital Controller Installation" |

---

## Digital Controller Wiring Connections (#8002 LCD)

The Davies Craig Digital Controller drives the EWP pump directly via internal PWM — it controls pump motor speed by varying voltage/duty cycle. There is no external signal input to the EWP150 from the ECU.

| Wire | Connection |
| :--- | :--- |
| RED | Battery +VE (fused direct — use ring terminal provided) |
| BROWN | Chassis earth (self-tapping screw to body metal — good contact required) |
| GREEN | Switched +12V ignition source |
| GREEN/BLACK stripe | Fan relay pin 85 (controller earths the relay — does NOT power it) |
| T-connector (BLUE + BLACK) | EWP pump connector |
| Black sensor lead | Davies Craig thermistor sensor (inline adapter in coolant hose) |

> ⚠️ **Critical:** The GREEN ignition wire **must NOT** connect to the MaxxECU output, ECU power, or ignition coils. Connect to a clean fused switched +12V relay output only. Davies Craig explicitly warns this can cause operational issues with the controller or damage the ECU.

> ⚠️ **Controller mounting:** Must be inside the passenger compartment — not the engine bay. Route harness through a ~20mm firewall grommet. Controller ambient temp must stay low; keep it away from direct sunlight.

---

## CLT Sensor Strategy — MaxxECU vs Davies Craig Controller

The EWP150 has no external signal input. The Davies Craig controller is the sole PWM driver for the pump. MaxxECU does not directly control the EWP speed.

**Two separate sensors (recommended approach for this build):**

| Sensor | Location | Consumer |
| :--- | :--- | :--- |
| Davies Craig thermistor (NTC, proprietary connector) | Inline adapter in **upper/hot-side hose** (engine coolant exit side, pre-radiator) — reads actual engine temp, not post-cooled. Alternatively: tap 1/4" NPT into the BBG rear coolant flange if accessible. Do NOT put in lower hose (post-radiator) — sensor reads ~10–20°C lower than actual engine temp, requiring compensation of the controller setpoint. | Davies Craig Digital Controller only |
| MaxxECU CLT sensor (2-wire NTC, 10kΩ @ 25°C typical) | Coolant port on engine — BBG rear coolant flange or block fitting | MaxxECU only |

Running two separate sensors is simpler than tapping both controllers off a single sensor. The sensors operate at different impedances and with different connectors — no compatibility issues with separate sensors. Davies Craig inline adapter (included in kit) accepts the Davies Craig proprietary thermistor; MaxxECU uses a standard 1/8" NPT or M10x1.0 NTC sensor in an engine port.

**Shared sensor (not recommended):** Theoretically possible by tapping the Davies Craig sensor signal wire in parallel to a MaxxECU analog input, but impedance loading could affect both readings. Not worth the complexity given the 07K has available coolant ports for two sensors independently.

---

## Post-Shutdown Cooling — How It Works

The Davies Craig controller monitors coolant temp via its own sensor. After ignition is switched off:
- Controller continues running the EWP until coolant drops **10°C below the set point** or **3 minutes** — whichever comes first (programmable threshold on #8002 LCD).
- MaxxECU is off. No MaxxECU power latch required.
- The controller draws power directly from battery (RED wire — always hot). Post-shutdown current draw is low (EWP at low speed ≈ 2–4A).

---

## Mechanical Pump Deletion — 07K Specific

Davies Craig recommended method for full pump deletion (best for this build):
1. Remove OEM 07K121011B mechanical pump and thermostat entirely.
2. Install block-off plate at water pump port (source from VW specialist or fabricate — not supplied by Davies Craig).
3. Remove thermostat — Davies Craig controller becomes the system's new thermostat.
4. Install EWP150 inline in **lower radiator hose**, as low as possible, outlet pointing toward engine.
5. Route heater core return line to EWP **inlet** (not outlet) — maintains heater function.
6. Block any thermostat bypass passages.

> ⚠️ Do not hard-mount the EWP to the chassis — mount to the radiator hose or use Davies Craig Part #8700 soft-mount bracket. Hard mounting transmits engine vibration into the pump housing.

---

## Bleeding Procedure (Pre-Fire Leak Test)

This is the key advantage for a fresh swap — perform before the engine ever fires:

1. Fill cooling system with coolant.
2. Disconnect Davies Craig T-connector from pump. Using the basic wiring harness from the EWP kit, connect BLUE wire to battery +VE and BLACK to earth — pump runs on direct battery power.
3. With radiator cap off, run 5–10 minutes to purge all air. Top up coolant as air escapes.
4. Check all connections for leaks under pump pressure.
5. Reconnect T-connector to Digital Controller once system is confirmed sealed and bled.

---

## Part Numbers

| Item | Part # | Notes |
| :--- | :--- | :--- |
| EWP150 Kit (12V) | #8060 | Pump + basic wiring harness + relay + clamps |
| EWP150 + LCD Digital Controller Combo | #8970 | Best value — pump + #8002 controller in one kit |
| LCD Digital Controller only | #8002 | If sourcing pump and controller separately |
| Mounting bracket (EWP115/140/150) | #8700 or #8710 | Soft-mount bracket for engine bay mounting |
