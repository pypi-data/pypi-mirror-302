"""
Data package for CapibaraGPT.

This package provides utilities for handling multilingual datasets,
including data loading, preprocessing, and augmentation.
"""

from .dataset import MultilingualDataset, DataLoader
from .preprocessing import preprocess_text
from .augmentation import augment_data

__all__ = ['MultilingualDataset', 'DataLoader',
           'preprocess_text', 'augment_data']

__version__ = '0.1.0'
