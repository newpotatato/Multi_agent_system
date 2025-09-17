"""
Simplified Graph Service for Multi-Agent System

This service manages broker connectivity and coordination
with simplified configuration.
"""

import random
import numpy as np
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.config import get_config


class GraphService:
    """
    Simplified graph service for broker connectivity.
    """
    
    def __init__(self, num_brokers):
        self.num_brokers = num_brokers
        self.adjacency_matrix = np.zeros((num_brokers, num_brokers))
        self.weights = {}  # Edge weights between brokers
        self.neighbors = {i: [] for i in range(num_brokers)}
        
        # Simple default parameters
        self.edge_probability = 0.3
        self.min_neighbors = 2
        self.max_neighbors = 5
        self.weight_decay = 0.95
        
        self._generate_initial_graph()
    
    def _generate_initial_graph(self):
        """Generate initial random connectivity graph"""
        # Create random connections
        for i in range(self.num_brokers):
            for j in range(i + 1, self.num_brokers):
                if random.random() < self.edge_probability:
                    self._add_edge(i, j)
        
        # Ensure minimum connectivity
        self._ensure_connectivity()
        
        # Initialize weights
        self._initialize_weights()
    
    def _add_edge(self, i, j):
        """Add edge between nodes i and j"""
        self.adjacency_matrix[i][j] = 1
        self.adjacency_matrix[j][i] = 1
        
        if j not in self.neighbors[i]:
            self.neighbors[i].append(j)
        if i not in self.neighbors[j]:
            self.neighbors[j].append(i)
    
    def _remove_edge(self, i, j):
        """Remove edge between nodes i and j"""
        self.adjacency_matrix[i][j] = 0
        self.adjacency_matrix[j][i] = 0
        
        if j in self.neighbors[i]:
            self.neighbors[i].remove(j)
        if i in self.neighbors[j]:
            self.neighbors[j].remove(i)
    
    def _ensure_connectivity(self):
        """Ensure minimum graph connectivity"""
        for i in range(self.num_brokers):
            while len(self.neighbors[i]) < self.min_neighbors:
                # Find random node to connect to
                candidates = [j for j in range(self.num_brokers) 
                            if j != i and j not in self.neighbors[i] 
                            and len(self.neighbors[j]) < self.max_neighbors]
                
                if candidates:
                    j = random.choice(candidates)
                    self._add_edge(i, j)
                else:
                    break  # No available candidates
    
    def _initialize_weights(self):
        """Initialize edge weights: b_ij = 2 / (deg(i) + deg(j))"""
        # Calculate node degrees
        degrees = [len(self.neighbors[i]) for i in range(self.num_brokers)]
        
        for i in range(self.num_brokers):
            for j in self.neighbors[i]:
                if i < j:  # Avoid duplication
                    # Edge weight: b_ij = 2 / (deg(i) + deg(j))
                    weight = 2.0 / (degrees[i] + degrees[j]) if (degrees[i] + degrees[j]) > 0 else 0.0
                    self.weights[(i, j)] = weight
                    self.weights[(j, i)] = weight
    
    def get_neighbors(self, broker_id):
        """Return list of neighbors for given broker"""
        return self.neighbors.get(broker_id, [])
    
    def get_weight(self, broker_i, broker_j):
        """Return edge weight between brokers i and j"""
        return self.weights.get((broker_i, broker_j), 0.0)
    
    def update_graph(self):
        """Periodically update graph connectivity"""
        # Apply weight decay
        for edge, weight in self.weights.items():
            self.weights[edge] = weight * self.weight_decay
        
        # Randomly modify graph structure
        if random.random() < 0.1:  # 10% chance of modification
            self._random_graph_modification()
    
    def _random_graph_modification(self):
        """Randomly modify graph structure"""
        action = random.choice(['add', 'remove', 'modify_weight'])
        
        if action == 'add':
            self._add_random_edge()
        elif action == 'remove':
            self._remove_random_edge()
        elif action == 'modify_weight':
            self._modify_random_weight()
    
    def _add_random_edge(self):
        """Add random edge"""
        candidates = []
        for i in range(self.num_brokers):
            for j in range(i + 1, self.num_brokers):
                if (self.adjacency_matrix[i][j] == 0 and 
                    len(self.neighbors[i]) < self.max_neighbors and
                    len(self.neighbors[j]) < self.max_neighbors):
                    candidates.append((i, j))
        
        if candidates:
            i, j = random.choice(candidates)
            self._add_edge(i, j)
            weight = random.uniform(0.1, 1.0)
            self.weights[(i, j)] = weight
            self.weights[(j, i)] = weight
    
    def _remove_random_edge(self):
        """Remove random edge (with constraints)"""
        candidates = []
        for i in range(self.num_brokers):
            if len(self.neighbors[i]) > self.min_neighbors:
                for j in self.neighbors[i]:
                    if len(self.neighbors[j]) > self.min_neighbors:
                        candidates.append((i, j))
        
        if candidates:
            i, j = random.choice(candidates)
            self._remove_edge(i, j)
            if (i, j) in self.weights:
                del self.weights[(i, j)]
            if (j, i) in self.weights:
                del self.weights[(j, i)]
    
    def _modify_random_weight(self):
        """Modify random edge weight"""
        if self.weights:
            edge = random.choice(list(self.weights.keys()))
            new_weight = random.uniform(0.1, 1.0)
            self.weights[edge] = new_weight
            # Update symmetric weight
            reverse_edge = (edge[1], edge[0])
            if reverse_edge in self.weights:
                self.weights[reverse_edge] = new_weight
    
    def get_graph_stats(self):
        """Return graph statistics"""
        total_edges = sum(len(neighbors) for neighbors in self.neighbors.values()) // 2
        avg_degree = total_edges * 2 / self.num_brokers if self.num_brokers > 0 else 0
        
        return {
            'num_nodes': self.num_brokers,
            'num_edges': total_edges,
            'average_degree': avg_degree,
            'density': total_edges / (self.num_brokers * (self.num_brokers - 1) / 2) if self.num_brokers > 1 else 0,
            'weights_count': len(self.weights)
        }
    
    def consensus_update(self, brokers, gamma_consensus=0.02):
        """
        Perform consensus SPSA update:
        θ_i ← θ_i - α * (ĝ + γ * Σ_{j∈neighbors[i]} b_ij * (θ_j - θ_i))
        
        Args:
            brokers: List or dict of brokers
            gamma_consensus: Consensus coefficient
        """
        # Convert brokers to dict if it's a list
        if isinstance(brokers, list):
            broker_dict = {i: broker for i, broker in enumerate(brokers)}
        else:
            broker_dict = brokers
        
        # Consensus update according to SPSA specification
        for broker_id, broker in broker_dict.items():
            neighbors = self.get_neighbors(broker_id)
            
            if not neighbors or not hasattr(broker, 'theta'):
                continue  # Skip brokers without neighbors or theta
            
            # Convert theta to numpy array for calculations
            theta_i = np.array(broker.theta)
            
            # Calculate consensus term: Σ_{j∈neighbors[i]} b_ij * (θ_j - θ_i)
            consensus_term = np.zeros_like(theta_i)
            
            for neighbor_id in neighbors:
                if neighbor_id in broker_dict and hasattr(broker_dict[neighbor_id], 'theta'):
                    neighbor_theta = np.array(broker_dict[neighbor_id].theta)
                    edge_weight = self.get_weight(broker_id, neighbor_id)
                    consensus_term += edge_weight * (neighbor_theta - theta_i)
            
            # Apply consensus correction
            consensus_correction = gamma_consensus * consensus_term
            
            # Update broker's theta
            updated_theta = theta_i + consensus_correction
            broker.theta = updated_theta.tolist()
    
    def visualize_graph(self):
        """Print simple text representation of the graph"""
        print("=== BROKER CONNECTIVITY GRAPH ===")
        for i in range(self.num_brokers):
            neighbors_info = []
            for j in self.neighbors[i]:
                weight = self.get_weight(i, j)
                neighbors_info.append(f"{j}({weight:.2f})")
            
            print(f"Broker {i}: {', '.join(neighbors_info) if neighbors_info else 'no neighbors'}")
        
        stats = self.get_graph_stats()
        print(f"\nStats: {stats['num_edges']} edges, "
              f"density {stats['density']:.2f}, "
              f"average degree {stats['average_degree']:.2f}")
    
    def __str__(self):
        return f"GraphService({self.num_brokers} brokers, {len(self.weights)//2} edges)"
