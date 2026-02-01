# iQuHACK 2026 Challenge Solution - Team theLion

**Team Lead:** Yuvraj Malik  
**Members:** Nicholas Bo You Chin, Niguun Soyombo-erdene, Sho Sakaue, Coleman Rohde

## Overview
This repository contains our winning solution for the IonQ Entanglement Distillation challenge at iQuHACK 2026. We successfully captured **30/30 nodes** in the network (Complete Domination) using a custom LOCC-compliant distillation protocol and an autonomous game agent.

## Key Features

### 1. LOCC Distillation Circuit (`solution.py`)
We implemented a variation of the **DEJMPS** purification protocol specifically adapted for the game's LOCC constraints:
- **Qubit Layout:** Alice controls qubits $0 \dots k-1$, Bob controls $k \dots 2k-1$.
- **Flag-based Post-selection:** Uses classical feedforward to compute parity checks (`c[i] ^ c[j]`) across distributed ancilla pairs. The server is instructed to post-select on the perfect correlation flag.
- **Variable Precision:** The generator supports any number of Bell pairs ($k$), allowing dynamic trade-offs between cost and fidelity.

### 2. Autonomous Agent (`auto_player.py`)
Our `AutoPlayer` bot systematically dominates the graph with a "Thrifty Expansion" strategy:
- **Adaptive Budgeting:** It first attempts to claim edges using only $k=2$ pairs (Cost: 2). It scales up to expensive circuits ($k=3, 4$) *only* if fidelity thresholds are not met, saving significant resources.
- **Sustainability First:** Properly weighs nodes with **Bonus Bell Pairs** as top priority, effectively ensuring the budget never runs out.
- **Smart Queueing:** Identifies all "Frontier" edges (connecting Owned $\to$ Unowned nodes) and ranks them by a custom utility score derived from game mechanics.

## Repository Structure
- `solution.py`: Core quantum circuit generation logic (Qiskit).
- `auto_player.py`: The autonomous bot script.
- `report.pdf`: Detailed submission report with strategy description and visualizations.
- `generate_viz.py`: Helper script used to generate circuit diagrams.
- `client.py`: The provided game client interface.

## Usage
To run the bot in the competition environment (Jupyter Notebook):

```python
from auto_player import AutoPlayer

# Assuming 'client' is already authenticated
bot = AutoPlayer(client)

# Run the automation loop
bot.run_loop()
```

---
*Created for iQuHACK 2026.*
