"""
Module for handling multilingual datasets for the CapibaraGPT model.

This module provides a class for creating and managing multilingual
datasets, including language detection and translation of
unsupported texts.

Classes:
    MultilingualDataset: Manages a multilingual dataset.

Dependencies:
    - torch: For Dataset functionality and tensors.
    - transformers: For the AutoTokenizer tokenizer.
    - capibara_model.utils: For language detection and translation functions.
"""

import logging
from typing import List, Dict, Any, Optional
from torch.utils.data import Dataset
from transformers import AutoTokenizer
import torch
from functools import lru_cache
import os
import json
from langdetect import detect
from googletrans import Translator
import os
from dotenv import load_dotenv
import pickle

logger = logging.getLogger(__name__)


class MultilingualDataset(Dataset):
    """
    A dataset class for handling multilingual text data.

    This class processes and prepares multilingual text data for use in language models,
    including language detection, translation, and tokenization.

    Attributes:
        data (List[Dict[str, Any]]): List of data items, each containing at least a 'text' field.
        supported_languages (List[str]): List of supported language codes.
        tokenizer: Tokenizer for encoding the text.
        max_length (int): Maximum length for tokenization.
        translation_cache (Dict[int, tuple]): Cache for storing translated texts.
    """

    @classmethod
    def from_directory(cls, directory: str, supported_languages: List[str], **kwargs):
        data = []
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                    data.extend(json.load(f))
        return cls(data, supported_languages, **kwargs)

    def __init__(self, data: List[Dict[str, Any]], supported_languages: List[str],
                 tokenizer: Optional[Any] = None, max_length: Optional[int] = None):
        """
        Initialize the MultilingualDataset.

        Args:
            data (List[Dict[str, Any]]): List of data items.
            supported_languages (List[str]): List of supported language codes.
            tokenizer (Optional[Any]): Pre-initialized tokenizer. If None, a default one will be used.
            max_length (Optional[int]): Maximum length for tokenization. If None, it will be set to 512.

        Raises:
            ValueError: If data is empty or not in the correct format.
            KeyError: If any data item is missing the 'text' field.
        """
        load_dotenv()
        self.max_length = max_length or int(
            os.getenv('CAPIBARA_MAX_LENGTH', 512))
        self._validate_input(data)
        self.data = data
        self.supported_languages = supported_languages
        self.tokenizer = tokenizer or AutoTokenizer.from_pretrained(
            "xlm-roberta-base")
        self.translation_cache = {}

        logger.info(f"Creating MultilingualDataset with {len(data)} items.")

    def _validate_input(self, data: List[Dict[str, Any]]):
        """Validate the input data."""
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError("Data must be a non-empty list of dictionaries.")
        if not all(isinstance(item, dict) for item in data):
            raise ValueError("All items in data must be dictionaries.")
        if not all('text' in item for item in data):
            raise KeyError("Each item in data must contain a 'text' key.")

    def __len__(self) -> int:
        """Return the number of items in the dataset."""
        return len(self.data)

    @lru_cache(maxsize=1000)
    def _detect_and_translate(self, idx: int) -> tuple:
        """Detect language and translate if necessary, with caching."""
        item = self.data[idx]
        text = item['text']
        lang = self._detect_language(text)

        if lang not in self.supported_languages:
            try:
                text = self._translate_text(text, self.supported_languages[0])
                lang = self.supported_languages[0]
                logger.info(f"Translated item {idx} from {
                            lang} to {self.supported_languages[0]}")
            except Exception as e:
                logger.error(f"Error translating text at index {idx}: {e}")
                # Fallback to original text and first supported language
                lang = self.supported_languages[0]

        return text, lang

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        """
        Get a single item from the dataset.

        Args:
            idx (int): Index of the item to retrieve.

        Returns:
            Dict[str, Any]: A dictionary containing 'input_ids', 'attention_mask', and 'lang'.

        Raises:
            IndexError: If the index is out of bounds.
        """
        if idx < 0 or idx >= len(self.data):
            raise IndexError(f"Index {idx} is out of bounds for dataset of length {
                             len(self.data)}.")

        text, lang = self._detect_and_translate(idx)

        if not text.strip():
            logger.warning(f"Empty text found at index {idx}")
            text = "[PAD]"  # or some other special token

        try:
            encoding = self.tokenizer(
                text,
                max_length=self.max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
        except Exception as e:
            logger.error(f"Error tokenizing text at index {idx}: {e}")
            # Return a dummy tensor in case of tokenization error
            return {
                'input_ids': torch.zeros(self.max_length, dtype=torch.long),
                'attention_mask': torch.zeros(self.max_length, dtype=torch.long),
                'lang': self.supported_languages.index(lang)
            }

        return {
            'input_ids': encoding['input_ids'].squeeze(dim=0),
            'attention_mask': encoding['attention_mask'].squeeze(dim=0),
            'lang': self.supported_languages.index(lang)
        }

    @staticmethod
    def _detect_language(text: str) -> str:
        """Detect the language of the given text."""
        try:
            return detect(text)
        except:
            return "en"  # default to English if detection fails

    @staticmethod
    def _translate_text(text: str, target_lang: str) -> str:
        """Translate the given text to the target language."""
        translator = Translator()
        try:
            return translator.translate(text, dest=target_lang).text
        except:
            return text  # return original text if translation fails

    def get_language_distribution(self) -> Dict[str, int]:
        """
        Get the distribution of languages in the dataset.

        Returns:
            Dict[str, int]: A dictionary with language codes as keys and their counts as values.
        """
        lang_dist = {}
        for idx in range(len(self)):
            _, lang = self._detect_and_translate(idx)
            lang_dist[lang] = lang_dist.get(lang, 0) + 1
        return lang_dist

    def save_translation_cache(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump(self.translation_cache, f)

    def load_translation_cache(self, filepath: str):
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                self.translation_cache = pickle.load(f)


# Example usage
if __name__ == "__main__":
    sample_data = [
        {"text": "Hello, world!"},
        {"text": "Bonjour le monde!"},
        {"text": "¡Hola mundo!"}
    ]
    supported_langs = ["en", "fr", "es"]

    dataset = MultilingualDataset(sample_data, supported_langs)
    print(f"Dataset size: {len(dataset)}")
    print(f"First item: {dataset[0]}")
    print(f"Language distribution: {dataset.get_language_distribution()}")
