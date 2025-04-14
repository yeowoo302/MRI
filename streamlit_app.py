import streamlit as st
import numpy as np

gamma = 2 * np.pi * 42.58e6  # rad/s/T
Gmax = 0.5  # T/m

st.title("Interactive G₍read₎ Calculator")

BW = st.slider("Bandwidth (kHz)", 10.0, 1000.0, 250.0) * 1e3
FOV_mm = st.slider("FOV (mm)", 0.1, 200.0, 100.0)
Nx = st.slider("Matrix Size (Nx)", 16, 512, 128)

FOV = FOV_mm / 1e3
dwell = 1 / BW
Tread = Nx * dwell
Gread = (BW * 2 * np.pi) / (gamma * FOV)
res = FOV / Nx
BW_limit = Gmax * gamma * FOV / (2 * np.pi)

st.markdown(f"**Gread:** {Gread * 1e3:.3f} mT/m")
st.markdown(f"Dwell time (Δt): {dwell * 1e6:.2f} µs")
st.markdown(f"Readout time (Tread): {Tread * 1e3:.2f} ms")
st.markdown(f"Resolution: {res * 1e3:.3f} mm")

if BW > BW_limit:
    st.error(f"⚠️ Gread exceeds limit! (limit BW ≈ {BW_limit/1e3:.1f} kHz)")
else:
    st.success("Gread is within safe range.")
