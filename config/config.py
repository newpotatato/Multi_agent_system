"""
Multi-Agent System Configuration

Unified configuration system for all components including algorithms,
system parameters, and API settings.
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SPSAConfig:
    """SPSA Algorithm Configuration"""
    alpha: float = 0.01           # Learning rate
    beta: float = 0.1             # Perturbation size
    gamma_consensus: float = 0.02 # Consensus coefficient
    update_frequency: int = 10    # Parameter update frequency (tasks)


@dataclass
class LVPConfig:
    """Load Vector Protocol Configuration"""
    h: float = 0.1           # Neighbor interaction coefficient
    gamma: float = 0.05      # Local load balance coefficient


@dataclass
class SystemConfig:
    """General System Configuration"""
    num_brokers: int = 3         # Number of brokers
    num_executors: int = 4       # Number of executors per broker
    max_concurrent_tasks: int = 3 # Max concurrent tasks per executor
    timeout_threshold: float = 30.0  # Task timeout in seconds
    log_level: str = "INFO"      # Logging level
    

@dataclass
class ModelConfig:
    """Predictive Models Configuration"""
    feature_dim: int = 10        # Task feature dimensions
    theta_dim: int = 5           # Parameter theta dimensions
    l1_lambda: float = 0.01      # L1 regularization coefficient
    history_size: int = 1000     # Training history size


@dataclass
class TaskConfig:
    """Task Classification Configuration"""
    confidence_threshold: float = 0.5  # Minimum confidence for classification
    max_tokens: int = 500              # Default max tokens for LLM tasks
    priority_weight: float = 0.3       # Priority importance in scheduling
    complexity_weight: float = 0.7     # Complexity importance in scheduling


class APIConfig:
    """API Keys and Provider Configuration"""
    
    def __init__(self, config_path: str = "api_keys.json"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not os.path.exists(self.config_path):
            return self._create_default_config()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default API configuration"""
        default_config = {
            "openai": {
                "api_key": "",
                "models": ["gpt-3.5-turbo", "gpt-4"],
                "base_url": "https://api.openai.com/v1",
                "description": "OpenAI GPT Models"
            },
            "anthropic": {
                "api_key": "",
                "models": ["claude-3-sonnet", "claude-3-haiku"],
                "base_url": "https://api.anthropic.com",
                "description": "Anthropic Claude Models"
            },
            "groq": {
                "api_key": "",
                "models": ["llama-3.1-70b", "mixtral-8x7b"],
                "base_url": "https://api.groq.com/openai/v1",
                "description": "Groq Fast Inference"
            },
            "huggingface": {
                "api_key": "",
                "models": ["microsoft/DialoGPT-medium"],
                "base_url": "https://api-inference.huggingface.co",
                "description": "Hugging Face Models"
            }
        }
        
        # Save default config
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
        except:
            pass  # Ignore write errors
        
        return default_config
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        service_config = self.config.get(service, {})
        if isinstance(service_config, str):
            return service_config if service_config else None
        elif isinstance(service_config, dict):
            api_key = service_config.get('api_key', '')
            return api_key if api_key else None
        return None
    
    def is_service_configured(self, service: str) -> bool:
        """Check if a service is properly configured"""
        api_key = self.get_api_key(service)
        return api_key is not None and api_key.strip() != ""
    
    def get_service_config(self, service: str) -> Dict[str, Any]:
        """Get complete service configuration"""
        return self.config.get(service, {})
    
    def get_configured_services(self) -> list:
        """Get list of configured services"""
        return [
            service for service in self.config.keys()
            if self.is_service_configured(service)
        ]
    
    def print_status(self):
        """Print configuration status"""
        print("API Configuration Status:")
        print("-" * 40)
        for service, config in self.config.items():
            status = "✓ Configured" if self.is_service_configured(service) else "✗ Not configured"
            if isinstance(config, dict):
                description = config.get('description', service.title())
                print(f"{service.upper()}: {status}")
                print(f"  {description}")
            else:
                print(f"{service.upper()}: {status}")
            print()


class MultiAgentConfig:
    """Main configuration class for the multi-agent system"""
    
    def __init__(self):
        self.spsa = SPSAConfig()
        self.lvp = LVPConfig()
        self.system = SystemConfig()
        self.model = ModelConfig()
        self.task = TaskConfig()
        self.api = APIConfig()
    
    def update_from_dict(self, config_dict: Dict[str, Any]):
        """Update configuration from dictionary"""
        for section, values in config_dict.items():
            if hasattr(self, section) and isinstance(values, dict):
                section_config = getattr(self, section)
                for key, value in values.items():
                    if hasattr(section_config, key):
                        setattr(section_config, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'spsa': self.spsa.__dict__,
            'lvp': self.lvp.__dict__,
            'system': self.system.__dict__,
            'model': self.model.__dict__,
            'task': self.task.__dict__
        }
    
    def save_to_file(self, path: str = "system_config.json"):
        """Save configuration to file"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def load_from_file(self, path: str = "system_config.json"):
        """Load configuration from file"""
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    config_dict = json.load(f)
                    self.update_from_dict(config_dict)
            except (json.JSONDecodeError, FileNotFoundError):
                pass  # Use defaults if file is invalid
    
    def print_summary(self):
        """Print configuration summary"""
        print("Multi-Agent System Configuration Summary")
        print("=" * 50)
        print(f"Brokers: {self.system.num_brokers}")
        print(f"Executors per broker: {self.system.num_executors}")
        print(f"Max concurrent tasks: {self.system.max_concurrent_tasks}")
        print(f"Task timeout: {self.system.timeout_threshold}s")
        print(f"SPSA learning rate: {self.spsa.alpha}")
        print(f"LVP neighbor coefficient: {self.lvp.h}")
        print(f"API services configured: {len(self.api.get_configured_services())}")


# Global configuration instance
_config_instance = None


def get_config() -> MultiAgentConfig:
    """Get the global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = MultiAgentConfig()
        _config_instance.load_from_file()
    return _config_instance


def get_api_config() -> APIConfig:
    """Get API configuration"""
    return get_config().api


# Export commonly used configurations
def get_spsa_config() -> SPSAConfig:
    """Get SPSA configuration"""
    return get_config().spsa


def get_lvp_config() -> LVPConfig:
    """Get LVP configuration"""
    return get_config().lvp


def get_system_config() -> SystemConfig:
    """Get system configuration"""
    return get_config().system


# Convenience function for quick API key access
def get_api_key(service: str) -> Optional[str]:
    """Quick access to API keys"""
    return get_api_config().get_api_key(service)
