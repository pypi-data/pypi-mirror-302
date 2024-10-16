"""
Setup configuration for the CapibaraENT project.

This script uses setuptools to define the installation configuration for
the CapibaraENT project, including metadata, dependencies, and entry scripts.

To install the project in development mode:
    pip install -e .

To build the package:
    python setup.py sdist bdist_wheel

To install the package:
    pip install .
"""

from setuptools import setup, find_packages
import os

# Read the contents of README.md for the long description
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "CapibaraENT: An advanced language model integrating Mamba SSM, multilingual handling, and ethical features."

setup(
    name='capibara-ent',
    version='0.1.4',
    description='Capibara: A Flexible Multimodal AI Library',
    author='Marco Durán',
    author_email='marco@anachroni.com',
    url='https://github.com/Anachroni/capibara',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.5.0',
        'docker',
        'nltk',
        'numpy',
        'pandas',
        'torch>=1.8.0',
        'torch-xla',
        'jax',
        'wandb',
        'tensorflow-hub'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'capibaraent=capibara.cli.capibaraent_cli:CapibaraENT',
        ],
    },
)
