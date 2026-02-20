import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# --- CONFIGURATION ---
TOTAL_QUBITS = 350  # Set to 1000 as requested
SIMULATOR = AerSimulator()

# --- PART 1: CORE BB84 FUNCTIONS ---

def encode_qubits(bits, bases):
    """Alice prepares qubits."""
    circuits = []
    for bit, basis in zip(bits, bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)  # Flip to |1>
        if basis == 1:
            qc.h(0)  # Rotate to X basis
        circuits.append(qc)
    return circuits

def measure_qubits(circuits, bases):
    """Bob (or Eve) measures qubits."""
    results = []
    for qc, basis in zip(circuits, bases):
        measure_qc = qc.copy()
        if basis == 1:
            measure_qc.h(0)  # Rotate if measuring in X basis
        measure_qc.measure(0, 0)

        # Run on Simulator
        transpiled_qc = transpile(measure_qc, SIMULATOR)
        job = SIMULATOR.run(transpiled_qc, shots=1, memory=True)
        result = int(job.result().get_memory()[0])
        results.append(result)
    return results

def eve_intercept_resend(circuits, alice_bases):
    """
    Eve's Attack:
    1. Intercepts (measures in random basis)
    2. Resends (encodes her result in her basis)
    """
    n = len(circuits)
    eve_bases = np.random.randint(0, 2, n)

    # Eve measures
    eve_bits = measure_qubits(circuits, eve_bases)

    # Eve creates NEW qubits to send to Bob
    new_circuits = encode_qubits(eve_bits, eve_bases)

    return new_circuits, eve_bases

# --- PART 2: MAIN SIMULATION ---

def run_simulation():
    print(f"\n--- RUNNING SIMULATION ({TOTAL_QUBITS} Qubits) ---")

    # 1. GENERATE DATA
    alice_bits = np.random.randint(0, 2, TOTAL_QUBITS)
    alice_bases = np.random.randint(0, 2, TOTAL_QUBITS)

    # 2. PREPARE QUBITS
    qubits = encode_qubits(alice_bits, alice_bases)

    # 3. EVE ATTACKS
    print(">> Status: Eve is intercepting the channel...\n")
    qubits, eve_bases = eve_intercept_resend(qubits, alice_bases)

    # 4. BOB MEASURES
    bob_bases = np.random.randint(0, 2, TOTAL_QUBITS)
    bob_results = measure_qubits(qubits, bob_bases)

    # 5. RESTORED TABLE FORMAT (Like First Code)
    # Columns: Idx | Alice Bit | Alice Bas | Bob Bas | Bob Bit | Match?
    print(f"{'Idx':<5} {'Alice Bit':<10} {'Alice Bas':<10} {'Bob Bas':<10} {'Bob Bit':<10} {'Match?'}")
    print("-" * 65)

    sifted_indices = []
    running_errors = []
    total_errors = 0
    sifted_count = 0

    for i in range(TOTAL_QUBITS):
        match_status = "Discarded"

        # Check if bases match (Sifting)
        if alice_bases[i] == bob_bases[i]:
            sifted_count += 1
            sifted_indices.append(i + 1) # Store Qubit Number (1-based)

            if alice_bits[i] == bob_results[i]:
                match_status = "YES"
                running_errors.append(0) # No error
            else:
                match_status = "ERROR"
                total_errors += 1
                running_errors.append(1) # Error occurred

        # Print first 15 rows to keep console clean (but processes 1000)
        if i < 15:
            # Using raw 0/1 integers as requested in "like the first one"
            print(f"{i+1:<5} {alice_bits[i]:<10} {alice_bases[i]:<10} {bob_bases[i]:<10} {bob_results[i]:<10} {match_status}")

    print("... (showing first 15 rows only, processed 1000) ...")
    print("-" * 65)

    if sifted_count == 0:
        print("No matches found.")
        return

    # 6. FINAL STATISTICS
    final_qber = total_errors / sifted_count
    print(f"\nRESULTS:")
    print(f"Total Qubits Sent: {TOTAL_QUBITS}")
    print(f"Sifted Key Length: {sifted_count}")
    print(f"Total Errors Found: {total_errors}")
    print(f"Final QBER: {final_qber:.2%} (Theory predicts ~25%)")

    # 7. GENERATE GRAPH (1000 Qubits)
    cumulative_errors = np.cumsum(running_errors)
    trials = np.arange(1, len(cumulative_errors) + 1)
    qber_curve = cumulative_errors / trials

    plt.style.use('dark_background')
    plt.figure(figsize=(10, 6))

    # Plot Simulated QBER
    plt.plot(sifted_indices, qber_curve, color='cyan', label='Simulated QBER', linewidth=1.5)

    # Plot Theoretical 25% Line
    plt.axhline(y=0.25, color='red', linestyle='--', linewidth=2, label='Theoretical QBER = 25%')

    plt.title(f'Intercept-Resend Attack: QBER (Total Qubits: {TOTAL_QUBITS})', fontsize=14, color='white')
    plt.xlabel('Number of Qubits', fontsize=12, color='white')
    plt.ylabel('Quantum Bit Error Rate (QBER)', fontsize=12, color='white')

    plt.ylim(0, 0.5)
    plt.xlim(0, TOTAL_QUBITS)

    plt.grid(True, color='gray', linestyle='--', alpha=0.5)
    plt.legend(loc='upper right', facecolor='black', edgecolor='white')

    print("\nDisplaying graph...")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_simulation()
