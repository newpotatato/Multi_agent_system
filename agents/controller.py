"""
Simplified Broker Controller for Multi-Agent System

This broker implements SPSA optimization and LVP load balancing
for task distribution among executors.
"""

import sys
import os
import random
import numpy as np
import time

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.models import predict_load, predict_waiting_time
from core.spsa import SPSA
from config.config import get_spsa_config, get_lvp_config, get_system_config


class Broker:
    """
    SPSA-optimized broker for intelligent task distribution.
    """
    
    def __init__(self, broker_id, executors):
        self.broker_id = broker_id
        self.executors = executors
        self.load = 0.0
        self.task_count = 0
        self.history = []
        self.performance_stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'total_time': 0.0,
            'average_load': 0.0
        }
        
        # SPSA parameters
        self.theta = np.random.uniform(-0.5, 0.5, len(executors))
        
        # Load balancing
        self.neighbors = []
        
    def add_neighbor(self, neighbor_broker):
        """Add a neighbor broker for load balancing"""
        if neighbor_broker not in self.neighbors:
            self.neighbors.append(neighbor_broker)
    
    def process_task(self, task_dict):
        """
        Process a single task using SPSA optimization.
        
        Args:
            task_dict: Dictionary containing task information
            
        Returns:
            Dictionary with processing results
        """
        start_time = time.time()
        
        try:
            # Select best executor using SPSA
            selected_executor = self._select_executor(task_dict)
            
            # Execute task
            if selected_executor:
                # Simulate task execution
                execution_time = random.uniform(0.5, 3.0)
                success = random.random() > 0.1  # 90% success rate
                
                # Update statistics
                self.task_count += 1
                self.performance_stats['total_tasks'] += 1
                
                if success:
                    self.performance_stats['successful_tasks'] += 1
                
                total_time = time.time() - start_time
                self.performance_stats['total_time'] += total_time
                
                # Update load
                self.load += execution_time * 0.1
                self._update_average_load()
                
                result = {
                    'status': 'completed',
                    'executor_id': selected_executor.executor_id,
                    'execution_time': total_time,
                    'success': success
                }
                
                # Store in history for SPSA learning
                self.history.append((task_dict, result, execution_time))
                
                # Update SPSA parameters if enough history
                if len(self.history) >= 10:
                    self._update_spsa_parameters()
                
                return result
                
            else:
                return {
                    'status': 'failed',
                    'error': 'No available executor',
                    'execution_time': time.time() - start_time
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def _select_executor(self, task_dict):
        """
        Select the best executor using SPSA-optimized parameters.
        """
        if not self.executors:
            return None
        
        # Calculate executor scores using SPSA parameters
        scores = []
        for i, executor in enumerate(self.executors):
            # Simple feature extraction from task
            features = self._extract_features(task_dict)
            
            # Calculate score using SPSA parameters
            score = np.dot(features, self.theta) + random.uniform(-0.1, 0.1)
            scores.append((score, executor))
        
        # Select executor with highest score
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[0][1]
    
    def _extract_features(self, task_dict):
        """Extract numerical features from task for SPSA optimization"""
        features = np.zeros(len(self.executors))
        
        # Basic features
        priority = task_dict.get('priority', 5)
        complexity = task_dict.get('complexity', 5)
        text_length = len(str(task_dict.get('prompt', '')))
        
        # Normalize features
        features[0] = priority / 10.0
        features[1] = complexity / 10.0
        features[2] = min(text_length / 1000.0, 1.0)
        
        # Add random features for remaining dimensions
        for i in range(3, len(features)):
            features[i] = random.uniform(-0.5, 0.5)
        
        return features
    
    def _update_spsa_parameters(self):
        """Update SPSA parameters based on performance history"""
        if len(self.history) < 10:
            return
        
        config = get_spsa_config()
        alpha = config.alpha
        beta = config.beta
        
        # Calculate loss function based on recent performance
        recent_history = self.history[-10:]
        loss = self._calculate_loss(recent_history)
        
        # SPSA update
        delta = np.random.choice([-1, 1], size=len(self.theta))
        
        theta_plus = self.theta + beta * delta
        theta_minus = self.theta - beta * delta
        
        loss_plus = self._simulate_loss(theta_plus)
        loss_minus = self._simulate_loss(theta_minus)
        
        # Gradient approximation
        grad_approx = (loss_plus - loss_minus) / (2 * beta) * delta
        
        # Update parameters
        self.theta -= alpha * grad_approx
        
        # Clip to reasonable bounds
        self.theta = np.clip(self.theta, -2.0, 2.0)
    
    def _calculate_loss(self, history):
        """Calculate loss function for SPSA optimization"""
        if not history:
            return 1.0
        
        total_loss = 0.0
        for task_dict, result, exec_time in history:
            # Loss based on execution time and success
            time_loss = exec_time / 5.0  # Normalize to expected max time
            success_loss = 0.0 if result['success'] else 1.0
            total_loss += time_loss + success_loss
        
        return total_loss / len(history)
    
    def _simulate_loss(self, theta):
        """Simulate loss for given theta parameters"""
        # Simple simulation - in practice this would be more sophisticated
        return np.sum(theta ** 2) * 0.1 + random.uniform(0, 0.1)
    
    def _update_average_load(self):
        """Update average load statistics"""
        if self.performance_stats['total_tasks'] > 0:
            self.performance_stats['average_load'] = (
                self.load / self.performance_stats['total_tasks']
            )
    
    def get_performance_stats(self):
        """Get current performance statistics"""
        stats = self.performance_stats.copy()
        
        if stats['total_tasks'] > 0:
            stats['success_rate'] = (
                stats['successful_tasks'] / stats['total_tasks'] * 100
            )
            stats['average_execution_time'] = (
                stats['total_time'] / stats['total_tasks']
            )
        else:
            stats['success_rate'] = 0.0
            stats['average_execution_time'] = 0.0
        
        return stats
    
    def balance_load(self):
        """Implement LVP load balancing with neighbors"""
        if not self.neighbors:
            return
        
        config = get_lvp_config()
        h = config.h
        gamma = config.gamma
        
        # Calculate load difference with neighbors
        neighbor_loads = [neighbor.load for neighbor in self.neighbors]
        if not neighbor_loads:
            return
        
        avg_neighbor_load = np.mean(neighbor_loads)
        load_difference = self.load - avg_neighbor_load
        
        # Apply LVP correction
        load_adjustment = -h * load_difference - gamma * load_difference
        
        # Apply adjustment (simplified)
        self.load = max(0, self.load + load_adjustment * 0.1)
    
    def __str__(self):
        return f"Broker({self.broker_id}, load={self.load:.2f}, tasks={self.task_count})"
