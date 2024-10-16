from setuptools import setup, find_packages

setup(
    name='capibara-ent',
    version='0.1.6',
    description='Capibara: A Flexible Multimodal AI Library',
    long_description='''
    Capibara is a powerful and flexible multimodal AI library designed to facilitate the development,
    training, and deployment of advanced language models. It offers a comprehensive suite of tools
    for natural language processing, including:

    - Customizable model architectures with support for various layer configurations
    - Synthetic embedding generation for enhanced text representation
    - Ethical content filtering to ensure responsible AI output
    - Integrated training pipeline with support for TPUs
    - Inference capabilities for deployed models
    - CLI tool for easy model management and experimentation

    Key features:
    - Modular design for easy extension and customization
    - Built-in support for popular deep learning frameworks like TensorFlow and PyTorch
    - Integration with Weights & Biases for experiment tracking and visualization
    - Docker support for containerized deployment
    - Hyperparameter optimization tools for model tuning

    Capibara is ideal for researchers, data scientists, and AI engineers looking to push the
    boundaries of natural language processing while maintaining ethical standards and
    operational efficiency.
    ''',
    long_description_content_type='text/markdown',
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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'capibaraent=capibara.cli.capibaraent_cli:CapibaraENT',
        ],
    },
    keywords='ai nlp machine-learning deep-learning language-models ethics',
)
