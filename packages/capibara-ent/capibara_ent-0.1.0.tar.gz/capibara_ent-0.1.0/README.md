# CapibaraENT CLI

CapibaraENT is a command-line tool for training, evaluating, and deploying Capibara-based language models, optimized for TPUs.

## Features

- Training and evaluation of Capibara models
- Built-in TPU support
- Model deployment
- Performance measurement
- Docker container execution
- Model deserialization from JSON

## Requirements

- Python 3.7+
- PyTorch 1.8+
- PyTorch/XLA
- Docker (optional, for container execution)

## Installation

1. Clone this repository:

 ```bash
   git clone https://github.com/your-username/capibaraent-cli.git
   cd capibaraent-cli
   ```

1. Install dependencies:

```bash
   pip install -r requirements.txt
   ```

## Usage

The CapibaraENT CLI offers various options for working with Capibara models:

```bash
python capibaraent_cli.py [options]

```

Available options:

- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `--train`: Train the model
- `--evaluate`: Evaluate the model
- `--use-docker`: Run the model inside Docker
- `--deserialize-model`: Deserialize the model from JSON
- `--deploy`: Deploy the model
- `--measure-performance`: Measure the model's performance
- `--model`: Path to the model JSON file (for deserialization)

### Usage Examples

1. Train a model:

```bash
   python capibaraent_cli.py --train
 ```

2. Evaluate a model:

```bash
   python capibaraent_cli.py --evaluate
 ```

3. Deploy a model:

```bash
   python capibaraent_cli.py --deploy
   ```

5. Measure model performance:

   ```bash
   python capibaraent_cli.py --measure-performance
   ```

6. Run a model in Docker:

   ```bash
   python capibaraent_cli.py --use-docker
   ```

7. Deserialize and run a model from JSON:

```bash
   python capibaraent_cli.py --deserialize-model --model model.json
```

## Configuration

Model configuration is handled through the `core/config.py` file. To modify the default settings, edit this file directly. Key configuration parameters include:

- `input_dim`
- `batch_size`
- `learning_rate`
- `device_type`

Example of `core/config.py`:

## Development

To contribute to the project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Marco Durán - <marco@anachroni.co>

Project Link: [https://github.com/anachroni-io/capibaraent-cli](https://github.com/anachroni-io)
