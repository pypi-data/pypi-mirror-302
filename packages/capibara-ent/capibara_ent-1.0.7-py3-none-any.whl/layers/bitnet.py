"""
Module that implements a BitNet layer for neural networks using JAX/Flax.

This module provides an implementation of the BitNet layer, which uses
grouped 1D convolutions and a GELU activation to process input arrays.

Classes:
    BitNetLayer: Implements a BitNet layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn
import logging

logger = logging.getLogger(__name__)


class BitNetLayer(nn.Module):
    """
    A BitNet layer implementation with 1D convolution and GELU activation.

    This layer applies a 1D convolution followed by GELU activation, with options
    for grouping, dropout, and layer normalization.

    Attributes:
        in_dim (int): Number of input channels.
        out_dim (int): Number of output channels.
        kernel_size (int): Size of the convolving kernel.
        groups (int): Number of groups for grouped convolution.
        dropout_rate (float): Dropout rate for regularization.
        use_layer_norm (bool): Whether to use layer normalization.
    """

    in_dim: int
    out_dim: int
    kernel_size: int = 3
    groups: int = None
    dropout_rate: float = 0.1
    use_layer_norm: bool = True

    @nn.compact
    def __call__(self, x: jnp.ndarray, training: bool = True) -> jnp.ndarray:
        """
        Forward pass of the BitNetLayer.

        Args:
            x (jnp.ndarray): Input array of shape (batch_size, sequence_length, in_dim).
            training (bool): Whether the model is in training mode.

        Returns:
            jnp.ndarray: Output array of shape (batch_size, sequence_length, out_dim).
        """
        self._validate_input(x)

        groups = self.groups or self.in_dim
        if self.in_dim % groups != 0 or self.out_dim % groups != 0:
            raise ValueError(f"Input dimension ({self.in_dim}) and output dimension ({self.out_dim}) "
                             f"must be divisible by the number of groups ({groups}).")

        # Transpose input for 1D convolution
        x = jnp.transpose(x, (0, 2, 1))

        padding = [(self.kernel_size - 1) // 2, (self.kernel_size - 1) // 2]
        x = nn.Conv(features=self.out_dim, kernel_size=(self.kernel_size,),
                    padding=padding, feature_group_count=groups, use_bias=False)(x)
        x = nn.gelu(x)
        x = nn.Dropout(rate=self.dropout_rate, deterministic=not training)(x)

        # Transpose back
        x = jnp.transpose(x, (0, 2, 1))

        if self.use_layer_norm:
            x = nn.LayerNorm()(x)

        return x

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim != 3:
            raise ValueError(f"Expected input array with 3 dimensions (batch_size, sequence_length, in_dim), "
                             f"but got {x.ndim} dimensions.")
        if x.shape[-1] != self.in_dim:
            raise ValueError(f"Expected number of input channels {
                             self.in_dim}, but got {x.shape[-1]}.")
        if x.shape[1] < self.kernel_size:
            raise ValueError(f"Sequence length must be at least {self.kernel_size} "
                             f"to apply kernel_size={self.kernel_size} convolution.")

    def get_config(self) -> dict:
        """
        Get the configuration of the BitNetLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "in_dim": self.in_dim,
            "out_dim": self.out_dim,
            "kernel_size": self.kernel_size,
            "groups": self.groups,
            "dropout_rate": self.dropout_rate,
            "use_layer_norm": self.use_layer_norm
        }


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a sample input array
    batch_size, in_dim, sequence_length = 32, 64, 128
    x = jax.random.normal(jax.random.PRNGKey(
        0), (batch_size, sequence_length, in_dim))

    # Initialize the BitNetLayer
    layer = BitNetLayer(in_dim=64, out_dim=128, kernel_size=3,
                        groups=16, dropout_rate=0.1, use_layer_norm=True)

    # Initialize parameters
    params = layer.init(jax.random.PRNGKey(1), x)

    # Perform forward pass
    output = layer.apply(params, x)

    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Layer config: {layer.get_config()}")
