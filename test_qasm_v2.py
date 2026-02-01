from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, qasm3
from qiskit.circuit import Clbit
from qiskit.circuit.classical import expr

def test_v2():
    qr = QuantumRegister(4, 'q')
    cr = ClassicalRegister(3, 'c')
    qc = QuantumCircuit(qr, cr)

    qc.measure(qr[0], cr[0])
    qc.measure(qr[3], cr[1])

    # Try using expr.bit_xor
    try:
        # Construct the expression
        target = cr[2]
        val = expr.bit_xor(cr[0], cr[1])
        
        # Store it
        # qc.store(target, val) # This is how it should work in recent Qiskit
        qc.store(target, val)
        
        print("Successfully added store instruction.")
        print(qasm3.dumps(qc))
        
    except Exception as e:
        print(f"Failed with expr: {e}")
        # Fallback check: inspect dir(expr)
        print(f"Available in expr: {dir(expr)}")

if __name__ == "__main__":
    test_v2()
