# This file is intentionally empty to mark the directory as a Python package.
# It allows the test modules to be imported correctly.

# In the future, if you need to initialize something for all tests, you can do it here.

# Common imports for all tests
from capibara_model.config import CapibaraConfig
from capibara_model.model import CapibaraTextGenerator

# Common configuration for tests
TEST_CONFIG = CapibaraConfig(
    input_dim=64,
    byte_output_dim=128,
    state_dim=256,
    mamba_output_dim=512,
    hidden_dim=1024,
    output_dim=2048,
    vocab_size=1000,
    max_length=50,
    num_layers=4
)

# Utility functions for tests
def create_test_model():
    """
    Creates a CapibaraTextGenerator model using the test configuration.

    This function provides a utility to create a model with the predefined
    configuration that is commonly used in testing. By centralizing the model 
    creation, tests can ensure they are using a consistent configuration across
    different test cases.

    Returns:
        CapibaraTextGenerator: A text generator model instance initialized with 
        the TEST_CONFIG settings.
    """
    return CapibaraTextGenerator(TEST_CONFIG)
