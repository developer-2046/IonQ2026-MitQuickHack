# iQuHACK 2026 IonQ Challenge - Solution Code
# Copy this entire file or the relevant functions into your notebook.

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, qasm3
from qiskit.circuit.classical import expr

def create_distillation_circuit(num_bell_pairs: int) -> QuantumCircuit:
    """
    Creates an LOCC-compliant distillation circuit for the IonQ game.
    
    Logic: Uses DEJMPS / BBPSSW protocol to purify the last Bell pair using all other pairs.
    
    Qubit Layout:
    Alice: 0 to N-1
    Bob: N to 2N-1
    
    Target Output Pair: (N-1, N) -> (Alice's last, Bob's first)
    Ancilla Pairs: (i, 2N-1-i) for i in 0..N-2
    """
    N = num_bell_pairs
    qr = QuantumRegister(2 * N, 'q')
    
    # Handle base case
    if N < 2:
        # No distillation possible with 1 pair
        return QuantumCircuit(qr, ClassicalRegister(1, 'c'))

    num_ancilla_pairs = N - 1
    
    # We need enough classical bits to store measurements and the final flag.
    # Alice measures N-1 bits. Bob measures N-1 bits. Flag needs 1 bit.
    total_clbits = 2 * num_ancilla_pairs + 1
    cr = ClassicalRegister(total_clbits, 'c')
    qc = QuantumCircuit(qr, cr)
    
    # Target (Output) Pair indices
    target_alice = N - 1
    target_bob = N
    
    accumulated_flag = None

    # Iterate over all available ancilla pairs to purify the target pair
    for i in range(num_ancilla_pairs):
        # Current ancilla pair indices
        # We pair (0, 2N-1), (1, 2N-2), etc.
        ancilla_alice = i
        ancilla_bob = 2 * N - 1 - i
        
        # --- LOCC Operations ---
        
        # 1. CNOT gates (BBPSSW protocol for bit-flip correction)
        # Control on Target (Data), Target on Ancilla
        # This copies X errors from Data to Ancilla.
        qc.cx(qr[target_alice], qr[ancilla_alice]) # Alice local
        qc.cx(qr[target_bob], qr[ancilla_bob])     # Bob local
        
        # 2. Measurement
        meas_alice_idx = i
        meas_bob_idx = num_ancilla_pairs + i
        
        qc.measure(qr[ancilla_alice], cr[meas_alice_idx])
        qc.measure(qr[ancilla_bob], cr[meas_bob_idx])
        
        # 3. Classical Post-Selection Logic
        # We need Parity(Alice) == Parity(Bob).
        # i.e., m_Alice XOR m_Bob == 0.
        # If any pair fails this check, the distillation fails.
        pair_check = expr.bit_xor(cr[meas_alice_idx], cr[meas_bob_idx])
        
        if accumulated_flag is None:
            accumulated_flag = pair_check
        else:
            # Aggregate failures: if ANY check is 1, flag becomes 1.
            accumulated_flag = expr.bit_or(accumulated_flag, pair_check)
            
    # Store the final flag bit
    flag_idx = 2 * num_ancilla_pairs
    if accumulated_flag is not None:
        qc.store(cr[flag_idx], accumulated_flag)
    
    return qc

def run_claim_loop(client, num_bell_pairs=2, attempts=30):
    """
    Convenience function to run the claiming loop.
    """
    print(f"--- Starting Claim Loop (k={num_bell_pairs}) ---")
    
    # 1. Get a claimable edge
    edges = client.get_claimable_edges()
    if not edges:
        print("No claimable edges found.")
        return
        
    target_edge = edges[0]
    edge_id = tuple(target_edge['edge_id'])
    print(f"Targeting edge: {edge_id}")
    print(f"Threshold: {target_edge.get('base_threshold')}, Difficulty: {target_edge.get('difficulty_rating')}")

    # 2. Generate Circuit
    circuit = create_distillation_circuit(num_bell_pairs)
    
    # 3. Determine Flag Bit Index
    # According to our generator: idx = 2 * (N - 1)
    flag_bit = 2 * (num_bell_pairs - 1)
    
    print(f"Submit with flag_bit index: {flag_bit}")
    
    # 4. Loop
    for attempt in range(attempts):
        result = client.claim_edge(edge_id, circuit, flag_bit, num_bell_pairs)
        data = result.get("data", {})
        
        success = data.get("success")
        fidelity = data.get("fidelity")
        
        status_symbol = "✅" if success else "❌"
        print(f"[{attempt+1}/{attempts}] {status_symbol} Success={success}, Fidelity={fidelity:.4f}")
        
        if success:
            print(f"🎉 CLAIMED EDGE {edge_id}!")
            break
            
# --- Usage Example ---
# if __name__ == "__main__":
#     # Assuming 'client' is already defined in your notebook:
#     run_claim_loop(client, num_bell_pairs=2) 
