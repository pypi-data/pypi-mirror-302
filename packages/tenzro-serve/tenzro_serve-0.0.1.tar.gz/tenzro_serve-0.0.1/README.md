# Tenzro Serve

<p align="center"><img width="40%" src="https://tenzro.com/assets/serve-logo.png" /></p>

[Tenzro Serve](https://tenzro.com/serve) is an open-source tool for transporting AI models and serving them locally on devices. It's part of the Tenzro ecosystem, designed to enable decentralized AI processing at the edge. Tenzro Serve provides an open system for AI model deployment, built on top of the ONNX (Open Neural Network Exchange) framework.

Tenzro Serve is widely supported and can be integrated with various frameworks, tools, and hardware. By enabling interoperability between different platforms and streamlining the path from development to production, Tenzro Serve helps increase the speed of innovation in the AI community. We invite the community to join us and further evolve Tenzro Serve.

## Acknowledgments and Origins

Tenzro Serve is built upon and extends the [ONNX project](https://github.com/onnx/onnx). We are grateful for the foundational work provided by ONNX and acknowledge the contributions of the ONNX community. Tenzro Serve aims to build upon this foundation to provide specialized capabilities for transporting and serving AI models locally on devices.

## Contribute

Tenzro Serve is a community project. We encourage you to join the effort and contribute feedback, ideas, and code. Your contributions can help shape both Tenzro Serve and the underlying ONNX framework.

Check out our [contribution guide](https://github.com/tenzro/serve/blob/main/CONTRIBUTING.md) to get started.

## Follow Us

Stay up to date with the latest Tenzro Serve news. [[Twitter](https://twitter.com/tenzr0)] [[LinkedIn](https://www.linkedin.com/company/tenzro)]

## Installation

### Official Python packages

Tenzro Serve released packages are published in PyPI.

```sh
pip install tenzro-serve
```

### Build Tenzro Serve from Source

Before building from source, uninstall any existing versions of tenzro-serve: 

```sh
pip uninstall tenzro-serve
```

#### Requirements

- Python 3.7+
- C++17 compatible compiler

Then you can build Tenzro Serve as:

```sh
git clone https://github.com/tenzro/serve.git
cd serve
git submodule update --init --recursive
pip install -e . -v
```

### Installation on ARM64 Architecture

For users on ARM64 architecture, such as Raspberry Pi or Apple Silicon Macs, follow these steps:

1. **Install Required Dependencies**: Ensure that you have the necessary tools and libraries installed. You may need to install additional dependencies specific to ARM64 systems.

2. **Clone the Repository**:
   ```sh
   git clone https://github.com/tenzro/serve.git
   cd serve
   git submodule update --init --recursive
   ```

3. **Build Tenzro Serve**:
   ```sh
   pip install -e . -v
   ```

4. **Verify Installation**:
   Run the following command to check if Tenzro Serve is properly installed:
   ```sh
   python -c "import tenzro_serve"
   ```

If you encounter any issues or require assistance, please refer to the [community forum](link-to-forum) or raise an issue in the GitHub repository.

## Verify Installation

After installation, run:

```sh
python -c "import tenzro_serve"
```

to verify it works.

## Testing

Tenzro Serve uses [pytest](https://docs.pytest.org) as the test driver. To run tests, first install pytest:

```sh
pip install pytest nbval
```

Then run the tests with:

```sh
pytest
```

## Development

Check out the [contributor guide](https://github.com/tenzro/tenzro-serve/blob/main/CONTRIBUTING.md) for instructions.

## License

[Apache License v2.0](LICENSE)

Note: As Tenzro Serve extends ONNX, it is distributed under the same Apache License v2.0. Please see the LICENSE file for full details.