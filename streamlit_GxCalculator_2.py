import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Constants
gamma = 2 * np.pi * 42.58e6  # rad/s/T
Gmax = 0.5                   # T/m
slew_rate = 3440             # T/m/s

st.title("🔊 Readout Gradient Lobe Visualizer")

# Sliders
BW = st.slider("Bandwidth (kHz)", 10.0, 1000.0, 250.0) * 1e3
FOV_mm = st.slider("FOV (mm)", 0.1, 200.0, 100.0)
Nx = st.slider("Matrix Size (Nx)", 16, 512, 128)

# Derived
FOV = FOV_mm / 1e3
dwell = 1 / BW
Tread = Nx * dwell
Gread = (BW * 2 * np.pi) / (gamma * FOV)
res = FOV / Nx
BW_limit = Gmax * gamma * FOV / (2 * np.pi)

# Output values
st.markdown(f"**Gread:** {Gread*1e3:.3f} mT/m")
st.markdown(f"**Δt:** {dwell*1e6:.2f} µs")
st.markdown(f"**Tread:** {Tread*1e3:.2f} ms")
st.markdown(f"**Resolution:** {res*1e3:.3f} mm")

if BW > BW_limit:
    st.error(f"Gread exceeds hardware limit! (Max BW ≈ {BW_limit/1e3:.1f} kHz)")
else:
    st.success("Gread is within hardware limits.")

# Ramp time
Tramp = Gread / slew_rate
dt = 1e-6  # simulation time resolution

# Time vectors
t_ramp_up = np.arange(0, Tramp, dt)
t_flat = np.arange(Tramp, Tramp + Tread, dt)
t_ramp_down = np.arange(Tramp + Tread, 2*Tramp + Tread, dt)
t_all = np.concatenate([t_ramp_up, t_flat, t_ramp_down])

# Waveform
g_up = Gread * (t_ramp_up / Tramp)
g_flat = np.ones_like(t_flat) * Gread
g_down = Gread * (1 - (t_ramp_down - (Tramp + Tread)) / Tramp)
g_all = np.concatenate([g_up, g_flat, g_down])

# Plot
fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(t_all * 1e3, g_all * 1e3)
ax.set_title("Gradient Lobe Shape (Readout)")
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Gradient Amplitude (mT/m)")
ax.grid(True)

st.pyplot(fig)
