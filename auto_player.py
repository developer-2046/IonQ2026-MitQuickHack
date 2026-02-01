import time
from solution import create_distillation_circuit

class AutoPlayer:
    def __init__(self, client):
        self.client = client
        self.cached_graph = client.get_graph()
        self.nodes = {n['node_id']: n for n in self.cached_graph.get('nodes', [])}
        self.blacklist = set() # Edges we failed to claim

    def _get_node_priority(self, node_id):
        node = self.nodes.get(node_id, {})
        # Heuristic: Bonus Alloc (Budget) >> Utility >> Capacity
        bonus = node.get('bonus_bell_pairs', 0)
        utility = node.get('utility_qubits', 0)
        # Prioritize keeping budget high (bonus > 0), then score
        return (bonus * 100) + utility

    def get_best_claimable_edge(self):
        edges = self.client.get_claimable_edges()
        if not edges:
            return None
            
        status = self.client.get_status()
        owned = set(status.get('owned_nodes', []))
        
        candidates = []
        for edge in edges:
            edge_id = tuple(edge['edge_id'])
            if edge_id in self.blacklist:
                continue
                
            # Identify target node (the one we don't own yet)
            n1, n2 = edge_id
            target = n2 if n1 in owned else n1
            
            prio = self._get_node_priority(target)
            diff = edge.get('difficulty_rating', 1)
            thresh = edge.get('base_threshold', 0.9)
            
            # Score: High Prio, Low Diff, Low Thresh
            score = prio - (diff * 0.1) - (thresh * 1.0)
            candidates.append((score, edge))
            
        if not candidates:
            return None
            
        # Sort descending by score
        candidates.sort(key=lambda x: x[0], reverse=True)
        return candidates[0][1]

    def attempt_claim(self, edge, max_k=4):
        edge_id = tuple(edge['edge_id'])
        print(f"Attempting to claim {edge_id}...")
        
        # Adaptive k: Start cheap (k=2), increase if needed
        # This saves budget on easy edges.
        for k in range(2, max_k + 1):
            flag_bit = 2 * (k - 1)
            print(f"  > Trying k={k} (cost={k}, flag_bit={flag_bit})...")
            
            try:
                circuit = create_distillation_circuit(k)
                result = self.client.claim_edge(edge_id, circuit, flag_bit, k)
                data = result.get('data', {})
                
                success = data.get('success', False)
                fid = data.get('fidelity', 0.0)
                print(f"    Result: Success={success}, Fidelity={fid:.4f}")
                
                if success:
                    print(f"  🎉 Claimed with k={k}!")
                    return True
            except Exception as e:
                print(f"    Error during claim attempt: {e}")
                time.sleep(1)
                
        print("  ❌ Failed to claim edge after trying all k. Blacklisting.")
        self.blacklist.add(edge_id)
        return False

    def run_loop(self, max_actions=50):
        print("Starting AutoPlayer Loop...")
        for i in range(max_actions):
            print(f"\n--- Turn {i+1}/{max_actions} ---")
            
            try:
                status = self.client.get_status()
                budget = status.get('budget', 0)
                print(f"Budget: {budget} Bell Pairs. Score: {status.get('score', 0)}")
                
                if budget < 2:
                    print("Budget too low to continue.")
                    break
                    
                edge = self.get_best_claimable_edge()
                if not edge:
                    print("No more claimable edges or all blacklisted.")
                    break
                    
                print(f"Selected Target: {edge['edge_id']} (Diff={edge.get('difficulty_rating')}, Thr={edge.get('base_threshold')})")
                
                result = self.attempt_claim(edge)
                
                # Small delay to respect server
                time.sleep(1)
                
            except Exception as e:
                print(f"Critical Loop Error: {e}")
                time.sleep(2)
                
        print("AutoPlayer Loop Finished.")
