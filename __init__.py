"""
Multi-Agent System Package

A sophisticated multi-agent system implementing SPSA optimization 
and LVP load balancing for intelligent task distribution.
"""

from .config import (
    get_config,
    get_api_config,
    get_spsa_config,
    get_lvp_config,
    get_system_config,
    get_api_key,
)

from .core.task import Task
from .core.spsa import SPSA
from .core.graph import GraphService

from .agents.controller import Broker
from .agents.executor import Executor
from .agents.real_llm_executor import RealLLMExecutor

try:
    from .providers.provider_manager import ProviderManager
except ImportError:
    # Handle missing provider dependencies gracefully
    ProviderManager = None

__version__ = "2.0.0"
__author__ = "Multi-Agent System Development Team"

__all__ = [
    # Configuration
    'get_config',
    'get_api_config', 
    'get_spsa_config',
    'get_lvp_config',
    'get_system_config',
    'get_api_key',
    
    # Core classes
    'Task',
    'SPSA',
    'GraphService',
    
    # Agents
    'Broker',
    'Executor',
    'RealLLMExecutor',
    
    # Providers
    'ProviderManager',
    
    # Metadata
    '__version__',
    '__author__',
]
