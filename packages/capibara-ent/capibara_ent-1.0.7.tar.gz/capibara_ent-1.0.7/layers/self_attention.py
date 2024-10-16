"""
Module that implements a Self-Attention layer for neural networks using JAX/Flax.

This module provides an implementation of the Self-Attention layer,
which uses multi-head attention and layer normalization to process
input arrays.

Classes:
    SelfAttentionLayer: Implements a Self-Attention layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn
import logging

logger = logging.getLogger(__name__)


class SelfAttentionLayer(nn.Module):
    """
    SelfAttentionLayer: A flexible self-attention layer with multi-head attention,
    layer normalization, dropout, and optional LayerDrop.

    This layer implements multi-head self-attention with pre-layer normalization,
    dropout for regularization, and optional LayerDrop for efficiency.

    Attributes:
        embed_dim (int): Embedding dimension.
        num_heads (int): Number of attention heads.
        dropout_rate (float): Dropout rate for regularization.
        layer_drop_prob (float): Probability of dropping the layer during training.
    """
    embed_dim: int
    num_heads: int
    dropout_rate: float = 0.1
    layer_drop_prob: float = 0.1

    @nn.compact
    def __call__(self, x: jnp.ndarray, attn_mask: jnp.ndarray = None, training: bool = True) -> jnp.ndarray:
        """
        Forward pass of the SelfAttentionLayer.

        Args:
            x (jnp.ndarray): Input array of shape (batch_size, seq_len, embed_dim).
            attn_mask (jnp.ndarray, optional): Attention mask of shape (seq_len, seq_len).
            training (bool): Whether the model is in training mode.

        Returns:
            jnp.ndarray: Output array of shape (batch_size, seq_len, embed_dim).
        """
        self._validate_input(x)
        logger.debug(f"Input shape: {x.shape}")

        # Apply LayerDrop
        if training and jax.random.uniform(jax.random.PRNGKey(0)) < self.layer_drop_prob:
            logger.debug("Applying LayerDrop: skipping this layer")
            return x

        # Apply pre-layer normalization
        normalized_x = nn.LayerNorm()(x)

        # Perform self-attention
        attn_output = nn.SelfAttention(
            num_heads=self.num_heads,
            dropout_rate=self.dropout_rate,
            deterministic=not training
        )(normalized_x, mask=attn_mask)
        logger.debug(f"Attention output shape: {attn_output.shape}")

        # Apply dropout to attention output
        attn_output = nn.Dropout(
            rate=self.dropout_rate, deterministic=not training)(attn_output)

        # Add residual connection
        x = x + attn_output

        # Apply final dropout
        x = nn.Dropout(rate=self.dropout_rate, deterministic=not training)(x)

        logger.debug(f"Output shape: {x.shape}")
        return x

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim != 3:
            raise ValueError(f"Expected input array with 3 dimensions (batch_size, seq_len, embed_dim), "
                             f"but got {x.ndim} dimensions.")
        if x.shape[-1] != self.embed_dim:
            raise ValueError(f"Expected embed_dim to be {
                             self.embed_dim}, but got {x.shape[-1]}.")

    def get_config(self) -> dict:
        """
        Get the configuration of the SelfAttentionLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "dropout_rate": self.dropout_rate,
            "layer_drop_prob": self.layer_drop_prob
        }


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a sample input array
    batch_size, seq_len, embed_dim = 32, 10, 256
    x = jax.random.normal(jax.random.PRNGKey(
        0), (batch_size, seq_len, embed_dim))

    # Initialize the SelfAttentionLayer
    layer = SelfAttentionLayer(
        embed_dim=256, num_heads=8, dropout_rate=0.1, layer_drop_prob=0.1)

    # Create a sample attention mask
    attn_mask = jnp.triu(jnp.ones((seq_len, seq_len)), k=1).astype(bool)

    # Initialize parameters
    params = layer.init(jax.random.PRNGKey(1), x, attn_mask)

    # Perform forward pass
    output = layer.apply(params, x, attn_mask)

    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Layer config: {layer.get_config()}")
