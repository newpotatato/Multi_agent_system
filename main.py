#!/usr/bin/env python3
"""
Multi-Agent System Main Entry Point

This script provides the main interface for running the multi-agent system
with different modes and configurations.
"""

import sys
import os
import argparse
import asyncio

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from config import get_config, get_api_config
from examples.basic_demo import run_demo as run_basic_demo
from examples.comparison_demo import run_comparison_demo
from examples.llm_demo import run_llm_demo


def print_banner():
    """Print the system banner"""
    print("=" * 60)
    print("Multi-Agent System with SPSA and LVP Algorithms")
    print("Version 2.0.0 - Restructured Architecture")
    print("=" * 60)


def check_configuration():
    """Check and display system configuration"""
    print("\nSystem Configuration:")
    print("-" * 40)
    
    config = get_config()
    config.print_summary()
    
    print("\nAPI Configuration:")
    print("-" * 40)
    api_config = get_api_config()
    api_config.print_status()


def run_basic():
    """Run basic demonstration"""
    print("\nStarting basic demonstration...")
    run_basic_demo()


def run_comparison():
    """Run algorithm comparison"""
    print("\nStarting algorithm comparison...")
    run_comparison_demo()


async def run_llm():
    """Run LLM demonstration"""
    print("\nStarting LLM demonstration...")
    await run_llm_demo()


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(
        description="Multi-Agent System with SPSA and LVP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --config                    Show configuration status
  python main.py --demo basic                Run basic demonstration
  python main.py --demo comparison          Run algorithm comparison
  python main.py --demo llm                 Run LLM demonstration
  python main.py --interactive              Start interactive mode
        """
    )
    
    parser.add_argument(
        '--demo',
        choices=['basic', 'comparison', 'llm'],
        help='Run specific demonstration'
    )
    
    parser.add_argument(
        '--config',
        action='store_true',
        help='Show configuration status and exit'
    )
    
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Start interactive mode'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Multi-Agent System 2.0.0'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        if args.config:
            check_configuration()
        
        elif args.demo == 'basic':
            run_basic()
        
        elif args.demo == 'comparison':
            run_comparison()
        
        elif args.demo == 'llm':
            asyncio.run(run_llm())
        
        elif args.interactive:
            run_interactive()
        
        else:
            # Default behavior - show help and configuration
            parser.print_help()
            print("\n" + "=" * 60)
            check_configuration()
    
    except KeyboardInterrupt:
        print("\nOperation interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def run_interactive():
    """Run interactive mode"""
    print("\nInteractive Mode")
    print("-" * 40)
    print("Available commands:")
    print("1. Basic demonstration")
    print("2. Algorithm comparison")
    print("3. LLM demonstration")  
    print("4. Show configuration")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == '1':
                run_basic()
            elif choice == '2':
                run_comparison()
            elif choice == '3':
                asyncio.run(run_llm())
            elif choice == '4':
                check_configuration()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1-5.")
                
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
