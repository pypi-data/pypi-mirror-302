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
    name="capibara-ent",  # The name of the package
    version="0.1.3",  # Initial version of the package
    author="Marco Durán",  # Your name as the author of the package
    author_email="marco@anachroni.com",  # Your email address
    description=(
        "Capibara: A Flexible Multimodal AI Library"
    ),  # A short description of the package
    long_description=long_description,  # The long description from README.md
    # Markdown format for the long description
    long_description_content_type="text/markdown",
    url="https://github.com/Anachroni/capibara",  # URL of your website
    # Automatically find and include relevant packages
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",  # The project is in the alpha stage
        "Intended Audience :: Developers",  # Target audience is developers
        "License :: OSI Approved :: MIT License",  # MIT License
        "Operating System :: OS Independent",  # Cross-platform support
        "Programming Language :: Python :: 3",  # Supported Python version
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",  # Specify the minimum required Python version
    install_requires=[
        'tensorflow==2.16.0',
        'protobuf>=5.26.1,<6.0dev',
        "docker",
        "nltk",
        "numpy",
        "pandas"
    ],
    extras_require={
        "dev": [  # Development dependencies for testing and formatting
            "pytest>=6.2.4",  # Pytest for unit testing
            "black>=21.7b0",  # Black for code formatting
            "flake8>=3.9.2",  # Flake8 for linting
            "isort>=5.9.3",  # Isort for sorting imports
            "mypy>=0.910",  # Mypy for type checking
            "pytest-cov>=2.12.0",  # Pytest-cov for coverage
            "pre-commit>=2.15.0",  # Pre-commit for Git hooks
        ],
        "tpu": [  # Dependencies specific for TPU use
            "torch_xla>=2.0",
        ],
        "arm": [  # Dependencies specific for ARM use
            "onnxruntime>=1.10.0",
        ],
    },
    entry_points={  # Define command-line scripts
        "console_scripts": [
            "capibara-train=capibara_model.scripts.run_training:main",  # Script for training
            # Script for interactive session
            "capibara-interact=capibara_model.scripts.interactive_session:main",
            "capibara-serve=capibara_model.scripts.serve_api:main",  # Script for serving API
            "capibara-infer=capibara_model.scripts.run_inference:main",  # Script for inference
        ],
    },
)
