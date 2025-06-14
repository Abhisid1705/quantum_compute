import streamlit as st
import random
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit.visualization import plot_bloch_multivector, plot_histogram
from qiskit.quantum_info import Statevector

# Import Aer backend safely
try:
    from qiskit_aer import Aer
except ImportError:
    try:
        from qiskit.providers.aer import Aer
    except ImportError:
        st.error("Qiskit Aer simulator not found. Please install qiskit-aer.")
        st.stop()

st.set_page_config(page_title="BB84 QKD Protocol Demo", layout="centered")
st.title("🔐 Quantum Key Distribution (BB84) Protocol Demo")

st.markdown("""
The **BB84 protocol** enables two parties (Alice & Bob) to securely share a secret key using quantum mechanics principles.

- Alice sends qubits randomly prepared in either the Z-basis (|0⟩, |1⟩) or X-basis (|+⟩, |−⟩).
- Bob measures in a randomly chosen basis.
- Alice and Bob compare bases publicly and keep bits where bases matched.
- Resulting key is secret and secure from eavesdroppers.

Try this demo to see how key bits are generated and how measurement outcomes look!
""")

num_bits = st.slider("Number of bits/qubits to transmit", min_value=4, max_value=32, value=8)

# Step 1: Alice's random bits and bases
alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
alice_bases = [random.choice(['Z', 'X']) for _ in range(num_bits)]

st.subheader("Alice's bits and bases")
st.write(f"Bits:  {alice_bits}")
st.write(f"Bases: {alice_bases}")

# Step 2: Bob's random bases
bob_bases = [random.choice(['Z', 'X']) for _ in range(num_bits)]
st.subheader("Bob's chosen bases")
st.write(f"Bases: {bob_bases}")

backend = Aer.get_backend('aer_simulator')

alice_states = []
bob_results = []

st.subheader("Quantum Transmission & Measurement Results")

for i in range(num_bits):
    qc = QuantumCircuit(1, 1)
    bit = alice_bits[i]
    basis = alice_bases[i]

    # Prepare Alice's qubit
    if basis == 'Z':
        if bit == 1:
            qc.x(0)  # |1>
    else:  # X basis preparation: |+> or |->
        qc.h(0)
        if bit == 1:
            qc.z(0)  # |-> = Z|+>

    # Save statevector for visualization
    sv = Statevector.from_instruction(qc)
    alice_states.append(sv)

    # Bob's measurement basis
    if bob_bases[i] == 'X':
        qc.h(0)

    qc.measure(0, 0)

    # Run circuit using backend.run() instead of execute
    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()

    measured_bit = int(max(counts, key=counts.get))
    bob_results.append(measured_bit)

    st.write(f"Qubit {i+1} - Alice bit: {bit} | Alice basis: {basis} | Bob basis: {bob_bases[i]} | Measured: {measured_bit}")
    fig = plt.figure(figsize=(3, 3))
    plot_bloch_multivector(sv.data, ax=fig.add_subplot(111))
    st.pyplot(fig)

# Step 4: Bases comparison and key extraction
matching_indices = [i for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
st.subheader("Bases Comparison (Keep bits where bases match)")
st.write(f"Matching Indices: {matching_indices}")

alice_key = [alice_bits[i] for i in matching_indices]
bob_key = [bob_results[i] for i in matching_indices]

st.write(f"Alice's key bits: {alice_key}")
st.write(f"Bob's key bits:   {bob_key}")

# Step 5: Key agreement statistics
matches = sum(a == b for a, b in zip(alice_key, bob_key))
total = len(matching_indices)
accuracy = (matches / total * 100) if total > 0 else 0

st.subheader("Key Agreement")
st.write(f"Bits matched: {matches} / {total}")
st.write(f"Key agreement accuracy: {accuracy:.2f}%")

if accuracy == 100:
    st.success("Perfect key agreement — communication is secure!")
elif accuracy > 50:
    st.warning("Partial key agreement — some errors, possible eavesdropping or noise.")
else:
    st.error("Low key agreement — communication not secure.")

# Step 6: Histogram of measurement results
st.subheader("Measurement Outcome Distribution (All Qubits)")
counts = {}
for bit in bob_results:
    counts[str(bit)] = counts.get(str(bit), 0) + 1

fig, ax = plt.subplots()
plot_histogram(counts, ax=ax)
st.pyplot(fig)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit and Qiskit")
