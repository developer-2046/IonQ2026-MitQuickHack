from solution import create_distillation_circuit
import matplotlib.pyplot as plt

def generate_images():
    # k=2
    qc2 = create_distillation_circuit(2)
    qc2.draw('mpl', filename='/home/yuvi/2026-IonQ/circuit_k2.png')
    print("Generated k=2 circuit image.")

    # k=3
    qc3 = create_distillation_circuit(3)
    qc3.draw('mpl', filename='/home/yuvi/2026-IonQ/circuit_k3.png')
    print("Generated k=3 circuit image.")

if __name__ == "__main__":
    generate_images()
