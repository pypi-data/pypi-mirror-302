
# BinaExperts SDK

This SDK provides tools for converting various dataset formats (COCO, YOLO, etc.). It is designed to be modular and extensible, allowing easy addition of new formats.

## Project Structure

```plaintext
binaexperts_sdk/
│
├── binaexperts/
│   ├── __init__.py
│   ├── convertors/
│   │   ├── __init__.py
│   │   ├── base.py                   # Base class for converters
│   │   ├── const.py                  # Constants used for dataset conversion settings and formats
│   │   ├── convertor.py              # Main class for managing dataset conversions
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── coco.json                 # Schema for COCO format
│   │   ├── yolo.json                 # Schema for YOLO format
│   │   ├── binaexperts.json          # Schema for BinaExperts format
│   │   ├── normalizer.json           # Schema for Normalizer format
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── utils.py
│ 
│
├── setup.py                          # Setup script for packaging the SDK
├── README.md                         # Project documentation
└── requirements.txt                  # Python dependencies

```
## Installation

You can install the BinaExperts SDK directly from PyPI using `pip`:

```bash
pip install binaexperts
```
## Usage

Once you've installed the BinaExperts SDK, you can start converting datasets between different formats. Here's how to use the SDK:

### Basic Example

```python
import binaexperts
convertor = binaexperts.Convertor()

# Convert COCO format to YOLO format
convertor.convert(
    source_format='coco',
    target_format='yolo',
    source_path='path/to/source_format_dataset.zip', 
    target_path='path/to/target_format_dataset.zip'
)
```
## Supported Formats

The BinaExperts SDK currently supports the following formats:

- COCO
- YOLO
- BinaExperts

## Features
- Dataset Conversion: Seamless conversion between COCO, YOLO, and BinaExperts formats.
- Modular Design: Easily extendable to support new formats and datasets in the future.

## Future Roadmap
- Local Inference: Add support for local inference with trained models directly within the SDK.
- Live Inference: Future versions will support live inference from video streams or camera inputs.
- Auto Training: Automatic training workflows with model selection, hyperparameter tuning, and training pipelines.
- Dataset Validation: Automatic validation of dataset integrity, including checks for missing annotations, corrupted images, and data consistency.
- Additional Format Support: Future support for additional dataset formats, expanding beyond COCO, YOLO, and BinaExperts.
- We Welcome Your Suggestions: We encourage you to provide suggestions for additional features you would like to see in the SDK.

## License
This project is licensed under the MIT License.