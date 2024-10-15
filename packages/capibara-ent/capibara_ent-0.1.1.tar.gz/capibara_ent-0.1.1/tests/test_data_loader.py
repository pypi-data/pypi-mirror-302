"""
Test module for the CapibaraGPT data loader.

This module contains unit tests for the CapibaraDataset and data loading functions,
including specific tests for use with TPUs.

Classes:
    TestDataLoader: Test class for the data loader.

Dependencies:
    - unittest: For creating and running unit tests.
    - torch: For tensor operations.
    - torch_xla: For TPU integration.
    - capibara_model: For the classes and functions being tested.
"""

import unittest
import torch
import torch_xla.core.xla_model as xm
import torch_xla.distributed.parallel_loader as pl
from capibara_model.config import CapibaraConfig
from capibara_model.model import CapibaraTextGenerator
from capibara_model.data import CapibaraDataset, CapibaraDataLoader


class TestCapibaraTPU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up the test environment for all test methods in the class.
        This method is called once before any test method is run.
        """
        # Set a fixed random seed for reproducibility
        torch.manual_seed(42)
        xm.set_rng_state(42)

    def setUp(self):
        """
        Sets up the test environment for each test method.

        Initializes the TPU device and creates a test configuration
        for data loading.
        """
        self.device = xm.xla_device()
        xm.set_rng_state(42, device=self.device)
        self.config = CapibaraConfig(
            batch_size=32,
            max_length=100,
            device=str(self.device),
            input_dim=64,
            byte_output_dim=128,
            state_dim=256,
            mamba_output_dim=512,
            hidden_dim=1024,
            output_dim=2048,
            vocab_size=1000,
            num_layers=4
        )
        self.mock_data = self.generate_mock_data(
            num_samples=100, sequence_length=50)

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
        model = CapibaraTextGenerator(self.config).to(self.device)

        xm.mark_step()  # Ensure model is moved to TPU before assertions

        self.assertIsInstance(model, CapibaraTextGenerator)
        self.assertEqual(str(next(model.parameters()).device),
                         str(self.device))

    def test_forward_pass(self):
        """
        Tests a forward pass through the model on TPU.
        """
        model = CapibaraTextGenerator(self.config).to(self.device)
        input_data = torch.randint(0, self.config.vocab_size, (
            self.config.batch_size, self.config.max_length), device=self.device)

        output = model(input_data)

        xm.mark_step()  # Ensure forward pass is completed before assertions

        self.assertEqual(output.shape, (self.config.batch_size,
                         self.config.max_length, self.config.vocab_size))

    def test_gradient_computation(self):
        """
        Tests gradient computation on TPU.

        This test ensures that the gradients are being computed correctly
        for a simple forward and backward pass using the model and TPU.
        """
        model = CapibaraTextGenerator(self.config).to(self.device)

        data = torch.randint(0, self.config.vocab_size, (self.config.batch_size,
                             self.config.max_length), device=self.device)
        labels = torch.randint(0, self.config.vocab_size,
                               (self.config.batch_size,), device=self.device)

        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
        criterion = torch.nn.CrossEntropyLoss()

        optimizer.zero_grad()
        output = model(data)
        loss = criterion(
            output.view(-1, self.config.vocab_size), labels.view(-1))
        loss.backward()

        xm.mark_step()  # Synchronize before verifying gradients

        for name, param in model.named_parameters():
            self.assertIsNotNone(param.grad, f"Gradient for {name} is None")
            self.assertFalse(torch.isnan(param.grad).any(),
                             f"NaN gradient for {name}")


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
