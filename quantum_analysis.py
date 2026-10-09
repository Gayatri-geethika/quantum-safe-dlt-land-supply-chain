import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def build_grover_toy_circuit(target="1010"):
    """
    Educational Grover demonstration.

    This is NOT an attack on ML-DSA. It models the general quantum
    unstructured-search idea relevant to quantum threat analysis.
    """
    n = len(target)
    qc = QuantumCircuit(n, n)

    # Put all states into superposition.
    qc.h(range(n))

    # Phase oracle for the chosen target.
    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)

    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    for i, bit in enumerate(reversed(target)):
        if bit == "0":
            qc.x(i)

    # Diffusion operator.
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))

    qc.measure(range(n), range(n))
    return qc

def run_quantum_threat_analysis():
    target = "1010"
    qc = build_grover_toy_circuit(target)

    backend = AerSimulator()
    compiled = transpile(qc, backend)
    result = backend.run(compiled, shots=2048).result()
    counts = result.get_counts()

    most_likely = max(counts, key=counts.get)
    target_probability = counts.get(target, 0) / 2048

    n = len(target)
    classical_scale = 2 ** n
    grover_scale = math.sqrt(classical_scale)

    return {
        "algorithm": "Grover toy search",
        "purpose": "Model quantum unstructured-search pressure",
        "target_state": target,
        "most_likely_state": most_likely,
        "target_probability": round(target_probability, 4),
        "classical_search_scale": classical_scale,
        "quantum_search_scale": round(grover_scale, 2),
        "shots": 2048,
        "measurement_counts": counts,
        "circuit_depth": qc.depth(),
        "qubits": qc.num_qubits,
        "important_note": (
            "This simulation demonstrates quantum search behavior; "
            "it does not break ML-DSA or claim a practical attack."
        )
    }
