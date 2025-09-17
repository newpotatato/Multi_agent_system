"""
Core algorithms and components for the multi-agent system.
"""

from .task import Task
from .spsa import SPSA
from .graph import GraphService

try:
    from .models import predict_load, predict_waiting_time
except ImportError:
    # Handle missing ML dependencies gracefully
    predict_load = None
    predict_waiting_time = None

__all__ = [
    'Task',
    'SPSA', 
    'GraphService',
    'predict_load',
    'predict_waiting_time',
]
