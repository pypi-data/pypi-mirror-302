from capibara_model.config import CapibaraConfig
import torch
import pytest
from typing import Dict, Any

__all__ = ['create_test_model', 'TEST_CONFIG', 'initialize_tests']

DEFAULT_CONFIG: Dict[str, Any] = {
    'input_dim': 64,
    'byte_output_dim': 128,
    'state_dim': 256,
    'mamba_output_dim': 512,
    'hidden_dim': 1024,
    'output_dim': 2048,
    'vocab_size': 1000,
    'max_length': 50,
    'num_layers': 4
}

# `TEST_CONFIG` defines the common configuration for model testing. This configuration should be used
# across all tests to ensure consistency unless a specific test requires different parameters.
# Modify this configuration only when you need to change the default testing environment for all tests.
TEST_CONFIG = CapibaraConfig(**DEFAULT_CONFIG)


def create_test_model(overrides: Dict[str, Any] = None, device: str = 'cpu'):
    """
    Creates a CapibaraTextGenerator model using the test configuration, allowing for optional overrides.

    Args:
        overrides (dict, optional): Dictionary with configuration fields to override.
        device (str, optional): The device to move the model to ('cpu', 'cuda', 'tpu'). Defaults to 'cpu'.

    Returns:
        CapibaraTextGenerator: A text generator model instance initialized with 
        the TEST_CONFIG settings or overridden settings, moved to the specified device.
    """
    from capibara_model.model import CapibaraTextGenerator

    config_dict = DEFAULT_CONFIG.copy()
    if overrides:
        config_dict.update(overrides)
    config = CapibaraConfig(**config_dict)
    model = CapibaraTextGenerator(config)

    # Move model to the specified device
    return model.to(torch.device(device))


@pytest.fixture
def capibara_test_model():
    """
    Pytest fixture that returns a CapibaraTextGenerator model instance for testing.

    Returns:
        CapibaraTextGenerator: A text generator model instance initialized with TEST_CONFIG settings.
    """
    return create_test_model()


def initialize_tests():
    """
    This function can be used for initializing any setup required for running all tests.
    This might include setting up random seeds, temporary directories, etc.
    """
    # Set a fixed random seed for reproducibility in tests
    torch.manual_seed(42)

    # Additional initialization steps can be added here as needed


if __name__ == '__main__':
    initialize_tests()
