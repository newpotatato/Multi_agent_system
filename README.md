# Multi-Agent System

A sophisticated multi-agent system implementing SPSA (Simultaneous Perturbation Stochastic Approximation) optimization and LVP (Load Vector Protocol) for intelligent task distribution and load balancing across multiple LLM providers.

## Overview

This system provides automated task classification, intelligent load balancing, and optimization algorithms to efficiently distribute computational tasks across multiple agents and LLM providers. It supports real-time optimization using SPSA algorithms and maintains optimal performance through adaptive load balancing.

## Features

- **Intelligent Task Classification**: Automatic classification of tasks into 9 categories using hybrid NLP techniques
- **SPSA Optimization**: Advanced stochastic optimization for parameter tuning and performance improvement
- **Load Vector Protocol (LVP)**: Dynamic load balancing across multiple agents
- **Multi-Provider LLM Support**: Integration with OpenAI, Anthropic, Groq, and Hugging Face
- **Real-time Performance Monitoring**: Comprehensive metrics and visualization tools
- **Adaptive Learning**: Machine learning models for load and execution time prediction

## System Architecture

```
multi_agent_system/
├── core/              # Core algorithms and task processing
│   ├── task.py        # Task classification and processing
│   ├── spsa.py        # SPSA optimization algorithm
│   ├── graph.py       # Agent connectivity and consensus
│   ├── models.py      # Predictive models for load estimation
│   └── broker_comparison.py  # Algorithm comparison tools
├── agents/            # System agents
│   ├── controller.py  # SPSA-optimized task brokers
│   ├── executor.py    # Task execution agents
│   ├── real_llm_executor.py  # Real LLM integration
│   └── round_robin_controller.py  # Baseline algorithm
├── providers/         # LLM provider implementations
│   ├── provider_manager.py    # Provider management
│   ├── openai_provider.py     # OpenAI integration
│   ├── anthropic_provider.py  # Anthropic Claude integration
│   ├── groq_provider.py       # Groq fast inference
│   └── huggingface_provider.py # Hugging Face models
├── visualization/     # Performance visualization tools
├── config/           # Unified configuration system
├── tests/            # Comprehensive test suite
├── examples/         # Usage examples and demonstrations
├── docs/            # Documentation
└── data/            # Data storage and results
```

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/Multi_agent_system.git
cd Multi_agent_system/multi_agent_system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys (optional for basic functionality):
```bash
# The system will create a template api_keys.json file
python -c "from config import get_api_config; get_api_config().print_status()"
```

### Basic Usage

Run a simple demonstration:
```bash
python examples/basic_demo.py
```

Test with real LLM providers:
```bash
python examples/llm_demo.py
```

Compare SPSA vs Round-Robin algorithms:
```bash
python examples/comparison_demo.py
```

### Configuration

The system uses a unified configuration system in `config/config.py`. Key parameters:

```python
from config import get_config

config = get_config()

# SPSA parameters
config.spsa.alpha = 0.01          # Learning rate
config.spsa.beta = 0.1            # Perturbation size

# System parameters  
config.system.num_brokers = 3     # Number of brokers
config.system.num_executors = 4   # Executors per broker

# Save configuration
config.save_to_file()
```

## Core Components

### Task Classification System

The system automatically classifies tasks into 9 categories:
- **Math**: Mathematical problems and equations
- **Code**: Programming and software development
- **Analysis**: Data analysis and research
- **Creative**: Creative writing and content generation
- **Explanation**: Educational and explanatory content
- **Planning**: Project management and planning
- **Research**: Information gathering and research
- **Optimization**: Performance and efficiency optimization
- **Text**: General text processing and manipulation

### SPSA Algorithm

Implements Simultaneous Perturbation Stochastic Approximation for:
- Parameter optimization across multiple agents
- Adaptive learning and performance improvement
- Consensus building between distributed brokers
- Dynamic load balancing optimization

### Load Vector Protocol (LVP)

Advanced load balancing featuring:
- Real-time load monitoring across all agents
- Predictive load estimation using machine learning
- Dynamic task redistribution based on agent capabilities
- Network-aware routing and optimization

### Multi-Provider LLM Support

Integrated support for:
- **OpenAI**: GPT-3.5, GPT-4, and future models
- **Anthropic**: Claude-3 family models
- **Groq**: High-speed inference with Llama and Mixtral
- **Hugging Face**: Open-source model ecosystem
- **Local Models**: Support for local model deployments

## Algorithm Comparison

The system includes built-in comparison tools to evaluate:

| Algorithm | Strengths | Use Cases |
|-----------|-----------|-----------|
| SPSA | Adaptive optimization, consensus building | Dynamic environments, multi-objective optimization |
| Round-Robin | Simple, predictable | Uniform workloads, baseline comparisons |
| LVP | Load-aware distribution | Variable task complexity, heterogeneous agents |

## Performance Monitoring

Comprehensive metrics tracking:
- Task execution times and success rates
- Agent load distribution and utilization
- Algorithm convergence and optimization progress
- Cost tracking for paid LLM providers
- Token usage and efficiency metrics

## Testing

Run the complete test suite:
```bash
# Unit tests
python -m pytest tests/test_task.py

# Integration tests
python tests/test_full_architecture.py

# Real LLM tests (requires API keys)
python tests/test_real_llm_pipeline.py
```

## API Reference

### Core Classes

```python
from core import Task, SPSA, GraphService
from agents import Broker, Executor, RealLLMExecutor
from providers import ProviderManager
from config import get_config

# Create and classify a task
task = Task("Solve x^2 + 5x + 6 = 0", priority=7, complexity=6)
print(f"Task type: {task.type}")

# Initialize system components
config = get_config()
executors = [Executor(f"executor_{i}") for i in range(4)]
broker = Broker("main_broker", executors)

# Process task
result = broker.process_task(task.to_dict())
```

### Configuration Management

```python
from config import get_config, get_api_config

# System configuration
config = get_config()
config.system.num_brokers = 5
config.spsa.alpha = 0.02
config.save_to_file()

# API configuration
api_config = get_api_config()
print(f"Configured services: {api_config.get_configured_services()}")
```

## Development

### Adding New Providers

1. Create a new provider class inheriting from `BaseProvider`
2. Implement required methods: `execute_task()`, `check_availability()`
3. Register the provider in `ProviderManager`

### Extending Task Classification

1. Add new task types to `core/task.py`
2. Update classification keywords and patterns
3. Retrain the classification model if needed

### Custom Algorithms

1. Implement algorithm in `core/` directory
2. Create corresponding agent controller
3. Add comparison metrics in `visualization/`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with comprehensive tests
4. Submit a pull request with detailed description

## Performance Benchmarks

Typical performance on standard hardware:
- Task classification: <100ms per task
- SPSA convergence: 50-100 iterations
- Load balancing response: <50ms
- End-to-end task processing: 1-30s (depending on complexity)

## License

MIT License - see LICENSE file for details.

## Citation

If you use this system in academic research, please cite:

```bibtex
@software{multi_agent_system,
  title={Multi-Agent System with SPSA and LVP Algorithms},
  author={Multi-Agent System Development Team},
  year={2025},
  url={https://github.com/your-username/Multi_agent_system}
}
```

## Version History

- **v1.0.0**: Initial release with SPSA optimization and LVP load balancing
- **v1.1.0**: Added real LLM provider support and enhanced visualization
- **v2.0.0**: Restructured architecture with simplified configuration system

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Check the documentation in `docs/`
- Review example implementations in `examples/`
