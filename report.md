# iQuHACK 2026 IonQ Challenge Report

**Team:** Antigravity  
**Result:** 30/30 Nodes Captured (Complete Graph Dominance)

## Executive Summary

Our strategy combined a robust **LOCC-compliant Entanglement Distillation protocol** with an **autonomous, budget-aware agent** to systematically capture the network. By prioritizing self-sustainability (nodes with bonus bell pairs) and using adaptive resource allocation, we maximized territory while maintaining a distinct advantage over competitors.

## 1. Entanglement Distillation Methodology

We implemented a variation of the **DEJMPS** (Deutsch-Ekert-Jozsa-Macchiavello-Popescu-Sanpera) purification protocol, adapted for the specific LOCC constraints of the challenge.

### Circuit Design
For an edge with $k$ Bell pairs, we designate:
- **Alice's Qubits:** $0 \dots k-1$
- **Bob's Qubits:** $k \dots 2k-1$
- **Target Pair (Output):** Qubits $(k-1)$ and $k$ (The "innermost" pair).
- **Ancilla Pairs:** All other pairs $(i, 2k-1-i)$ for $i < k-1$.

### Algorithm Steps
1.  **Bit-Flip Correction (CNOTs):** We apply local CNOT gates targeting the Ancilla pairs, controlled by the Target pair. This propagates $X$-errors from the Target to the Ancilla.
    -   Alice: $CX(\text{Target}_A \to \text{Ancilla}_A)$
    -   Bob: $CX(\text{Target}_B \to \text{Ancilla}_B)$
2.  **Parity Measurement:** Both parties measure their Ancilla qubits.
3.  **Classical Post-Selection (LOCC Flag):**
    -   We compute the parity check: $\text{Check} = m_{A} \oplus m_{B}$.
    -   Success Condition: $\text{Check} == 0$ (Correlation matches).
    -   If *any* ancilla pair fails this check, the entire process is flagged as a failure.
    -   Qiskit Logic: `c[flag] = c[0] ^ c[1] | c[2] ^ c[3] ...`

This protocol effectively suppresses bit-flip errors, raising the fidelity of the raw Bell pairs above the $0.90$ threshold required for claiming edges.

### Visualizations

**Figure 1: Distillation Circuit for k=2 (1 Ancilla Pair)**
![k=2 Circuit](/home/yuvi/2026-IonQ/circuit_k2.png)
*Alice (q0, q1) and Bob (q2, q3) use pair (0,3) to purify (1,2).*

**Figure 2: Distillation Circuit for k=3 (2 Ancilla Pairs)**
![k=3 Circuit](/home/yuvi/2026-IonQ/circuit_k3.png)
*Two ancilla pairs are used to purify the central pair.*

## 2. Autonomous Network Strategy

To achieve 100% map coverage, we developed an `AutoPlayer` agent with the following heuristics:

### Adaptive Resource Allocation (The "Thrifty" Heuristic)
The game charges Bell Pairs based on the input size $k$. To conserve our budget:
1.  The agent first attempts to claim an edge with **k=2** (Cost: 2).
2.  Only if fidelity is insufficient does it scale to **k=3** or **k=4**.
This ensures we never "overpay" for easy edges, allowing us to stretch our initial 40-pair budget significantly further.

### Priority Queueing
We ranked claimable edges based on a custom utility function:
$$ \text{Score} = (100 \times \text{BonusPairs}) + \text{UtilityQubits} - (0.1 \times \text{Difficulty}) $$
1.  **Sustainability First:** Nodes providing **Bonus Bell Pairs** were top priority. Capturing these early effectively gave us "infinite" ammo.
2.  **Utility Second:** High-point nodes were targeted next to secure the leaderboard.
3.  **Difficulty Penalty:** Low-difficulty edges were preferred as tie-breakers to minimize risk.

### Robustness
- **Blacklisting:** Edges that failed consistently (due to noise or high difficulty) were temporarily ignored to prevent budget drain.
- **Expansionist logic:** The agent always targeted edges connecting to *new* nodes, ensuring rapid graph traversal.

## Conclusion
By formalizing the LOCC constraints into a reusable Qiskit generator and wrapping it in a rational agent, we achieved a perfect game state. The DEJMPS protocol provided the necessary fidelity guarantees, while the economic strategy ensured we could afford to claim the entire board.
