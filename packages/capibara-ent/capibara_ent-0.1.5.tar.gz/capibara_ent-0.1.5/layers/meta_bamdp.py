"""
Module that implements a MetaBAMDP layer for neural networks using JAX/Flax.

This module provides an implementation of the MetaBAMDP (Meta Bayesian 
Adaptive Markov Decision Process) layer, which uses linear transformations, 
GELU activation, and layer normalization to process input arrays.

Classes:
    MetaBAMDPLayer: Implements a MetaBAMDP layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn
import logging

logger = logging.getLogger(__name__)


class MetaBAMDPLayer(nn.Module):
    """
    MetaBAMDPLayer: A flexible neural network layer with linear transformations,
    customizable activation, normalization, dropout, and optional residual connection.

    This layer implements two linear transformations with a customizable activation function,
    layer normalization, dropout for regularization, and an optional residual connection.

    Attributes:
        input_dim (int): Input dimension.
        hidden_dim (int): Hidden dimension for the intermediate representation.
        output_dim (int): Output dimension.
        dropout_rate (float): Dropout rate for regularization.
        use_residual (bool): Whether to use a residual connection.
        activation (str): Type of activation function to use.
    """
    input_dim: int
    hidden_dim: int
    output_dim: int
    dropout_rate: float = 0.1
    use_residual: bool = True
    activation: str = 'gelu'

    @nn.compact
    def __call__(self, x: jnp.ndarray, training: bool = True) -> jnp.ndarray:
        """
        Forward pass of the MetaBAMDPLayer.

        Args:
            x (jnp.ndarray): Input array of shape (batch_size, ..., input_dim).
            training (bool): Whether the model is in training mode.

        Returns:
            jnp.ndarray: Output array of shape (batch_size, ..., output_dim).
        """
        self._validate_input(x)
        logger.debug(f"Input shape: {x.shape}")

        # Flatten all dimensions except the batch size
        original_shape = x.shape
        x = jnp.reshape(x, (x.shape[0], -1))

        residual = x if self.use_residual else None

        hidden = nn.Dense(features=self.hidden_dim, use_bias=False)(x)
        activated = self._get_activation()(hidden)
        dropped = nn.Dropout(rate=self.dropout_rate,
                             deterministic=not training)(activated)
        output = nn.Dense(features=self.output_dim, use_bias=False)(dropped)

        if self.use_residual:
            if self.input_dim != self.output_dim:
                residual = nn.Dense(features=self.output_dim,
                                    use_bias=False)(residual)
            output = output + residual

        normalized_output = nn.LayerNorm()(output)

        # Reshape the output to match the input shape
        normalized_output = jnp.reshape(
            normalized_output, (*original_shape[:-1], self.output_dim))

        logger.debug(f"Output shape: {normalized_output.shape}")
        return normalized_output

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim < 2:
            raise ValueError(f"Expected input array with at least 2 dimensions (batch_size, ..., input_dim), "
                             f"but got {x.ndim} dimensions.")
        if x.shape[-1] != self.input_dim:
            raise ValueError(f"Expected last dimension to be {
                             self.input_dim}, but got {x.shape[-1]}.")

    def _get_activation(self):
        """Get the activation function."""
        if self.activation == 'relu':
            return nn.relu
        elif self.activation == 'gelu':
            return lambda x: nn.gelu(x, approximate=True)
        elif self.activation == 'tanh':
            return nn.tanh
        else:
            raise ValueError(f"Unsupported activation function: {
                             self.activation}")

    def get_config(self) -> dict:
        """
        Get the configuration of the MetaBAMDPLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "input_dim": self.input_dim,
            "hidden_dim": self.hidden_dim,
            "output_dim": self.output_dim,
            "dropout_rate": self.dropout_rate,
            "use_residual": self.use_residual,
            "activation": self.activation
        }


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a sample input array
    batch_size, seq_length, input_dim = 32, 10, 256
    x = jax.random.normal(jax.random.PRNGKey(
        0), (batch_size, seq_length, input_dim))

    # Initialize the MetaBAMDPLayer
    layer = MetaBAMDPLayer(input_dim=256, hidden_dim=512, output_dim=256,
                           dropout_rate=0.1, use_residual=True,
                           activation='gelu')

    # Initialize parameters
    params = layer.init(jax.random.PRNGKey(1), x)

    # Perform forward pass
    output = layer.apply(params, x)

    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Layer config: {layer.get_config()}")
