import os
import re
import sys

def process_worker(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Check if already injected
    if 'LAYER A — Power Electronics' in content or 'power_electronics' in content:
        return

    # Add Params
    params_inject = """  // LAYER A-E Energy Chain Params
  D_pwm: 0.5, V_bus_nom: 600, t_r: 1e-7, t_f: 1e-7, f_sw: 10000, C_gate: 1e-9, V_gs: 15, R_bus: 0.1, V_line: 400,
  k_h: 0.01, k_e: 0.001, B_field: 1.5, f_elec: 50,
  efficiency: 0.9, N_teeth: 50, N_balls: 8, d_ball: 0.01, D_pitch: 0.05, alpha_contact: 0, I_nominal: 10,
  L_shaft: 1.0, G_shear: 79e9, J_polar: 1e-4, L_belt: 2.0, E_belt: 1e9, A_belt: 0.001, eta_gear: 0.98, F_radial: 500, r_bearing: 0.02, k_shaft: 1e6, J_shaft: 0.05,
  L_span: 1.0, k_fabric: 0.5, A_heat: 1.0, gamma_ink: 0.03, r_nozzle: 1e-5, C_piezo: 1e-6, V_drive: 50,
  T_load: 10, K_t: 1.5, K_e: 1.5, L_motor: 0.05, R_motor: 0.5,"""
    content = re.sub(r'(const PARAMS = \{)', r'\1\n' + params_inject, content)

    # Add State
    state_inject = """  I_env: 0, delta_I: 0, fault_stall: false, fault_overcurrent: false,"""
    content = re.sub(r'(const state = \{)', r'\1\n' + state_inject, content)

    # Add Hist/Spark
    hist_inject = """hist.I_signature = []; spark.I_signature = [];"""
    content = re.sub(r'(const hist = \{.*?;.*?)\n', r'\1\n' + hist_inject + '\n', content)

    push_inject = """  pushHist(hist.I_signature, s.I_env || 0); pushSpark(spark.I_signature, s.I_env || 0);"""
    # Insert at the end of tick() before the closing brace
    # Wait, some workers have different tick structures. We'll append to tick() later.

    # Add Worker Code
    worker_inject = """
    case 'power_electronics': // LAYER A
      result = {
        V_dc: 1.35 * p.V_line,
        V_bus: p.V_line * 1.35 - (p.I_load || 0) * p.R_bus,
        D: p.V_input ? p.V_input / (p.V_line * 1.35 + 1e-6) : 0.5,
        P_sw: 0.5 * (p.V_line * 1.35) * (p.I_load || 0) * (p.t_r + p.t_f) * p.f_sw,
        E_gate: 0.5 * p.C_gate * p.V_gs * p.V_gs
      };
      break;
    case 'motor_electrical_adv': // LAYER B
      let V_back_emf = p.K_e * (p.omega || 0);
      result = {
        delta_I: ((p.V_bus || 600) - V_back_emf) * p.D * (1/p.f_sw) / p.L_motor,
        P_elec: (p.V_input || 0) * (p.I_load || 0),
        P_cu: (p.I_load || 0) * (p.I_load || 0) * p.R_motor,
        P_fe: p.k_h * p.f_elec * p.B_field * p.B_field + p.k_e * p.f_elec * p.f_elec * p.B_field * p.B_field
      };
      break;
    case 'current_signature': // LAYER C
      let rpm = (p.omega || 0) * 60 / (2 * Math.PI);
      result = {
        I_env: p.T_load / (p.K_t * p.efficiency),
        f_mesh: p.N_teeth * rpm / 60,
        f_bpfo: (p.N_balls / 2) * (rpm / 60) * (1 - (p.d_ball / p.D_pitch) * Math.cos(p.alpha_contact)),
        THD_i: 0.05
      };
      break;
    case 'mechanical_drive': // LAYER D
      result = {
        theta_twist: (p.T_net || 0) * p.L_shaft / (p.G_shear * p.J_polar),
        delta_belt: (p.F_belt || 0) * p.L_belt / (p.E_belt * p.A_belt),
        P_gear: (p.T_net || 0) * (p.omega || 0) * (1 - p.eta_gear),
        T_bearing: p.mu_b * p.F_radial * p.r_bearing,
        omega_crit: Math.sqrt(p.k_shaft / p.J_shaft)
      };
      break;
    case 'load_energy': // LAYER E
      result = {
        E_tension: 0.5 * (p.T_tension || 0)**2 * p.L_span / (p.E_fabric * p.A_fabric),
        P_nip: (p.F_nip || 0) / (2 * (p.r_roller || 0.1) * (p.w_fabric || 1)),
        Q_fabric: p.k_fabric * p.A_heat * (p.dT_dx || 0),
        E_meniscus: Math.PI * p.r_nozzle**2 * p.gamma_ink,
        E_piezo: 0.5 * p.C_piezo * p.V_drive**2
      };
      break;
"""
    content = re.sub(r"(switch\s*\(fn\)\s*\{)", r'\1' + worker_inject, content)

    # Add to tick()
    tick_inject = """
  // ── LAYER A-E: Energy Chain (Parallel) ──
  const [resA, resB, resC, resD, resE] = await execParallel([
    { fn: 'power_electronics', params: { V_line: p.V_line, I_load: s.I_motor || s.I_load || 0, R_bus: p.R_bus, V_input: s.V_input || 0, t_r: p.t_r, t_f: p.t_f, f_sw: p.f_sw, C_gate: p.C_gate, V_gs: p.V_gs } },
    { fn: 'motor_electrical_adv', params: { K_e: p.K_e, omega: s.omega || 0, V_bus: 600, D: 0.5, f_sw: p.f_sw, L_motor: p.L_motor, V_input: s.V_input || 0, I_load: s.I_motor || s.I_load || 0, R_motor: p.R_motor, k_h: p.k_h, f_elec: p.f_elec, B_field: p.B_field, k_e: p.k_e } },
    { fn: 'current_signature', params: { omega: s.omega || 0, T_load: p.T_load, K_t: p.K_t, efficiency: p.efficiency, N_teeth: p.N_teeth, N_balls: p.N_balls, d_ball: p.d_ball, D_pitch: p.D_pitch, alpha_contact: p.alpha_contact } },
    { fn: 'mechanical_drive', params: { T_net: s.T_net || 0, L_shaft: p.L_shaft, G_shear: p.G_shear, J_polar: p.J_polar, F_belt: s.F_belt || 0, L_belt: p.L_belt, E_belt: p.E_belt, A_belt: p.A_belt, omega: s.omega || 0, eta_gear: p.eta_gear, mu_b: p.mu_b || 0.01, F_radial: p.F_radial, r_bearing: p.r_bearing, k_shaft: p.k_shaft, J_shaft: p.J_shaft } },
    { fn: 'load_energy', params: { T_tension: s.T_tension || 0, L_span: p.L_span, E_fabric: p.E_fabric || 1e9, A_fabric: p.A_fabric || 0.001, F_nip: s.F_nip || 0, r_roller: p.r_roller || 0.1, w_fabric: p.w_fabric || 1, k_fabric: p.k_fabric, A_heat: p.A_heat, dT_dx: s.dT_dx || 0, r_nozzle: p.r_nozzle, gamma_ink: p.gamma_ink, C_piezo: p.C_piezo, V_drive: p.V_drive } }
  ]);
  s.I_env = resC.I_env;
  s.delta_I = resB.delta_I;
  if (s.fault_stall) s.I_env *= 2.5; // Stall injection
  if (s.fault_overcurrent) s.I_env *= 1.5; // Overcurrent injection
  
  if (typeof hist !== 'undefined' && hist.I_signature) {
     pushHist(hist.I_signature, s.I_env);
     if (typeof spark !== 'undefined' && spark.I_signature) pushSpark(spark.I_signature, s.I_env);
  }
"""
    # Insert before the last closing brace of tick
    # Finding the end of tick is tricky. We can look for `s.tickCount++;` or similar.
    # We will just replace `s.tickCount++;` with our injection + `s.tickCount++;`
    content = re.sub(r'(s\.tickCount\+\+;)', tick_inject + r'\n  \1', content)

    # Add HTML Chart
    chart_html = """
      <div class="chart-card">
        <div class="chart-title">Current Signature i(t) <span class="ct-value" id="ct_I_sig" style="color:#BA7517">—</span></div>
        <div class="chart-canvas-wrap"><canvas id="chart_signature" height="130"></canvas></div>
      </div>
"""
    content = re.sub(r'(<div class="charts-grid">)', r'\1\n' + chart_html, content)

    # Add Chart render
    render_inject = """
  const sigCanvas = document.getElementById('chart_signature');
  if (sigCanvas && typeof drawChart === 'function' && hist.I_signature) {
     drawChart('chart_signature', hist.I_signature, '#BA7517');
     const ct_I_sig = document.getElementById('ct_I_sig');
     if (ct_I_sig) ct_I_sig.textContent = (state.I_env || 0).toFixed(2) + ' A';
  }
"""
    content = re.sub(r'(function render\(\)\s*\{)', r'\1\n' + render_inject, content)

    # Write back
    with open(filepath, 'w') as f:
        f.write(content)

process_worker('/Users/mac/Desktop/DIVINE INDUSTRIES/faulter-wireless/faulter-software/worker13_rewinder.html')
print("Injected into worker13!")
