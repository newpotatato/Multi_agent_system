#!/usr/bin/env python3
"""
Real LLM Multi-Agent System Demonstration

This script demonstrates the multi-agent system working with real LLM providers
like OpenAI, Anthropic, and Groq.
"""

import sys
import os
import asyncio

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.task import Task
from agents.real_llm_executor import RealLLMExecutor
from providers.provider_manager import create_default_provider_manager
from config.config import get_api_config


async def create_test_tasks():
    """Create a set of test tasks for LLM demonstration"""
    tasks = [
        {
            'id': 'task_1',
            'type': 'math',
            'prompt': 'Solve: x^2 + 5x + 6 = 0. Show your work step by step.',
            'max_tokens': 150
        },
        {
            'id': 'task_2',
            'type': 'code',
            'prompt': 'Write a Python function that finds the factorial of a number.',
            'max_tokens': 100
        },
        {
            'id': 'task_3',
            'type': 'creative',
            'prompt': 'Write a haiku about artificial intelligence.',
            'max_tokens': 50
        },
        {
            'id': 'task_4',
            'type': 'analysis',
            'prompt': 'Explain the benefits and risks of renewable energy.',
            'max_tokens': 200
        }
    ]
    return tasks


async def setup_llm_system():
    """Set up the LLM-based multi-agent system"""
    print("Setting up LLM multi-agent system...")
    
    # Load API configuration
    try:
        config = get_api_config()
        print("\nAPI Configuration Status:")
        config.print_status()
    except FileNotFoundError:
        print("\nWarning: No API configuration found. Using free providers only.")
        config = None
    
    # Create provider manager
    provider_manager = create_default_provider_manager()
    
    # Check provider availability
    await provider_manager.check_all_providers()
    available_providers = provider_manager.get_available_providers()
    
    if not available_providers:
        print("Error: No LLM providers are available!")
        return None, None
    
    print(f"\nAvailable providers: {list(available_providers.keys())}")
    
    # Create LLM executors for different providers
    executors = []
    for provider_name, models in available_providers.items():
        if models:  # If provider has available models
            executor = RealLLMExecutor(f"executor_{provider_name}", provider_manager)
            executors.append(executor)
    
    return executors, provider_manager


async def run_llm_demo():
    """Run the LLM demonstration"""
    print("=" * 60)
    print("Multi-Agent System with Real LLM Providers")
    print("=" * 60)
    
    # Setup system
    executors, provider_manager = await setup_llm_system()
    if not executors:
        return
    
    # Create test tasks
    tasks = await create_test_tasks()
    
    print(f"\nCreated {len(tasks)} test tasks")
    print(f"System has {len(executors)} LLM executors")
    
    # Display task information
    print("\nTask Information:")
    print("-" * 40)
    for i, task in enumerate(tasks, 1):
        print(f"Task {i}: {task['type'].upper()}")
        print(f"  Prompt: {task['prompt']}")
        print(f"  Max tokens: {task['max_tokens']}")
        print()
    
    # Execute tasks
    print("Executing tasks with LLM providers...")
    results = []
    
    for i, task in enumerate(tasks):
        executor = executors[i % len(executors)]
        print(f"\nAssigning Task {i+1} to {executor.executor_id}")
        
        # Check if executor accepts the task
        accepted, reason = executor.accept_task(task)
        if not accepted:
            print(f"  Task rejected: {reason}")
            continue
        
        print("  Executing...")
        
        # Execute task
        try:
            result = await executor.execute_task(task)
            results.append(result)
            
            # Display result
            if result['status'] == 'success':
                print(f"  SUCCESS (Time: {result['duration']:.2f}s)")
                print(f"  Result: {result['result'][:100]}...")
                print(f"  Tokens: {result['tokens']}, Cost: ${result['cost']:.6f}")
            else:
                print(f"  FAILED: {result['result']}")
                
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            results.append({
                'status': 'error',
                'result': str(e),
                'duration': 0,
                'tokens': 0,
                'cost': 0
            })
    
    # Display summary
    print("\n" + "=" * 60)
    print("EXECUTION SUMMARY")
    print("=" * 60)
    
    successful_tasks = sum(1 for r in results if r['status'] == 'success')
    total_time = sum(r['duration'] for r in results)
    total_tokens = sum(r['tokens'] for r in results)
    total_cost = sum(r['cost'] for r in results)
    
    print(f"Total tasks: {len(tasks)}")
    print(f"Successful: {successful_tasks}")
    print(f"Failed: {len(tasks) - successful_tasks}")
    print(f"Success rate: {(successful_tasks / len(tasks)) * 100:.1f}%")
    print(f"Total execution time: {total_time:.2f}s")
    print(f"Average time per task: {total_time / len(tasks):.2f}s")
    print(f"Total tokens used: {total_tokens}")
    print(f"Total cost: ${total_cost:.6f}")
    
    # Display executor statistics
    print("\nExecutor Statistics:")
    print("-" * 40)
    for executor in executors:
        executor.print_stats()
        print()
    
    print("LLM demo completed successfully!")


if __name__ == "__main__":
    try:
        asyncio.run(run_llm_demo())
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError during demo: {str(e)}")
        import traceback
        traceback.print_exc()
