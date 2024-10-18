"""
Module that implements a MambaByte layer for neural networks using JAX/Flax.

This module provides an implementation of the MambaByte layer, which uses
a 1D convolution and GELU activation to process input arrays,
with dimension transposition before and after the processing.

Classes:
    MambaByteLayer: Implements a MambaByte layer.

Dependencies:
    - jax: For array operations and automatic differentiation.
    - flax: For neural network module definitions.
"""

import jax
import jax.numpy as jnp
from flax import linen as nn
import logging

logger = logging.getLogger(__name__)


class MambaByteLayer(nn.Module):
    """
    Implements a MambaByte layer.

    This class provides a layer that applies a 1D convolution followed by
    a GELU activation to input arrays, with dimension transpositions
    before and after processing.

    Attributes:
        input_dim (int): Input dimension of the layer.
        output_dim (int): Output dimension of the layer.
        kernel_size (int): Size of the convolving kernel.
        dropout_rate (float): Dropout rate for regularization.
        use_bias (bool): Whether to use bias in the convolution.
    """
    input_dim: int
    output_dim: int
    kernel_size: int = 3
    dropout_rate: float = 0.1
    use_bias: bool = False

    @nn.compact
    def __call__(self, x: jnp.ndarray, training: bool = True) -> jnp.ndarray:
        """
        Performs the MambaByte layer operation on the input array.

        This method applies a dimension transposition, followed by a 1D convolution 
        and a GELU activation, and finally another dimension transposition to the input array.

        Args:
            x (jnp.ndarray): The input array with shape (batch, sequence_length, input_dim).
            training (bool): Whether the model is in training mode.

        Returns:
            jnp.ndarray: The output array with shape (batch, sequence_length, output_dim).
        """
        self._validate_input(x)
        logger.debug(f"Input shape: {x.shape}")

        # Transpose the input array to move the feature dimension to the middle: (batch, input_dim, sequence_length)
        x = jnp.transpose(x, (0, 2, 1))

        # Apply 1D convolution across the sequence dimension
        x = nn.Conv(features=self.output_dim, kernel_size=(self.kernel_size,),
                    padding='SAME', use_bias=self.use_bias)(x)

        # Apply GELU activation to introduce non-linearity
        x = nn.gelu(x, approximate=True)

        # Apply dropout for regularization
        x = nn.Dropout(rate=self.dropout_rate, deterministic=not training)(x)

        # Transpose back to the original shape: (batch, sequence_length, output_dim)
        x = jnp.transpose(x, (0, 2, 1))

        # Apply layer normalization
        x = nn.LayerNorm()(x)

        logger.debug(f"Output shape: {x.shape}")
        return x

    def _validate_input(self, x: jnp.ndarray):
        """Validate the input array dimensions."""
        if x.ndim != 3:
            raise ValueError(f"Expected input array with 3 dimensions (batch, sequence_length, input_dim), "
                             f"but got {x.ndim} dimensions.")
        if x.shape[-1] != self.input_dim:
            raise ValueError(f"Expected input_dim to be {
                             self.input_dim}, but got {x.shape[-1]}.")
        if x.shape[1] < self.kernel_size:
            raise ValueError(f"Sequence length must be at least {self.kernel_size} "
                             f"to apply a kernel_size={self.kernel_size} convolution.")

    def get_config(self) -> dict:
        """
        Get the configuration of the MambaByteLayer.

        Returns:
            dict: A dictionary containing the layer's configuration.
        """
        return {
            "input_dim": self.input_dim,
            "output_dim": self.output_dim,
            "kernel_size": self.kernel_size,
            "dropout_rate": self.dropout_rate,
            "use_bias": self.use_bias
        }


# Example usage
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Create a sample input array
    batch_size, sequence_length, input_dim = 32, 128, 256
    x = jax.random.normal(jax.random.PRNGKey(
        0), (batch_size, sequence_length, input_dim))

    # Initialize the MambaByteLayer
    layer = MambaByteLayer(input_dim=256, output_dim=512, kernel_size=3,
                           dropout_rate=0.1, use_bias=False)

    # Initialize parameters
    params = layer.init(jax.random.PRNGKey(1), x)

    # Perform forward pass
    output = layer.apply(params, x)

    print(f"Input shape: {x.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Layer config: {layer.get_config()}")
