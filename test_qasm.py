from qiskit import QuantumCircuit, qasm3, QuantumRegister, ClassicalRegister

def test_qasm_xor():
    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, cr)

    # Alice ops
    qc.cx(qr[1], qr[0])
    qc.measure(qr[0], cr[0])

    # Bob ops
    qc.cx(qr[2], qr[3])
    qc.measure(qr[3], cr[1])

    # Classical XOR
    # In Qiskit, we need to ensure this exports to: c[2] = c[0] ^ c[1];
    # Or similar valid QASM 3.
    
    # Method 1: Using expressions (recommended for QASM 3)
    # Note: Qiskit support for high-level QASM 3 logic is evolving.
    # Let's try the direct assignment if supported.
    
    # Check if we can do this directly on Clbits
    try:
        # Create an expression for the XOR
        xor_expr = qc.clbits[0] ^ qc.clbits[1] 
        # Store result in clbits[2]
        qc.store(qc.clbits[2], xor_expr)
    except Exception as e:
        print(f"Error with qc.store(xor): {e}")

    try:
        qasm_str = qasm3.dumps(qc)
        print("--- Generated QASM 3 ---")
        print(qasm_str)
        print("------------------------")
        
        # simple check
        if "bit[3] c;" in qasm_str and ("c[2] = c[0] ^ c[1];" in qasm_str or "c[2] = c[0] ^ c[1]" in qasm_str):
             print("SUCCESS: XOR logic found.")
        else:
             print("WARNING: XOR logic might use different syntax.")
             
    except Exception as e:
        print(f"Error dumping QASM: {e}")

if __name__ == "__main__":
    test_qasm_xor()
