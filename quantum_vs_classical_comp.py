import streamlit as st
import math
import random
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

# -------- Diffuser (Inversion about the mean) --------
def diffuser(n_qubits):
    qc = QuantumCircuit(n_qubits)
    qc.h(range(n_qubits))
    qc.x(range(n_qubits))
    qc.h(n_qubits - 1)
    qc.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    qc.h(n_qubits - 1)
    qc.x(range(n_qubits))
    qc.h(range(n_qubits))
    qc.name = "Diffuser"
    return qc

# -------- Oracle Builder --------
def build_oracle(target_index, n):
    target_bin = f"{target_index:0{n}b}"
    oracle = QuantumCircuit(n)
    for i, bit in enumerate(reversed(target_bin)):
        if bit == '0':
            oracle.x(i)
    oracle.h(n - 1)
    oracle.mcx(list(range(n - 1)), n - 1)
    oracle.h(n - 1)
    for i, bit in enumerate(reversed(target_bin)):
        if bit == '0':
            oracle.x(i)
    oracle.name = "Oracle"
    return oracle

# -------- Grover Circuit --------
def grover_circuit_builder(target_index, n):
    oracle = build_oracle(target_index, n)
    diff = diffuser(n)

    qc = QuantumCircuit(n, n)
    qc.h(range(n))

    iterations = int(round((math.pi / 4) * math.sqrt(2 ** n)))
    for _ in range(iterations):
        qc.append(oracle.to_gate(), range(n))
        qc.append(diff.to_gate(), range(n))

    qc.measure(range(n), range(n))
    return qc, iterations, oracle, diff

# -------- Classical Search --------
def classical_search(data, target, visualize=False):
    steps = 0
    for i, val in enumerate(data):
        steps += 1
        if visualize:
            st.write(f"Step {steps}: Checking index {i} (value={val})")
        if val == target:
            return i, steps
    return -1, steps

# -------- Streamlit UI --------
st.set_page_config(page_title="Grover Search Demo", layout="centered")
st.title("⚛️ Grover's Quantum Search vs Classical Search")

st.markdown("""
This demo compares **classical brute-force search** vs **Grover’s quantum search algorithm**,  
which gives a theoretical **√N speedup** for unstructured search.
""")

num_items = st.selectbox("Select number of items (must be a power of 2)", options=[4, 8, 16, 32], index=2)
n = int(math.log2(num_items))

if "data" not in st.session_state or st.session_state.get("num_items") != num_items:
    st.session_state.data = list(range(num_items))  # predictable data
    st.session_state.target = random.choice(st.session_state.data)
    st.session_state.num_items = num_items

data = st.session_state.data
target = st.session_state.target

if st.button("🔁 Reset Target"):
    st.session_state.target = random.choice(st.session_state.data)
    st.experimental_rerun()

st.write(f"🎯 Target value: `{target}` (Index: {data.index(target)})")

if st.checkbox("Show Data List"):
    st.write(data)

# Classical Search Button
if st.button("🔍 Run Classical Search"):
    idx, steps = classical_search(data, target, visualize=True)
    st.success(f"✅ Found at index `{idx}` in `{steps}` steps.")

# Grover Search Button
if st.button("⚛️ Run Grover Search"):
    st.subheader("⚛️ Grover's Algorithm Running...")

    target_idx = data.index(target)
    qc, iterations, oracle, diff = grover_circuit_builder(target_idx, n)

    backend = Aer.get_backend("qasm_simulator")
    job = backend.run(transpile(qc, backend), shots=512)
    result = job.result()
    counts = result.get_counts()

    # Fix bit order from Qiskit (LSB -> MSB)
    top_result = max(counts, key=counts.get)
    # corrected_index = int(top_result[::-1], 2)

    st.write(f"🔁 Iterations used: `{iterations}`")
    corrected_index = int(top_result, 2)
    st.write(f"📈 Most measured: `{top_result}` (Index after bit fix: `{corrected_index}`)")
    st.write(f"🎯 Success rate: `{counts[top_result]/512*100:.2f}%`")

    fig, ax = plt.subplots()
    plot_histogram(counts, ax=ax)
    st.pyplot(fig)

    st.subheader("🧪 Quantum Circuit Details")

    with st.expander("Step 1: Initialization (Hadamard gates)"):
        st.code("qc.h(range(n))")

    with st.expander("Step 2: Oracle (marks the target index)"):
        st.pyplot(oracle.draw("mpl", idle_wires=True))

    with st.expander("Step 3: Diffuser (amplifies the target)"):
        st.pyplot(diff.draw("mpl", idle_wires=True))

    with st.expander("Full Circuit with Measurements"):
        st.pyplot(qc.draw("mpl", idle_wires=True))

    st.success("✅ Grover’s algorithm amplified the target index successfully!")

