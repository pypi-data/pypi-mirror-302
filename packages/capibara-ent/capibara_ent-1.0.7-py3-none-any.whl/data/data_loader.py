"""
Module for loading multilingual data for the CapibaraGPT model.

This module provides a class to create and manage DataLoaders
for training, validation, and test datasets in multiple languages.

Classes:
    MultilingualDataLoader: Manages the loading of multilingual data.

Dependencies:
    - torch: For DataLoader functionality.
    - .dataset: For the MultilingualDataset class.
"""

import logging
from pathlib import Path
from typing import Dict, Optional
import torch
from torch.utils.data import DataLoader
from .multilingual_dataset import MultilingualDataset
import os
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        load_dotenv()  # Carga las variables de .env
        self.train_data_path = os.path.join(
            os.getenv('CAPIBARA_DATA_PATH'), 'train')
        self.val_data_path = os.path.join(
            os.getenv('CAPIBARA_DATA_PATH'), 'val')
        self.test_data_path = os.path.join(
            os.getenv('CAPIBARA_DATA_PATH'), 'test')
        self.batch_size = int(os.getenv('CAPIBARA_BATCH_SIZE'))
        self.max_length = int(os.getenv('CAPIBARA_MAX_LENGTH'))
        # Ajusta según tus necesidades
        self.supported_languages = ['es', 'en', 'pt']
        self.num_workers = 4  # Ajusta según tus necesidades


class MultilingualDataLoader:
    """
    A class to handle loading and management of multilingual datasets.

    This class creates and manages DataLoaders for training, validation, and testing
    of multilingual data, with various optimizations and error checks.

    Attributes:
        config (object): Configuration object containing necessary parameters.
        train_dataset (MultilingualDataset): Dataset for training.
        val_dataset (MultilingualDataset): Dataset for validation.
        test_dataset (MultilingualDataset): Dataset for testing.
        device (torch.device): Device to load the data onto (CPU or GPU).
    """

    def __init__(self, config):
        """
        Initialize the MultilingualDataLoader.

        Args:
            config (object): Configuration object with required attributes.

        Raises:
            AttributeError: If required attributes are missing from config.
            ValueError: If num_workers is invalid or if datasets are empty.
            FileNotFoundError: If data paths do not exist.
        """
        self.config = config
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

        logger.info("Initializing MultilingualDataLoader...")

        self._validate_config()
        self._validate_data_paths()
        self._initialize_datasets()

    def _validate_config(self):
        """Validate the configuration object."""
        required_attributes = [
            'train_data_path', 'val_data_path', 'test_data_path',
            'supported_languages', 'batch_size', 'num_workers'
        ]
        for attr in required_attributes:
            if not hasattr(self.config, attr):
                raise AttributeError(f"Config object must contain '{
                                     attr}' attribute.")

        if not isinstance(self.config.num_workers, int) or self.config.num_workers < 0:
            raise ValueError(
                "Number of workers must be a non-negative integer.")

    def _validate_data_paths(self):
        """Validate the existence of data paths."""
        for path_attr in ['train_data_path', 'val_data_path', 'test_data_path']:
            path = getattr(self.config, path_attr)
            if not Path(path).exists():
                raise FileNotFoundError(f"Data path '{path}' does not exist.")

    def _initialize_datasets(self):
        """Initialize the datasets."""
        try:
            self.train_dataset = MultilingualDataset(
                self.config.train_data_path, self.config.supported_languages)
            self.val_dataset = MultilingualDataset(
                self.config.val_data_path, self.config.supported_languages)
            self.test_dataset = MultilingualDataset(
                self.config.test_data_path, self.config.supported_languages)
        except Exception as e:
            raise RuntimeError(f"Error initializing dataset: {e}")

        if len(self.train_dataset) == 0:
            raise ValueError("The training dataset is empty.")
        if len(self.val_dataset) == 0:
            raise ValueError("The validation dataset is empty.")
        if len(self.test_dataset) == 0:
            raise ValueError("The test dataset is empty.")

    def _create_loader(self, dataset: MultilingualDataset, batch_size: int, shuffle: bool) -> DataLoader:
        """
        Create a DataLoader with the given parameters.

        Args:
            dataset (MultilingualDataset): The dataset to load.
            batch_size (int): The batch size for the DataLoader.
            shuffle (bool): Whether to shuffle the data.

        Returns:
            DataLoader: The created DataLoader.
        """
        return DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            num_workers=self.config.num_workers,
            pin_memory=True,
            prefetch_factor=2
        )

    def get_train_loader(self, batch_size: Optional[int] = None) -> DataLoader:
        """
        Get the DataLoader for the training dataset.

        Args:
            batch_size (int, optional): Custom batch size for training. 
                                        If None, uses the config's batch_size.

        Returns:
            DataLoader: DataLoader for the training dataset.
        """
        batch_size = batch_size or self.config.batch_size
        logger.info(
            f"Creating training DataLoader with batch size {batch_size}")
        return self._create_loader(self.train_dataset, batch_size, shuffle=True)

    def get_val_loader(self, batch_size: Optional[int] = None, shuffle: bool = False) -> DataLoader:
        """
        Get the DataLoader for the validation dataset.

        Args:
            batch_size (int, optional): Custom batch size for validation. 
                                        If None, uses the config's batch_size.
            shuffle (bool): Whether to shuffle the validation data.

        Returns:
            DataLoader: DataLoader for the validation dataset.
        """
        batch_size = batch_size or self.config.batch_size
        logger.info(
            f"Creating validation DataLoader with batch size {batch_size}")
        return self._create_loader(self.val_dataset, batch_size, shuffle=shuffle)

    def get_test_loader(self, batch_size: Optional[int] = None, shuffle: bool = False) -> DataLoader:
        """
        Get the DataLoader for the test dataset.

        Args:
            batch_size (int, optional): Custom batch size for testing. 
                                        If None, uses the config's batch_size.
            shuffle (bool): Whether to shuffle the test data.

        Returns:
            DataLoader: DataLoader for the test dataset.
        """
        batch_size = batch_size or self.config.batch_size
        logger.info(f"Creating test DataLoader with batch size {batch_size}")
        return self._create_loader(self.test_dataset, batch_size, shuffle=shuffle)

    def get_dataset_sizes(self) -> Dict[str, int]:
        """
        Get the sizes of all datasets.

        Returns:
            Dict[str, int]: A dictionary containing the sizes of train, val, and test datasets.
        """
        return {
            "train": len(self.train_dataset),
            "val": len(self.val_dataset),
            "test": len(self.test_dataset)
        }


config = Config()
data_loader = MultilingualDataLoader(config)
