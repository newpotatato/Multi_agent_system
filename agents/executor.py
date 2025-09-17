"""
Simplified Executor for Multi-Agent System

This executor simulates task execution with configurable load capacity
and performance metrics.
"""

import time
import random
from datetime import datetime
import sys
import os

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.config import get_system_config


class Executor:
    """
    Simplified executor for task processing with load management.
    """
    
    def __init__(self, executor_id, load_capacity=10):
        self.executor_id = executor_id
        self.load_capacity = load_capacity
        self.current_load = 0
        self.task_count = 0
        self.performance_stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'total_time': 0.0,
            'total_tokens': 0
        }
    
    def accept_task(self, task):
        """
        Accept or reject a task based on current load.
        
        Args:
            task: Task dictionary or object
            
        Returns:
            tuple: (accepted: bool, reason: str)
        """
        if self.current_load >= self.load_capacity:
            return False, "Executor at capacity"
        
        # Accept task with high probability unless overloaded
        acceptance_prob = max(0.1, 1.0 - (self.current_load / self.load_capacity))
        
        if random.random() < acceptance_prob:
            return True, "Task accepted"
        else:
            return False, "Task rejected due to load"
    
    def execute_task(self, task):
        """
        Execute a task and return results with metrics.
        
        Args:
            task: Task dictionary
            
        Returns:
            Dictionary with execution results
        """
        start_time = datetime.now()
        self.current_load += 1
        
        try:
            # Extract task properties
            task_id = task.get('id', f'task_{self.task_count}')
            complexity = task.get('complexity', 5)
            priority = task.get('priority', 5)
            
            # Simulate execution time based on complexity
            base_time = (complexity / 10.0) * 2.0  # 0-2 seconds base
            execution_time = base_time + random.uniform(-0.5, 1.0)
            execution_time = max(0.1, execution_time)  # Minimum 0.1s
            
            # Quick simulation (don't actually wait)
            time.sleep(execution_time * 0.1)  # 10x faster simulation
            
            # Simulate token generation
            tokens_generated = int(complexity * 20 + random.randint(10, 100))
            
            # Success probability based on load
            load_factor = 1.0 - (self.current_load / self.load_capacity)
            success_prob = 0.95 * load_factor + 0.05  # 5-95% success rate
            
            if random.random() < success_prob:
                status = "success"
                result = f"Task {task_id} completed by {self.executor_id}"
                self.performance_stats['successful_tasks'] += 1
            else:
                status = "error"
                result = f"Task {task_id} failed during execution"
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Update statistics
            self.task_count += 1
            self.performance_stats['total_tasks'] += 1
            self.performance_stats['total_time'] += duration
            self.performance_stats['total_tokens'] += tokens_generated
            
            self.current_load -= 1
            
            return {
                'task_id': task_id,
                'executor_id': self.executor_id,
                'start_time': start_time,
                'end_time': end_time,
                'duration': duration,
                'tokens': tokens_generated,
                'status': status,
                'result': result,
                'cost': tokens_generated * 0.001  # Simple cost calculation
            }
            
        except Exception as e:
            end_time = datetime.now()
            self.current_load = max(0, self.current_load - 1)
            
            return {
                'task_id': task.get('id', 'unknown'),
                'executor_id': self.executor_id,
                'start_time': start_time,
                'end_time': end_time,
                'duration': (end_time - start_time).total_seconds(),
                'tokens': 0,
                'status': 'error',
                'result': f"Execution failed: {str(e)}",
                'cost': 0.0
            }
    
    def get_availability(self):
        """Get current availability as a percentage."""
        return max(0, (self.load_capacity - self.current_load) / self.load_capacity)
    
    def get_status(self):
        """Get current executor status."""
        return {
            'id': self.executor_id,
            'current_load': self.current_load,
            'load_capacity': self.load_capacity,
            'utilization': self.current_load / self.load_capacity,
            'availability': self.get_availability(),
            'task_count': self.task_count
        }
    
    def get_performance_stats(self):
        """Get performance statistics."""
        stats = self.performance_stats.copy()
        
        if stats['total_tasks'] > 0:
            stats['success_rate'] = (
                stats['successful_tasks'] / stats['total_tasks'] * 100
            )
            stats['average_time'] = stats['total_time'] / stats['total_tasks']
            stats['average_tokens'] = stats['total_tokens'] / stats['total_tasks']
        else:
            stats['success_rate'] = 0.0
            stats['average_time'] = 0.0
            stats['average_tokens'] = 0.0
        
        return stats
    
    def reset_stats(self):
        """Reset performance statistics."""
        self.performance_stats = {
            'total_tasks': 0,
            'successful_tasks': 0,
            'total_time': 0.0,
            'total_tokens': 0
        }
        self.task_count = 0
    
    def __str__(self):
        return f"Executor({self.executor_id}, load={self.current_load}/{self.load_capacity})"
