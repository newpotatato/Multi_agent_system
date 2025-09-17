#!/usr/bin/env python3
"""
Algorithm Comparison Demonstration

This script compares the performance of SPSA optimization vs Round-Robin
task distribution in the multi-agent system.
"""

import sys
import os
import time
import statistics

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.task import Task
from core.spsa import SPSA
from agents.controller import Broker
from agents.round_robin_controller import RoundRobinController
from agents.executor import Executor


def create_test_workload(size='medium'):
    """Create a test workload of various complexity levels"""
    workloads = {
        'small': 10,
        'medium': 25,
        'large': 50
    }
    
    num_tasks = workloads.get(size, 25)
    tasks = []
    
    # Create diverse tasks with different complexities
    task_templates = [
        ("Solve mathematical equation", "math", 5, 6),
        ("Write Python code", "code", 6, 7),
        ("Analyze data trends", "analysis", 7, 8),
        ("Create creative content", "creative", 4, 5),
        ("Explain technical concept", "explanation", 5, 6),
        ("Optimize system performance", "optimization", 8, 9),
        ("Research topic", "research", 6, 7),
        ("Plan project timeline", "planning", 5, 6),
    ]
    
    for i in range(num_tasks):
        template = task_templates[i % len(task_templates)]
        task = Task(
            prompt=f"{template[0]} #{i+1}",
            priority=template[2] + (i % 3) - 1,  # Vary priority
            complexity=template[3] + (i % 3) - 1   # Vary complexity
        )
        tasks.append(task)
    
    return tasks


def setup_spsa_system():
    """Set up system with SPSA optimization"""
    # Create executors with varying capabilities
    executors = [
        Executor("executor_1", load_capacity=8),
        Executor("executor_2", load_capacity=10),
        Executor("executor_3", load_capacity=12),
        Executor("executor_4", load_capacity=9),
    ]
    
    # Create SPSA-optimized brokers
    brokers = [
        Broker(f"spsa_broker_{i}", executors) 
        for i in range(3)
    ]
    
    return brokers, executors


def setup_roundrobin_system():
    """Set up system with Round-Robin distribution"""
    # Create same executors for fair comparison
    executors = [
        Executor("executor_1", load_capacity=8),
        Executor("executor_2", load_capacity=10),
        Executor("executor_3", load_capacity=12),
        Executor("executor_4", load_capacity=9),
    ]
    
    # Create Round-Robin controller
    controller = RoundRobinController("rr_controller", executors)
    
    return [controller], executors


def run_algorithm_test(system_type, tasks):
    """Run test with specified algorithm"""
    print(f"\nRunning {system_type} algorithm test...")
    
    if system_type == "SPSA":
        brokers, executors = setup_spsa_system()
    else:
        brokers, executors = setup_roundrobin_system()
    
    # Track execution metrics
    start_time = time.time()
    results = []
    execution_times = []
    load_distributions = []
    
    # Process all tasks
    for i, task in enumerate(tasks):
        broker = brokers[i % len(brokers)]
        
        # Record start time for this task
        task_start = time.time()
        
        # Process task
        result = broker.process_task(task.to_dict())
        results.append(result)
        
        # Record execution time
        task_time = time.time() - task_start
        execution_times.append(task_time)
        
        # Record load distribution across executors
        current_loads = [executor.current_load for executor in executors]
        load_distributions.append(current_loads)
    
    total_time = time.time() - start_time
    
    # Calculate metrics
    successful_tasks = sum(1 for r in results if r.get('status') == 'completed')
    success_rate = (successful_tasks / len(tasks)) * 100
    avg_execution_time = statistics.mean(execution_times)
    
    # Calculate load balance metrics
    load_variances = []
    for loads in load_distributions:
        if len(set(loads)) > 1:  # Only if there's variation
            load_variances.append(statistics.variance(loads))
    
    avg_load_variance = statistics.mean(load_variances) if load_variances else 0
    
    return {
        'algorithm': system_type,
        'total_time': total_time,
        'success_rate': success_rate,
        'avg_execution_time': avg_execution_time,
        'load_balance': avg_load_variance,
        'successful_tasks': successful_tasks,
        'total_tasks': len(tasks),
        'results': results
    }


def run_comparison_demo():
    """Run the algorithm comparison demonstration"""
    print("=" * 60)
    print("Algorithm Comparison: SPSA vs Round-Robin")
    print("=" * 60)
    
    # Create test workload
    print("\nGenerating test workload...")
    tasks = create_test_workload('medium')
    print(f"Created {len(tasks)} test tasks")
    
    # Display task distribution
    task_types = {}
    for task in tasks:
        task_types[task.type] = task_types.get(task.type, 0) + 1
    
    print("\nTask Type Distribution:")
    for task_type, count in task_types.items():
        print(f"  {task_type}: {count} tasks")
    
    # Run tests with both algorithms
    print("\nRunning comparison tests...")
    print("=" * 40)
    
    # Test SPSA algorithm
    spsa_results = run_algorithm_test("SPSA", tasks)
    
    # Test Round-Robin algorithm  
    rr_results = run_algorithm_test("Round-Robin", tasks)
    
    # Display comparison results
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS")
    print("=" * 60)
    
    # Create comparison table
    print(f"{'Metric':<20} {'SPSA':<15} {'Round-Robin':<15} {'Winner':<10}")
    print("-" * 65)
    
    metrics = [
        ('Total Time (s)', 'total_time', 'lower'),
        ('Success Rate (%)', 'success_rate', 'higher'),
        ('Avg Task Time (s)', 'avg_execution_time', 'lower'),
        ('Load Balance', 'load_balance', 'lower'),
        ('Successful Tasks', 'successful_tasks', 'higher'),
    ]
    
    spsa_wins = 0
    rr_wins = 0
    
    for metric_name, metric_key, better in metrics:
        spsa_val = spsa_results[metric_key]
        rr_val = rr_results[metric_key]
        
        if better == 'lower':
            winner = "SPSA" if spsa_val < rr_val else "Round-Robin"
            if spsa_val < rr_val:
                spsa_wins += 1
            else:
                rr_wins += 1
        else:
            winner = "SPSA" if spsa_val > rr_val else "Round-Robin"
            if spsa_val > rr_val:
                spsa_wins += 1
            else:
                rr_wins += 1
        
        print(f"{metric_name:<20} {spsa_val:<15.3f} {rr_val:<15.3f} {winner:<10}")
    
    print("-" * 65)
    print(f"{'OVERALL WINNER':<20} {'SPSA: ' + str(spsa_wins):<15} {'RR: ' + str(rr_wins):<15} {'SPSA' if spsa_wins > rr_wins else 'Round-Robin':<10}")
    
    # Performance analysis
    print(f"\nPerformance Analysis:")
    print("-" * 40)
    
    if rr_results['total_time'] > 0:
        time_improvement = ((rr_results['total_time'] - spsa_results['total_time']) / rr_results['total_time']) * 100
        if time_improvement > 0:
            print(f"SPSA was {time_improvement:.1f}% faster than Round-Robin")
        else:
            print(f"Round-Robin was {abs(time_improvement):.1f}% faster than SPSA")
    else:
        print("Both algorithms completed in negligible time")
    
    success_improvement = spsa_results['success_rate'] - rr_results['success_rate']
    
    print(f"SPSA had {success_improvement:.1f}% points higher success rate")
    
    # Load balancing analysis
    if spsa_results['load_balance'] < rr_results['load_balance']:
        if rr_results['load_balance'] > 0:
            balance_improvement = ((rr_results['load_balance'] - spsa_results['load_balance']) / rr_results['load_balance']) * 100
            print(f"SPSA achieved {balance_improvement:.1f}% better load balancing")
        else:
            print("Both algorithms achieved perfect load balancing")
    else:
        if spsa_results['load_balance'] > 0:
            balance_improvement = ((spsa_results['load_balance'] - rr_results['load_balance']) / spsa_results['load_balance']) * 100
            print(f"Round-Robin achieved {balance_improvement:.1f}% better load balancing")
        else:
            print("Both algorithms achieved perfect load balancing")
    
    print("\nComparison completed successfully!")


if __name__ == "__main__":
    try:
        run_comparison_demo()
    except KeyboardInterrupt:
        print("\nComparison interrupted by user")
    except Exception as e:
        print(f"\nError during comparison: {str(e)}")
        import traceback
        traceback.print_exc()
