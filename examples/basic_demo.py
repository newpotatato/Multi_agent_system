#!/usr/bin/env python3
"""
Basic Multi-Agent System Demonstration

This script demonstrates the core functionality of the multi-agent system
with SPSA optimization and LVP load balancing.
"""

import sys
import os
import asyncio

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.task import Task
from core.spsa import SPSA
from core.graph import GraphService
from agents.controller import Broker
from agents.executor import Executor


def create_test_tasks():
    """Create a set of test tasks for demonstration"""
    tasks = [
        Task("Solve the equation x^2 + 5x + 6 = 0", priority=7, complexity=6),
        Task("Write a Python function to sort a list", priority=5, complexity=4),
        Task("Explain the concept of machine learning", priority=6, complexity=7),
        Task("Create a simple web page layout", priority=4, complexity=5),
        Task("Optimize database query performance", priority=8, complexity=8),
    ]
    return tasks


def setup_system():
    """Set up the multi-agent system components"""
    print("Setting up multi-agent system...")
    
    # Create executors
    executors = [
        Executor(f"executor_{i}", load_capacity=10) 
        for i in range(4)
    ]
    
    # Create brokers
    brokers = [
        Broker(f"broker_{i}", executors) 
        for i in range(3)
    ]
    
    # Create graph service for broker coordination
    graph_service = GraphService(brokers)
    
    # Initialize SPSA optimizer
    spsa = SPSA(
        alpha=0.01,    # learning rate
        beta=0.1,      # perturbation size
        gamma=0.02     # consensus coefficient
    )
    
    return brokers, executors, graph_service, spsa


def run_demo():
    """Run the basic demonstration"""
    print("=" * 60)
    print("Multi-Agent System with SPSA and LVP - Basic Demo")
    print("=" * 60)
    
    # Setup system
    brokers, executors, graph_service, spsa = setup_system()
    
    # Create test tasks
    tasks = create_test_tasks()
    
    print(f"\nCreated {len(tasks)} test tasks")
    print(f"System has {len(brokers)} brokers and {len(executors)} executors")
    
    # Display task information
    print("\nTask Classification Results:")
    print("-" * 40)
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}: {task.type.upper()}")
        print(f"  Prompt: {task.prompt[:60]}...")
        print(f"  Priority: {task.priority}, Complexity: {task.complexity}")
        print(f"  Confidence: {task.get_confidence_score():.2f}")
        print()
    
    # Distribute tasks among brokers
    print("Distributing tasks to brokers...")
    results = []
    
    for i, task in enumerate(tasks):
        broker = brokers[i % len(brokers)]
        print(f"Assigning Task {i+1} to {broker.broker_id}")
        
        # Simulate task execution
        result = broker.process_task(task.to_dict())
        results.append(result)
    
    # Display results
    print("\nExecution Results:")
    print("-" * 40)
    successful_tasks = 0
    total_time = 0
    
    for i, result in enumerate(results, 1):
        if result.get('status') == 'completed':
            successful_tasks += 1
            execution_time = result.get('execution_time', 0)
            total_time += execution_time
            print(f"Task {i}: SUCCESS (Time: {execution_time:.2f}s)")
        else:
            print(f"Task {i}: FAILED ({result.get('error', 'Unknown error')})")
    
    # Display summary
    print("\nSummary:")
    print("-" * 40)
    print(f"Total tasks: {len(tasks)}")
    print(f"Successful: {successful_tasks}")
    print(f"Failed: {len(tasks) - successful_tasks}")
    print(f"Success rate: {(successful_tasks / len(tasks)) * 100:.1f}%")
    print(f"Total execution time: {total_time:.2f}s")
    print(f"Average time per task: {total_time / len(tasks):.2f}s")
    
    # Display broker statistics
    print("\nBroker Statistics:")
    print("-" * 40)
    for broker in brokers:
        stats = broker.get_performance_stats()
        print(f"{broker.broker_id}:")
        print(f"  Tasks processed: {stats.get('total_tasks', 0)}")
        print(f"  Average load: {stats.get('average_load', 0):.2f}")
        print(f"  Success rate: {stats.get('success_rate', 0):.1f}%")
        print()
    
    print("Demo completed successfully!")


if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError during demo: {str(e)}")
        import traceback
        traceback.print_exc()
