import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

st.set_page_config(page_title="Quantum Interference Demo", layout="centered")

st.title("🌌 Quantum Interference Visualized with Coin Tosses")
st.markdown("""
This demo shows how **quantum interference** helps amplify some outcomes and cancel others — using a **coin toss analogy** 🎲.  
We will:
- Create superposition (like flipping two fair coins)
- Flip the phase of only the Tails-Tails state
- Interfere the results so some coin combos disappear and others remain

Hover over each step to understand what it's doing!
""")

# Step-by-step circuit
qc = QuantumCircuit(2, 2)

# Step 1: Hadamard Gates
with st.expander("✅ Step 1: Create Superposition with Hadamard Gates"):
    st.write("Each Hadamard gate puts a qubit into a mix of Heads and Tails.")
    st.info("""
    Coin 1 becomes (Heads + Tails)/√2  
    Coin 2 becomes (Heads + Tails)/√2  
    Combined state: all 4 combinations are equally likely
    """)
    qc.h(0)
    qc.h(1)

# Step 2: Phase Flip |11>
with st.expander("🔄 Step 2: Flip Phase of Tails-Tails (|11⟩)"):
    st.write("Only the Tails-Tails combination gets a minus sign.")
    st.warning("""
    New state: (HH + HT + TH - TT)/2
    """)
    qc.cz(0, 1)

    st.markdown("### 🌊 Interference Visualization")
    st.markdown("Below, the orange wave is flipped, showing destructive interference:")

    x = np.linspace(0, 4 * np.pi, 100)
    y1 = np.sin(x)
    y2 = -np.sin(x)  # Phase-flipped wave
    y_total = y1 + y2

    fig, ax = plt.subplots()
    ax.plot(x, y1, label='Original Amplitude', linestyle='--')
    ax.plot(x, y2, label='Flipped Amplitude (|11⟩)', linestyle='--')
    ax.plot(x, y_total, label='Combined Result (Destructive Interference)', linewidth=2)
    ax.set_title("Destructive Interference")
    ax.legend()
    st.pyplot(fig)

# Step 3: Hadamard Again (Interference)
with st.expander("💥 Step 3: Interference via Hadamard Again"):
    st.write("Interference causes some coin combos to cancel out and others to amplify.")
    st.success("""
    This step redistributes probability amplitudes.
    Some outputs become more likely, others become zero.
    """)
    qc.h(0)
    qc.h(1)

# Measurement
with st.expander("📏 Step 4: Measure the Coins"):
    st.write("Now we collapse the state and observe one of the remaining coin combos.")
    qc.measure([0, 1], [0, 1])

# Display circuit
st.subheader("📐 Quantum Circuit Diagram")
st.pyplot(qc.draw("mpl"))

# Simulate
sim = AerSimulator()
compiled = transpile(qc, sim)
result = sim.run(compiled, shots=1024).result()
counts = result.get_counts()

# Coin Toss Label Mapping
coin_labels = {
    "00": "🪙🪙 Heads-Heads",
    "01": "🪙🔁 Heads-Tails",
    "10": "🔁🪙 Tails-Heads",
    "11": "🔁🔁 Tails-Tails"
}
readable_counts = {coin_labels.get(k, k): v for k, v in counts.items()}

# Plot histogram
st.subheader("🎲 Measurement Results (Coin Combos)")
st.bar_chart(readable_counts)

st.success("Notice how interference amplifies some coin outcomes and cancels others!")
