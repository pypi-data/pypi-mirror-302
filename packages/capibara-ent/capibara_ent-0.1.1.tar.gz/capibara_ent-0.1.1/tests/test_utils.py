"""
Test module for CapibaraGPT utilities.

This module contains unit tests for utility functions of the CapibaraGPT model,
including activations, data processing, and language utilities. The tests are
executed in a TPU environment.

Classes:
    TestActivations: Tests for activation functions.
    TestDataProcessing: Tests for data processing functions.
    TestLanguageUtils: Tests for language utility functions.

Dependencies:
    - unittest: For creating and running unit tests.
    - torch: For tensor operations.
    - torch_xla: For TPU integration.
    - capibara_model.utils: Modules containing the functions to be tested.
"""

import unittest
import torch
import os
import torch_xla
import torch_xla.core.xla_model as xm
import torch_xla.distributed.parallel_loader as pl
from unittest.mock import patch
from capibara_model.config import CapibaraConfig
from capibara_model.model import CapibaraTextGenerator
from capibara_model.data import CapibaraDataset, CapibaraDataLoader
from capibara_model.utils.activations import gelu, swish
from capibara_model.utils.positional_encoding import PositionalEncoding
from capibara_model.utils.mask import create_masks
from capibara_model.utils.language_utils import detect_language, translate_text


class TestCapibaraTPU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment for all test methods in the class.
        This method is called once before any test method is run.
        """
        torch.manual_seed(42)
        try:
            cls.device = xm.xla_device()
            xm.set_rng_state(42, device=cls.device)
        except RuntimeError:
            cls.device = None

    def setUp(self):
        """
        Sets up the test environment for each test method.

        Initializes the TPU device and creates a test configuration
        for data loading.
        """
        if self.device is None:
            self.skipTest(
                "TPU device not available. Skipping TPU-based tests.")

        # Simplified configuration for tests
        self.config = CapibaraConfig(
            batch_size=32,
            max_length=50,
            device=str(self.device),
            input_dim=16,
            byte_output_dim=32,
            state_dim=64,
            mamba_output_dim=128,
            hidden_dim=256,
            output_dim=512,
            vocab_size=1000,
            num_layers=2
        )
        self.model = CapibaraTextGenerator(self.config).to(self.device)

    def tearDown(self):
        """
        Clean up the environment after tests.

        Deletes the model.
        """
        del self.model

    def test_model_creation(self):
        """
        Tests the creation of the CapibaraTextGenerator model on TPU.
        """
        xm.mark_step()  # Ensure model is moved to TPU before assertions

        self.assertIsInstance(self.model, CapibaraTextGenerator)
        self.assertEqual(
            str(next(self.model.parameters()).device), str(self.device))

    def test_forward_pass(self):
        """
        Tests a forward pass through the model on TPU.
        """
        input_data = torch.randint(0, self.config.vocab_size, (
            self.config.batch_size, self.config.max_length), device=self.device)

        output = self.model(input_data)
        xm.mark_step()  # Ensure forward pass is completed before assertions

        self.assertEqual(output.shape, (self.config.batch_size,
                         self.config.max_length, self.config.vocab_size))

    def test_gradient_computation(self):
        """
        Tests gradient computation on TPU.

        This test ensures that the gradients are being computed correctly
        for a simple forward and backward pass using the model and TPU.
        """
        data = torch.randint(0, self.config.vocab_size, (self.config.batch_size,
                             self.config.max_length), device=self.device)
        labels = torch.randint(0, self.config.vocab_size,
                               (self.config.batch_size,), device=self.device)

        optimizer = torch.optim.SGD(self.model.parameters(), lr=0.01)
        criterion = torch.nn.CrossEntropyLoss()

        optimizer.zero_grad()
        output = self.model(data)
        loss = criterion(
            output.view(-1, self.config.vocab_size), labels.view(-1))
        loss.backward()

        xm.mark_step()  # Synchronize before verifying gradients

        for name, param in self.model.named_parameters():
            self.assertIsNotNone(param.grad, f"Gradient for {name} is None")
            self.assertFalse(torch.isnan(param.grad).any(),
                             f"NaN gradient for {name}")
            self.assertGreater(torch.abs(param.grad).sum(
            ).item(), 0.0, f"Zero gradient for {name}")

    def test_save_load_model(self):
        """
        Tests saving and loading the model on TPU.
        """
        input_data = torch.randint(0, self.config.vocab_size, (
            self.config.batch_size, self.config.max_length), device=self.device)
        original_output = self.model(input_data)
        xm.mark_step()  # Synchronize the step

        try:
            # Save the state on CPU to avoid device issues
            cpu_state_dict = {k: v.to('cpu')
                              for k, v in self.model.state_dict().items()}
            torch.save(cpu_state_dict, 'temp_model.pth')

            loaded_model = CapibaraTextGenerator(self.config).to(self.device)
            loaded_model.load_state_dict(torch.load(
                'temp_model.pth', map_location='cpu'))
            loaded_output = loaded_model(input_data)
            xm.mark_step()  # Synchronize the step after loading and running the model

            self.assertTrue(torch.allclose(
                original_output, loaded_output, atol=1e-5))
        finally:
            if os.path.exists('temp_model.pth'):
                os.remove('temp_model.pth')

    def test_gelu(self):
        """
        Tests the GELU activation function.
        """
        x = torch.randn(10).to(self.device)
        output = gelu(x)
        xm.mark_step()

        self.assertEqual(output.shape, x.shape)

    def test_gelu_specific_values(self):
        """
        Tests GELU activation with specific input values.
        """
        x = torch.tensor([0.0, 1.0, -1.0, 2.0, -2.0]).to(self.device)
        output = gelu(x)
        xm.mark_step()

        expected_output = torch.tensor(
            [0.0000, 0.8413, -0.1587, 1.9545, -0.0455]).to(self.device)
        self.assertTrue(torch.allclose(output, expected_output, atol=1e-4))

    def test_swish(self):
        """
        Tests the Swish activation function.
        """
        x = torch.randn(10).to(self.device)
        output = swish(x)
        xm.mark_step()

        self.assertEqual(output.shape, x.shape)

    def test_swish_specific_values(self):
        """
        Tests Swish activation with specific input values.
        """
        x = torch.tensor([0.0, 1.0, -1.0, 2.0, -2.0]).to(self.device)
        output = swish(x)
        xm.mark_step()

        expected_output = torch.tensor(
            [0.0000, 0.7311, -0.2689, 1.7616, -0.2384]).to(self.device)
        self.assertTrue(torch.allclose(output, expected_output, atol=1e-4))

    def test_positional_encoding_shape(self):
        """
        Tests the shape of the positional encoding.
        """
        max_len, d_model = 100, 512
        pe = PositionalEncoding(d_model, max_len=max_len)
        encoding = pe(torch.zeros(1, max_len, d_model).to(self.device))
        xm.mark_step()

        self.assertEqual(encoding.shape, (1, max_len, d_model))

    def test_positional_encoding_values(self):
        """
        Tests the values of the positional encoding.
        """
        max_len, d_model = 100, 512
        pe = PositionalEncoding(d_model, max_len=max_len)
        encoding = pe(torch.zeros(1, max_len, d_model).to(self.device))
        xm.mark_step()

        self.assertTrue(torch.all(encoding >= -1) and torch.all(encoding <= 1))

    def test_create_masks_shape(self):
        """
        Tests the shape of created masks.
        """
        seq_len, batch_size = 10, 2
        src_mask, tgt_mask = create_masks(
            seq_len, batch_size, device=self.device)
        xm.mark_step()

        self.assertEqual(src_mask.shape, (batch_size, 1, seq_len))
        self.assertEqual(tgt_mask.shape, (batch_size, seq_len, seq_len))

    def test_create_masks_device(self):
        """
        Tests the device of created masks.
        """
        seq_len, batch_size = 10, 2
        src_mask, tgt_mask = create_masks(
            seq_len, batch_size, device=self.device)
        xm.mark_step()

        self.assertEqual(src_mask.device, self.device)
        self.assertEqual(tgt_mask.device, self.device)

    def test_create_masks_values(self):
        """
        Tests the values of created masks.
        """
        seq_len, batch_size = 10, 2
        src_mask, tgt_mask = create_masks(
            seq_len, batch_size, device=self.device)
        xm.mark_step()

        self.assertTrue(torch.all(src_mask == 1))
        self.assertTrue(torch.tril(torch.ones(seq_len, seq_len)
                                   ).to(self.device).equal(tgt_mask[0]))

    @patch('capibara_model.utils.language_utils.detect_language', return_value='en')
    def test_detect_language(self, mock_detect):
        """
        Tests the language detection function.
        """
        text = "Hello, how are you?"
        lang = detect_language(text)
        self.assertEqual(lang, "en")

    @patch('capibara_model.utils.language_utils.translate_text', return_value='Hola, ¿cómo estás?')
    def test_translate_text(self, mock_translate):
        """
        Tests the text translation function.
        """
        text = "Hello, how are you?"
        translated = translate_text(text, source_lang="en", target_lang="es")
        self.assertIsInstance(translated, str)
        self.assertNotEqual(text, translated)


def _mp_fn(index, flags):
    """
    Main function for multi-processing.
    This function will be called by each TPU process.
    """
    device = xm.xla_device()
    xm.set_rng_state(42)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCapibaraTPU)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


if __name__ == '__main__':
    # Use all available TPU cores (usually 8 for a TPU v3-8)
    xm.spawn(_mp_fn, args=(), nprocs=8, start_method='fork')
