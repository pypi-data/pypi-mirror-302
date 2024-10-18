from capibara_model.data import CapibaraDataset, CapibaraDataLoader
from capibara_model.config import CapibaraConfig
import unittest
import torch
import torch_xla
import torch_xla.core.xla_model as xm
import torch_xla.distributed.parallel_loader as pl
import os
import sys

# Añadir el directorio raíz del proyecto al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_mock_data(num_samples, sequence_length, vocab_size):
    """Genera datos simulados para las pruebas."""
    return [{'text': ' '.join([str(torch.randint(0, vocab_size, (1,)).item()) for _ in range(sequence_length)])}
            for _ in range(num_samples)]


def create_test_config():
    """Crea una configuración de prueba para TPU."""
    return CapibaraConfig(
        batch_size=32,
        max_length=50,
        device='xla',
        input_dim=16,
        byte_output_dim=32,
        state_dim=64,
        mamba_output_dim=128,
        hidden_dim=256,
        output_dim=512,
        vocab_size=1000,
        num_layers=2
    )


def load_tests(loader, standard_tests, pattern):
    """Carga todos los tests de los archivos en la carpeta tests."""
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern="test_*.py")
    standard_tests.addTests(package_tests)
    return standard_tests


class TPUTestRunner:
    @staticmethod
    def run(index):
        device = xm.xla_device()
        xm.set_rng_state(42)

        # Configurar el entorno de prueba
        config = create_test_config()
        mock_data = generate_mock_data(
            num_samples=100, sequence_length=50, vocab_size=config.vocab_size)

        # Crear un dataset y dataloader de prueba
        dataset = CapibaraDataset(mock_data, config)
        dataloader = pl.MpDeviceLoader(
            CapibaraDataLoader(dataset, config), device)

        # Ejecutar las pruebas
        test_loader = unittest.TestLoader()
        all_tests = load_tests(test_loader, unittest.TestSuite(), "test_*.py")

        for test in all_tests:
            if hasattr(test, 'device'):
                test.device = device
            if hasattr(test, 'config'):
                test.config = config
            if hasattr(test, 'mock_data'):
                test.mock_data = mock_data
            if hasattr(test, 'dataloader'):
                test.dataloader = dataloader

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(all_tests)


if __name__ == "__main__":
    # Usar todos los núcleos TPU disponibles (generalmente 8 para TPU v3-8)
    xm.spawn(TPUTestRunner.run, args=(), nprocs=8, start_method='fork')
