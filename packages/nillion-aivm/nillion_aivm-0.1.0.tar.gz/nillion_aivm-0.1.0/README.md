# Nillion AIVM

AIVM is a framework designed for private inference using cryptographic protocols. This project allows you to run a development network (devnet) and perform private inference tasks using examples provided in the repository.

## Table of Contents

- [Installing AIVM](#installing-aivm)
  - [Recommended Installation](#base-installation)
  - [Using Poetry](#using-poetry)
  - [Using venv](#using-venv)
- [Running AIVM](#running-aivm)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installing AIVM

### Recommended Instalation
1. Install on your existing OS python installation. Requires Python >=3.12:

   ```shell
   git clone https://github.com/NillionNetwork/aivm.git
   cd aivm
   ```

3. Install dependencies:

   ```shell
   pip install .
   ```
If you are going to run the examples, do:

   ```shell
   pip install ".[examples]"
   ```
### Using Poetry

1. Install Poetry (if not already installed):

   ```bash
   pip install poetry
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/NillionNetwork/aivm.git
   cd aivm
   ```

3. Install dependencies:

   ```bash
   poetry install
   ```

4. Activate the virtual environment:

   ```bash
   poetry shell
   ```

5. Install AIVM:

   ```bash
   poetry install
   ```

### Using venv

1. Clone the repository:

   ```bash
   git clone https://github.com/NillionNetwork/aivm.git
   cd aivm
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:

   On Linux/macOS:

   ```bash
   source .venv/bin/activate
   ```

   On Windows:

   ```bash
   .\venv\Scripts\activate
   ```

4. Install the package:

   ```bash
   pip install .
   ```

## Running AIVM

1. Start the AIVM devnet:

   ```bash
   aivm-devnet
   ```

2. Open the provided Jupyter notebook `examples/getting-started.ipynb` to run private inference examples on AIVM.

3. After completing your tasks, terminate the devnet process by pressing `CTRL+C`.

## Usage

For additional usage, refer to the examples provided in the `examples` folder, which demonstrates how to set up private inference workflows using AIVM.