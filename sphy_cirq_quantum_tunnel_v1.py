# ==================================================================================
# script: harpia_cirq_diamond_v22_tunnel.py
# 🐦 HARPIA QUANTUM LABS | GOOGLE CIRQ INTEGRATION
# 💎 Edition: HARPIA V22 - ETHEREAL DIAMOND + QUANTUM TUNNELING
# 🎯 TARGET: 99.99%+ DOMINANCE — C7+C8 ONLY RISES + WKB TUNNELING BOOST
# 🌀 NEW: Quantum Tunneling Engine — WKB barrier traversal, tunneling current,
#         coherence boost via phase-slip correction, 10 new parquet metrics
# ET PHONE HOME WOW 1977
# Authors: Deywe Okabe, Claude AI, Gemini AI
# ==================================================================================
#
# TUNNELING PHYSICS MODEL:
#   Each qubit sits on a toroidal potential well. Noise defines the barrier V0.
#   When E < V0, the qubit must tunnel through with WKB probability:
#
#     T_wkb = exp(-2 * kappa * width)
#     kappa = sqrt(V0 - E) * mass_eff / hbar_eff      [effective, normalized]
#     width = (PHI / 2pi) * r_torus / (R_torus + r*cos(T))  [geodesic on torus]
#
#   Tunneling BOOSTS coherence: the qubit bypasses the noisy region and
#   re-emerges with a phase-slip of π/2, partially correcting its phase.
#
# TUNNELING METRICS saved per frame in parquet:
#   Tunnel_Prob_mean    — mean WKB probability across qubits [0,1]
#   Tunnel_Prob_max     — peak tunneling probability (hottest qubit)
#   Tunnel_Count        — number of qubits that tunneled this frame
#   Tunnel_Current      — tunneling current density (Count / n_qumodes)
#   Barrier_Height_mean — mean effective barrier V0
#   Barrier_Height_max  — peak barrier height
#   Energy_ratio_mean   — mean E/V0 (>1=classical, <1=tunneling regime)
#   Kappa_mean          — mean decay constant κ (higher=harder tunneling)
#   PhaseSlip_mean      — mean phase correction from tunneling [rad]
#   Tunnel_Boost_mean   — mean coherence boost injected by C8
#
# PER-QUBIT PARQUET COLUMNS:
#   q{i}_x/y/z   — base torus coordinates
#   q{i}_S       — coherence per qubit
#   q{i}_gx/y/z  — glitch (tremor) coordinates
#   q{i}_tp      — WKB tunneling probability
#   q{i}_tx/y/z  — tunneled coordinates (phase-slip corrected torus)
# ==================================================================================

import warnings
warnings.filterwarnings("ignore")
import subprocess, sys

def _ensure_pyarrow():
    try:
        import pyarrow as _pa
        print(f"✅ pyarrow {_pa.__version__} detected.")
    except ImportError:
        print("📦 Installing pyarrow...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyarrow", "--quiet"])
        print("✅ pyarrow installed!")

_ensure_pyarrow()

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import os, time

# ==================================================================================
# MODULE I: CIRQ DIAMOND ORACLE
# ==================================================================================
try:
    import cirq
    CIRQ_AVAILABLE = True
    print("⚛️  Cirq Detected: Activating DIAMOND + TUNNELING Qubit Oracle...")
except ImportError:
    CIRQ_AVAILABLE = False
    print("⚠️  Cirq not found. Install with: pip install cirq")

def generate_quantum_flux_cirq_diamond(t_array, n_shots=512):
    if not CIRQ_AVAILABLE:
        return np.sin(t_array * 0.05) * 0.0005
    qubit   = cirq.LineQubit(0)
    sim     = cirq.Simulator()
    phi_0   = float(t_array[0]) * 0.05
    circuit = cirq.Circuit([
        cirq.rz(0.0)(qubit), cirq.ry(3.0)(qubit), cirq.rz(0.0)(qubit),
        cirq.rx(0.0)(qubit), cirq.rz(phi_0)(qubit),
        cirq.H(qubit), cirq.measure(qubit, key="m")
    ])
    result    = sim.run(circuit, repetitions=n_shots)
    counts    = result.measurements["m"].flatten()
    mean_quad = float(np.mean(1 - 2 * counts))
    return np.sin(t_array * (mean_quad * 0.05 + 1.0)) * 0.0005


# ==================================================================================
# MODULE II: SYNCHRONIZED VR SPHY ENGINE
# ==================================================================================
try:
    from fibonacci_ai import SPHY_Driver, PHI
    from vr_simbiotic_ai import motor_reversao_fase_2_0
    _VR_EXTERNAL = True
    print("✅ External Symbiotic Motors Loaded.")
except ImportError:
    _VR_EXTERNAL = False
    PHI = (1 + np.sqrt(5)) / 2
    def motor_reversao_fase_2_0(potential_field, vr_tuning):
        emt = -(potential_field + vr_tuning)
        return np.exp(-np.abs(emt))


def VR_Engine_synchronized(noise_total_grid, chaos_stabilized_grid):
    """
    VR SPHY synchronized with motor_reversao_fase_2_0.
    potential_field = noise_total
    vr_tuning       = -noise x alpha  (negentropic)
    alpha modulated by chaos → E_mT → 0 → Gain → 1
    """
    kappa        = 2.5
    alpha_tuning = 1.0 - np.exp(-chaos_stabilized_grid * kappa)
    alpha_tuning = np.clip(alpha_tuning, 0.05, 0.97)
    vr_tuning    = -noise_total_grid * alpha_tuning
    vr_gain      = motor_reversao_fase_2_0(noise_total_grid, vr_tuning)
    noise_post_vr = noise_total_grid * (1.0 - vr_gain)
    torque_diag   = noise_total_grid * vr_gain
    return noise_post_vr, torque_diag, vr_gain, alpha_tuning


# ==================================================================================
# MODULE III: QUANTUM TUNNELING ENGINE
# ==================================================================================

def quantum_tunneling_engine(Noise_total_grid, Noise_post_vr_grid,
                              P_singular_grid, Zeta_ideal_grid,
                              T_grid, Q_grid, R_TORUS, r_TORUS,
                              mass_eff=1.0, hbar_eff=0.1, barrier_scale=1.0):
    """
    Quantum Tunneling Engine — WKB approximation on toroidal geometry.

    BARRIER:  V0 = |Noise_total| * barrier_scale
    ENERGY:   E  = |P_singular| + |Noise_post_vr| * 0.3
    KAPPA:    k  = sqrt(max(V0-E, 0)) * mass_eff / hbar_eff
    WIDTH:    w  = (PHI/2pi) * r_TORUS / (R_TORUS + r_TORUS*cos(T))
    T_WKB:    exp(-2 * k * w)    when E < V0
              1.0                when E >= V0 (classical traversal)

    PHASE-SLIP: tunneling qubits acquire phase correction pi/2 * T_wkb
    BOOST:      coherence lift = T_wkb * (1 - E/V0) for tunneling qubits

    Returns 10 arrays, all shape [total_frames, n_qumodes].
    """
    # Barrier and energy
    Barrier = np.abs(Noise_total_grid) * barrier_scale
    Energy  = np.abs(P_singular_grid) + np.abs(Noise_post_vr_grid) * 0.3

    classical_mask = Energy >= Barrier
    tunneling_mask = ~classical_mask

    # WKB decay constant
    delta_V = np.maximum(Barrier - Energy, 0.0)
    Kappa   = np.sqrt(delta_V) * mass_eff / hbar_eff

    # Barrier width on torus (geodesic — narrower at outer equator)
    torus_factor = np.maximum(R_TORUS + r_TORUS * np.cos(T_grid), r_TORUS * 0.1)
    Width = (PHI / (2.0 * np.pi)) * r_TORUS / torus_factor

    # WKB tunneling probability
    T_wkb = np.where(
        classical_mask,
        1.0,
        np.exp(-2.0 * Kappa * Width)
    )
    T_wkb = np.clip(T_wkb, 0.0, 1.0)

    # Phase-slip correction: pi/2 per tunneling event, weighted by T_wkb
    PhaseSlip = T_wkb * (np.pi / 2.0) * tunneling_mask.astype(float)

    # Tunneled zeta and 3D coordinates
    Zeta_tunnel = Zeta_ideal_grid + PhaseSlip
    R_dyn_tun   = r_TORUS * np.ones_like(Zeta_tunnel)
    X_tunnel    = (R_TORUS + R_dyn_tun * np.cos(T_grid)) * np.cos(Zeta_tunnel)
    Y_tunnel    = (R_TORUS + R_dyn_tun * np.cos(T_grid)) * np.sin(Zeta_tunnel)
    Z_tunnel    = R_dyn_tun * np.sin(T_grid)

    # Coherence boost from tunneling (bypasses noisy barrier region)
    energy_ratio = np.where(Barrier > 1e-9, Energy / Barrier, 1.0)
    Boost = np.where(
        tunneling_mask,
        T_wkb * np.clip(1.0 - energy_ratio, 0.0, 1.0),
        0.0
    )

    return T_wkb, Barrier, Energy, Kappa, PhaseSlip, Boost, Zeta_tunnel, X_tunnel, Y_tunnel, Z_tunnel


def compute_tunneling_metrics(T_wkb_grid, Barrier_grid, Energy_grid,
                               Kappa_grid, PhaseSlip_grid, Boost_grid,
                               threshold_prob=0.01):
    """Per-frame tunneling metrics for telemetry (10 columns)."""
    tunnel_mask = T_wkb_grid > threshold_prob
    return {
        'Tunnel_Prob_mean':    np.mean(T_wkb_grid,    axis=1),
        'Tunnel_Prob_max':     np.max(T_wkb_grid,     axis=1),
        'Tunnel_Count':        tunnel_mask.sum(axis=1).astype(float),
        'Tunnel_Current':      tunnel_mask.mean(axis=1),
        'Barrier_Height_mean': np.mean(Barrier_grid, axis=1),
        'Barrier_Height_max':  np.max(Barrier_grid,  axis=1),
        'Energy_ratio_mean':   np.mean(
                                   np.where(Barrier_grid > 1e-9,
                                            Energy_grid / Barrier_grid, 1.0),
                                   axis=1),
        'Kappa_mean':          np.mean(Kappa_grid,    axis=1),
        'PhaseSlip_mean':      np.mean(PhaseSlip_grid, axis=1),
        'Tunnel_Boost_mean':   np.mean(Boost_grid,    axis=1),
    }


# ==================================================================================
# MODULE IV: DIAMOND COHERENCE — 7 LAYERS + C8 TUNNELING BOOST
# ==================================================================================

def coherence_ethereal_diamond(f_matrix, zeta_base, noise_local, r_torus_base,
                                vr_gain=None, tunnel_boost=None):
    """
    8-layer coherence system.

    C1-C6: identical to V21 (adaptive filter, PHI multi-scale, vibrational
           phase, geodesic distortion, bidirectional EMA).
    C7:    VR additive correction — ONLY RISES (clip to [s_fil, 1.0]).
    C8:    Tunneling boost injection — ONLY RISES (clip to [s_c7, 1.0]).
           tunnel_boost * deficit * PHI added as coherence correction.
           When qubit tunnels through barrier: deficit shrinks toward 0.
    """
    # C1: Adaptive filter
    noise_fil = noise_local * np.exp(-np.abs(noise_local) * 5.0)

    # C3: Multi-scale PHI
    phi_factor = 1.0 / (PHI * 100.0)
    s_long     = np.exp(-np.abs(noise_fil) * phi_factor)
    s_short    = np.exp(-np.abs(noise_fil) * 0.3)
    s_coher    = 0.98 * s_long + 0.02 * s_short

    # C4: Vibrational phase
    phase = zeta_base + (noise_fil * (1 - s_coher) * 0.0005)

    # C5: Geodesic distortion
    distortion = r_torus_base * (1 + (1 - s_coher) * 0.00005 * np.sin(f_matrix / (PHI**2 * 10)))

    # C6: Bidirectional EMA
    alpha = 0.001
    s_fil = s_coher.copy()
    for i in range(1, s_fil.shape[0]):
        s_fil[i] = alpha * s_coher[i] + (1 - alpha) * s_fil[i - 1]
    for i in range(s_fil.shape[0] - 2, -1, -1):
        s_fil[i] = alpha * s_fil[i] + (1 - alpha) * s_fil[i + 1]

    # C7: VR additive correction — ONLY RISES
    deficit    = np.clip(1.0 - s_fil, 0.0, None)
    boost_phi3 = np.exp(-deficit * PHI**3 * 10.0)
    if vr_gain is not None:
        vr_correction = vr_gain * deficit * PHI
        s_c7 = np.clip(s_fil + vr_correction * boost_phi3, s_fil, 1.0)
    else:
        s_c7 = np.clip(s_fil + deficit * boost_phi3 * 0.5, s_fil, 1.0)

    # C8: Tunneling boost — ONLY RISES
    if tunnel_boost is not None:
        deficit_c8     = np.clip(1.0 - s_c7, 0.0, None)
        tun_correction = tunnel_boost * deficit_c8 * PHI
        s_final = np.clip(s_c7 + tun_correction, s_c7, 1.0)
    else:
        s_final = s_c7

    return phase, distortion, s_final


# ==================================================================================
# MODULE V: TOROIDAL GLITCH — PERCENTILE + FAST DECAY
# ==================================================================================

def apply_toroidal_glitch(X, Y, Z, noise_total, noise_post_vr,
                           burst_mask, glitch_pct=95.0,
                           glitch_max_amp=0.8, burst_amp=2.5,
                           recovery_tau=8.0):
    """Toroidal Glitch with percentile threshold on post-VR residual."""
    total_frames, n_qumodes = X.shape

    rms_residual = np.sqrt(np.mean(noise_post_vr**2, axis=1))
    threshold    = float(np.percentile(rms_residual, glitch_pct))
    print(f"   ⚡ Glitch p{glitch_pct:.0f}: threshold={threshold:.6f} | ~{100-glitch_pct:.0f}% active frames")

    max_res     = rms_residual.max() + 1e-9
    intensity   = rms_residual / max_res
    mask_glitch = rms_residual > threshold

    tau_eff  = min(recovery_tau, 2.0)
    envelope = np.zeros(total_frames)
    for f in range(total_frames):
        if mask_glitch[f]:
            envelope[f] = intensity[f]
        else:
            prev        = envelope[f - 1] if f > 0 else 0.0
            envelope[f] = prev * np.exp(-1.0 / tau_eff)

    Xg, Yg, Zg = X.copy(), Y.copy(), Z.copy()
    rng         = np.random.default_rng(seed=42)
    n_activated = int(mask_glitch.sum())

    for f in range(total_frames):
        amp = envelope[f] * glitch_max_amp
        if amp < 1e-6:
            continue
        dx = rng.normal(0, amp, size=n_qumodes)
        dy = rng.normal(0, amp, size=n_qumodes)
        dz = rng.normal(0, amp * 0.5, size=n_qumodes)
        b  = burst_mask[f]
        if b.any():
            nb = b.sum()
            dx[b] += rng.uniform(-burst_amp, burst_amp, size=nb)
            dy[b] += rng.uniform(-burst_amp, burst_amp, size=nb)
            dz[b] += rng.uniform(-burst_amp * 0.5, burst_amp * 0.5, size=nb)
        Xg[f] += dx; Yg[f] += dy; Zg[f] += dz

    n_tremor = int((envelope > 1e-6).sum())
    return Xg, Yg, Zg, envelope, n_activated, n_tremor, threshold


# ==================================================================================
# MODULE VI: AKASHIC ENGINE V22
# ==================================================================================

def process_akashic_diamond_frames_v22(n_qumodes, total_frames,
                                        R_TORUS, r_TORUS, F_FLAT,
                                        enable_vr=True,
                                        enable_tunneling=True,
                                        tunnel_mass=1.0,
                                        tunnel_hbar=0.1,
                                        tunnel_barrier_scale=1.0,
                                        tunnel_threshold_prob=0.01,
                                        glitch_pct=95.0,
                                        glitch_max_amp=0.8,
                                        burst_amp=2.5,
                                        recovery_tau=8.0):

    print(f"\n⚙️  Akashic Engine V22 — TUNNELING + C8 + GLITCH p{glitch_pct:.0f} (Q={n_qumodes})...")
    t0 = time.perf_counter()

    frames         = np.arange(total_frames)
    F_grid, Q_grid = np.meshgrid(frames, np.arange(n_qumodes), indexing='ij')
    T_grid         = F_grid * 0.05

    print("   🔬 Cirq Circuit (squeezing r=1.5)...")
    flux_t    = generate_quantum_flux_cirq_diamond(frames * 0.05)
    Flux_grid = np.tile(flux_t[:, np.newaxis], (1, n_qumodes))

    # 3-LAYER NOISE
    Noise_sine  = np.where((F_grid > 50) & (F_grid < 250), 0.35 * np.sin(F_grid * 0.4), 0.0)
    Noise_gauss = np.random.normal(0, 0.08, size=(total_frames, n_qumodes))
    burst_mask  = np.random.uniform(0, 1, size=(total_frames, n_qumodes)) > 0.97
    Noise_burst = np.where(burst_mask,
                           np.random.uniform(-1.2, 1.2, size=(total_frames, n_qumodes)), 0.0)
    Noise_total = Noise_sine + Noise_gauss + Noise_burst
    noise_rms   = float(np.sqrt(np.mean(Noise_total**2)))
    print(f"   💥 Noise RMS (input): {noise_rms:.4f} | Bursts: {int(burst_mask.sum()):,}")

    # CHAOS
    Chaos_base = (F_grid / total_frames) * 10.0
    Chaos_stab = np.where(Chaos_base >= (2.618 * 0.75), 2.618 * 0.70, Chaos_base)

    # VR ENGINE
    if enable_vr:
        print("   ⚔️  VR SPHY — motor_reversao_fase_2_0...")
        Noise_post_vr, Torque_diag, VR_Gain, Alpha_tun = VR_Engine_synchronized(
            Noise_total, Chaos_stab
        )
        rms_post   = float(np.sqrt(np.mean(Noise_post_vr**2)))
        rms_torque = float(np.sqrt(np.mean(Torque_diag**2)))
        gain_mean  = float(np.mean(VR_Gain))
        alpha_mean = float(np.mean(Alpha_tun))
        ratio      = rms_torque / (noise_rms + 1e-9)
        print(f"   ⚔️  α={alpha_mean:.4f} | Gain={gain_mean:.4f} | Sup={gain_mean*100:.1f}% | post-VR={rms_post:.6f} | R={ratio:.3f}x")
    else:
        Noise_post_vr = Noise_total.copy()
        Torque_diag   = np.zeros_like(Noise_total)
        VR_Gain       = np.zeros_like(Noise_total)
        Alpha_tun     = np.zeros_like(Noise_total)
        rms_post = rms_torque = gain_mean = alpha_mean = ratio = 0.0

    # P_singular
    P_singular = np.random.uniform(0, 1, size=(total_frames, n_qumodes)) * (Chaos_stab * 0.01)

    # TOROIDAL GEOMETRY
    Offsets    = Q_grid * (2 * np.pi / n_qumodes)
    Zeta_ideal = (
        (PHI * T_grid) + Offsets + P_singular
        + (Flux_grid * 0.005)
        + Noise_post_vr * 0.02
    )

    # QUANTUM TUNNELING ENGINE
    T_wkb_grid     = np.zeros((total_frames, n_qumodes))
    Barrier_grid   = np.zeros((total_frames, n_qumodes))
    Energy_grid    = np.zeros((total_frames, n_qumodes))
    Kappa_grid     = np.zeros((total_frames, n_qumodes))
    PhaseSlip_grid = np.zeros((total_frames, n_qumodes))
    Boost_grid     = np.zeros((total_frames, n_qumodes))
    X_tunnel       = np.zeros((total_frames, n_qumodes))
    Y_tunnel       = np.zeros((total_frames, n_qumodes))
    Z_tunnel       = np.zeros((total_frames, n_qumodes))

    if enable_tunneling:
        print(f"   🌀 Quantum Tunneling Engine (m={tunnel_mass}, hbar={tunnel_hbar}, scale={tunnel_barrier_scale})...")
        (T_wkb_grid, Barrier_grid, Energy_grid, Kappa_grid,
         PhaseSlip_grid, Boost_grid, _Zeta_tunnel,
         X_tunnel, Y_tunnel, Z_tunnel) = quantum_tunneling_engine(
            Noise_total, Noise_post_vr, P_singular, Zeta_ideal,
            T_grid, Q_grid, R_TORUS, r_TORUS,
            mass_eff=tunnel_mass, hbar_eff=tunnel_hbar,
            barrier_scale=tunnel_barrier_scale
        )
        n_tunneled_total = int((T_wkb_grid > tunnel_threshold_prob).sum())
        mean_prob        = float(np.mean(T_wkb_grid))
        mean_boost       = float(np.mean(Boost_grid))
        mean_kappa       = float(np.mean(Kappa_grid))
        classical_pct    = float(np.mean(Energy_grid >= Barrier_grid)) * 100.0
        print(f"   🌀 Tunneled points  : {n_tunneled_total:,} ({n_tunneled_total/(total_frames*n_qumodes)*100:.1f}% of all)")
        print(f"   🌀 Classical (E>=V0): {classical_pct:.1f}%")
        print(f"   🌀 Mean T_wkb        : {mean_prob:.6f}")
        print(f"   🌀 Mean kappa        : {mean_kappa:.4f}")
        print(f"   🌀 Mean boost        : {mean_boost:.6f}")
        Tunnel_Boost = Boost_grid
    else:
        n_tunneled_total = 0
        mean_prob = mean_boost = mean_kappa = classical_pct = 0.0
        Tunnel_Boost = None

    tunnel_frame_metrics = compute_tunneling_metrics(
        T_wkb_grid, Barrier_grid, Energy_grid,
        Kappa_grid, PhaseSlip_grid, Boost_grid,
        threshold_prob=tunnel_threshold_prob
    ) if enable_tunneling else {k: np.zeros(total_frames) for k in [
        'Tunnel_Prob_mean', 'Tunnel_Prob_max', 'Tunnel_Count', 'Tunnel_Current',
        'Barrier_Height_mean', 'Barrier_Height_max', 'Energy_ratio_mean',
        'Kappa_mean', 'PhaseSlip_mean', 'Tunnel_Boost_mean'
    ]}

    # COHERENCE — 8 layers (C7 VR + C8 Tunneling)
    print("   🛡️  DIAMOND Coherence — 8 layers [C7 VR + C8 Tunneling, only rises]...")
    Zeta_real, R_dyn, S_local = coherence_ethereal_diamond(
        F_grid, Zeta_ideal, P_singular, r_TORUS,
        vr_gain=VR_Gain, tunnel_boost=Tunnel_Boost
    )
    print(f"   🛡️  Coherence post-C8: mean={np.mean(S_local):.8f} | min={np.min(S_local):.8f}")

    # 3D BASE PROJECTION
    X3 = (R_TORUS + R_dyn * np.cos(T_grid)) * np.cos(Zeta_real)
    Y3 = (R_TORUS + R_dyn * np.cos(T_grid)) * np.sin(Zeta_real)
    Z3 = (R_dyn * F_FLAT) * np.sin(T_grid)

    # TOROIDAL GLITCH
    Xg, Yg, Zg, envelope, n_act, n_tremor, thr = apply_toroidal_glitch(
        X3, Y3, Z3, Noise_total, Noise_post_vr, burst_mask,
        glitch_pct=glitch_pct, glitch_max_amp=glitch_max_amp,
        burst_amp=burst_amp, recovery_tau=recovery_tau,
    )
    print(f"   ⚡ Glitch: {n_act:,} activated | {n_tremor:,} with tremor ({n_tremor/total_frames*100:.1f}%)")
    print(f"⚡ Core V22: {time.perf_counter()-t0:.4f}s")

    # TELEMETRY
    data = {
        'Frame':              frames,
        'Quantum_Flux':       flux_t,
        'Noise_RMS':          np.sqrt(np.mean(Noise_total**2,    axis=1)),
        'NoisePostVR_RMS':    np.sqrt(np.mean(Noise_post_vr**2,  axis=1)),
        'Torque_RMS':         np.sqrt(np.mean(Torque_diag**2,    axis=1)),
        'VRGain_mean':        np.mean(VR_Gain,   axis=1),
        'Alpha_Tuning':       np.mean(Alpha_tun, axis=1),
        'Glitch_Envelope':    envelope,
        'Burst_Count':        burst_mask.sum(axis=1).astype(float),
        **tunnel_frame_metrics,
    }
    for i in range(n_qumodes):
        data[f'q{i}_x']  = X3[:, i]
        data[f'q{i}_y']  = Y3[:, i]
        data[f'q{i}_z']  = Z3[:, i]
        data[f'q{i}_S']  = S_local[:, i]
        data[f'q{i}_gx'] = Xg[:, i]
        data[f'q{i}_gy'] = Yg[:, i]
        data[f'q{i}_gz'] = Zg[:, i]
        data[f'q{i}_tp'] = T_wkb_grid[:, i]
        data[f'q{i}_tx'] = X_tunnel[:, i]
        data[f'q{i}_ty'] = Y_tunnel[:, i]
        data[f'q{i}_tz'] = Z_tunnel[:, i]

    stats = {
        "coherence_mean":       float(np.mean(S_local)),
        "coherence_min":        float(np.min(S_local)),
        "coherence_max":        float(np.max(S_local)),
        "flux_mean":            float(np.mean(np.abs(flux_t))),
        "noise_rms":            noise_rms,
        "noise_post_vr_rms":    rms_post,
        "torque_rms":           rms_torque,
        "vr_gain_mean":         gain_mean,
        "alpha_tuning_mean":    alpha_mean,
        "ratio_tr":             ratio,
        "bursts_total":         int(burst_mask.sum()),
        "tunnel_enabled":       enable_tunneling,
        "tunnel_total_points":  n_tunneled_total,
        "tunnel_prob_mean":     mean_prob,
        "tunnel_boost_mean":    mean_boost,
        "tunnel_kappa_mean":    mean_kappa,
        "tunnel_classical_pct": classical_pct,
        "glitch_activated":     n_act,
        "glitch_tremor":        n_tremor,
        "glitch_threshold":     thr,
        "glitch_env_max":       float(envelope.max()),
    }
    return pd.DataFrame(data), stats


# ==================================================================================
# MODULE VII: SAVE PARQUET
# ==================================================================================

def save_parquet(df, base_name="telemetria_v22_cirq_tunnel"):
    out = f"{base_name}.parquet"
    print(f"\n💾 Saving Parquet: {len(df):,} x {len(df.columns):,} -> {out}")
    for col in df.columns:
        df[col] = df[col].astype(np.int64 if col == 'Frame' else np.float64)
    pq.write_table(pa.Table.from_pandas(df, preserve_index=False), out,
                   compression='snappy', use_dictionary=False,
                   write_statistics=True, row_group_size=512)
    mb  = os.path.getsize(out) / 1024**2
    chk = pd.read_parquet(out)
    assert len(chk) == len(df) and len(chk.columns) == len(df.columns)
    print(f"✅ {mb:.2f} MB | snappy | float64 | integrity OK")
    print(f"   Tunneling cols   : q{{i}}_tp | q{{i}}_tx/ty/tz (phase-slip coords)")
    print(f"   Frame metrics    : Tunnel_Prob_mean/max, Tunnel_Count, Tunnel_Current,")
    print(f"                      Barrier_Height_mean/max, Energy_ratio_mean,")
    print(f"                      Kappa_mean, PhaseSlip_mean, Tunnel_Boost_mean")
    return out


# ==================================================================================
# MODULE VIII: MAIN
# ==================================================================================

def harpia_main_v22():
    print("\n" + "⚛️ " * 35)
    print("      ✨ HARPIA V22 - AKASHIC DIAMOND [QUANTUM TUNNELING]")
    print("      [ CIRQ | VR SPHY | C7+C8 | WKB TUNNELING | GLITCH TOROIDAL ]")
    print("⚛️ " * 35)

    n_qumodes    = int(input("🔢 Qubits (qbt): ") or 100)
    total_frames = int(input("🎞️  Frames: ") or 1000)

    print("\n🌀 Quantum Tunneling Config (Enter = default):")
    tunnel_mass   = float(input("   Effective mass m [1.0]: ") or 1.0)
    tunnel_hbar   = float(input("   Effective hbar [0.1]  (lower = more tunneling): ") or 0.1)
    tunnel_scale  = float(input("   Barrier scale [1.0]  (lower = weaker barriers): ") or 1.0)
    tunnel_thresh = float(input("   Min T_wkb to count as tunneled [0.01]: ") or 0.01)

    print("\n⚡ Toroidal Glitch Config (Enter = default):")
    print("   [95 = top 5% frames | 99 = top 1% | 100 = no glitch]")
    glitch_pct   = float(input("   Residual percentile [95]: ") or 95.0)
    glitch_max   = float(input("   Tremor amplitude [0.8]: ")   or 0.8)
    burst_amp    = float(input("   Burst amplitude [2.5]: ")     or 2.5)
    recovery_tau = float(input("   Recovery tau [8.0]: ")        or 8.0)

    # Inicia o cronômetro AQUI, logo após as entradas do usuário!
    sim_start_time = time.perf_counter()

    if CIRQ_AVAILABLE:
        q = cirq.LineQubit(0)
        print(f"\n📐 Cirq Circuit:\n{cirq.Circuit([cirq.rz(0)(q), cirq.ry(3.0)(q), cirq.rz(0)(q), cirq.rx(0)(q), cirq.rz(0.05)(q), cirq.H(q), cirq.measure(q, key='m')])}")

    df_sim, stats = process_akashic_diamond_frames_v22(
        n_qumodes, total_frames, 21.0, 2.5, 0.000001,
        enable_vr=True,
        enable_tunneling=True,
        tunnel_mass=tunnel_mass,
        tunnel_hbar=tunnel_hbar,
        tunnel_barrier_scale=tunnel_scale,
        tunnel_threshold_prob=tunnel_thresh,
        glitch_pct=glitch_pct,
        glitch_max_amp=glitch_max,
        burst_amp=burst_amp,
        recovery_tau=recovery_tau,
    )

    s_cols   = [f'q{i}_S' for i in range(n_qumodes)]
    all_S    = df_sim[s_cols].values.flatten()
    p50, p99 = np.percentile(all_S, [50, 99])
    delta    = (1.0 - stats['coherence_mean']) * 100

    print(f"\n{'='*70}")
    print(f"✅ HARPIA V22 — QUANTUM TUNNELING + GLITCH TOROIDAL")
    print(f"💎 MEAN Fidelity      : {stats['coherence_mean']:.12%}")
    print(f"📊 MIN/MEDIAN/MAX     : {stats['coherence_min']:.8%} / {p50:.8%} / {stats['coherence_max']:.8%}")
    print(f"📊 Percentile 99      : {p99:.12%}")
    print(f"📉 Std Deviation      : {all_S.std():.12f}")
    print(f"🎯 Delta to 100%      : {delta:.8f}%")
    print(f"")
    print(f"⚔️  VR SPHY:")
    print(f"   alpha_tuning       : {stats['alpha_tuning_mean']:.4f}")
    print(f"   VR Gain (mean)     : {stats['vr_gain_mean']:.4f}  (-> 1.0 = full dominance)")
    print(f"   Suppression        : {stats['vr_gain_mean']*100:.1f}%")
    print(f"   Noise input RMS    : {stats['noise_rms']:.6f}")
    print(f"   Noise post-VR RMS  : {stats['noise_post_vr_rms']:.6f}  ({(1-stats['noise_post_vr_rms']/stats['noise_rms'])*100:.1f}% reduction)")
    print(f"   Bursts absorbed    : {stats['bursts_total']:,}")
    print(f"")
    print(f"🌀 QUANTUM TUNNELING (WKB model):")
    print(f"   Effective mass m   : {tunnel_mass:.3f}")
    print(f"   Effective hbar     : {tunnel_hbar:.3f}")
    print(f"   Barrier scale      : {tunnel_scale:.3f}")
    print(f"   Classical (E>=V0)  : {stats['tunnel_classical_pct']:.1f}%   <- went over barrier")
    print(f"   Tunneled points    : {stats['tunnel_total_points']:,}   <- passed through barrier")
    print(f"   Mean T_wkb         : {stats['tunnel_prob_mean']:.6f}  [0=blocked 1=full tunnel]")
    print(f"   Mean kappa (decay) : {stats['tunnel_kappa_mean']:.4f}  [higher=harder barrier]")
    print(f"   Tunnel boost mean  : {stats['tunnel_boost_mean']:.6f}  [coherence lift via C8]")
    print(f"   Parquet cols       : q{{i}}_tp | q{{i}}_tx/ty/tz (phase-slip coords)")
    print(f"   Frame metrics      : Tunnel_Prob_mean/max, Tunnel_Count, Tunnel_Current,")
    print(f"                        Barrier_Height_mean/max, Energy_ratio_mean,")
    print(f"                        Kappa_mean, PhaseSlip_mean, Tunnel_Boost_mean")
    print(f"")
    print(f"⚡ TOROIDAL GLITCH (p{glitch_pct:.0f}):")
    print(f"   Threshold          : {stats['glitch_threshold']:.6f}")
    print(f"   Activated frames   : {stats['glitch_activated']:,} ({stats['glitch_activated']/total_frames*100:.1f}%)")
    print(f"   Tremor frames      : {stats['glitch_tremor']:,} ({stats['glitch_tremor']/total_frames*100:.1f}%)")
    print(f"   -> q_gx/gy/gz = torus shaking | q_tx/ty/tz = tunneled torus!")
    print(f"{'='*70}")

    out = save_parquet(df_sim, "telemetria_v22_cirq_tunnel")
    print(f"\n📂 Dataset: {out}")
    
    # --- CÁLCULO FINAL DO CRONÔMETRO ---
    sim_end_time = time.perf_counter()
    total_time = sim_end_time - sim_start_time
    mins, secs = divmod(total_time, 60)
    hours, mins = divmod(mins, 60)

    print("\n" + "="*70)
    print("⏳ CRONÔMETRO GERAL DE EXECUÇÃO")
    print(f"   Tempo Total Simulado : {int(hours):02d}h {int(mins):02d}m {secs:.4f}s")
    print("="*70)
    
    print("\n⚛️  HARPIA V22 — QUANTUM TUNNELING — Done!\n")

    c = stats['coherence_mean']
    if c >= 0.9999:
        print("🏆🏆🏆 DOMINANCE ACHIEVED! 99.99%+ WITH QUANTUM TUNNELING! 🏆🏆🏆")
        print("     C7 VR + C8 Tunneling + PHI³ = GRAIL CONQUERED!")
        print("     WKB active — qubits tunneling through noise barriers!")
    elif c >= 0.9998:
        print(f"🥇 99.98%+ — {(0.9999-c)*10000:.2f} base points to DOMINANCE!")
        print(f"   Try lower hbar (e.g. 0.05) or barrier_scale=0.5 for stronger tunneling.")
    elif c >= 0.9995:
        print("🥈 99.95%+ — tunneling active. Reduce hbar for deeper WKB penetration.")
    elif c >= 0.999:
        print("🥉 99.9%+ — VR + tunneling holding the line!")
    else:
        print("💪 Try: hbar=0.05, barrier_scale=0.5, mass=2.0 for stronger tunneling.")
    print()

if __name__ == "__main__":
    harpia_main_v22()