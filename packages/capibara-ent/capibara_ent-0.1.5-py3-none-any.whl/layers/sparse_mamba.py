"""
Module that implements a SparseMamba layer for neural networks using JAX/Flax.

This module provides an implementation of the SparseMamba layer, 
which uses linear transformations and GELU activation to process 
input arrays in a sparse and efficient manner.

Classes:
    SparseMambaLayer: Implements a SparseMamba layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
    - jax.experimental.sparse: For sparse array operations.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn
from jax.experimental import sparse
import logging

logger = logging.getLogger(__name__)


class SparseMambaLayer(nn.Module):
    """
    SparseMambaLayer: An optimized neural network layer for sparse operations,
    designed for efficient execution on TPUs.

    This layer implements two linear transformations with GELU activation,
    dropout for regularization, and optional residual connection. It's optimized
    for sparse array operations and TPU compatibility.

    Attributes:
        input_dim (int): Input dimension.
        output_dim (int): Output dimension.
        dropout_rate (float): Dropout rate for regularization.
        use_residual (bool): Whether to use a residual connection.
    """
    input_dim: int
    output_dim: int
    dropout_rate: float = 0.1
    use_residual: bool = True

    @nn.compact
    def __call__(self, x: jnp.ndarray, training: bool = True) -> jnp.ndarray:
        """
        Forward pass of the SparseMambaLayer.

        Args:
            x (jnp.ndarray): Input array of shape (batch_size, input_dim).
                Can be either dense or sparse (BCOO format).
            training (bool): Whether the model is in training mode.

        Returns:
            jnp.ndarray: Output array of shape (batch_size, input_dim).
        """
        self._validate_input(x)
        logger.debug(f"Input shape: {x.shape}, Is sparse: {
                     sparse.BCOO.is_sparse(x)}")

        if sparse.BCOO.is_sparse(x):
            x = self._sparse_forward(x, training)
        else:
            x = self._dense_forward(x, training)

        logger.debug(f"Output shape: {x.shape}")
        return x

    def _sparse_forward(self, x: sparse.BCOO, training: bool) -> jnp.ndarray:
        """Forward pass for sparse arrays."""
        residual = x if self.use_residual else None

        x = sparse.bcoo_dot_general(x, self.param(
            'linear1', nn.initializers.xavier_uniform(), (self.input_dim, self.output_dim)).T)
        x = nn.gelu(x.todense(), approximate=True)
        x = nn.Dropout(rate=self.dropout_rate, deterministic=not training)(x)
        x = nn.Dense(features=self.input_dim, use_bias=False)(x)

        if self.use_residual:
            x = x + residual.todense()

        return x

    def _dense_forward(self, x: jnp.ndarray, training: bool) -> jnp.ndarray:
        """Forward pass for dense arrays."""
        residual = x if self.use_residual else None

        x = nn.Dense(features=self.output_dim, use_bias=False)(x)
        x = nn.gelu(x, approximate=True)
        x = nn.Dropout(rate=self.dropout_rate, deterministic=not training)(x)
        x = nn.Dense(features=self.input_dim, use_bias=False)(x)

        if self.use_residual:
            x = x + residual

        return x

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim != 2:
            raise ValueError(f"Expected input array with 2 dimensions (batch_size, input_dim), "
                             f"but got {x.ndim} dimensions.")
        if x.shape[-1] != self.input_dim:
            raise ValueError(f"Expected input_dim to be {
                             self.input_dim}, but got {x.shape[-1]}.")

    def get_config(self) -> dict:
        """
        Get the configuration of the SparseMambaLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "input_dim": self.input_dim,
            "output_dim": self.output_dim,
            "dropout_rate": self.dropout_rate,
            "use_residual": self.use_residual
        }


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a sample input array (dense)
    batch_size, input_dim = 32, 256
    x_dense = jax.random.normal(jax.random.PRNGKey(0), (batch_size, input_dim))

    # Create a sample input array (sparse)
    indices = jnp.array(jnp.nonzero(jax.random.uniform(
        jax.random.PRNGKey(1), (batch_size, input_dim)) > 0.9)).T
    values = jax.random.uniform(jax.random.PRNGKey(2), (indices.shape[0],))
    x_sparse = sparse.BCOO((values, indices), shape=(batch_size, input_dim))

    # Initialize the SparseMambaLayer
    layer = SparseMambaLayer(
        input_dim=256, output_dim=512, dropout_rate=0.1, use_residual=True)

    # Initialize parameters
    params = layer.init(jax.random.PRNGKey(3), x_dense)

    # Perform forward pass with dense input
    output_dense = layer.apply(params, x_dense)

    # Perform forward pass with sparse input
    output_sparse = layer.apply(params, x_sparse)

    print(f"Dense input shape: {x_dense.shape}")
    print(f"Dense output shape: {output_dense.shape}")
    print(f"Sparse input shape: {x_sparse.shape}")
    print(f"Sparse output shape: {output_sparse.shape}")
    print(f"Layer config: {layer.get_config()}")
