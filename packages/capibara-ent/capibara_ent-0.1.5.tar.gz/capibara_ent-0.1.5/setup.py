from setuptools import setup, find_packages

setup(
    name='capibara-ent',
    version='0.1.5',
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
        'wandb'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
