from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Configuración del paquete
setup(
    name="capibara-ent",
    version="1.0.7",
    author="Marco Durán",
    author_email="marco@anachroni.com",
    description="A flexible multimodal AI library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anachroni/capibara",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.7",
    install_requires=[
        "tensorflow>=2.5.0",
        "docker",
        "nltk",
        "numpy",
        "pandas",
        "torch>=1.8.0",
        "torch-xla",
        "jax",
        "flax",
        "optax",
        "wandb",
        "tensorflow-hub",
        "tqdm",
        "PyYAML"
    ],
    entry_points={
        "console_scripts": [
            "capibaraent=capibara.cli.capibaraent_cli:main",
        ],
    },
    keywords="ai nlp machine-learning deep-learning language-models ethics tpu training",
)
