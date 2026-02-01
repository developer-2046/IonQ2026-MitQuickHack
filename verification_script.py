import random
import time
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, qasm3
from qiskit.circuit.classical import expr
from client import GameClient

def create_distillation_circuit(num_bell_pairs: int) -> QuantumCircuit:
    N = num_bell_pairs
    qr = QuantumRegister(2 * N, 'q')
    
    if N < 2:
        cr = ClassicalRegister(1, 'c')
        qc = QuantumCircuit(qr, cr)
        return qc

    num_ancilla_pairs = N - 1
    cr = ClassicalRegister(2 * num_ancilla_pairs + 1, 'c')
    qc = QuantumCircuit(qr, cr)
    
    target_alice = N - 1
    target_bob = N
    
    accumulated_flag = None

    for i in range(num_ancilla_pairs):
        ancilla_alice = i
        ancilla_bob = 2 * N - 1 - i
        
        # DEJMPS: CNOT Data -> Ancilla
        qc.cx(qr[target_alice], qr[ancilla_alice])
        qc.cx(qr[target_bob], qr[ancilla_bob])
        
        meas_alice_idx = i
        meas_bob_idx = num_ancilla_pairs + i
        
        qc.measure(qr[ancilla_alice], cr[meas_alice_idx])
        qc.measure(qr[ancilla_bob], cr[meas_bob_idx])
        
        # check = m_A ^ m_B
        check = expr.bit_xor(cr[meas_alice_idx], cr[meas_bob_idx])
        
        if accumulated_flag is None:
            accumulated_flag = check
        else:
            accumulated_flag = expr.bit_or(accumulated_flag, check)
            
    flag_idx = 2 * num_ancilla_pairs
    if accumulated_flag is not None:
        qc.store(cr[flag_idx], accumulated_flag)
    
    return qc

def run_verification():
    print("Initializing Client...")
    pid = f"antigravity_bot_{random.randint(10000, 99999)}"
    client = GameClient()
    
    print(f"Registering {pid}...")
    reg = client.register(pid, "AntigravityBot", location="remote")
    if not reg.get('ok') and reg.get('error', {}).get('code') != 'PLAYER_EXISTS':
        print(f"Registration failed: {reg}")
        return

    print("Checking status...")
    status = client.get_status()
    print(f"Status: {status}")
    
    candidates = reg.get('data', {}).get('starting_candidates', [])
    if not candidates and not status.get('starting_node'):
        print("No candidates and no starting node!")
        return
        
    if not status.get('starting_node'):
        start_node = candidates[0]['node_id']
        print(f"Selecting Starting Node: {start_node}")
        sel = client.select_starting_node(start_node)
        print(f"Selection result: {sel}")
        time.sleep(1) # Wait for propagation

    print("Re-checking status...")
    status = client.get_status()
    print(f"Owned Nodes: {status.get('owned_nodes')}")

    print("Fetching graph...")
    graph = client.get_graph()
    print(f"Graph stats: {len(graph.get('nodes', []))} nodes, {len(graph.get('edges', []))} edges")

    print("Fetching claimable edges...")
    edges = client.get_claimable_edges()
    print(f"Found {len(edges)} claimable edges")
    
    if not edges:
        print("DEBUG: Checking connectivity manually")
        owned = set(status.get('owned_nodes', []))
        for edge in graph.get('edges', []):
            n1, n2 = edge['edge_id']
            if (n1 in owned) != (n2 in owned):
                print(f"Potential edge match: {edge['edge_id']}")
        return

    target_edge = edges[0]
    edge_id_tuple = tuple(target_edge['edge_id'])
    print(f"Targeting edge: {edge_id_tuple} (Threshold: {target_edge.get('base_threshold')})")

    k = 2
    print(f"Generating circuit for k={k}...")
    circuit = create_distillation_circuit(k)
    flag_bit = 2 * (k - 1)
    
    print(f"Submitting claim with flag_bit={flag_bit}...")
    
    success_count = 0
    attempts = 5
    
    for i in range(attempts):
        resp = client.claim_edge(edge_id_tuple, circuit, flag_bit, k)
        data = resp.get('data', {})
        success = data.get('success', False)
        fid = data.get('fidelity', 0.0)
        print(f"Attempt {i+1}: Success={success}, Fidelity={fid:.4f}, Prob={data.get('success_probability')}")
        
        if success:
            success_count += 1
            
    print(f"Final Results: {success_count}/{attempts} successful claims.")
    
    if success_count > 0:
        print("VERIFICATION SUCCESSFUL")
    else:
        print("VERIFICATION FAILED")

if __name__ == "__main__":
    run_verification()
