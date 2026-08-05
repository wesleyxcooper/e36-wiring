# E-Throttle PID Tuning — MaxxECU RACE + 07K TB

Cross-reference: `harnesses/epedal-bmw-e46.wv` · `harnesses/epedal-hella-6pv.wv` · `schematics/epedal-dbw.py` · `docs/dbw-pinouts.md`

---

## What PID tuning is and why it matters

When MaxxECU controls the throttle body, it runs a closed-loop PID (Proportional–Integral–Derivative) feedback controller between the **commanded position** (derived from the pedal's APS signal) and the **actual TB plate position** (measured by the TB's own TPS1/TPS2 sensors). The controller drives the TB motor with varying voltage/direction to keep actual position tracking commanded position.

Without correct PID values:
- Too low P: TB responds sluggishly — pedal input lags by hundreds of ms
- Too high P: TB overshoots and oscillates — audible buzz from motor, erratic TPS trace
- Too high I: integral windup causes sustained overshoot on step inputs
- Too high D: derivative term amplifies sensor noise — visible jitter in TPS reading

The correct values depend on the specific TB's motor resistance, spring return force, and plate mass. These differ between the **stock 07K 65mm TB** and any upgraded unit (e.g. VW 3.6 VR6 `03H 133 062`, ~74mm). Always re-tune PID after changing the throttle body.

---

## Pre-conditions before activation

1. **Wiring verified:** All 6 pedal wires through bulkhead, both APS1 and APS2 reading correct voltages on a multimeter at idle (≈0.70V APS1, ≈0.36V APS2 with key on, no crank).
2. **TB wired:** All 6 TB connector pins confirmed (Motor+, Motor−, TPSGND, +5V, TPS1, TPS2). Verify TPS1 and TPS2 both read plausible voltages with key on.
3. **TB motor disconnected:** Disconnect the TB motor power wires (Motor+ and Motor−) **before** enabling e-throttle in MTune for the first time. Leave sensor wires connected. This prevents runaway throttle from an uninitialised motor drive output.
4. **MTune connected:** USB or wireless to MaxxECU, real-time data visible.

---

## Calibration sequence in MTune

### Step 1 — Enable e-throttle

MTune path: `Settings › E-Throttle`

- Set **E-Throttle mode** to `Active`
- Assign **APS1** and **APS2** to the correct AIN inputs (the ones your pedal wires terminate at)
- Assign **TPS1** and **TPS2** to the correct AIN inputs (the ones the TB sensor wires terminate at)
- Assign **TB motor output** to the correct GPO pair (H-bridge capable output)
- Save settings

### Step 2 — Pedal calibration wizard

MTune path: `Settings › E-Throttle › Pedal calibration`

1. Fully release the pedal (idle position) and click `Capture idle`
2. Fully depress the pedal (WOT) and click `Capture WOT`
3. Wizard records min/max voltage for both APS1 and APS2
4. Verify captured values match expected ranges:
   - APS1: ≈0.70V idle, ≈4.50V WOT
   - APS2: ≈0.36V idle, ≈2.20V WOT
   - APS2 should track at approximately half the APS1 voltage across the full range
5. Save and confirm ratio tolerance is enabled (MaxxECU will fault if tracks disagree beyond ~10%)

### Step 3 — TB calibration (physical stop capture)

MTune path: `Settings › E-Throttle › Throttle body calibration`

- Reconnect TB motor wires now (sensors have been verified live, motor can be activated safely with the wizard in control)
- Run the **auto-calibration sweep**: MaxxECU drives the TB to its physical closed and open stops, records the TPS1/TPS2 voltage at each extreme
- Verify: TPS1 idle ≈ lower voltage (closed), TPS1 WOT ≈ higher voltage (open); TPS2 mirrors at ~half ratio
- The wizard sets the TB position table — do not manually edit these values

### Step 4 — PID tuning

MTune path: `Settings › E-Throttle › PID`

**Start with MaxxECU defaults for the Bosch 0280 750 family** (the stock 07K TB family). MaxxECU ships conservative defaults that work as a safe starting point for most Bosch units.

#### Option A — Auto-tune (recommended first step)

1. Engine running at idle, MTune connected
2. Navigate to `Settings › E-Throttle › PID › Auto-tune`
3. Follow the auto-tune procedure — MaxxECU sweeps the TB through a series of step inputs and calculates P, I, D from the response
4. Accept auto-tune values and save
5. Verify result on the scope (Step 5 below)

#### Option B — Manual tuning

If auto-tune is not available or gives unsatisfactory results:

| Parameter | Start value | Direction if TB lags | Direction if TB oscillates |
|---|---|---|---|
| **P (Proportional)** | MaxxECU default (~10–20) | Increase | Decrease |
| **I (Integral)** | MaxxECU default (~0.1–0.5) | Slight increase | Decrease or set 0 temporarily |
| **D (Derivative)** | 0 initially | Add small values if oscillation persists after P/I settle | Reduce — D amplifies noise |

Typical workflow:
1. Start with D=0, I=0, P at default
2. Increase P until TB response is fast but just before oscillation begins
3. Add small I to correct any steady-state offset at a fixed pedal position
4. Add D only if P+I still oscillates — D damps the response but amplifies sensor noise

### Step 5 — Verify on MTune scope

MTune path: `Realtime Data › Scope`

Add these channels to the scope:
- **APS% (pedal position)** — what you're commanding
- **TPS% (throttle position)** — what the TB is doing
- **TB motor duty** (if available) — motor drive effort

Snap the pedal sharply between idle and ~30%, ~50%, and WOT several times. Assess:

| What you see | Diagnosis | Fix |
|---|---|---|
| TPS follows APS with minimal delay, no bounce | Good — PID is settled | None |
| TPS lags behind APS by >50ms | P too low | Increase P |
| TPS overshoots APS then bounces 2–3 cycles | P too high | Decrease P |
| TPS settles slowly, creeps to target | I too low | Increase I |
| TPS oscillates continuously even at steady pedal | D too high or P too high | Reduce P first, then D |
| TPS jitters at fixed pedal position | D too high — amplifying sensor noise | Reduce D |

Target: TPS tracks APS with <20ms lag on step inputs, zero sustained oscillation, <2% steady-state offset.

---

## Safety monitoring — never disable

MaxxECU runs four independent e-throttle safety checks at all times:

| Check | What it monitors | Fault action |
|---|---|---|
| **APS ratio** | APS1:APS2 ratio within tolerance (~10%) | Cuts TB motor, TB spring-closes |
| **TPS ratio** | TPS1:TPS2 ratio within tolerance | Cuts TB motor |
| **APS vs TPS agreement** | Actual TB position within range of commanded position | Cuts TB motor if persistent |
| **Signal range** | APS and TPS voltages within calibrated min/max bounds | Cuts TB motor on out-of-range |

When any safety check triggers, MaxxECU cuts motor output and the TB return spring closes the plate. The engine goes to idle or cuts.

**Never disable these checks.** Do not attempt to bypass safety faults by widening tolerances beyond MaxxECU defaults — diagnose the root cause (wiring fault, bad sensor, incorrect calibration) instead.

---

## Common faults and root causes

| Symptom | Likely cause | Check |
|---|---|---|
| E-throttle fault at key-on, no movement | Wiring fault or calibration not run | Verify APS/TPS voltages in real-time data before enabling motor |
| TB motor hums but plate does not move | Motor wired backwards OR motor+/motor− polarity reversed | Swap motor wires at MaxxECU or TB connector |
| APS ratio fault | APS1/APS2 track wires crossed or open circuit | Verify both APS voltages independently |
| TPS ratio fault after TB swap | TB position not recalibrated after swap | Re-run TB calibration wizard |
| TB oscillates at all times (P loop instability) | P too high, or TPS wiring has noise | Reduce P; add shield drain if TPS wires are unshielded |
| TB response OK at idle, sluggish at WOT | PID gain table uses single value; needs 2D PID table by TPS position | Check MaxxECU e-throttle advanced settings for position-dependent gains |

---

## TB upgrade — re-tune required

If upgrading from the stock 07K 65mm TB to the VW 3.6 VR6 `03H 133 062` (~74mm):

1. Re-run full TB calibration wizard (physical stop positions will differ)
2. Re-run PID auto-tune or re-tune manually — the larger plate and different motor response require new values
3. Verify scope trace on upgraded TB before driving
4. The pedal calibration is TB-agnostic — no need to re-run pedal wizard

---

## Reference links

- [MaxxECU E-Throttle Settings](https://maxxecu.se/webhelp/settings-ethrottle.html)
- [MaxxECU E-Throttle Body Wiring](https://maxxecu.se/webhelp/wirings-e-throttle_bodies.html)
- [MaxxECU E-Pedal Wiring](https://maxxecu.se/webhelp/wirings-e_pedals.html)
- `docs/dbw-pinouts.md` — pedal and TB pinout tables (this repo)
- `schematics/epedal-dbw.py` — dual-track sensor circuit schematic (this repo)
