import streamlit as st
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector

st.set_page_config(page_title="Quantum Entanglement Visualizer", layout="centered")
st.title("🔗 Quantum Entanglement Visualizer")

st.markdown("""
This app demonstrates **entanglement**: two qubits become linked so that measuring one instantly tells you about the other.
""")

# Build quantum circuit
qc = QuantumCircuit(2, 2)
qc.h(0)      # (1) Superposition on qubit 0
qc.cx(0, 1)  # (2) Entangle qubit 1 with qubit 0
qc.measure(0, 0)
qc.measure(1, 1)

st.markdown("### ⚙️ Quantum Circuit Diagram")
st.markdown("""
1. **H gate** on qubit 0: creates superposition  
2. **CNOT gate**: entangles qubit 1 with qubit 0  
3. **Measurements**: collapse and record results
""")

# Render circuit diagram as matplotlib figure
fig_circ = qc.draw(output='mpl', fold=-1)
st.pyplot(fig_circ)

# Simulation controls
shots = st.slider("Number of shots (experiments):", min_value=100, max_value=5000, step=100, value=1000)

# Run simulation
sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=shots).result()
counts = result.get_counts()

# Plot results
st.markdown("### 📊 Measurement Results")
fig_hist, ax = plt.subplots(figsize=(6, 4))
plot_histogram(counts, ax=ax)
ax.set_title(f"Outcomes over {shots} shots")
st.pyplot(fig_hist)

# Interpretation
with st.expander("📘 What this means"):
    st.markdown("""
- You should see mostly **`00` and `11`**, *not* `01` or `10`.  
- That means qubit 1 always matches qubit 0 — they’re **entangled**.  
- When you measure one, you instantly know the other, even though it's random which pair you see.
""")

# Optional Bloch sphere representation
if st.checkbox("Show Bloch Sphere (pre-measurement)"):
    qc_bloch = QuantumCircuit(2)
    qc_bloch.h(0)
    qc_bloch.cx(0, 1)
    state = Statevector.from_instruction(qc_bloch)
    fig_bloch = plot_bloch_multivector(state)
    st.pyplot(fig_bloch)

# Bonus detail
with st.expander("🧠 Deep Dive"):
    st.markdown(r"""
- The state produced is the **Bell state**:
- This is a key resource for advanced quantum protocols like teleportation and secure key distribution.
""")
    # st.latex(r"|\Phi^+\rangle = \frac{1}{\sqrt{2}} \left( |00\rangle + |11\rangle \right)")


# Footer
st.markdown("---")
st.markdown("🧠 What Does It Mean? This state means: The two qubits are in superposition together.")

st.markdown("st.mWhen you measure them, you’ll get:")

st.markdown("00 half the time")

st.markdown("11 the other half")

st.markdown("You will never see 01 or 10")

st.markdown("The outcome is random — but the two results are always the same.")
