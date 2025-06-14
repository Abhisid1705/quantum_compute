import streamlit as st
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.quantum_info import Statevector

# Setup
st.set_page_config(page_title="Quantum Superposition", layout="centered")
st.title("🌌 Quantum Superposition Visualizer")

st.markdown("""
Welcome to the **Quantum Superposition Demo**!  
This app shows how a quantum bit (qubit) can exist in multiple states until it's observed.
""")

# Explanatory section
with st.expander("📘 Appendix: Key Terms Explained"):
    st.markdown("""
    - **Qubit**: The basic unit of quantum information. Can be `|0⟩`, `|1⟩`, or both at the same time!
    - **Superposition**: A quantum state that combines `|0⟩` and `|1⟩` simultaneously.
    - **Hadamard Gate (H)**: A quantum gate that puts a qubit into perfect superposition.
    - **Shots**: Number of times the experiment is repeated to gather statistics.  
      More shots = more accurate measurement probabilities.
    - **Measurement**: The act of observing a qubit. This forces it to collapse into either `0` or `1`.
    """)

# User options
st.markdown("### 🧪 Step 1: Set up the Qubit")
initial_state = st.radio("Initial state of the qubit:", ["|0⟩", "|1⟩"])
shots = st.slider("Number of shots (experiments to repeat):", 100, 2000, step=100, value=1000)
show_bloch = st.checkbox("Show Bloch Sphere", value=True)

# Build quantum circuit
qc = QuantumCircuit(1, 1)
if initial_state == "|1⟩":
    qc.x(0)
qc.h(0)  # Hadamard gate creates superposition
qc.measure(0, 0)

# Simulate
simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=shots).result()
counts = result.get_counts()

# Plot histogram
st.markdown("### 📊 Step 2: Measurement Results")

fig, ax = plt.subplots(figsize=(6, 4))  # Wider for cleaner layout
plot_histogram(counts, ax=ax, bar_labels=False)
ax.set_title(f"Results after {shots} shots")
ax.set_ylabel("Counts")
ax.set_xlabel("Measured Output")

# Annotate bars
total_shots = sum(counts.values())
for bar in ax.patches:
    height = bar.get_height()
    percent = f"{height / total_shots:.1%}"
    label = f"{int(height)} shots\n({percent})"
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + (0.02 * shots),  # dynamic padding
        label,
        ha='center',
        fontsize=10,
        color='black'
    )

st.pyplot(fig)

# Optional Bloch Sphere
if show_bloch:
    st.markdown("### 🌀 Step 3: Bloch Sphere (Before Measurement)")
    qc_bloch = QuantumCircuit(1)
    if initial_state == "|1⟩":
        qc_bloch.x(0)
    qc_bloch.h(0)
    state = Statevector.from_instruction(qc_bloch)
    fig2 = plot_bloch_multivector(state)
    st.pyplot(fig2)

# Interpretation box
with st.expander("🧠 What does this mean? (Click to expand)"):
    st.markdown(f"""
    - The qubit was initialized to **{initial_state}**, then transformed using a **Hadamard gate**.
    - This puts it into a superposition: a 50-50 blend of `|0⟩` and `|1⟩`.
    - When measured **{shots} times**, the qubit **collapses** to either `0` or `1` each time.
    - This graph shows how many times each outcome was observed.
    
    📌 If the counts are close to 50/50 — that's **quantum superposition in action**!
    """)

# Footer
st.markdown("---")
st.markdown(
"Little info on Baloch sphere :  The Bloch sphere is a 3D unit sphere used to represent the state of a single qubit. Any qubit state can be visualized as a vector (arrow) from the center of the sphere to its surface."

"The Z-axis corresponds to classical states:"

"|0⟩ → arrow pointing up (north pole)"

" |1⟩ → arrow pointing down (south pole)"

"The X-axis and Y-axis represent quantum superposition and phase information:"

"|+⟩ = (|0⟩ + |1⟩)/√2 → points in +X direction"

"|-⟩ = (|0⟩ - |1⟩)/√2 → points in –X direction"
    
)
