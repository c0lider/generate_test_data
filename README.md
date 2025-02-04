# How to

- [How to](#how-to)
  - [Description](#description)
  - [Installation](#installation)
  - [Run the script](#run-the-script)

## Description

This script reads binary Terabee measurement files and generates heatmap PNGs. It transforms sensor data into color-coded images that highlight depth variations for easy visualization.

> The script assumes, that input files are located inside the `input` directory and that the measurements have a frame size of 80\*60 pixels

## Installation

1. Create and activate a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Run the script

To use the script simply run:

```bash
python script.py
```

A progress bar will appear, indicating the conversion progress

> The resulting files will be located inside the `output` directory
