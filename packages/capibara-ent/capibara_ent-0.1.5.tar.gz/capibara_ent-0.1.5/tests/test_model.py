"""
Test module for the CapibaraGPT model on TPU.

This module contains unit tests to verify the correct functionality
of the CapibaraGPT model in a TPU environment, including forward pass,
entropy calculation, gradient computation, and save/load operations.

Classes:
    TestCapibaraTPU: Test class for CapibaraGPT on TPU.

Dependencies:
    - unittest: For creating and running unit tests.
    - torch: For tensor operations.
    - torch_xla: For TPU integration.
    - capibara_model: For CapibaraGPT and Config classes.
"""

import unittest
import torch
import torch_xla
import torch_xla.core.xla_model as xm
import torch_xla.distributed.parallel_loader as pl
from capibara_model.config import CapibaraConfig
from capibara_model.model import CapibaraTextGenerator
from capibara_model.data import CapibaraDataset, CapibaraDataLoader
import os


class TestCapibaraTPU(unittest.TestCase):
    """
    Test class for the CapibaraGPT model on TPU.

    This class contains test methods to verify the correct functionality
    of the CapibaraGPT model in a TPU environment, including initialization,
    forward pass, entropy calculation, gradient computations, and save/load operations.
    """

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
        self.mock_data = self.generate_mock_data(
            num_samples=100, sequence_length=50)

    def tearDown(self):
        """
        Clean up the environment after tests.

        Deletes the model.
        """
        del self.model

    def generate_mock_data(self, num_samples, sequence_length):
        """
        Generates mock data for testing.

        Args:
            num_samples (int): Number of mock samples to generate.
            sequence_length (int): Length of each sequence.

        Returns:
            list: A list of dictionaries containing 'text' data for testing.
        """
        return [{'text': 'Sample text ' * sequence_length} for _ in range(num_samples)]

    def test_data_loader_creation(self):
        """
        Tests the creation of the CapibaraDataLoader with TPU support.
        """
        dataset = CapibaraDataset(self.mock_data, self.config)
        mp_device_loader = pl.MpDeviceLoader(
            CapibaraDataLoader(dataset, self.config), self.device)

        xm.rendezvous('init_sync')  # Synchronize before starting the test

        per_device_loader = mp_device_loader.per_device_loader(self.device)
        batches = [next(iter(per_device_loader))
                   for _ in range(3)]  # Only check the first 3 batches

        xm.mark_step()  # Ensure all operations are completed before assertions

        self.assertEqual(len(batches), 3)
        for batch in batches:
            self.assertEqual(
                batch.shape, (self.config.batch_size, self.config.max_length))

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
        self.assertTrue(torch.all(output >= 0) and torch.all(output <= 1))

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

    def test_entropy_calculation(self):
        """
        Tests the entropy calculation of the model on TPU.
        """
        input_data = torch.randint(0, self.config.vocab_size, (
            self.config.batch_size, self.config.max_length), device=self.device)
        entropy = self.model.calculate_entropy(input_data)
        xm.mark_step()  # Synchronize the step to ensure entropy calculation has finished

        self.assertIsInstance(entropy, float)
        # Verify that entropy is non-negative
        self.assertGreaterEqual(entropy, 0.0)


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
