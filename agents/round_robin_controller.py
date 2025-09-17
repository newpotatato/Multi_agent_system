"""
Simplified Round Robin Controller for Multi-Agent System

This controller implements simple round-robin task distribution
for comparison with SPSA optimization.
"""

import sys
import os
import random
import time

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.config import get_system_config


class RoundRobinController:
    """
    Simple round-robin controller for task distribution.
    """
    
    def __init__(self, controller_id, executors):
        self.controller_id = controller_id
        self.executors = executors
        self.current_executor = 0
        self.load = 0.0
        self.task_count = 0
        self.performance_stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'total_time': 0.0,
            'average_load': 0.0
        }
    
    def process_task(self, task_dict):
        """
        Process a single task using round-robin distribution.
        
        Args:
            task_dict: Dictionary containing task information
            
        Returns:
            Dictionary with processing results
        """
        start_time = time.time()
        
        try:
            # Select next executor in round-robin fashion
            selected_executor = self._select_next_executor()
            
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
                
                # Update load (simple increment)
                self.load += execution_time * 0.1
                self._update_average_load()
                
                return {
                    'status': 'completed',
                    'executor_id': selected_executor.executor_id,
                    'execution_time': total_time,
                    'success': success
                }
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
    
    def _select_next_executor(self):
        """Select the next executor in round-robin order"""
        if not self.executors:
            return None
        
        executor = self.executors[self.current_executor]
        self.current_executor = (self.current_executor + 1) % len(self.executors)
        return executor
    
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
        """Simple load balancing (no-op for round-robin)"""
        # Round-robin doesn't need complex load balancing
        pass
    
    def __str__(self):
        return f"RoundRobinController({self.controller_id}, load={self.load:.2f}, tasks={self.task_count})"
