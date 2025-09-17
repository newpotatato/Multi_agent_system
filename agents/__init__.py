"""
Agents module

Агенты системы: брокеры и исполнители.
"""

from .controller import Broker
from .executor import Executor

__all__ = ['Broker', 'Executor', 'RealLLMExecutor', 'RoundRobinController']
