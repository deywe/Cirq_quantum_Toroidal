# ==================================================================================
# 🐦 HARPIA QUANTUM LABS - PLAYER EDITION (PARQUET & CSV SUPPORT)
# 💎 Edition: ETHEREAL DIAMOND v8.1 (Universal Loader)
# ----------------------------------------------------------------------------------
# "Suporte nativo para datasets Parquet (Strawberry Fields / Akashic)."
# ==================================================================================

import matplotlib
try:
    matplotlib.use('Qt5Agg')
except:
    matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
import sys
import warnings
import os

# Silencia avisos de fontes para manter o terminal limpo
warnings.filterwarnings("ignore", category=UserWarning)

def harpia_player_v8(file_path="telemetria_v21_diamond_perfect.parquet"):
    print(f"\n[LOADING] Detectando formato de: {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"❌ Erro: Arquivo '{file_path}' não encontrado.")
        return

    try:
        # Lógica de detecção de extensão
        if file_path.endswith('.parquet'):
            print("⚡ Formato Parquet detectado. Usando motor PyArrow...")
            df_sim = pd.read_parquet(file_path)
        else:
            print("📄 Formato CSV detectado. Carregando...")
            df_sim = pd.read_csv(file_path)
            
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return

    # Mapeamento de colunas (Suporte para nomes q ou qumode)
    qubit_cols = [col for col in df_sim.columns if col.endswith('_x')]
    n_qubits = len(qubit_cols)
    total_frames = len(df_sim)

    # Parâmetros Geométricos Harpia
    R_TORO, r_TORO, F_ACHAT = 21.0, 2.5, 0.000001
    
    print(f"[OK] Pontos Quânticos: {n_qubits} | Frames: {total_frames}")

    fig = plt.figure(figsize=(16, 12), facecolor='#050505')
    ax = fig.add_subplot(111, projection='3d', facecolor='#050505')
    ax.axis('off')
    ax.set_box_aspect([1, 1, 0.3]) 

    # Renderização do Wireframe do Toro
    u, v = np.mgrid[0:2*np.pi:100j, 0:2*np.pi:50j]
    x_t = (R_TORO + r_TORO * np.cos(v)) * np.cos(u)
    y_t = (R_TORO + r_TORO * np.cos(v)) * np.sin(u)
    z_t = (r_TORO * F_ACHAT) * np.sin(v)
    ax.plot_wireframe(x_t, y_t, z_t, color='#00FFFF', alpha=0.15, linewidth=0.4)

    alpha_val = 0.4 if n_qubits > 500 else 0.8
    marker_size = 2 if n_qubits > 500 else 6
    cores = plt.cm.cool(np.linspace(0, 1, n_qubits))
    
    lasers = [ax.plot([], [], [], color=cores[i], lw=1.0, alpha=alpha_val)[0] for i in range(n_qubits)]
    pontos = [ax.plot([], [], [], 'o', color='white', markersize=marker_size, alpha=1.0)[0] for i in range(n_qubits)]
    
    texto_info = ax.text2D(0.02, 0.98, '', transform=ax.transAxes, 
                           color='white', fontsize=11, fontfamily='monospace', weight='bold')

    def update(frame):
        row = df_sim.iloc[frame]
        
        # Lógica de Status Baseada na Telemetria
        if abs(row.get('Ruido_Vibracional', 0)) > 0.3:
            status_cor, status_txt = '#FF0055', "!! INERTIA LOCK !!"
        elif row.get('Caos_Fenix', 0) < 0.9 * row.get('Caos_Original', 1): 
            status_cor, status_txt = '#00FFFF', "<> FENIX DIAMOND <>"
        else:
            status_cor, status_txt = '#FFFFFF', ">> VR ETHEREAL <<"
        
        s_cols = [col for col in df_sim.columns if col.endswith('_S')]
        s_medio = row[s_cols].mean() if s_cols else 1.0

        texto_info.set_text(
            f"[{status_txt}]\n"
            f"SOURCE: {os.path.basename(file_path)}\n"
            f"FRAME: {frame}/{total_frames}\n"
            f"FIDELIDADE: {s_medio:.4%} | NODES: {n_qubits}"
        )
        texto_info.set_color(status_cor)
        
        # Otimização de rastro (Trails)
        lookback_val = 5 if n_qubits > 200 else 15
        lookback = max(0, frame - lookback_val)
        trail = df_sim.iloc[lookback:frame+1]
        
        for i in range(n_qubits):
            lasers[i].set_data(trail[f'q{i}_x'], trail[f'q{i}_y'])
            lasers[i].set_3d_properties(trail[f'q{i}_z'])
            
            pontos[i].set_data([row[f'q{i}_x']], [row[f'q{i}_y']])
            pontos[i].set_3d_properties([row[f'q{i}_z']])
        
        ax.view_init(elev=35, azim=frame * 0.5)
        return lasers + pontos + [texto_info]

    fig.suptitle(
        'HARPIA QUANTUM PLAYER v8.1\n' +
        f'OFFLINE DATASET VISUALIZER | N={n_qubits}',
        color='white', fontsize=14, fontweight='bold', y=0.96
    )

    ani = FuncAnimation(fig, update, frames=total_frames, interval=20, blit=False)
    plt.show()

if __name__ == "__main__":
    # Agora você pode passar qualquer um dos dois como argumento
    # Ex: python player.py telemetria_v18_sf.parquet
    file_target = sys.argv[1] if len(sys.argv) > 1 else "telemetria_v21_cirq_diamond.parquet"
    harpia_player_v8(file_target)