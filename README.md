# Nassenger 8 — Neuro-Symbolic Digital Twin Engine

**Project Origin:** Faulter Wireless — Divine Industries  
**Machine:** Konica Minolta NASSENGER 8 Industrial Inkjet Textile Printer  
**Architecture:** Neuro-Symbolic Digital Twin (Symbolic Physics + Neural Orchestration)

---

## 🎯 Project Vision

Build a **full-fidelity digital twin** of the NASSENGER 8 industrial textile printer using:

- **Symbolic Layer:** 61 physics formula templates + deterministic solver (Python/NumPy)
- **Neural Layer:** Qwen Code agent for orchestration, reasoning, and code generation
- **UI Layer:** Interactive HTML/CSS/JS simulation widgets (one per worker)

The twin simulates **16 parallel workers** (subsystems) that form an "assembly river" — fabric flows through each stage sequentially, with each worker modeled as a coupled state-space system.

---

## 🖨️ Machine Overview — NASSENGER 8

### Core Specifications
- **Type:** Scan-type (scanning carriage) inkjet textile printer
- **Technology:** Drop-on-demand piezo inkjet (KM1024 printhead series)
- **Print Width:** 1,850 mm
- **Max Fabric Thickness:** 15 mm
- **Printheads:** 16 (2-line) or 32 (4-line) KM1024 heads, 1024 nozzles each
- **Colors:** 8 standard, 9 optional (reactive, disperse, acid dye inks)
- **Max Speed:** 480 m²/h (4-line, Draft mode)
- **Operating Environment:** 15–30°C, 40–70% RH
- **Print Unit Dimensions:** 5080×2010×2040 mm, ~3300 kg
- **Power:** 
  - Print unit: AC 200–240V 30A single phase
  - Dryer: AC 380V 50A 3-phase
- **Peripherals:** Ink rack, unwinder, dryer+winder (separate units)

### KM1024 Printhead Specifications
- **Nozzles:** 1024 per head (256×4 rows)
- **Nozzle Pitch:** 70.5 µm
- **Native Resolution:** 360 dpi
- **Print Width per Head:** 72.1 mm
- **Row Spacing:** 2.82 mm staggered
- **Drop Velocity:** 6.0 ± 0.5 m/s
- **Drop Volume:** ~14 pl (mid), up to 42 pl (large)
- **Grayscale:** 8 levels (3-bit)
- **Placement Accuracy:** <±5 µm
- **Technology:** Shear-mode piezo, DoD
- **Drive Frequency:** Up to 45 kHz (KM1024i variant)

---

## 🧩 System Architecture

### 7 Functional Subsystems

Each subsystem is mapped with state variables, governing equations, and physical parameters:

1. **Printhead Array** — DoD physics, drop formation, nozzle back-pressure
2. **Carriage / Scanning System** — DC motor, belt drive, encoder, PID/TDOF control
3. **Fabric Transport** — Feed roller, banding error, web tension, dancer roller
4. **Ink Supply System** — Hagen-Poiseuille, subtank dynamics, damper compliance, purge
5. **Dryer & Winder** — Drying kinetics, heat transfer, winder torque vs growing roll
6. **RIP / Image Processing** — Color separation, halftoning, nozzle compensation
7. **Maintenance Station** — Clog probability, evaporation, purge effectiveness, CRI index

---

## 📐 Formula Database — 61 Unique Templates

Organized into **8 engineering domains:**

### 1. Electrical (8 formulas)
- Ohm's law
- DC motor back-EMF
- Motor electrical time constant
- Power dissipation
- RC charge/discharge
- PWM duty cycle → voltage
- Three-phase power
- Transformer voltage

### 2. Mechanical (10 formulas)
- Newton's 2nd law
- Rotational dynamics
- Belt tension ratio (Euler-Eytelwein)
- Bearing friction torque
- Gear speed ratio
- Fatigue life S-N curve
- Hertz contact stress
- Vibration natural frequency
- Beam deflection
- Torque-speed curve

### 3. Thermal (8 formulas)
- Fourier conduction
- Newton's cooling
- Stefan-Boltzmann radiation
- Thermal resistance network
- Heat capacity
- Thermal time constant
- Arrhenius equation
- Psychrometric enthalpy

### 4. Fluid/Ink (8 formulas)
- Hagen-Poiseuille
- Reynolds number
- Bernoulli
- Continuity equation
- Young-Laplace surface tension
- Capillary pressure
- Viscosity-temperature Arrhenius
- Darcy filter pressure drop

### 5. DoD Inkjet-Specific (6 formulas)
- Ohnesorge number
- Weber number
- Rayleigh drop volume
- Drop velocity vs voltage
- Drop ballistic landing error
- Piezoelectric actuator force

### 6. Fabric/Material (5 formulas)
- Web tension elastic model
- Newton's drying law
- Convective mass transfer
- Kubelka-Munk color model
- Fabric thermal diffusivity

### 7. Control Systems (6 formulas)
- PID controller
- 2nd order transfer function
- Disturbance observer (DOB)
- Encoder pulse → position
- Bode gain margin
- State-space representation

### 8. Reliability/Maintenance (5 formulas)
- Weibull failure probability
- MTBF
- Clog Risk Index
- Nozzle evaporation rate
- Purge effectiveness

### 9. Image/Signal Processing (5 formulas)
- Floyd-Steinberg halftoning
- Multi-pass interleaving
- Dead nozzle compensation
- Ink coverage → volume
- Color separation spectral

---

## 🏭 16 Workers — Assembly River Model

The "assembly river" mental model: fabric flows like a river, each worker is a chain of components acting on it.

### Worker 1 — Unwinder
**Components:** Brake motor + dancer roller + tension sensor  
**Function:** Controls fabric roll geometry, web tension, and PID-based tension regulation  
**Formulas:** 8-step series chain  
**State Variables:** `r(t)`, `ω(t)`, `T(t)`, `I(t)`, `T_m(t)`  
**Status:** ✅ Complete

### Worker 2 — Fabric Feed/Advance
**Components:** Servo motor + drive roller + pinch roller + encoder  
**Function:** Speed control with PID, encoder feedback, and banding error detection  
**Formulas:** 8-step series chain  
**State Variables:** `v(t)`, `ω(t)`, `I_s(t)`, `θ(t)`, `d(t)`  
**Status:** ✅ Complete

### Worker 3 — Fabric Tensioning
**Components:** Dancer roller + spring actuator + PID feedback  
**Function:** Controls web tension via elastic model, dancer dynamics, and 1st-order actuator  
**Formulas:** 8-step series chain  
**State Variables:** `T(t)`, `x(t)`, `v_d(t)`, `F_s(t)`, `F_a(t)`  
**Status:** ✅ Complete

### Worker 4 — Fabric Flattening
**Components:** Spreader bar + edge guides + anti-curl rollers  
**Function:** Removes incoming curl, controls edge lateral offset, enforces flatness via beam deflection  
**Formulas:** 8-step series chain  
**State Variables:** `δ_f(t)`, `x_e(t)`, `M(t)`, `c_r(t)`, `F_s(t)`  
**Status:** ✅ Complete

### Worker 5 — Carriage Scanning (X)
**Components:** DC servo motor + timing belt + linear rail + encoder  
**Function:** Triangular scan trajectory, belt tension ratio, rail friction, position PID control  
**Formulas:** 8-step series chain  
**State Variables:** `x(t)`, `v(t)`, `I(t)`, `ω(t)`, `F_b(t)`  
**Status:** ✅ Complete

### Worker 6 — Printhead Array
**Components:** 32× KM1024 heads · 32,768 nozzles · DoD piezoelectric  
**Function:** Oh/We/Z printability · drop ballistic · grayscale · clog tracking  
**Formulas:** 8-step series chain  
**State Variables:** `V_d(t)`, `Oh(t)`, `N_a(t)`, `H(t)`, `x_d(t)`  
**Status:** ✅ Complete

### Worker 7 — Ink Supply ×8 Channels
**Components:** Tank + pump + filter + subtank + damper (8 parallel channels)  
**Function:** Manages manifold pressures, subtank levels, and channel balancing  
**Formulas:** 8-step series chain  
**State Variables:** `V_tank`, `Q_pump`, `dP_filter`, `V_sub`, `P_back`, `level_pct`, `dP_balance`, `flow_rate`  
**Status:** ✅ Complete

### Worker 8 — Nozzle Health Monitor
**Components:** Optical detector + camera + nozzle map + RIP signal  
**Function:** Real-time nozzle status tracking, detects dead/weak/satellite nozzles with RIP compensation  
**Formulas:** 8-step series chain  
**State Variables:** `signal`, `contrast`, `dead_count`, `weak_count`, `health_pct`, `compensation_count`, `failure_rate`, `trend`  
**Status:** ✅ Complete

### Worker 9 — Head Height Adjustment
**Components:** Stepper + lead screw + vertical carriage axis  
**Function:** Manages print head vertical position, gap measurement, mechanical load compensation  
**Formulas:** 8-step series chain  
**State Variables:** `h_current`, `v_vertical`, `T_stepper`, `F_axial`, `h_measured`, `height_error`, `PID_output`, `steps_remaining`  
**Status:** ✅ Complete

### Worker 10 — Maintenance/Capping Station
**Components:** Cap + wiper blade + suction pump  
**Function:** Automated printhead preservation, cap seal force modeling, vacuum-driven suction, CRI tracking  
**Formulas:** 8-step series chain  
**State Variables:** `F_seal`, `P_cap`, `Q_suction`, `V_extracted`, `F_wipe`, `streak_count`, `P_clog`, `CRI`  
**Status:** ✅ Complete

### Worker 11 — RIP/Image Processing Engine
**Components:** CPU/FPGA + ICC + halftoning + firing bitmap  
**Function:** High-speed raster image processor, DPI scaling, color transformation, nozzle compensation  
**Formulas:** 8-step series chain  
**State Variables:** `DPI_out`, `color_error`, `halftone_error`, `compensation_count`, `data_rate`, `buffer_pct`, `latency`, `throughput`  
**Status:** ✅ Complete

### Worker 12 — Dryer
**Components:** 3-phase heating + hot air blower + air knife  
**Function:** Industrial textile dryer, heat transfer, fabric temperature rise, Newton's law drying kinetics  
**Formulas:** 8-step series chain  
**State Variables:** `P_heat`, `Q_transfer`, `T_fabric`, `moisture`, `drying_rate`, `F_air`, `E_total`, `efficiency`  
**Status:** ✅ Complete

### Worker 13 — Rewinder/Winder
**Components:** Servo + torque control + dancer roller  
**Function:** Constant-tension winding system, roll geometry expansion, torque-speed margin tracking  
**Formulas:** 8-step series chain  
**State Variables:** `r_roll`, `J_roll`, `T_cmd`, `T_motor`, `T_web`, `x_dancer`, `omega_winder`, `torque_margin`  
**Status:** ✅ Complete

### Worker 14 — Belt Washing Unit
**Components:** Water spray + rotating brush + air blade dryer  
**Function:** Cleans conveyor belt using spray impact, brush friction, and air blade drying  
**Formulas:** 8-step series chain  
**State Variables:** `Q_spray`, `Re`, `P_impact`, `T_brush`, `P_brush`, `eta_clean`, `cleanliness`, `moisture`  
**Status:** 🚧 In Development

### Worker 15 — Environmental Sensing
**Components:** Temp + humidity sensors + operator alerts  
**Function:** Monitors ambient conditions, validates operating envelope, triggers alerts  
**Formulas:** 8-step series chain  
**State Variables:** `T_amb`, `RH`, `dew_point`, `T_delta`, `RH_delta`, `alert_level`, `uptime`, `compliance`  
**Status:** 🚧 In Development

### Worker 16 — Central Control Panel
**Components:** WYSIWYG UI + job queue + all PID supervision  
**Function:** Master orchestrator, job scheduling, real-time monitoring, fault aggregation  
**Formulas:** 8-step series chain  
**State Variables:** `job_count`, `queue_depth`, `active_workers`, `fault_count`, `uptime`, `throughput`, `efficiency`, `status`  
**Status:** 🚧 In Development

---

## 🧮 Simulation Structure

### Architecture
- **~38 series formulas** (order-dependent, sequential within each worker chain)
- **~23 parallel threads** (independent workers running simultaneously)
- **~250 equations** evaluated per simulation timestep
- **State-space system:** `x' = Ax + Bu`
  - **A matrix** encodes series dependencies
  - **16 workers** = block-diagonal parallel partitions of the matrix

### Coupling Model
The entire machine simulation is a **coupled state-space system** where:
- Each worker = one block in a block-diagonal A matrix
- Inter-worker connections = off-diagonal coupling terms
- `v_downstream` from Worker 1 feeds into Worker 2's input
- Tension from Worker 3 affects Worker 1's PID setpoint
- This coupling makes it a **true digital twin**, not just 16 isolated simulations

---

## 🛠️ Technology Stack

### Symbolic Layer (Physics Solver)
- **Language:** Python / NumPy
- **Storage:** JSON formula database
- **Execution:** Deterministic, real-time capable

### Neural Layer (Orchestration)
- **Agent:** Qwen Code (Qwen3-Coder backbone)
- **Role:** Code generation, orchestration, reasoning about simulation state
- **NOT using:** Raw 2B Qwen instruct model (too small)

### UI Layer (Interactive Widgets)
- **Tech:** HTML5 / CSS3 / JavaScript (Vanilla)
- **Architecture:** One HTML file per worker
- **Features:**
  - Real-time physics simulation (requestAnimationFrame, dt=10ms)
  - Interactive parameter sliders
  - Live canvas charts (4 per worker)
  - SVG schematics with live updates
  - Fault injection panels
  - Formula chain display
  - Dark mode support
  - Mobile responsive

### Parallel Execution
- **Browser:** Web Workers API for true parallel threads
- **Python:** multiprocessing module
- **Worker Pool:** 4 workers per simulation for formula evaluation

---

## 📂 Project Structure

```
faulter-software/
├── README.md                    # This file
├── dashboard.html               # Master dashboard (16 worker cards + river flow)
├── worker1_unwinder.html        # Worker 1 simulation
├── worker2_feed.html            # Worker 2 simulation
├── worker3_tensioning.html      # Worker 3 simulation
├── worker4_flattening.html      # Worker 4 simulation
├── worker5_carriage.html        # Worker 5 simulation
├── worker6_printhead.html       # Worker 6 simulation
├── worker7_inksupply.html       # Worker 7 simulation
├── worker8_nozzlehealth.html    # Worker 8 simulation
├── worker9_headheight.html      # Worker 9 simulation
├── worker10_maintenance.html    # Worker 10 simulation
├── worker11_rip.html            # Worker 11 simulation
├── worker12_dryer.html          # Worker 12 simulation
├── worker13_rewinder.html       # Worker 13 simulation
├── worker14_beltwashing.html    # Worker 14 simulation (in dev)
├── worker15_environmental.html  # Worker 15 simulation (in dev)
└── worker16_control.html        # Worker 16 simulation (in dev)
```

---

## 🚀 Getting Started

### Running the Dashboard
1. Open `dashboard.html` in a modern web browser
2. Click any worker card to open its simulation
3. Use the river flow visualization to see the assembly chain

### Running Individual Workers
1. Open any `workerN_*.html` file directly
2. Click **▶ Play** to start simulation
3. Adjust parameters using sliders
4. Observe live charts and schematic updates
5. Use speed controls (1×, 5×, 10×, 50×) to accelerate simulation

### Simulation Controls
- **Play/Pause:** Start/stop simulation
- **Reset:** Return to initial state
- **Speed:** 1×, 5×, 10×, 50× time acceleration
- **Sliders:** Adjust physical parameters in real-time
- **Formula Chain:** Expand to see all 8 steps with equations

---

## 🎨 UI Design Philosophy

### Visual Language
- **Clean, minimal interface** inspired by Apple design
- **Dark mode support** via CSS prefers-color-scheme
- **Color coding:**
  - 🔵 Blue (#378ADD) — Mechanical/motion
  - 🟢 Green (#1D9E75) — Healthy/optimal
  - 🟠 Amber (#BA7517) — Warning/caution
  - 🔴 Red (#D85A30) — Critical/error

### Layout Pattern (3-column)
- **Left:** Parameter controls (sliders)
- **Center:** Schematic + charts + formula chain
- **Right:** Live state variables with sparklines

### State Card System
- **OK:** Green border
- **Warning:** Amber border + background tint
- **Critical:** Red border + background tint
- **Sparkline:** 50-point mini-chart per variable

---

## 🔬 Key Technical Insights

### Worker 1 Example — Unwinder Formula Chain
8-step series formula chain:
1. **Roll geometry:** `r(t)`, `J(t)`, `m_roll(t)` — radius shrinks as fabric unwinds
2. **Motor electrical:** `L·di/dt = V - IR - K_e·ω`
3. **Brake/motor torque:** `T_net = K_t·I - T_friction - T_load`
4. **Rotational dynamics:** `α = T_net/J`, `ω(t)`, `v_fabric(t)`
5. **Web tension:** `T = E·A·(v_downstream - v_fabric)/v_nominal + T_0`
6. **Dancer roller:** `x_dancer = T/k_spring`
7. **PID controller:** `u(t) = Kp·e + Ki·∫e + Kd·de/dt`
8. **Motor thermal:** `dT_motor/dt` via Newton's cooling + I²R heating

### Parallel vs Sequential Execution
- **Parallel:** Independent formulas within a step (e.g., multiple channel pressures)
- **Sequential:** Order-dependent formulas across steps (e.g., torque → speed → position)
- **Web Workers:** Browser-based parallel execution for formula evaluation

---

## 📊 Simulation Performance

### Target Metrics
- **Timestep:** 10 ms (100 Hz update rate)
- **Real-time factor:** 1× to 50× acceleration
- **Formula evaluations:** ~250 per timestep
- **Chart update:** 60 FPS (requestAnimationFrame)
- **History length:** 300 points (3 seconds at 100 Hz)

### Optimization Strategies
- Web Worker pool (4 workers) for parallel formula execution
- Canvas-based charts (hardware accelerated)
- Efficient state update batching
- Minimal DOM manipulation

---

## 🔮 Future Roadmap

### Phase 1: Complete All 16 Workers ✅ (13/16 done)
- [x] Workers 1-13 complete
- [ ] Worker 14 — Belt Washing
- [ ] Worker 15 — Environmental Sensing
- [ ] Worker 16 — Central Control Panel

### Phase 2: Master Orchestrator
- [ ] Build master orchestrator that runs all 16 workers in parallel
- [ ] Connect workers so outputs of one feed inputs of next (the river)
- [ ] Implement inter-worker coupling (off-diagonal A matrix terms)

### Phase 3: Qwen Code Integration
- [ ] Add Qwen Code as supervisory AI layer on top
- [ ] Implement natural language query interface
- [ ] Enable AI-driven fault diagnosis and optimization

### Phase 4: Final Dashboard
- [ ] Single dashboard showing all 16 workers simultaneously
- [ ] Live fabric river flowing through all stages
- [ ] Real-time performance metrics
- [ ] Fault aggregation and alerting

---

## 📖 References

### Machine Documentation
- Konica Minolta NASSENGER 8 Product Page
- KM1024 Printhead Technical Specification Sheet
- Industrial Inkjet Printing Standards (ISO/IEC)

### Physics & Engineering
- Fluid Mechanics: Hagen-Poiseuille, Reynolds, Bernoulli
- Thermodynamics: Fourier, Newton's Cooling, Arrhenius
- Control Systems: PID, State-Space, Transfer Functions
- Inkjet Physics: Ohnesorge, Weber, Rayleigh

### Software Architecture
- State-Space System Modeling
- Web Workers API (MDN)
- Canvas 2D Rendering (HTML5)
- Neuro-Symbolic AI Architecture

---

## 👥 Team

**Project Lead:** Faulter Wireless — Divine Industries  
**AI Agent:** Amazon Q (Qwen Code orchestration)  
**Target Machine:** Konica Minolta NASSENGER 8

---

## 📄 License

Proprietary — Divine Industries / Faulter Wireless  
All rights reserved.

---

## 🎯 Project Status

**Current Phase:** Phase 1 (13/16 workers complete)  
**Next Milestone:** Complete Workers 14, 15, 16  
**Target Completion:** Q2 2024

---

**Last Updated:** 2024  
**Version:** 1.0.0-alpha
