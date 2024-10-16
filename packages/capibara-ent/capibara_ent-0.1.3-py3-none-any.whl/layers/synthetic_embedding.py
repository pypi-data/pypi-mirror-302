"""
Module that implements a Synthetic Embedding layer for neural networks using JAX/Flax.

This module provides an implementation of the Synthetic Embedding layer,
which uses a linear transformation and GELU activation to process input
arrays, creating synthetic representations.

Classes:
    SyntheticEmbeddingLayer: Implements a Synthetic Embedding layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn
import logging

logger = logging.getLogger(__name__)


class SyntheticEmbeddingLayer(nn.Module):
    """
    SyntheticEmbeddingLayer: An optimized neural network layer for synthetic embeddings,
    designed for efficient execution on TPUs.

    This layer implements a linear transformation followed by GELU activation,
    layer normalization, and optional residual connection. It's optimized
    for TPU compatibility and includes various performance enhancements.

    Attributes:
        dim (int): Input and output dimension.
        dropout_rate (float): Dropout rate for regularization.
        use_residual (bool): Whether to use a residual connection.
    """
    dim: int
    dropout_rate: float = 0.1
    use_residual: bool = True

    @nn.compact
    def __call__(self, x: jnp.ndarray, mask: jnp.ndarray = None, training: bool = True) -> jnp.ndarray:
        """
        Forward pass of the SyntheticEmbeddingLayer.

        Args:
            x (jnp.ndarray): Input array of shape (batch_size, seq_len, dim).
            mask (jnp.ndarray, optional): Mask array of shape (batch_size, seq_len).
            training (bool): Whether the model is in training mode.

        Returns:
            jnp.ndarray: Output array of shape (batch_size, seq_len, dim).
        """
        self._validate_input(x)
        logger.debug(f"Input shape: {x.shape}, dtype: {x.dtype}")

        # Handle sparse arrays (if needed)
        # Note: JAX doesn't have built-in sparse array support like PyTorch
        # You might need to implement custom sparse operations if required

        # Apply mask if provided
        if mask is not None:
            x = x * mask[:, :, jnp.newaxis]

        residual = x if self.use_residual else None

        x = nn.Dense(features=self.dim, use_bias=False)(x)
        logger.debug(f"Shape after linear transformation: {x.shape}")

        x = nn.gelu(x, approximate=True)
        logger.debug(f"Shape after GELU activation: {x.shape}")

        x = nn.LayerNorm()(x)
        logger.debug(f"Shape after layer normalization: {x.shape}")

        x = nn.Dropout(rate=self.dropout_rate, deterministic=not training)(x)

        if self.use_residual:
            x = x + residual

        logger.debug(f"Output shape: {x.shape}")
        return x

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim != 3:
            raise ValueError(f"Expected input array with 3 dimensions (batch_size, seq_len, dim), "
                             f"but got {x.ndim} dimensions.")
        if x.shape[-1] != self.dim:
            raise ValueError(f"Expected dim to be {
                             self.dim}, but got {x.shape[-1]}.")

    def get_config(self) -> dict:
        """
        Get the configuration of the SyntheticEmbeddingLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "dim": self.dim,
            "dropout_rate": self.dropout_rate,
            "use_residual": self.use_residual
        }


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a sample input array
    batch_size, seq_len, dim = 32, 10, 256
    x = jax.random.normal(jax.random.PRNGKey(0), (batch_size, seq_len, dim))

    # Create a sample mask
    mask = jnp.ones((batch_size, seq_len))
    mask = mask.at[:, 5:].set(0)  # Mask out the last 5 tokens

    # Initialize the SyntheticEmbeddingLayer
    layer = SyntheticEmbeddingLayer(
        dim=256, dropout_rate=0.1, use_residual=True)

    # Initialize parameters
    params = layer.init(jax.random.PRNGKey(1), x, mask)

    # Perform forward pass
    output = layer.apply(params, x, mask)

    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Layer config: {layer.get_config()}")
