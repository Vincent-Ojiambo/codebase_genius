# Sample Data Processor

A demonstration project for the Codebase Genius documentation system. This project showcases various Python programming concepts including object-oriented design, abstract base classes, type hints, and documentation practices.

## Features

- **Abstract Base Classes**: Demonstrates inheritance and polymorphism
- **Type Hints**: Full type annotation support
- **Docstrings**: Comprehensive documentation for all methods and classes
- **JSON Processing**: Example of data validation and transformation
- **Error Handling**: Proper exception handling and validation
- **Unit Testing**: Basic test framework included

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd sample_repo

# Install dependencies (if any)
pip install -r requirements.txt

# Run the application
python src/main.py

# Run tests
python src/main.py test
```

## Usage

### Basic Usage

```python
from src.main import JSONProcessor

# Create a processor with configuration
config = {
    "input_format": "json",
    "output_format": "enhanced_json",
    "validation_rules": {
        "require_keys": ["id", "name"],
        "max_size": 1000
    }
}

processor = JSONProcessor(config)

# Process data
data = {"id": 1, "name": "Sample", "value": 42}
if processor.validate_data(data):
    result = processor.process_data(data)
    processor.save_results(result, "output/processed.json")
```

### Command Line

```bash
# Run main application
python src/main.py

# Run tests
python src/main.py test
```

## API Reference

### Classes

#### `DataProcessor`
Abstract base class for data processors.

**Methods:**
- `validate_data(data)`: Validate input data
- `process_data(data)`: Process validated data
- `save_results(results, output_path)`: Save results to file

#### `JSONProcessor`
Concrete implementation for JSON data processing.

**Methods:**
- All methods from `DataProcessor`
- `_get_timestamp()`: Get current timestamp
- `_calculate_stats(data)`: Calculate data statistics

### Functions

#### `main()`
Main entry point for the application.

#### `run_tests()`
Run unit tests for the data processor.

## Architecture

The project follows a clean architecture pattern:

```
src/
├── main.py          # Main entry point and core logic
└── (other modules)

tests/
└── test_main.py     # Unit tests

docs/
└── README.md        # This documentation
```

## Dependencies

- Python 3.8+
- Standard library only (no external dependencies)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License
