# Text Mixer (2026 Edition)

A persistent CLI tool that creatively scrambles text files using configurable "word-tail" chunks. Built to modern coding standards using `uv` for strict environment and dependency management.

## Features

* **Drop-and-Go I/O:** Automatically detects and processes the newest file dropped into the `input/` directory.
* **Adjustable Granularity:** Choose a mixing level between 1 and 9 to control chunk sizes during the shuffling process.
* **Persistent Workflow:** Keeps the engine running to allow multiple consecutive mixings without restarting the application.
* **Modern Architecture:** Configured with `uv` for lightning-fast dependency management and standard `pathlib` routing.

## Prerequisites

* Python 3.14 or higher
* `uv` package manager installed

## Installation

1. Clone this repository to your local machine.
2. Navigate to the project directory and sync the environment:
   ```bash
   uv sync
   ```

## Usage

1. Place your source text file into the `input/` folder. (The application will automatically create this folder on first run if it doesn't exist).
2. Run the application:
   ```bash
   uv run text_mixer.py
   ```
3. Follow the CLI prompts to enter your desired granularity (1-9). 
4. Your scrambled file will be automatically saved to the `output/` folder, timestamped and tagged with your chosen granularity.

Type `q` at the prompt at any time to exit gracefully.